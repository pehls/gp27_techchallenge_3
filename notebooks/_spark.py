import os
from tqdm import tqdm
from datetime import datetime, date, timedelta
from pyspark.sql import SparkSession
import pyspark.sql.types as t
import pyspark.sql.functions as f
from pyspark.sql import SparkSession, SQLContext
import warnings

warnings.filterwarnings("ignore", category=Warning)

def get_spark(extra_configs = {}):
    # Set the path to your service account key JSON file
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r"D:/fiap-tech-challenge-3.json"
    # spark = get_spark()
    spark = SparkSession.builder\
        .master("local[*]")\
        .appName('spark')\
        .config('spark.executor.cores','8')\
        .config('spark.driver.memory','48G')\
        .config('spark.executor.memory','8G')\
        .config("spark.jars", "gs://spark-lib/bigquery/spark-bigquery-latest_2.12.jar")\
        .config("spark.jars", "D:/spark_temp/spark-bigquery-with-dependencies_2.13-0.32.2.jar")\
        .config("spark.jars", "https://storage.googleapis.com/hadoop-lib/gcs/gcs-connector-hadoop3-latest.jar")\
        .config("credentialsFile", r"D:\fiap-tech-challenge-3.json")\
        .getOrCreate()
    return spark

def spark_lower_cols(df):
    for col in df.columns:
        df = df.withColumnRenamed(col, col.lower())
    return df

def _display(df, n=5):
    import pandas as pd
    _df = pd.DataFrame(df.head(n), columns=df.columns())
    display(_df)