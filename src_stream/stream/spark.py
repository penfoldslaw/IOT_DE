##### To run this code is best to do a make run or just go to Makefile to see the command being used to run it, might also put the 
##### code to run it in the run.sh

from pyspark import SparkConf, SparkContext
from pyspark.sql import SparkSession

# Initialize SparkContext
conf = SparkConf().setAppName("officalnow").setMaster("spark://spark-master:7077")
sc = SparkContext(conf=conf)

spark = SparkSession.builder.appName("officalnow").getOrCreate()
spark.sparkContext.setLogLevel("ERROR")

# Create an RDD and perform a simple computation
rdd = sc.parallelize([1, 2, 3, 4, 5])
rdd_sum = rdd.sum()

print(f"The sum of the RDD is: {rdd_sum}")
print("Spark Local IP:", conf.get("spark.driver.host"))
print("Spark Master IP:", conf.get("spark.master"))

sc.stop()
