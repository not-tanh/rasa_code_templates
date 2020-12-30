from typing import Any, Text, Dict

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import requests
from bs4 import BeautifulSoup

news_url = 'https://vnexpress.net/'
news_type_to_path = {
    'thế giới': 'the-gioi',
    'kinh doanh': 'kinh-doanh',
    'giải trí': 'giai-tri',
    'thể thao': 'the-thao',
    'pháp luật': 'phap-luat',
    'giáo dục': 'giao-duc',
    'sức khỏe': 'suc-khoe',
    'đời sống': 'doi-song',
    'du lịch': 'du-lich',
    'khoa học': 'khoa-hoc'
}
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/64.0.3282.186 '
                  'Safari/537.36'
}


class ActionGetNews(Action):
    def name(self) -> Text:
        return 'action_get_news'

    @staticmethod
    def get_news_by_type(news_types):
        # Returns top story in vnexpress
        results = []
        if type(news_types) is str:
            news_types = [news_types]
        news_types = set(news_types)
        for news_type in news_types:
            news_path = news_type_to_path.get(news_type, '')
            if not news_path:
                continue
            r = requests.get(news_url + news_path, headers=headers)
            soup = BeautifulSoup(r.text, 'lxml')
            top_story_article = soup.find('article', {'class': 'article-topstory'})
            title = top_story_article.find('h3', {'class': 'title-news'}).text.strip()
            desc = top_story_article.find('p', {'class': 'description'}).text
            location_stamp = top_story_article.find('span', {'class': 'location-stamp'})
            location_stamp = location_stamp.text.strip() if location_stamp else ''
            # Delete location stamp in description (if any)
            desc = desc.replace(location_stamp, '', 1).strip()
            results.append('Tin %s:\n%s\n%s' % (news_type.lower(), title, desc))
        return results

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]):
        # Implement this yourself
        dispatcher.utter_message(text='Xin lỗi bạn, mình không tìm thấy thông tin')
