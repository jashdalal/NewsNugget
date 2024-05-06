"""Kafka Listner"""
import six
import sys
import time

# Need to this import before importing Kafka due its compatibility issues with latest version of python
if sys.version_info >= (3, 12, 0):
    sys.modules['kafka.vendor.six.moves'] = six.moves
from kafka import KafkaProducer

from fetch_news import news_api
from summarize import *

producer = KafkaProducer(bootstrap_servers='localhost:9092')
news_json_file = "news_json_file_{}.json"

def news() -> str:
    """Fetch news using the new API function

    Returns:
        JSON file name where the news article details are stored
    """
    # Generate a new json file name
    news_file_name = news_json_file.format(time.time())
    # Hit news API
    # If there is no new news return None.
    news_file_name = news_api(news_file_name)
    # Summarize news
    news_file_name = summarize_wrapper(news_file_name)
    return news_file_name


def news_listner() -> None:
    """Kafka Listner functions that listens to the API and process it before publishing a JSON news article file name"""
    while True:
        # Get the news json file name
        new_news = news()
        # If there is new news, publish the file name for consumer to read and process.
        if new_news:
            producer.send('news_topic', new_news.encode('utf-8'))
            producer.flush()
        # Avoid hitting the API repetitively
        time.sleep(10*60)


if __name__ == "__main__":
    news_listner()
