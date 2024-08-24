##### To run this code is best to do a make run or just go to Makefile to see the command being used to run it, might also put the 
##### code to run it in the run.sh

from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StructType, StructField, StringType, IntegerType
import time
import configparser

config = configparser.ConfigParser()
config.read('/jackpot/stream/config.cfg') # this file path is from docker
topic_1 = config.get('mqtt', 'topic_1')
topic_2 = config.get('mqtt','topic_2')

topics = f"{topic_1},{topic_2}"

# Initialize SparkSession
spark = SparkSession.builder \
    .appName("officialnow") \
    .master("spark://spark-master:7077") \
    .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.4.0") \
    .getOrCreate()

spark.sparkContext.setLogLevel("ERROR") # hides alot of logs 


# Define schema for Kafka data
schema = StructType([
    StructField("id", StringType()),
    StructField("timestamp", StringType()),
    StructField("rpm", IntegerType()),
    StructField("gear", IntegerType()),
    StructField("steer", IntegerType()),
    StructField("throttle_position", IntegerType()),
    StructField("Brake", IntegerType()),
    StructField("tire_temps", StringType())
])

tire_temps_schema = StructType([
    StructField("front_left", IntegerType()),
    StructField("front_right", IntegerType()),
    StructField("rear_left", IntegerType()),
    StructField("rear_right", IntegerType())
])

# Read from Kafka
df = spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "kafka:9094") \
    .option("subscribe",topics) \
    .option("startingOffsets", "earliest") \
    .load()

# Create an RDD and perform a simple computation
rdd = spark.sparkContext.parallelize([1, 2, 3, 4, 5]) # force the Spark context to be fully initialized and stay active,
rdd_sum = rdd.sum() # Without this operation, Spark might be incorrectly initialized or terminated prematurely

# Parse the Kafka value column
df_parsed = df.selectExpr("CAST(value AS STRING)") \
              .select(from_json(col("value"), schema).alias("data")) \
              .select("data.*")

df_parsed = df_parsed.withColumn("tire_temps", from_json(col("tire_temps"), tire_temps_schema)) # only being used because of nested json


df_parsed = df_parsed.select(
    col("id"),
    col("timestamp"),
    col("rpm"),
    col("gear"),
    col("steer"),
    col("throttle_position"),
    col("Brake"),
    col("tire_temps.front_left").alias("front_left_temp"),
    col("tire_temps.front_right").alias("front_right_temp"),
    col("tire_temps.rear_left").alias("rear_left_temp"),
    col("tire_temps.rear_right").alias("rear_right_temp")
) # only being used because of nested json



# Start streaming query
query = df_parsed.writeStream \
    .outputMode("append") \
    .format("console") \
    .option("truncate", "false") \
    .start() \
    .awaitTermination()



# Print the sum of the RDD and Spark information
# print(f"The sum of the RDD is: {rdd_sum}")
# print("Spark Local IP:", spark.conf.get("spark.driver.host"))
# print("Spark Master IP:", spark.conf.get("spark.master"))
# df_parsed.printSchema()

# Stop the SparkSession
spark.stop()
