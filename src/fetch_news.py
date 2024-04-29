import json
import requests


def fetch_news(api_key, query, language='en'):
    url = f'https://newsdata.io/api/1/news'
    params = {
        'apikey': api_key,
        'q': query,
        'language': language
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raise an exception for 4XX or 5XX errors

        print(f"Request URL: {response.request.url}")

        # Parse the JSON response
        data = response.json()

        # Parse the JSON response
        data = response.json()
        return data

    except requests.exceptions.RequestException as e:
        print(f"Error fetching news: {e}")
        return None

def main():
    # Set your NewsData.io API key here
    api_key = 'pub_4128925dfa2a70c562b279e6cda7553c93e46'

    # Set query parameters
    query = 'bollywood'

    language = 'en'

    # Fetch news articles
    news_data = fetch_news(api_key, query, language)

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
        print(json.dumps(news_data, indent=4))

    else:
        print("Failed to fetch news data.")

def news_api(file_name: str):
    # Fetch news using news API and return news if there is new news and None if there is no new news.
    return None


if __name__ == "__main__":
    main()
