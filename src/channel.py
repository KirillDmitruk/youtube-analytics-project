import json
import os

from googleapiclient.discovery import build

KEY_API_YOUTUBE = os.getenv("KEY_API_YOUTUBE")


class Channel:
    """Класс для ютуб-канала"""

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""

        self.__channel_id = channel_id
        self.make_attribute_info()

    def __repr__(self):
        return (f"{self.channel_id} id канала\n"
                f"{self.title} название канала\n"
                f"{self.video_count} количество видео\n"
                f"{self.url} url")

    def __str__(self):
        return f'{self.title} {self.url}'

    def __add__(self, other):
        return int(self.subscriber_count) + int(other.subscriber_count)

    def __sub__(self, other):
        return int(self.subscriber_count) - int(other.subscriber_count)

    def __lt__(self, other):
        return int(self.subscriber_count) < int(other.subscriber_count)

    def __le__(self, other):
        return int(self.subscriber_count) <= int(other.subscriber_count)

    def __gt__(self, other):
        return int(self.subscriber_count) > int(other.subscriber_count)

    def __ge__(self, other):
        return int(self.subscriber_count) >= int(other.subscriber_count)

    def __eq__(self, other):
        return int(self.subscriber_count) == int(other.subscriber_count)

    def get_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        youtube = build('youtube', 'v3', developerKey=KEY_API_YOUTUBE)
        return youtube.channels().list(id=self.channel_id, part='snippet,statistics').execute()

    def print_info(self):
        """
        Выводит информацию на экран.
        """
        info = self.get_info()
        print(info)

    def make_attribute_info(self):
        """
        Создает и заполняет атрибуты класса из полученной информации.
        """
        info = self.get_info()
        self.title = info['items'][0]['snippet']['title']
        self.video_count = info['items'][0]["statistics"]["videoCount"]
        self.description = info['items'][0]['snippet']['description']
        self.url = f"https://www.youtube.com/channel/{self.channel_id}"
        self.subscriber_count = info['items'][0]["statistics"]["subscriberCount"]
        self.view_count = info['items'][0]["statistics"]["subscriberCount"]

    @property
    def channel_id(self):
        return self.__channel_id

    @classmethod
    def get_service(cls):
        """
        Возвращает объект для работы с YouTube API.
        """
        return build('youtube', 'v3', developerKey=KEY_API_YOUTUBE)

    def to_json(self):
        """
        Создает файл json с информацией из атрибутов класса.
        """
        with open('youtube_statistics.json', 'w', encoding='utf-8') as file:
            file.write(json.dumps(self.__dict__))