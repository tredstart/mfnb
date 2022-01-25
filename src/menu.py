import random

from src.api import Api
from src.character import Character
from src.jutsu import Jutsu, known_modes


def start_game():
    print(">> Create or Accept battle? <<")
    response = input()
    if response.lower() == "create" or response.lower() == "accept":
        return response.lower()
    return None


def create_character(api: Api, tools, uid, link):
    print("> Pick your character: ")
    response = input()
    character_json = api.handle_character(response, api.get_character_link)
    jutsu = []
    character = Character(character_json, tools, uid)
    api.handle_battle(uid, character.name, link)
    print("* getting jutsu...")
    for j in api.handle_character(response, api.get_jutsu_link)['jutsu']:
        jutsu_name = j.replace(" ", "_")
        jutsu_type = api.get_jutsu_type(jutsu_name)
        jutsu_ = Jutsu(j, character.iq * character.hand_seals)
        jutsu_.set_type(jutsu_type)
        for mode in known_modes:
            if mode in jutsu_name:
                jutsu_.set_mode(mode)
                break

        jutsu.append(jutsu_)
        print('#', end='', flush=True)
    character.set_jutsu(jutsu)
    for j in character.jutsu:
        j.set_chakra_requirement(random.randint(int(character.chakra * 0.03),
                                                int(character.chakra / (character.stamina * character.iq))))
    print()
    print("* character created!")
    print("* waiting for opponent *")
    return character


def get_opponent(battle):
    if battle["move"] == battle["white"]:
        opponent = battle["black_name"]
    else:
        opponent = battle["white_name"]
    return opponent


def display_damage(battle: dict, character: Character):
    opponent = get_opponent(battle)
    if battle["jutsu_damage"] != "" or battle["tools_damage"] != 0:
        total_damage = 0
        # todo dodge chance somewhere here
        print(f"> {opponent} used: ")
        if battle["jutsu_damage"] != 0:
            print(battle["jutsu_used"])
            types = battle["jutsu_types"].split(", ")
            jutsu_damage = [float(x) for x in battle["jutsu_damage"].split(" ") if x != ""]
            j_damage = 0
            for t, j in zip(types, jutsu_damage):
                j_damage += j / character[t]
            total_damage += j_damage
            print(f"with {j_damage}")
        if battle["tools_damage"] != 0:
            print(battle["tools_used"])
            print(f"with {battle['tools_damage']}")
            total_damage += battle['tools_damage']
        print(f"Total: {total_damage}")
        character.hp -= total_damage
    else:
        print(f"> {opponent} played strategy...")


def pick_jutsu(jutsu_used, jutsu_types, jutsu_damage, character, i, moveset):
    number_of_usable_jutsu = 0
    for i, jutsu in enumerate(character.jutsu):
        chakra_after = character.chakra - jutsu.chakra_requirement
        if chakra_after >= 0:
            number_of_usable_jutsu += 1
            print(f"({i}) {jutsu.name} \t", end=' ')
        if i % 3 == 0:
            print()
    if number_of_usable_jutsu == 0:
        print("Not enough chakra")
        return jutsu_used, jutsu_types, jutsu_damage
    choice = int(input())

    j_damage, move_number = character.use_jutsu(i, character.jutsu[choice], moveset)
    if j_damage != 0:
        jutsu_damage += str(j_damage) + " "
        jutsu_used += character.jutsu[choice].name + ", "
        t = character.jutsu[choice].type
        jutsu_types += t + ", "
        character.chakra -= character.jutsu[choice].chakra_requirement
        return jutsu_used, jutsu_types, jutsu_damage, move_number


def pick_tools(tools_used, tools_damage, tools):
    number_of_usable_tools = 0
    t = {}
    for key, value in tools.items():
        if value['number'] > 0:
            number_of_usable_tools += 1
            print(f">> {key} \t")
            t[key[0]] = key
    if number_of_usable_tools == 0:
        print("Not enough tools")
    else:
        response = input()
        k = response.upper()
        if k in t.keys():
            tools_damage += tools[t[k]]['base_damage']
            tools_used += t[k] + ", "
            tools[t[k]]['number'] -= 1
        else:
            print("can't use that")
        return tools_used, tools_damage


def gain_chakra(character):
    character.chakra += character.starting_chakra_amount / 10
