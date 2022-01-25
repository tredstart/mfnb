known_modes = ["Sage", "Path", "Paths", "Tails", "Baryon", "Tailed"]


class Jutsu(object):
    chakra_requirement = 0
    requires_mode = None
    type = None
    base_damage = 0

    def __init__(self, name, damage):
        self.name = name
        self.base_damage = damage

    def set_chakra_requirement(self, requirement):
        self.chakra_requirement = requirement

    def set_mode(self, requirement):
        self.requires_mode = requirement

    def set_type(self, t):
        self.type = t
