import pyspark
from pyspark.sql import SparkSession
from pyspark import sql
from pyspark.sql.types import StructType,StructField,StringType,IntegerType
from pyspark.sql.functions import from_json,col


url = 'jdbc:postgresql://localhost:5432/gpadmin' # Коннект к БД
login = 'gpadmin' #Логин БД
password = 'gpadmin' #Пароль БД
table = 'test_evteev' # название таблицы куда пишем данные

spark = (SparkSession
 .builder
 .appName('pyspark_example')
 .config("spark.jars.packages", "org.apache.spark:spark-streaming-kafka-0-10_2.12:3.1.3,org.apache.spark:spark-sql-kafka-0-10_2.12:3.1.3") \
 .config("spark.executor.extraClassPath", "TZ_ATEMPT_2/spark-3.1.3-bin-hadoop3.2/jarspostgresql-42.5.0.jar") \
 .config("spark.sql.streaming.forceDeleteTempCheckpointLocation", True)
 .getOrCreate())

schema = StructType([ \
    StructField("ID", IntegerType(), True), \
    StructField("FIRSTNAME", StringType(), True), \
    StructField("LASTNAME", StringType(), True),\
    StructField("PHONE", StringType(), True), \
    StructField("EMAIL", StringType(), True) \
  ])

df_test = spark \
            .readStream \
            .format("kafka") \
            .option("kafka.bootstrap.servers", 'localhost:9092') \
            .option("subscribe",'test_evteev') \
            .option("startingOffsets", "earliest") \
            .load() \
            .select(from_json(col("value").cast("string"), schema).alias("t")) \
            .select("t.*")  


def write_to_gp(df,epoch_id) -> None:         
    df.write \
        .mode('append') \
        .format("jdbc") \
        .option("url", url) \
        .option("driver", "org.postgresql.Driver") \
        .option("dbtable", table) \
        .option("user", login) \
        .option("password", password) \
        .save() 

df_test.writeStream \
    .foreachBatch(write_to_gp) \
    .start() \
    .awaitTermination()