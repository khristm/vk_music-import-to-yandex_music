import asyncio
from yandex_music import Client, ClientAsync
from datetime import datetime
from yandex_music.utils.difference import Difference


def is_new_playlist():
    print("=" * 50)
    while True:
        user_data = input("Добавить в отдельный плэйлист?(Д/Н): ").upper()
        if user_data == "Д":
            print("=" * 50)
            return True
        if user_data == "Н":
            print("=" * 50)
            return False
        print("Некорректный выбор введи Д либо Н")

class ClientForImport:
    def __init__(self):
        self.counter = 0
        self.client = None
        self.revision_playlist = 0
        self.playlist = None
        self.is_new_playlist = False
        self.list_songs = []
    async def __init_client_yandex(self,token):
        try:
           self.client = await ClientAsync(token).init()
        except Exception as e:
            print(f"Ошибка при инициализации клиента яндекс музыки: {e}")
    async def __create_playlist(self):
        try:
            new_playlist = await self.client.users_playlists_create(
                            title=f"import from VK {datetime.now().strftime('%d.%m.%Y')}",
                            visibility='private')
            self.playlist = new_playlist
            self.revision_playlist = new_playlist.revision
            return True
        except Exception as e:
            print(f"Не смогли создать новый плейлист с ошибкой: {e}")
            return False
    async def start_package_import(self, token, tracklist, user_new_playlist:bool):
        await self.__init_client_yandex(token)
        if self.client is None:
            return
        if user_new_playlist:
            self.is_new_playlist = True
            playlist_created = await self.__create_playlist()
            if not playlist_created:
                return
        print("=" * 50)
        print("Поиск в яндексе треков для добавления")
        print("=" * 50)
        await self.__async_search_tracks(tracklist)
        print("Поиск окончен, добавляем треки......")
        print("=" * 50)
        await self.__import_in_yandex()
        print(f"В яндекс перенесено треков: {self.counter}")
    async def __search_song_and_add_in_list(self, song_name):
        try:
            search_result = await self.client.search(song_name)
        except Exception as e:
            print(f"Ошибка при поиске трека {song_name}, текст ошибки: {e}")
            return None
        if not search_result.tracks or not search_result.tracks.results:
            print(f"Трек {song_name} не найден в яндексе")
            return None
        track_in_yandex = search_result.tracks.results[0]
        album_id = track_in_yandex.albums[0].id if track_in_yandex.albums else None
        print(f"Трек {song_name} найден в яндексе и включен в список к добавлению ")
        self.counter += 1
        if self.is_new_playlist:
            return {"id":str(track_in_yandex.id), "album_id":str(album_id), 'type': 'track'}
        return str(track_in_yandex.id)
    async def __import_in_yandex(self):
        if not self.list_songs:
            return
        if self.is_new_playlist:
            change_diff=Difference()
            change_diff.add_insert(at=0,tracks=self.list_songs)
            operation_diff = change_diff.to_json()
            await self.client.users_playlists_change(
                kind=self.playlist.kind,
                diff=operation_diff,
                revision=self.revision_playlist
            )
            return
        await self.client.users_likes_tracks_add(track_ids=self.list_songs)
        return
    async def __async_search_tracks(self, song_list:list[str]):
        song_list.reverse()
        BATCH_SIZE=10
        for i in range(0, len(song_list), BATCH_SIZE):
            chunk = song_list[i:i + BATCH_SIZE]
            task = [self.__search_song_and_add_in_list(song) for song in chunk]
            result = await asyncio.gather(*task)
            for res in result:
                if res is not None:
                    self.list_songs.append(res)
            await asyncio.sleep(0.5)








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