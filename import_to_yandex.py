from yandex_music import Client
from datetime import datetime
import time

class ClientForImport:
    def __init__(self):
        self.counter = 0
        self.client = None
        self.revision_playlist = 0
        self.playlist = None
        self.is_new_playlist = False
    def __init_client_yandex(self,token):
        try:
           self.client = Client(token).init()
        except Exception as e:
            print(f"Ошибка при инициализации клиента яндекс музыки: {e}")
    def __is_new_playlist(self):
        print("=" * 50)
        while True:
            user_data = input("Добавить в отдельный плэйлист?(Д/Н): ").upper()
            if user_data=="Д":
                print("=" * 50)
                self.is_new_playlist = True
                return True
            if user_data=="Н":
                print("=" * 50)
                self.is_new_playlist = False
                return False
            print("Некорректный выбор введи Д либо Н")
    def __create_playlist(self):
        new_playlist = self.client.users_playlists_create(
                        title=f"import from VK {datetime.now().strftime('%d.%m.%Y')}",
                        visibility='private')
        self.playlist = new_playlist
        return new_playlist
    def __search_song(self, song_name):
        time.sleep(0.3)
        search_result = self.client.search(song_name)
        if not search_result.tracks or not search_result.tracks.results:
            return False
        track_in_yandex = search_result.tracks.results[0]
        album_id = track_in_yandex.albums[0].id if track_in_yandex.albums else None
        if track_in_yandex:
            time.sleep(0.3)
            if self.is_new_playlist:
                self.client.users_playlists_insert_track(
                    kind=self.playlist.kind,
                    track_id=track_in_yandex.id,
                    album_id=album_id,
                    revision=self.revision_playlist
                )
                self.revision_playlist += 1
            else:
                track_in_yandex.like()
        else:
            return False
        return True
    def start_import(self, token, tracklist):
        self.__init_client_yandex(token)
        if self.client is None:
            return
        is_new_playlist = self.__is_new_playlist()
        if is_new_playlist:
            new_playlist = self.__create_playlist()
            self.revision_playlist = new_playlist.revision
        print("Поиск и добавление треков в Я.Музыке")
        for track in tracklist:
            print(f"Поиск трека: {track}")
            result = self.__search_song(track)
            if result:
                self.counter += 1
                print("Трек найден и добавлен")
            else:
                print(f"Трек: {track} не найден")
        print(f"Добавили в яндекс треков: {self.counter}")


class ClientForAuth:
    def __init__(self):
        self.client = Client()
    def get_my_token(self):
        token = self.__generate_yandex_token()
        return token
    def __generate_yandex_token(self):
        print("Ожидание авторизации пользователя в яндексе...")
        # Метод засыпает и ждет, пока пользователь введет код на сайте Яндекса
        token_info = self.client.device_auth(on_code=self.__on_code_callback)
        print("\nАвторизация успешно завершена!")
        print(f"Ваш Access Token: {token_info.access_token}")
        print(f"Токен действителен (в секундах): {token_info.expires_in}")
        return token_info.access_token
    @staticmethod
    def __on_code_callback(code):
        """
        Эта функция вызывается автоматически, когда Яндекс сгенерирует код.
        """
        print("=" * 50)
        print(f"1. Перейдите по ссылке: {code.verification_url}")
        print(f"2. Введите этот проверочный код: {code.user_code}")
        print("=" * 50)

yandex_import = ClientForImport()
yandex_auth = ClientForAuth()