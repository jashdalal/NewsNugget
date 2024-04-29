import json
import six
import sys
import time

# Need to this import before importing Kafka due its compatibility issues with latest version of python
if sys.version_info >= (3, 12, 0):
    sys.modules['kafka.vendor.six.moves'] = six.moves
from kafka import KafkaProducer

from fetch_news import news_api
from summarize import summarize

producer = KafkaProducer(bootstrap_servers='localhost:9092')
news_json_file = "news_json_file_{}"

# TODO: Add a scheduler use python schedule library to fetch news like every 12 hours.


def news() -> str:
    """Fetch news using the new API function"""
    print("Hit news API:")
    news_file_name = news_json_file.format_map(time.time())
    # Write the news to the given json file. Return file name again if there is new news and none if there is no new news
    # news_file_name = new_api(news_file_name)
    # Summarize news
    # new_file_name = process_news(news_file_name)
    return news_file_name

def process_news(file_name: str) -> str:
    """Summarize news and add the summarize content to the same json file"""
    # Summarize news and do the logistics for it
    # summarize(file_name)
    return file_name


def news_listner() -> None:
    # Get the news json file name
    # new_news = news()
    ################# TEST CODE #################
    print("Start Reading:")
    t = time.time() + 3000
    file_size = 0
    while True:
        with open('new_api_file.txt', 'r') as file:
            file.seek(file_size)
            new_content = file.read()
            print(new_content, end='')
            file_size = file.tell()
            if time.time() > t:
                break
            if new_content:
                producer.send('news_topic', new_content.encode('utf-8'))
                producer.flush()
                continue
    ##################################
    # If there is new news, publish the file name for consumer to read and process.
    # if new_news:
        # producer.send('news_topic', new_news.encode('utf-8'))
        # producer.flush()


if __name__ == "__main__":
    news_listner()
