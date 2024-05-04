import json
import six
import sys

if sys.version_info >= (3, 12, 0):
    sys.modules['kafka.vendor.six.moves'] = six.moves
from kafka import KafkaConsumer
import schedule
from schedule import every, repeat

consumer = KafkaConsumer(
    'news_topic', bootstrap_servers='localhost:9092', auto_offset_reset='earliest')

# def scheduler():
#     """Schedule an email to the user every 2 mins"""
#     schedule.every(10).minutes.do(send_email)

@repeat(every(10).minutes)
def send_email(file_name: str) -> str:
    """Send email based on the template and get the data from file_name json file"""
    pass

def consume_news():
    for message in consumer:
        # Test line
        news_file_name = message.value.decode('utf-8')
        print(news_file_name)
        # Consume the news file name and process it by passing it to the function.
        # send_email(news_file_name)
        # scheduler(news_file_name)

if __name__ == "__main__":
    consume_news()
