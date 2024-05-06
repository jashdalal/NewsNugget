"""Fetch News"""
import json
import requests

def fetch_news(api_key = 'pub_4128925dfa2a70c562b279e6cda7553c93e46', language = 'en'):
    """Fetch news using the newsdata.io API

    Args:
        api_key (str) : newsdata.io API keys. Default is pub_4128925dfa2a70c562b279e6cda7553c93e46
        language (en) : Language of the fetched news article. Default is English

    Returns:
        dict: JSON Dict if fetch news article was successful else
        None: If news API returned an error.
    """
    url = f'https://newsdata.io/api/1/news'
    params = {
        'apikey': api_key,
        'country': 'us',
        'language': language,
        'size': 10  # Number of news article per API hit can between 1 to 50.
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raise an exception for 4XX or 5XX errors

        print(f"Request URL: {response.request.url}")

        # Parse the JSON response
        data = response.json()

        return data

    except requests.exceptions.RequestException as e:
        print(f"Error fetching news: {e}")
        return None

def news_api(file_name: str):
    """Fetch News data dict and write it to JSON file

    Args:
        file_name (str) : JSON file name where the news data dict should be stored

    Returns:
        str: JSON file_name if fetch news article was successful else
        None: If news API returned an error.
    """
    # Fetch news articles
    news_data = fetch_news()

    if news_data:
        if 'results' in news_data:
            found_paid_content = False

            for article in news_data['results']:
                if 'content' in article and article['content'] == 'ONLY AVAILABLE IN PAID PLANS':
                    found_paid_content = True
                    break

            if found_paid_content:
                with open('sample_data.json', 'r', encoding='utf-8') as f:
                    news_data = json.load(f)
       
        # Pretty print the response
        news_json = json.dumps(news_data, indent=4)
        with open(file_name, 'w') as fp:
            fp.write(news_json)

        return file_name

    else:
        print("Failed to fetch news data.")
        return None

if __name__ == "__main__":
    news_api('test.json')
