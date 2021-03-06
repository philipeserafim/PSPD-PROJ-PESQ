from pyspark.sql import SparkSession
from pyspark.sql.functions import split, explode, col
import pyspark.sql.functions as F

spark = SparkSession \
  .builder \
  .appName("WordCount-PSPD") \
  .config("spark.scheduler.mode", "FAIR")\
  .config("spark.streaming.concurrentJobs","10")\
  .config("spark.sql.streaming.stateStore.stateSchemaCheck", False) \
  .getOrCreate()

spark.sparkContext.setLogLevel("ERROR")

# Create DataFrame representing the stream of input lines from connection to localhost:9092
lines = spark \
  .readStream\
  .format("kafka")\
  .option("kafka.bootstrap.servers", "localhost:9092")\
  .option("subscribe", "PSPD-PROJ") \
  .load()

df = lines.selectExpr("CAST(key AS STRING)", "CAST(value AS STRING)")

# Split the lines into words
words = lines.select(
   explode(
      split(lines.value, " ")
   ).alias("word")
)

# Start running the query that prints the running counts to the console
countWords = words \
  .groupBy("word") \
  .count() \
  .orderBy("count", ascending=False) \
  .writeStream \
  .outputMode("complete")\
  .format("console") \
  .option('numRows', 10)\
  .start()

p_words = words \
  .filter(F.upper(F.col("word").substr(1, 1)) == "P")\
  .groupBy() \
  .count() \
  .selectExpr("cast (count as string) value") \
  .writeStream \
  .outputMode("update")\
  .format("kafka")\
  .trigger(processingTime='30 second')\
  .option("kafka.bootstrap.servers", "localhost:9092")\
  .option("checkpointLocation", "./checkpoints-pWords") \
  .option("topic", "p-words")\
  .start()

r_words = words \
  .filter(F.upper(F.col("word").substr(1,1)) == "R") \
  .groupBy() \
  .count() \
  .selectExpr("cast (count as string) value") \
  .writeStream \
  .outputMode("update")\
  .format("kafka")\
  .trigger(processingTime='30 second')\
  .option("kafka.bootstrap.servers", "localhost:9092")\
  .option("topic", "r-words")\
  .option("checkpointLocation", "./checkpoints-rWords") \
  .start()

s_words = words \
  .filter(F.upper(F.col("word").substr(1,1)) == "S") \
  .groupBy() \
  .count() \
  .selectExpr("cast (count as string) value") \
  .writeStream \
  .outputMode("update")\
  .format("kafka")\
  .trigger(processingTime='30 second')\
  .option("kafka.bootstrap.servers", "localhost:9092")\
  .option("topic", "s-words")\
  .option("checkpointLocation", "./checkpoints-sWords") \
  .start()

words6 = words \
  .filter(F.length("word") == "6") \
  .groupBy() \
  .count() \
  .selectExpr("cast (count as string) value") \
  .writeStream \
  .outputMode("update")\
  .format("kafka")\
  .trigger(processingTime='30 second')\
  .option("kafka.bootstrap.servers", "localhost:9092")\
  .option("topic", "words-6")\
  .option("checkpointLocation", "./checkpoints-6words") \
  .start()

words8 = words \
  .filter(F.length("word") == "8") \
  .groupBy() \
  .count() \
  .selectExpr("cast (count as string) value") \
  .writeStream \
  .outputMode("update")\
  .format("kafka")\
  .trigger(processingTime='30 second')\
  .option("kafka.bootstrap.servers", "localhost:9092")\
  .option("topic", "words-8")\
  .option("checkpointLocation", "./checkpoints-8words") \
  .start()

words11 = words \
  .filter(F.length("word") == "11") \
  .groupBy() \
  .count() \
  .selectExpr("cast (count as string) value") \
  .writeStream \
  .outputMode("update")\
  .format("kafka")\
  .trigger(processingTime='30 second')\
  .option("kafka.bootstrap.servers", "localhost:9092")\
  .option("topic", "11-words")\
  .option("checkpointLocation", "./checkpoints-11words") \
  .start()

spark.streams.awaitAnyTermination()
