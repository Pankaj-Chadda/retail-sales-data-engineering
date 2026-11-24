# Databricks notebook source
source_path = "abfss://retail-container@retailstorage2003.dfs.core.windows.net/bronze/"

# COMMAND ----------

# MAGIC %md
# MAGIC ### Read the raw data from bronze layer

# COMMAND ----------


df_transactions = spark.read.parquet(f"{source_path}transaction/")
df_stores = spark.read.parquet(f"{source_path}store/")
df_products = spark.read.parquet(f"{source_path}product/")
df_customers = spark.read.parquet(f"{source_path}customer/Pankaj-Chadda/Data-Engineer/refs/heads/main/")

# COMMAND ----------

df_transactions.show()

# COMMAND ----------

# MAGIC %md
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC ### Creating silver layer - data cleaning

# COMMAND ----------

from pyspark.sql.functions import col

# Typecasting
df_transactions = df_transactions.select(
    col("transaction_id").cast("int"),
    col("customer_id").cast("int"),
    col("product_id").cast("int"),
    col("store_id").cast("int"),
    col("quantity").cast("int"),
    col("transaction_date").cast("date"),

)
df_products = df_products.select(
    col("product_id").cast("int"),
    col("product_name"),
    col("category"),
    col("price").cast("double")
)
df_stores = df_stores.select(
    col("store_id").cast("int"),
    col("store_name"),
    col("location")
)
df_customers = df_customers.select(
    "customer_id","first_name","last_name","email","city","registration_date"
).dropDuplicates(["customer_id"])



# COMMAND ----------

df_transactions.printSchema()

# COMMAND ----------

# MAGIC %md
# MAGIC ### Joining the tables

# COMMAND ----------

from pyspark.sql.functions import col

df_silver = df_transactions\
    .join(df_customers,"customer_id")\
    .join(df_products,"product_id")\
    .join(df_stores,"store_id")\
    .withColumn("total_amount",col("quantity") * col("price"))

# COMMAND ----------

display(df_silver)

# COMMAND ----------

# MAGIC %md
# MAGIC ### Dump the data to ADLS location 

# COMMAND ----------

silver_path = "abfss://retail-container@retailstorage2003.dfs.core.windows.net/silver/"

df_silver.write.mode("overwrite").format("delta").save(silver_path)

# COMMAND ----------

# MAGIC %md
# MAGIC ### Create silver dataset

# COMMAND ----------

spark.sql("""DROP TABLE IF EXISTS RETAIL_SILVER_CLEANED""")
spark.sql(f"""
CREATE TABLE IF NOT EXISTS RETAIL_SILVER_CLEANED
USING DELTA
LOCATION '{silver_path}'
""")

# COMMAND ----------

spark.sql("SELECT * FROM RETAIL_SILVER_CLEANED").show()

# COMMAND ----------

df_silver.show()

# COMMAND ----------

# MAGIC %md
# MAGIC ### Gold Layer

# COMMAND ----------

# Load clean transaction from silver layer
silver_df = spark.read.format("delta").load(silver_path)

# COMMAND ----------

from pyspark.sql.functions import sum, avg, countDistinct

gold_df = silver_df.groupBy(
    "transaction_date",
    "product_id","product_name","category",
    "store_id","store_name","location"
).agg(
    sum("quantity").alias("total_quantity_sold"),
    sum("total_amount").alias("total_sales_amount"),
    countDistinct("transaction_id").alias("number_of_transactions"),
    avg("total_amount").alias("average_transaction_value")
)
display(gold_df)



# COMMAND ----------

gold_path = "abfss://retail-container@retailstorage2003.dfs.core.windows.net/gold/"

gold_df.write.mode("overwrite").format("delta").save(gold_path)


# COMMAND ----------

spark.sql(f"""
    CREATE TABLE IF NOT EXISTS retail_gold_sales_summary
    USING DELTA
    LOCATION '{gold_path}';
    """
)

# COMMAND ----------

# MAGIC %sql SELECT * FROM retail_gold_sales_summary;