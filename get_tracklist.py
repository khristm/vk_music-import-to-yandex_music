import os
from vkpymusic import Service, TokenReceiver
import time
import sys
import requests

class MusicAgent:
    def __init__(self):
        self.path_config=None
        self.__set_path()
        self.service = None
        self.tracks = []
        if not self.__check_config() :
            self.__create_config()
    def __set_path(self):
        if getattr(sys, 'frozen', False):
            exe_dir = os.path.dirname(sys.executable)
            os.chdir(exe_dir)
            self.path_config=os.path.join(exe_dir,"config_vk.ini")
        else:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            os.chdir(script_dir)
            self.path_config=os.path.join(script_dir,"config_vk.ini")
    def __check_config(self):
        try:
            test_user_with_open_music="1117142401"
            self.service = Service.parse_config(self.path_config)
            self.service.get_songs_by_userid(user_id=test_user_with_open_music)
            time.sleep(1.5)
            print("Настройки учетки вк подключены из памяти")
            return True
        except Exception as e:
            print(f"Настройки токена для вк из конфига не рабочие, ошибка: {e}, требуется авторизация")
            return False
    def __create_config(self):
        time.sleep(1)
        print("Ожидание авторизации пользователя в ВК...")
        login = os.getenv("VK_LOGIN", False)
        password = os.getenv("VK_PASSWORD", False)
        while True:
            if not (login or password) :
                print("=" * 50)
                login = input("Логин ВК: ")
                password = input("Пароль ВК: ")
                print("=" * 50)
            try:
                receiver = TokenReceiver(login, password)
                if receiver.auth():
                    receiver.save_to_config(self.path_config)
                    self.service = Service.parse_config(self.path_config)
                    break
            except Exception as e:
                print(f"Неудачная авторизация в ВК, ошибка: {e}")
                login=False
                password=False
                time.sleep(5)
    @staticmethod
    def __track_to_str(tracks):
        str_tracks = []
        if not tracks:
            return str_tracks
        for track in tracks:
            track_full_name = track.artist + " - " + track.title
            if track_full_name not in str_tracks:
                str_tracks.append(track_full_name)
        str_tracks.reverse()
        return str_tracks
    def get_tracklist(self, user_id):
        if self.service is None:
            return None
        count = 100
        offset = 0
        while True:
            try:
                tracks = self.service.get_songs_by_userid(user_id=user_id,count=count, offset=offset)
                offset += 100
                if not tracks:
                    break
                self.tracks.extend(tracks)
                time.sleep(1.5)
            except Exception as e:
                print(e)
                return None
        return self.__track_to_str(self.tracks)
    def get_id_user(self,nickname):
        user_agent = self.service.user_agent
        # noinspection PyProtectedMember
        token = self.service._Service__token
        url = "https://api.vk.com/method/users.get"
        params = {
            "user_ids": nickname,
            "access_token": token,
            "v": "5.131"
        }
        headers = {
            "User-Agent": user_agent,
            "Accept": "*/*",
            "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
            "Connection": "keep-alive"
        }
        try:
            response = requests.get(url, params=params,headers=headers)
            res = response.json()
            user_data = res["response"]
            if user_data:
                vk_id = user_data[0]["id"]
                return vk_id
            else:
                return None
        except Exception as e:
            print(f"Ошибка сети при запросе к VK API: {e}")
            return None


music_agent = MusicAgent()



