from src.jutsu import Jutsu


class Character(object):
    hp = 0
    chakra = 0
    jutsu = None
    starting_chakra_amount = 0

    def __init__(self, char, tools, uid):
        self.uid = uid
        self.tools = tools
        self.ninjutsu = char["Ninjutsu"]
        self.taijutsu = char["Taijutsu"]
        self.genjutsu = char["Genjutsu"]
        self.iq = char["Intelligence"]
        self.strength = char["Strength"]
        self.speed = char["Speed"]
        self.stamina = char["Stamina"]
        self.hand_seals = char["Hand seals"]
        self.total = char["Total"]
        self.name = char["Name"]

    def __getitem__(self, item: str):
        if item == "Taijutsu":
            return self.taijutsu
        if item == "Ninjutsu":
            return self.ninjutsu
        if item == "Genjutsu":
            return self.genjutsu

    def __generate_stats(self):
        self.chakra = self.total * len(self.jutsu)
        self.hp = (self.total - self.ninjutsu - self.taijutsu
                   - self.genjutsu - self.stamina) * self.stamina + self.chakra
        self.starting_chakra_amount = self.chakra

    def __activate_mode(self, mode):
        print(f"{mode} activated!")
        self.chakra *= 10
        self.hp = (self.total - self.ninjutsu - self.taijutsu
                   - self.genjutsu - self.stamina) * self.stamina + self.chakra

    def set_jutsu(self, jutsu_):
        self.jutsu = jutsu_
        self.__generate_stats()

    def use_jutsu(self, move_number, jutsu_: Jutsu, moveset):
        if jutsu_.requires_mode and move_number + 1 == moveset:
            print("Cannot use this right now!")
            return 0
        if jutsu_.requires_mode:
            self.__activate_mode(jutsu_.requires_mode)
            move_number += 1

        jutsu_damage = jutsu_.base_damage * self[jutsu_.type] * (0.045 * self.chakra)
        return jutsu_damage, move_number

    def __repr__(self):
        return f'{self.name}:\n' \
               f'HP: {self.hp}\n' \
               f'Chakra: {self.chakra}\n'
