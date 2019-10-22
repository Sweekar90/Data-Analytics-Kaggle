# Databricks notebook source
# MAGIC %md
# MAGIC 
# MAGIC ## Overview
# MAGIC 
# MAGIC This notebook will show you how to create and query a table or DataFrame that you uploaded to DBFS. [DBFS](https://docs.databricks.com/user-guide/dbfs-databricks-file-system.html) is a Databricks File System that allows you to store data for querying inside of Databricks. This notebook assumes that you have a file already inside of DBFS that you would like to read from.
# MAGIC 
# MAGIC This notebook is written in **Python**, so the default cell type is Python. However, you can use different languages by using the `%LANGUAGE` syntax. Python, Scala, SQL, and R are all supported.

# COMMAND ----------

import pyspark
from pyspark.sql import functions as sf
from pyspark.sql.functions import concat, lit, regexp_replace, trim, col, lower, size
from string import punctuation
from pyspark.ml.feature import Tokenizer, RegexTokenizer, StopWordsRemover
from pyspark.sql.functions import *
from pyspark.sql import *
from pyspark.sql.types import *
from pyspark.sql.functions import array_distinct

# COMMAND ----------

## Loading the filtered discussion data

# File location and type
file_location = "/FileStore/tables/data_merge.json"
file_type = "json"

# CSV options
infer_schema = "false"
first_row_is_header = "false"
delimiter = ","

# The applied options are for CSV files. For other file types, these will be ignored.
df = spark.read.format(file_type) \
  .option("inferSchema", infer_schema) \
  .option("header", first_row_is_header) \
  .option("sep", delimiter) \
  .load(file_location)

display(df)

# COMMAND ----------

df_combine = df.select(concat(df['overview'], lit(' '), df['comments']).alias('combine_text'))
display(df_combine)

# COMMAND ----------

def removePunctuation(column):
    """Removes punctuation, changes to lower case, and strips leading and trailing spaces.

    Note:
        Only spaces, letters, and numbers should be retained.  Other characters should should be
        eliminated (e.g. it's becomes its).  Leading and trailing spaces should be removed after
        punctuation is removed.

    Args:
        column (Column): A Column containing a sentence.

    Returns:
        Column: A Column named 'sentence' with clean-up operations applied.
    """
    
    regex_result = regexp_replace(column,r'<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});', '')  #regexp_replace(str, pattern, replacement)
    trim_result = trim(regex_result)  #Trim the spaces from both ends for the specified string column.
    lower_result = lower(trim_result) #Converts a string column to lower case.
    return lower_result

# COMMAND ----------

ff = df_combine.select(removePunctuation(col('combine_text')).alias('refined_text'))
display(ff)

# COMMAND ----------

regexTokenizer = RegexTokenizer(inputCol = "refined_text", outputCol = "words", pattern = "overfit|underfit|missing values|imbalance|covariate shift|outlier|leakage|calibration|dataset shift|drift", gaps=False)

# COMMAND ----------

regexTokenized = regexTokenizer.transform(ff)

display(regexTokenized)

# COMMAND ----------

wo_dupes = regexTokenized.withColumn("words_without_dupes", array_distinct("words"))

display(wo_dupes)

# COMMAND ----------

countdf = regexTokenized.select('*',size('words').alias('size'))

display(countdf)

# COMMAND ----------

countdf_wo_dupes = wo_dupes.select('*',size('words_without_dupes').alias('dupes_wo_size'))

display(countdf_wo_dupes)

# COMMAND ----------

wokey = countdf[countdf['size'] == 0].count()
wkey = countdf[countdf['size'] != 0].count()

result1_DF = [Row(Discussions = 'Discussions without defect keywords', Count = wokey), Row(Discussions = 'Discussions about defects', Count = wkey)]

schema = StructType([StructField('Discussions', StringType()), StructField('Count',IntegerType())])
result1 = spark.createDataFrame(result1_DF, schema)

display(result1)

# COMMAND ----------

countsdupes = countdf_wo_dupes.select(sf.explode('words_without_dupes').alias('keys_wodupes')).groupBy('keys_wodupes').count().collect()

# COMMAND ----------

schemao = StructType([StructField('keys_wodupes', StringType()), StructField('count_wodupes',IntegerType())])
result2 = spark.createDataFrame(countsdupes, schemao)

display(result2)

# COMMAND ----------

counts = countdf.select(sf.explode('words').alias('keys')).groupBy('keys').count().collect()

# COMMAND ----------

schema = StructType([StructField('keys', StringType()), StructField('count',IntegerType())])
result2 = spark.createDataFrame(counts, schema)

display(result2)

# COMMAND ----------

display(result1)

# COMMAND ----------

# Create a view or table

temp_table_name = "data_merge_json"

df.createOrReplaceTempView(temp_table_name)

# COMMAND ----------

# MAGIC %sql
# MAGIC 
# MAGIC /* Query the created temp table in a SQL cell */
# MAGIC 
# MAGIC select * from `data_merge_json`

# COMMAND ----------

# With this registered as a temp view, it will only be available to this particular notebook. If you'd like other users to be able to query this table, you can also create a table from the DataFrame.
# Once saved, this table will persist across cluster restarts as well as allow various users across different notebooks to query this data.
# To do so, choose your table name and uncomment the bottom line.

permanent_table_name = "data_merge_json"

# df.write.format("parquet").saveAsTable(permanent_table_name)

# COMMAND ----------

from pyspark.ml.feature import Tokenizer, RegexTokenizer
from pyspark.sql.functions import col, udf
from pyspark.sql.types import IntegerType

sentenceDataFrame = spark.createDataFrame([
    (0, "Hi I heard about Spark"),
    (1, "I wish Java could use case classes"),
    (2, "Logistic regression models are neat"),
    (3, "My name is Anthony Gonsalves")
], ["id", "sentence"])

tokenizer = Tokenizer(inputCol="sentence", outputCol="words")

countTokens = udf(lambda words: len(words), IntegerType())

tokenized = tokenizer.transform(sentenceDataFrame)
tokenized.select("sentence", "words")\
    .withColumn("tokens", countTokens(col("words"))).show(truncate=False)

# COMMAND ----------

l = ["heard", "i", "neat"]

# COMMAND ----------

regexTokenizer = RegexTokenizer(inputCol="sentence", outputCol="words", pattern="heard|wish|java|name", gaps=False)
# alternatively, pattern="\\w+", gaps(False)

regexTokenized = regexTokenizer.transform(sentenceDataFrame)
regexTokenized.select("sentence", "words") \
    .withColumn("tokens", countTokens(col("words"))).show(truncate=False)


# COMMAND ----------

regexfiltered = regexTokenized.filter(regexTokenized['words'].isin(l))

# COMMAND ----------

