import random
import sys
from time import sleep

from src.api import Api
from src.menu import create_character, start_game, display_damage, get_opponent, pick_jutsu, pick_tools, gain_chakra

tools = {
    "Shuriken": {
        "number": random.randint(10, 15),
        "base_damage": random.randint(10, 20)
    },
    "Kunai": {
        "number": random.randint(5, 10),
        "base_damage": random.randint(20, 30)
    }
}

if __name__ == '__main__':
    start = start_game()
    api = Api(debug=False)
    if not start:
        exit(1)
    character = None
    if start == "create":
        uid = random.randint(1, int(sys.maxsize / 2))
        character = create_character(api, tools, uid, api.set_new_battle_link)
        battle = api.get_battle()
        while battle["black"] == "" or battle["opponent_hp"] == "":
            sleep(3)
            battle = api.get_battle()

    elif start == "accept":
        uid = random.randint(int(sys.maxsize / 2), sys.maxsize)
        character = create_character(api, tools, uid, api.set_accept_battle_link)
        api.set_stats(character.hp)
    else:
        exit(2)
    print(character)

    while character.hp > 0:
        battle = api.get_battle()

        while battle['move'] != character.uid:
            sleep(5)
            battle = api.get_battle()
        print("--------New Move--------")
        print(f"{get_opponent(battle)} HP:")
        print(battle["opponent_hp"])
        if battle['move_number'] < 0:
            break

        if battle['move_number'] != 1:
            display_damage(battle, character)
            if character.hp <= 0:
                api.set_move()
                api.change_side()
                break
        print(character)
        jutsu_used = ""
        tools_used = ""
        jutsu_damage = ""
        jutsu_types = ""
        tools_damage = 0
        move = 0
        for i in range(battle['moveset']):
            if move >= battle['moveset']:
                break
            print(">> (1) Jutsu \t (2) Tools \t (3) Gain chakra")
            res = int(input())
            if res == 1:
                jutsu_used, jutsu_types, jutsu_damage, move = pick_jutsu(jutsu_used, jutsu_types,
                                                                         jutsu_damage, character, move,
                                                                         battle["moveset"])
            elif res == 2:
                tools_used, tools_damage = pick_tools(tools_used, tools_damage, character.tools)
            elif res == 3:
                gain_chakra(character)
            else:
                print("Move wasted")
            move += 1
        api.set_move(jutsu_used, jutsu_types, jutsu_damage, tools_used, tools_damage,
                     battle['move_number'] + 1, character.hp)

        api.change_side()
        print(character)
        print("------_End of move------")
    print("great game!")
