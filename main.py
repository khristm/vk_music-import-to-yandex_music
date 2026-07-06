from get_tracklist import music_agent
from check_userid_VK import check_vk
from import_to_yandex import yandex_import, yandex_auth


def start():
    while True:
        user_id = input("Введи url страницы, либо никнейм, либо id в ВК откуда дергаем треки: ")
        clear_id = check_vk.start(user_id)
        if clear_id:
            tracks = music_agent.get_tracklist(clear_id)
            if not tracks:
                print("Треки не найдены")
                continue
            print(f"Найдено треков: {len(tracks)}")
            """Здесь логика импорта в я.музыку"""
            token = yandex_auth.get_my_token()
            yandex_import.start_import(token, tracks)
        else:
            print("Не найден в вк указаный пользователь, повтори ввод")
    print("Перенос из ВК в Я.Музыка выполнен, это окно автоматически закроется через 60 секунд")

def test(clear_id, token):
    while True:
        if clear_id:
            tracks = music_agent.get_tracklist(clear_id)
            if not tracks:
                print("Треки не найдены")
                continue
            print(f"Найдено треков: {len(tracks)}")
            """Здесь логика импорта в я.музыку"""
            yandex_import.start_import(token, tracks)
            break
        print("Не найден в вк указаный пользователь, повтори ввод")
    print("Перенос из ВК в Я.Музыка выполнен, это окно автоматически закроется через 60 секунд")

if __name__=="__main__":
    start()
