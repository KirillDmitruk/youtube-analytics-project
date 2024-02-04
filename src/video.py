from src.channel import Channel


class Video(Channel):
    def __init__(self, id_video):
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.id_video = id_video
        try:
            self.make_attribute_info()
        except:
            self.title = None
            self.url = None
            self.view_count = None
            self.like_count = None

    def __str__(self):
        return f"{self.title}"

    def get_info(self) -> None:
        """Выводит в консоль информацию о канале."""

        youtube = self.get_service()
        return youtube.videos().list(id=self.id_video, part="snippet,contentDetails,statistics").execute()

    def make_attribute_info(self):
        """
        Создает и заполняет атрибуты класса из полученной информации.
        """
        info = self.get_info()
        self.title = info['items'][0]['snippet']['title']
        self.url = f"https://www.youtube.com/watch?v={self.id_video}"
        self.view_count = info['items'][0]['statistics']['viewCount']
        self.like_count = info['items'][0]['statistics']['likeCount']


class PLVideo(Video):
    def __init__(self, id_video, id_play_list):
        self.id_play_list = id_play_list
        self.id_video = id_video
        super().make_attribute_info()
        self.make_attribute_info()

    def get_info_playlist(self) -> None:
        """Выводит в консоль информацию о канале."""
        youtube = self.get_service()
        return youtube.playlistItems().list(playlistId=self.id_play_list, videoId=self.id_video,
                                            part="snippet,contentDetails").execute()

    def make_attribute_info(self):
        """
        Создает и заполняет атрибуты класса из полученной информации.
        """
        info = self.get_info_playlist()
        self.url = f"https://www.youtube.com/watch?v={self.id_video}&list={self.id_play_list}"
        self.title = info['items'][0]['snippet']['title']