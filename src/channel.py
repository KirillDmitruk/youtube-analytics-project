import json
import os

# необходимо установить через: pip install google-api-python-client
from googleapiclient.discovery import build


class Channel:
    """Класс для ютуб-канала"""

    def __init__(self, channel_id) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.__channel_id = channel_id
        youtube = self.get_service()
        channel = youtube.channels().list(id=channel_id, part='snippet,statistics').execute()
        self.title = channel['items'][0]['snippet']['title']
        self.description = channel['items'][0]['snippet']['description']  # описание канала
        self.url = f'https://www.youtube.com/channel/{channel_id}'  # ссылка на канал
        self.subscriberCount = channel['items'][0]['statistics']['subscriberCount']  # количество подписчиков
        self.video_count = channel['items'][0]['statistics']['videoCount']  # количество видео
        self.viewCount = channel['items'][0]['statistics']['viewCount']  # общее количество просмотров


    @property
    def channel_id(self):
        return self.__channel_id


    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        # YT_API_KEY скопирован из гугла и вставлен в переменные окружения
        api_key: str = os.getenv('YT_API_KEY')
        # создать специальный объект для работы с API
        youtube = build('youtube', 'v3', developerKey=api_key)
        channel_id = 'UCwHL6WHUarjGfUM_586me8w'  # HighLoad Channel
        channel = youtube.channels().list(id=channel_id, part='snippet,statistics').execute()
        print(json.dumps(channel, indent=4, ensure_ascii=False))


    @classmethod
    def get_service(cls):
        # YT_API_KEY скопирован из гугла и вставлен в переменные окружения
        api_key: str = os.getenv('YT_API_KEY')
        # создать специальный объект для работы с API
        youtube = build('youtube', 'v3', developerKey=api_key)
        return youtube


    def to_json(self, file_name):
        with open(file_name, 'w', encoding='utf-8') as file:
            json.dump(self.dict, file, indent=4, ensure_ascii=False)
