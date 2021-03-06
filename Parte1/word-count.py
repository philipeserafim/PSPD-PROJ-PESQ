#nc -lk -p 9999

#su - hadoop
#ssh localhost
#spark-submit --master local[2] word-count.py localhost 9999

import sys
import argparse

from pyspark.sql import SparkSession
from pyspark.sql.functions import split, explode, col

spark = SparkSession \
    .builder \
    .appName("WordCount-PSPD") \
    .getOrCreate()

spark.sparkContext.setLogLevel("WARN")

# Create DataFrame representing the stream of input lines from connection to localhost:9999
lines = spark \
    .readStream \
    .format("socket") \
    .option("host", "localhost") \
    .option("port", 9999) \
    .load()

# Split the lines into words
words = lines.select(
   explode(
       split(lines.value, " ")
   ).alias("word")
)

# Generate running word count
wordCounts = words.groupBy("word").count()

# Start running the query that prints the running counts to the console
query = wordCounts \
    .orderBy("count", ascending=False) \
    .writeStream \
    .outputMode("complete") \
    .format("console") \
    .start() 

query.awaitTermination()