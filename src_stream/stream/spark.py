##### To run this code is best to do a make run or just go to Makefile to see the command being used to run it, might also put the 
##### code to run it in the run.sh

from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, udf
from pyspark.sql.types import StructType, StructField, StringType, IntegerType
from pyspark.sql.functions import expr
from pyspark.sql.functions import *
import uuid
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
    .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.2,com.datastax.spark:spark-cassandra-connector_2.12:3.5.1") \
    .config("spark.cassandra.connection.host", "cassandra")\
    .config("spark.cassandra.connection.port", "9042")\
    .config("spark.cassandra.auth.username","cassandra")\
    .config("spark.cassandra.auth.password","cassandra")\
    .getOrCreate()

spark.sparkContext.setLogLevel("ERROR") # hides alot of logs 


# Define schema for Kafka data
schema = StructType([
    StructField("id", IntegerType()),
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

def generate_uuid():
    return str(uuid.uuid4())

uuid_udf = udf(generate_uuid, StringType())

df_parsed = df_parsed.withColumn("uuid", uuid_udf())


df_parsed = df_parsed.select(
    col("uuid"),
    col("id"),
    col("brake"),
    col("tire_temps.front_left").alias("front_left_temp"),
    col("tire_temps.front_right").alias("front_right_temp"),
    col("gear"),
    col("tire_temps.rear_left").alias("rear_left_temp"),
    col("tire_temps.rear_right").alias("rear_right_temp"),
    col("rpm"),
    col("steer"),
    col("throttle_position"),
    col("timestamp"),
) # only being used because of nested json



# # Start streaming query and writing it to the console
# query = df_parsed.writeStream \
#     .outputMode("append") \
#     .format("console") \
#     .option("truncate", "false") \
#     .start() \
#     .awaitTermination()




def process_batch(df, batch_id):
    df.write \
      .format("org.apache.spark.sql.cassandra") \
      .options(keyspace="telemetry_keyspace", table="f1_data") \
      .mode("append") \
      .save()
    df.show()

# Writing the DataFrame to Cassandra
cassandra_query = df_parsed.writeStream \
    .foreachBatch(process_batch) \
    .outputMode("update") \
    .start() \
    .awaitTermination()

spark.stop()
