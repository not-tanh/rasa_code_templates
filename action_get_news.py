from typing import Any, Text, Dict

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import requests
from bs4 import BeautifulSoup

news_url = 'https://vnexpress.net/'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/64.0.3282.186 '
                  'Safari/537.36'
}


class ActionGetNews(Action):
    def name(self) -> Text:
        # Implement this yourself
        pass

    @staticmethod
    def get_news():
        # Returns top story in vnexpress
        r = requests.get(news_url, headers=headers)
        soup = BeautifulSoup(r.text, 'lxml')
        top_story_article = soup.find('article', {'class': 'article-topstory'})
        title = top_story_article.find('h3', {'class': 'title-news'}).text.strip()
        desc = top_story_article.find('p', {'class': 'description'}).text
        location_stamp = top_story_article.find('span', {'class': 'location-stamp'}).text.strip()
        # Delete location stamp in description
        desc = desc.replace(location_stamp, '', 1).strip()
        return '%s\n%s' % (title, desc)

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]):
        # Implement this yourself
        pass
