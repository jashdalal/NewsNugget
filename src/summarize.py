import json
from pyspark.sql import SparkSession
from pyspark.sql.functions import udf
from pyspark.sql.types import StructType, StructField, StringType, ArrayType, IntegerType
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer


def summarize(news_article: str):
    # Read the news content parallely and summarize and add the summary to the file_name

    prompt = f"Summarize the below news article in about 50 words. Highlight the major takeaways from the article : {news_article}"
    
    model_name = "google/flan-t5-base"
    model = AutoModelForSeq2SeqLM.from_pretrained(
        model_name
    ).to("cpu")

    tokenizer = AutoTokenizer.from_pretrained(model_name, padding_side="right")

    model_inputs = tokenizer([prompt], return_tensors="pt").to("cpu")

    generated_ids = model.generate(**model_inputs, max_new_tokens=100, num_beams=1, no_repeat_ngram_size=2, top_k=50, top_p=0.95, temperature=0.7)
    output = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)

    summary = output[0]
    return summary

def summarize_wrapper(file_path):
    file_reader = open(file_path)
    news_data_json = json.load(file_reader)
    news_data = news_data_json['results']
    
    # Create a SparkSession
    spark = SparkSession.builder \
    .appName("JSON to DataFrame with Custom Function") \
    .getOrCreate()
    
    # Define schema for the DataFrame
    schema = StructType([
        StructField("article_id", StringType(), True),
        StructField("title", StringType(), True),
        StructField("link", StringType(), True),
        StructField("keywords", ArrayType(StringType()), True),
        StructField("creator", StringType(), True),
        StructField("video_url", StringType(), True),
        StructField("description", StringType(), True),
        StructField("content", StringType(), True),
        StructField("pubDate", StringType(), True),
        StructField("image_url", StringType(), True),
        StructField("source_id", StringType(), True),
        StructField("source_priority", IntegerType(), True),
        StructField("source_url", StringType(), True),
        StructField("source_icon", StringType(), True),
        StructField("language", StringType(), True),
        StructField("country", ArrayType(StringType()), True),
        StructField("category", ArrayType(StringType()), True),
        StructField("ai_tag", StringType(), True),
        StructField("sentiment", StringType(), True),
        StructField("sentiment_stats", StringType(), True),
        StructField("ai_region", StringType(), True)
    ])
    
    # Create a DataFrame from the array of JSON objects
    # df = spark.createDataFrame(news_data)
    df = spark.createDataFrame(news_data, schema)

    # Register the custom function as a UDF (User Defined Function)
    custom_function_udf = udf(summarize, StringType())
    
    # Apply the custom function on the content column and create a new column called 'summary'
    df = df.withColumn("summary", custom_function_udf(df["content"]))

    # Show the DataFrame
    # df.show(truncate=False)
    df.select("summary").show(truncate=False)
    
    output_file_path = "src/summarized_data.json"
    df_list = df.rdd.map(lambda row: row.asDict()).collect()

    # Write the list of dictionaries to a JSON file
    with open(output_file_path, "w") as json_file:
        json.dump(df_list, json_file, indent=2)
    
    # Stop the SparkSession
    spark.stop()

if __name__=="__main__":
    summarize_wrapper('src/sample_data.json')

