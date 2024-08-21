##### To run this code is best to do a make run or just go to Makefile to see the command being used to run it, might also put the 
##### code to run it in the run.sh

from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StructType, StructField, StringType, IntegerType
import time

# Initialize SparkSession
spark = SparkSession.builder \
    .appName("officialnow") \
    .master("spark://spark-master:7077") \
    .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.4.0") \
    .getOrCreate()

spark.sparkContext.setLogLevel("ERROR")

# Create an RDD and perform a simple computation
rdd = spark.sparkContext.parallelize([1, 2, 3, 4, 5])
rdd_sum = rdd.sum()

# Define schema for Kafka data
schema = StructType([
    StructField("id", StringType()),
    StructField("timestamp", StringType()),
    StructField("rpm", IntegerType()),
    StructField("gear", IntegerType()),
    StructField("steer", IntegerType()),
    StructField("throttle_position", IntegerType()),
    StructField("tire_temps", StringType())
])

# Read from Kafka
df = spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "kafka:9094") \
    .option("subscribe", "f1-telemetry-1") \
    .option("startingOffsets", "earliest") \
    .load()

# Parse the Kafka value column
df_parsed = df.selectExpr("CAST(value AS STRING)") \
              .select(from_json(col("value"), schema).alias("data")) \
              .select("data.*")

# Start streaming query
query = df_parsed.writeStream \
    .outputMode("append") \
    .format("console") \
    .option("truncate", "false") \
    .start() \
    .awaitTermination()



# Print the sum of the RDD and Spark information
print(f"The sum of the RDD is: {rdd_sum}")
print("Spark Local IP:", spark.conf.get("spark.driver.host"))
print("Spark Master IP:", spark.conf.get("spark.master"))
df_parsed.printSchema()

# Stop the SparkSession
spark.stop()
