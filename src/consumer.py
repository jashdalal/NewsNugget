"""Kafka Consumer"""
import json
import requests
import six
import sys
import time

# Compatibility issues with kafka and latest python version
if sys.version_info >= (3, 12, 0):
    sys.modules['kafka.vendor.six.moves'] = six.moves
from kafka import KafkaConsumer

from email_newsletter import send_email

# Initialize Kafka Consumer
consumer = KafkaConsumer(
    'news_topic', bootstrap_servers='localhost:9092', auto_offset_reset='earliest')
user_preference_file = 'preferences.json'  # JSON file name to store user preference

def user_preference_getter() -> str:
    """Interface to MangoDB and get the latest data from the DB and store it in a JSON file

    Returns:
        User preference JSON file name
    """
    userdata = requests.get("http://localhost:3000/userData")
    userdata = json.dumps(userdata.json())
    with open(user_preference_file, 'w') as fp:
        fp.write(userdata)
    return user_preference_file

def email(file_name: str):
    """Get the updated user data and send Email accordingly

    Args:
        file_name (str) : JSON file name containing all the fetched and summarize news article responce
    """
    user_preference_file = user_preference_getter()
    send_email(file_name, user_preferences_file=user_preference_file)

def consume_news():
    """Kafka Consumer function used to fetch the publish the news file name and send Email
    Code will run every 10 mins to avoid fluding the email inbox of the subscriber
    """
    for message in consumer:
        # Listen for the publisher for the generated NEWS JSON file
        news_file_name = message.value.decode('utf-8')
        # Use JSON file to read and send email
        print("Sending Email...")
        email(news_file_name)
        print("Email sent!!")
        # Add a sleep time as we do not want to flood the users inbox every minute
        time.sleep(10*60)

if __name__ == "__main__":
    consume_news()
