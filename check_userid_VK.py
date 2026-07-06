import re
from get_tracklist import music_agent

class CheckIDVK:
    def __init__(self,vk_client):
        self.vk_client = vk_client
        self.id_from_front=None
        self.id_vk=None
    def start(self,id_from_front:str):
        self.id_vk = None
        self.id_from_front = id_from_front
        id_vk = self.check_str()
        if id_vk:
            self.id_vk = id_vk
        return self.id_vk
    def check_str(self):
        match = re.search(r'id(\d+)', self.id_from_front)
        if match:
            return match.group(1)
        try:
            vk_id = int(self.id_from_front)
            return vk_id
        except ValueError:
            pass
        clean_match = re.search(r'vk\.com/([^/?#\s]+)', self.id_from_front)
        if clean_match:
            nickname = clean_match.group(1)
            id_vk = self.vk_client.get_id_user(nickname)
            if id_vk:
                return id_vk
        dog_match = re.search(r'@([^/?#\s]+)', self.id_from_front)
        if dog_match:
            id_vk = self.vk_client.get_id_user(dog_match.group(1))
            if id_vk:
                return id_vk
        id_vk = self.vk_client.get_id_user(self.id_from_front)
        if id_vk:
            return id_vk
        return None

check_vk = CheckIDVK(music_agent)