import asyncio
from get_tracklist import music_agent
from check_userid_VK import check_vk
from import_to_yandex import yandex_import, yandex_auth, is_new_playlist
import os


async def start():
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
            playlist = is_new_playlist()
            await yandex_import.start_package_import(token, tracks, playlist)
        else:
            print("Не найден в вк указаный пользователь, повтори ввод")
    print("Перенос из ВК в Я.Музыка выполнен")

async def test(clear_id, token):
    while True:
        if clear_id:
            tracks = music_agent.get_tracklist(clear_id)
            if not tracks:
                print("Треки не найдены")
                continue
            print(f"Найдено треков: {len(tracks)}")
            """Здесь логика импорта в я.музыку"""
            playlist = is_new_playlist()
            await yandex_import.start_package_import(token, tracks, playlist)
            break
        print("Не найден в вк указаный пользователь, повтори ввод")
    print("Перенос из ВК в Я.Музыка выполнен")

async def test_with_token():
    yandex_token=os.getenv("TOKEN_YANDEX")
    id_in_vk=os.getenv("ID_TEST_USER")
    await test(id_in_vk, yandex_token)

if __name__=="__main__":
    #asyncio.run(start())
    asyncio.run(test_with_token())
