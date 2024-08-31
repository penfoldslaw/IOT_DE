from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StructType, StructField, StringType, IntegerType
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
import pandas as pd
import configparser
import time
import os


# Read configuration
config = configparser.ConfigParser()
config.read('/jackpot/stream/config.cfg')  # this file path is from docker
topic_1 = config.get('mqtt', 'topic_1')
topic_2 = config.get('mqtt','topic_2')
topics = f"{topic_1},{topic_2}"

# Initialize SparkSession
spark = SparkSession.builder \
    .appName("officialnow") \
    .master("spark://spark-master:7077") \
    .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.2,com.datastax.spark:spark-cassandra-connector_2.12:3.5.1") \
    .config("spark.cassandra.connection.host", "cassandra") \
    .config("spark.cassandra.connection.port", "9042") \
    .config("spark.cassandra.auth.username", "cassandra") \
    .config("spark.cassandra.auth.password", "cassandra") \
    .getOrCreate()

spark.sparkContext.setLogLevel("ERROR")  # hides a lot of logs

rdd = spark.sparkContext.parallelize([1, 2, 3, 4, 5]) # force the Spark context to be fully initialized and stay active,
rdd_sum = rdd.sum() # Without this operation, Spark might be incorrectly initialized or terminated prematurely

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
    .option("subscribe", "f1telemetry1") \
    .option("startingOffsets", "earliest") \
    .load()

# Create an RDD and perform a simple computation (to keep the Spark context active)
rdd = spark.sparkContext.parallelize([1, 2, 3, 4, 5])
rdd_sum = rdd.sum()

# Parse the Kafka value column
df_parsed = df.selectExpr("CAST(value AS STRING)") \
              .select(from_json(col("value"), schema).alias("data")) \
              .select("data.*")

df_parsed = df_parsed.withColumn("tire_temps", from_json(col("tire_temps"), tire_temps_schema))

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
)

# Initialize Cassandra connection
def get_cassandra_session():
    auth_provider = PlainTextAuthProvider(username='cassandra', password='cassandra')
    cluster = Cluster(['localhost'], auth_provider=auth_provider)
    session = cluster.connect()
    return session

# Function to insert data into Cassandra
def insert_into_cassandra(df):
    session = get_cassandra_session()
    insert_query = """
    INSERT INTO f1_data (id, timestamp, rpm, gear, steer, throttle_position, Brake, front_left_temp, front_right_temp, rear_left_temp, rear_right_temp)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    
    for row in df.itertuples(index=False):
        session.execute(insert_query, (
            row.id,
            row.timestamp,
            row.rpm,
            row.gear,
            row.steer,
            row.throttle_position,
            row.Brake,
            row.front_left_temp,
            row.front_right_temp,
            row.rear_left_temp,
            row.rear_right_temp
        ))

def process_batch(df, batch_id):
    # Convert DataFrame to Pandas to collect data
    df_pandas = df.toPandas()
    insert_into_cassandra(df_pandas)
    print(f"Processed batch {batch_id}")

# Writing the DataFrame to Cassandra
cassandra_query = df_parsed.writeStream \
    .foreachBatch(process_batch) \
    .outputMode("update") \
    .start() \
    .awaitTermination()

spark.stop()
