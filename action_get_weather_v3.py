from typing import Any, Text, Dict

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import requests
from bs4 import BeautifulSoup

google_url = 'https://www.google.com.vn/search'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/64.0.3282.186 '
                  'Safari/537.36'
}


class ActionGetWeatherInfo(Action):
    def name(self) -> Text:
        return 'action_get_weather_info'

    @staticmethod
    def get_weather_in_location(locations):
        # Returns list of weather conditions, degrees and location
        results = []
        if type(locations) is str:
            locations = [locations]
        locations = set(locations)
        for location in locations:
            r = requests.get(google_url,
                             params={'q': 'thời tiết ở %s' % location, 'cr': 'countryVN', 'lr': 'lang_vi', 'hl': 'vi'},
                             headers=headers)
            soup = BeautifulSoup(r.text, 'lxml')
            weather_box = soup.find('div', {'id': 'wob_dcp'})
            if weather_box:
                degree = soup.find('span', {'id': 'wob_tm'})
                condition = weather_box.text
                results.append((condition.lower(), degree.text.strip(), location))
        return results

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]):
        locations = tracker.get_slot('location')
        results = self.get_weather_in_location(locations)
        if results:
            for condition, degree, location in results:
                dispatcher.utter_message(template='utter_weather',
                                         condition=condition, degree=degree, location=location)
        else:
            dispatcher.utter_message(text='Xin lỗi bạn, mình không tìm thấy thông tin')