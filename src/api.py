import json

import requests


class Api(object):
    base_link = "https://nabapi.herokuapp.com/"
    get_character_link = "api/character/"
    set_new_battle_link = "api/new_battle/"
    set_accept_battle_link = "api/accept_battle/"
    get_current_battle_link = "api/current_battle/"
    set_stats_link = "api/set_current_stats/"
    get_current_stats = "api/get_current_stats/"
    move_link = "api/move/"
    get_jutsu_link = "api/get_jutsu/"
    get_jutsu_type_link = "api/get_jutsu_type/"
    change_side_link = "api/change_side/"

    def __init__(self, debug=False):
        if debug:
            self.base_link = "http://localhost:8000/"

    def handle_character(self, name, link):
        link = f'{self.base_link}{link}{name}/'
        response = requests.get(link)
        return response.json()

    def handle_battle(self, uid, name, battle_link):
        character = {
            "uid": uid,
            "name": name
        }
        link = f"{self.base_link}{battle_link}"
        headers = {"Content-type": "application/json"}
        response = requests.post(link, headers=headers, data=json.dumps(character))
        return response.json()

    def get_battle(self):
        link = f'{self.base_link}{self.get_current_battle_link}'
        response = requests.get(link)
        return response.json()

    def set_stats(self, hp):
        stats = {
            "hp": hp,
        }
        link = f"{self.base_link}{self.set_stats_link}"
        headers = {"Content-type": "application/json"}
        response = requests.post(link, headers=headers, data=json.dumps(stats))
        return response.json()

    def get_stats(self):
        link = f'{self.base_link}{self.get_current_stats}'
        response = requests.get(link)
        return response.json()

    def get_jutsu_type(self, name):
        link = f'{self.base_link}{self.get_jutsu_type_link}{name}/'
        response = requests.get(link)
        raw_text = response.json()['content']
        if "Taijutsu" in raw_text:
            return "Taijutsu"
        elif "Genjutsu" in raw_text:
            return "Genjutsu"
        else:
            return "Ninjutsu"

    def set_move(self, jutsu_used="", jutsu_types="", jutsu_damage="",
                 tools_used="", tools_damage=0, move_number=-1, opponent_hp=0):
        link = f"{self.base_link}{self.move_link}"
        body = {
            "jutsu_used": jutsu_used,
            "jutsu_types": jutsu_types,
            "jutsu_damage": jutsu_damage,
            "tools_used": tools_used,
            "tools_damage": tools_damage,
            "move_number": move_number,
            "opponent_hp": opponent_hp
        }
        headers = {"Content-type": "application/json"}
        response = requests.post(link, headers=headers, data=json.dumps(body))
        return response.json()

    def change_side(self):
        link = f"{self.base_link}{self.change_side_link}"
        response = requests.post(link)
        return response.json()