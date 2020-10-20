#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 13 09:36:12 2020

@author: mickael
"""
import random
import pickle
import copy
import yaml
# import os
import time

# Vol honteux de script pour pas faire dl de module hors Conda
# from prettytable import PrettyTable
from prettyt import PrettyTable


def xp_to_level(xp):
    """
    Inutile
    chaque level = 1000 xp
    """
    # xp_per_level = []
    return round(xp/1000)


def print_list(txt):
    for elt in txt:
        print(elt)


def load_ascii(filename):
    with open(filename, 'r') as f:
        ascii_txt = f.readlines()
    return [elt.strip("\n") for elt in ascii_txt]


def load_dict_yaml(fname):
    with open(fname, "r") as f:
        d_elem = yaml.load(f)
    return d_elem


def req_input(list_possible):
    """
    Request input from user within a list of possible choice.
    """
    if type(list_possible) == dict:
        list_possible = list(list_possible.keys())

    action = input()
    while action.lower() not in list_possible:
        print("wrong input, possible expected values: " +
              str(list_possible))
        action = input()
    return action.lower()


def hp_fct(x, a, b):
    return value_function(x, a=a, b=b)


"""
dragon_values[key] = value_function(dragon_values["level"],
                                            a=dragon_values["proficiency"],
                                            b=dragon_values["b_" + key])
"""


def value_function(x, n=1.5, a=1, b=0):
    """
    x = level
    n = power
    b = Base stat value
    a = proficiency
    """
    return x**n + a*x + b


def affine_value_function(x, a=1, b=0):
    """
    b = Base stat value
    a = proficiency
    x = level
    """
    return a*x + b


def asses_dragon(dragon_obj):
    return "it's a " + str(dragon_obj.proficiency) + " Star dragon."


def generate_name(sex=""):
    if sex not in ["male", "female"]:
        sex = random.choice(["male", "female"])
    prefix = load_ascii(sex+"_prefix_dragon_name.txt")
    suffix = load_ascii(sex+"_suffix_dragon_name.txt")
    name = random.choice(prefix) + random.choice(suffix)
    return name.capitalize()


def generate_dragon_values(name="",
                           elem_type="",
                           sex="",
                           level="",
                           xp="",
                           proficiency="",
                           hp="",
                           mp="",
                           b_attack="",
                           b_defense="",
                           b_attack_spe="",
                           b_defense_spe=""
                           ):
    dragon_values = {}
    dragon_values["name"] = name
    dragon_values["elem_type"] = elem_type
    dragon_values["sex"] = sex
    dragon_values["hp"] = hp
    dragon_values["mp"] = mp
    dragon_values["level"] = level
    dragon_values["xp"] = xp
    dragon_values["proficiency"] = proficiency
    dragon_values["b_attack"] = b_attack
    dragon_values["b_defense"] = b_defense
    dragon_values["b_attack_spe"] = b_attack_spe
    dragon_values["b_defense_spe"] = b_defense_spe

    if not elem_type:
        dragon_values["elem_type"] = random.choice(["air",
                                                    "fire",
                                                    "water",
                                                    "earth"])

    if not sex:
        dragon_values["sex"] = random.choice(["male", "female"])

    if not name:
            dragon_values["name"] = generate_name(sex=dragon_values["sex"])

    if not level:
        dragon_values["level"] = 1

    if not proficiency:
        dragon_values["proficiency"] = random.randint(1, 10)

    if not hp:
        dragon_values["hp"] = affine_value_function(dragon_values["level"]/10,
                                                    a=dragon_values["proficiency"]/10 + 5,
                                                    b=10)*15
    if not mp:
        dragon_values["mp"] = value_function(dragon_values["level"],
                                             a=dragon_values["proficiency"],
                                             b=1)*2
    if not xp:
        dragon_values["xp"] = 0

    # base stat nudge by the elem type:
    d_b_stat = load_dict_yaml("base_stat.yaml")
    for key in ["attack", "defense", "attack_spe", "defense_spe"]:
        if dragon_values["b_" + key] == "":
            dragon_values["b_" + key] = d_b_stat[dragon_values["elem_type"]]["b_" + key]  # random.randint(1, 10)

        dragon_values[key] = value_function(dragon_values["level"],
                                            a=dragon_values["proficiency"],
                                            b=dragon_values["b_" + key])

    return dragon_values


def generate_dragon(dragon_values={}):
    if not dragon_values:
        dragon_values = generate_dragon_values()
    return dragon(dragon_values)


def show_all_stats(list_d):
    """
    Use of PrettyTable module
    """
    x = PrettyTable()
    x.add_column("Number:",
                 ["Name", "Elem Type", "Level", "HP", "MP", "Attack",
                  "Attack_spe", "Defense", "Defense_spe", "Rating"]
                 )
    i = 1
    for d in list_d:
        x.add_column(str(i),
                     [d.name,
                      d.elem_type.capitalize(),
                      d.level,
                      round(d.hp),
                      round(d.mp),
                      round(d.attack),
                      round(d.attack_spe),
                      round(d.defense),
                      round(d.defense_spe),
                      d.proficiency])
        i += 1
    print(x)


"""
╔╦╗╦═╗╔═╗╔═╗╔═╗╔╗╔
 ║║╠╦╝╠═╣║ ╦║ ║║║║
═╩╝╩╚═╩ ╩╚═╝╚═╝╝╚╝
"""


class dragon():
    def __init__(self, dragon_values):
        """
        Expected arguments:
        self.name = dragon_values["name"]
        self.elem_type = dragon_values["elem_type"]
        self.sex = dragon_values["sex"]
        self.level = dragon_values["level"]
        self.hp = dragon_values["hp"]
        self.mp = dragon_values["mp"]
        self.attack = dragon_values["attack"]
        self.defense = dragon_values["defense"]
        self.attack_spe = dragon_values["attack_spe"]
        self.defense_spe = dragon_values["defense_spe"]
        """
        for key in dragon_values:
            setattr(self, key, dragon_values[key])
        self.atk_spe_cost = 5

    def resume(self):
        print(self.name + " " +
              self.elem_type + " " +
              "Level: " + self.level + " " +
              "Rating: " + self.rating)

    def level_up(self, nb_level=1):
        """
        nb_level = number of gained level
        """
        if self.level >= 10:
            print("Dragon at max level, consider releasing or "
                  "fighting the Dragon Of Doom")
            return "max level"

        self.level += nb_level
        self.hp = value_function(self.level / 5,
                                 a=self.proficiency/10 + 5,
                                 b=1)*15

        self.mp = value_function(self.level,
                                 a=self.proficiency,
                                 b=1)*2

        for key in ["attack", "defense", "attack_spe", "defense_spe"]:
            setattr(self, key, value_function(self.level,
                                              a=self.proficiency,
                                              b=getattr(self, "b_" + key)
                                              )
                    )
        self.atk_spe_cost = affine_value_function(self.atk_spe_cost,
                                                  a=self.proficiency/10 + 1,
                                                  b=1)*2

    def attack_damage(self):
        """
        Useless
        """
        if self.attack_spe > self.attack and self.mp > self.atk_spe_cost:
            self.mp -= self.atk_spe_cost
            return self.attack_spe
        else:
            return self.attack

    def pokemon_damage(self, e_defense, e_defense_spe):
        # spe
        if self.attack_spe > self.attack and self.mp > self.atk_spe_cost:
            self.mp -= self.atk_spe_cost
            atk = self.attack_spe
            e_def = e_defense_spe
        # normal
        else:
            atk = self.attack
            e_def = e_defense
        formula = ((self.level*0.4 + 2)*atk)/e_def
        return formula


"""
╔╗ ╔═╗╔╦╗╔╦╗╦  ╔═╗  ═╦═╔╗╔╔═╗╔╦╗╔═╗╔╗╔╔═╗╔═╗
╠╩╗╠═╣ ║  ║ ║  ║╣    ║ ║║║╚═╗ ║ ╠═╣║║║║  ║╣
╚═╝╩ ╩ ╩  ╩ ╩═╝╚═╝  ═╩═╝╚╝╚═╝ ╩ ╩ ╩╝╚╝╚═╝╚═╝
"""


class battle_instance():
    """
    Class in charge of resolving battle
    between two dragons.
    """
    def __init__(self, player_dragon, enemy_dragon):
        self.p_dragon = copy.deepcopy(player_dragon)
        self.e_dragon = copy.deepcopy(enemy_dragon)

    def show_stats(self):
        """
        Useless
        """
        print("name: ", self.p_dragon.name, self.e_dragon.name)
        print("elem_type: ", self.p_dragon.elem_type, self.e_dragon.elem_type)
        print("level: ", self.p_dragon.level, self.e_dragon.level)
        print("hp: ", self.p_dragon.hp, self.e_dragon.hp)
        print("mp: ", self.p_dragon.mp, self.e_dragon.mp)
        print("attack: ", self.p_dragon.attack, self.e_dragon.attack)
        print("attack_spe: ", self.p_dragon.attack_spe,
              self.e_dragon.attack_spe)
        print("defense: ", self.p_dragon.defense,
              self.e_dragon.defense)
        print("defense_spe: ", self.p_dragon.defense_spe,
              self.e_dragon.defense_spe)
        print("Rating:", self.p_dragon.proficiency, self.e_dragon.proficiency)
        print("\n")

    def resolve_battle(self):
        print("Fight in Progress...", "")
        # For user experience
        time.sleep(1)
        while True:
            # print("p_dragon hp: ", round(self.p_dragon.hp))
            if self.p_dragon.hp > 0:
                dmg = self.p_dragon.pokemon_damage(self.e_dragon.defense,
                                                   self.e_dragon.defense_spe)
                self.e_dragon.hp -= dmg
            else:
                return "Player dragon defeated."
            # print("e_dragon hp: ", round(self.e_dragon.hp))
            if self.e_dragon.hp > 0:
                dmg = self.e_dragon.pokemon_damage(self.p_dragon.defense,
                                                   self.p_dragon.defense_spe)
                self.p_dragon.hp -= dmg
            else:
                return "Enemy dragon defeated."


"""
╔═╗╔═╗╔╦╗╔═╗╦ ╦╔═╗╦═╗╦  ╔╦╗
║ ╦╠═╣║║║║╣ ║║║║ ║╠╦╝║   ║║
╚═╝╩ ╩╩ ╩╚═╝╚╩╝╚═╝╩╚═╩═╝═╩╝
"""


class game_world():
    """
    main class to operate the game
    """
    def __init__(self):
        self.dragons_list = [generate_dragon()]
        self.maximum_dragons_list = 3
        self.inventory = []
        self.victory_token = 0
        self.town_choices = {"a": self.arena,
                             "s": self.shop,
                             "b": self.breed,
                             "t": self.team_manager,
                             "sa": self.save_world,
                             "l": self.load_world,
                             "q": self.gw_quit}

        self.arena_choices = {"f": self.arena_battle_choosing,
                              "g": self.main_town,
                              "d": self.arena_battle_dod,
                              "s": self.show_owned_dragon}

        self.arena_find_enemy = {"g": self.main_town}

        self.shop_choices = {"b": self.shop_dragon,
                             "u": self.shop_upgrade,
                             "g": self.main_town}
        self.shop_dragon_choices = {"g": self.shop}

        self.team_manager_choices = {"b": self.breed,
                                     "f": self.team_manager_free,
                                     "g": self.main_town}

        self.dragon_of_doom = dragon(generate_dragon_values(name="Leviathan",
                                                            elem_type="darkness",
                                                            level=10))

        self.ascii_town = load_ascii("ascii_town.txt")
        self.ascii_shop = load_ascii("ascii_shop.txt")
        self.ascii_arena = load_ascii("ascii_arena.txt")

        self.type_matrix = load_dict_yaml("matrix_elem.yaml")

        print("Welcome in Dragon of Doom !!!", "", "")

    def autosave(self):
        with open("saves/autosave", "wb") as savefile:
            pickle.dump([self.dragons_list,
                         self.maximum_dragons_list,
                         self.inventory,
                         self.victory_token,
                         self.dragon_of_doom],
                        savefile)

    def save_world(self):
        """
        save attribute in a pickle file
        """
        savename = input("Choose a savename:")
        with open("saves/" + savename, "wb") as savefile:
            pickle.dump([self.dragons_list,
                         self.maximum_dragons_list,
                         self.inventory,
                         self.victory_token,
                         self.dragon_of_doom],
                        savefile)
        print("Progression Saved")

    def load_world(self):
        """
        load attributes from specified pickle file
        """
        savename = input("Choose a save to load:")
        with open("saves/" + savename, "rb") as savefile:
            attr_list = pickle.load(savefile)
        self.dragon_list = attr_list[0]
        self.maximum_dragons_list = attr_list[1]
        self.inventory = attr_list[2]
        self.victory_token = attr_list[3]
        self.dragon_of_doom = attr_list[4]
        print("Save loaded.")

    def gw_quit(self):
        print("Session ended.")
        return "Coward die in shame"

    def show_owned_dragon(self):
        if not self.dragons_list:
            print("", "", "No dragons owned.")
        else:
            show_all_stats(self.dragons_list)
        """
        for d in self.dragons_list:
            print("")
            show_stats(d)
        """

    def main_town(self):

        txt = ["", "",
               "You're in the Town, where do you want to go?",
               "(A)rena    (S)hop",
               "(B)reed    (T)eam management",
               "(Sa)ve     (L)oad",
               "(Q)uit"]
        print_list(self.ascii_town)
        print_list(txt)
        action = req_input(self.town_choices)
        if action == "sa":
            self.save_world()
            return self.main_town()
        elif action == "l":
            self.load_world()
            return self.main_town()
        # Autosave
        self.autosave()
        return self.town_choices[action]()

    def team_manager(self):
        self.show_owned_dragon()
        txt = ["", "",
               "You're in the Team manager screen:",
               "You got " + str(self.victory_token) + " Victory Token.",
               "(B)reed    (F)ree",
               "(G)o back to town"]
        print_list(txt)
        action = req_input(self.team_manager_choices)
        return self.team_manager_choices[action]()

    def team_manager_free(self):
        self.show_owned_dragon()
        txt = ["", "",
               "Which Dragon would you like to set free:",
               "(1), (2) ... (n)",
               "(G)o back to team manager."]
        print_list(txt)
        action = input()
        if action.isdigit():
            try:
                print("Farewell " + self.dragons_list[int(action)-1].name)
                del self.dragons_list[int(action)-1]
            except (IndexError, ValueError):
                print("No dragon with that number.")

        return self.team_manager()

    def arena(self):
        txt = ["",
               "You're in the Arena:",
               "(F)ind enemy    (G)o back to town",
               "(S)how owned dragons",
               "Fight the (D)ragon Of Doom"]
        print_list(self.ascii_arena)
        print_list(txt)
        action = req_input(self.arena_choices)

        if action == "s":
            if not self.dragons_list:
                print("You don't Have any Dragon.")
            else:
                self.show_owned_dragon()
            return self.arena()

        elif action == "f":
            if not self.dragons_list:
                print("You don't Have any Dragon to bring in the Arena.")
                return self.arena()
            else:
                return self.arena_choices[action]()

        return self.arena_choices[action]()

    def arena_battle_choosing(self):
        txt = ["", "",
               "Choose which of your dragon will be fighting:",
               "(number of your dragon)",
               "(G)o back to town"]
        print_list(txt)

        self.show_owned_dragon()
        # show_all_stats(self.dragons_list)

        action = input()
        if action == "g":
            return self.arena()

        else:
            try:
                num = int(action)

            except (IndexError, ValueError):
                print("Wrong input.")
                return self.arena()

        print("", "There is 3 Dragons to choose to fight:")
        enemy_dragons = []
        p_dragon_level = self.dragons_list[num-1].level
        for _ in range(3):
            e_level = random.choice([0, 0, 1])
            e_level = p_dragon_level + e_level
            if e_level > 10:
                e_level = 10

            e_dragon = dragon(generate_dragon_values(level=e_level))
            enemy_dragons.append(e_dragon)

        show_all_stats(enemy_dragons)
        txt = ["(1), (2) or (3)",
               "(G)o back to town"]
        print_list(txt)

        action = req_input(["1", "2", "3", "g"])
        if action == "g":
            return self.arena()
        else:
            e_num = int(action)
            result = battle_instance(self.dragons_list[num-1],
                                     enemy_dragons[e_num-1]).resolve_battle()

        if result == "Player dragon defeated.":
            print("Your dragon died in the arena.")
            self.dragons_list.remove(self.dragons_list[num-1])

        elif result == "Enemy dragon defeated.":
            print("Your dragon is victorious!")
            if self.dragons_list[num-1].level < 10:
                print("And leveled up!")
                nbl = enemy_dragons[e_num-1].level - self.dragons_list[num-1].level + 1
                self.dragons_list[num-1].level_up(nb_level=nbl)
            else:
                print("Your Dragon is at maximum level, "
                      "consider training another one instead.")

        return self.arena()

    def arena_battle_dod(self):
        print("The dragon of Doom awaits you:")
        self.show_owned_dragon()
        # show_all_stats([self.dragon_of_doom])

        txt = ["", "",
               "Choose which of your dragon will be fighting the Dragon Of Doom",
               "(number of your dragon)",
               "(G)o back to town"]
        # show_all_stats(self.dragons_list)

        print_list(txt)

        action = input()
        if action == "g":
            return self.arena()

        else:
            try:
                num = int(action)

            except (IndexError, ValueError):
                print("Wrong input.")
                return self.arena()

        result = battle_instance(self.dragons_list[num-1],
                                 self.dragon_of_doom).resolve_battle()

        if result == "Player dragon defeated.":
            print("Your dragon died at the mercy of the Dragon Of Doom..."
                  " Pathetic.")
            self.dragons_list.remove(self.dragons_list[num-1])

        elif result == "Enemy dragon defeated.":
            print_list(["Congratulation on defeating the Dragon Of Doom!",
                        "The adventure is far from finished.", "",
                        "The winner is now the new Dragon of Doom!!!"])
            self.dragon_of_doom = self.dragons_list[num-1]
            self.dragons_list.remove(self.dragons_list[num-1])
            self.victory_token += 1

        return self.main_town()

    def shop(self):
        txt = ["", "",
               "You're in the shop:",
               "(B)uy a Dragon,    Buy an (u)pgrade",
               "(G)o back to town"
               ]
        print_list(self.ascii_shop)
        print_list(txt)
        action = req_input(self.shop_choices)
        if action == "b":
            if self.maximum_dragons_list == len(self.dragons_list):
                print("You cannot add more Dragon to your team.")
                return self.shop()
            else:
                return self.shop_dragon()

        return self.shop_choices[action]()

    def shop_dragon(self):
        l_dragon = [generate_dragon() for _ in range(3)]
        show_all_stats(l_dragon)
        txt = ["Which Dragon would you like to buy?",
               "(1), (2) or (3)",
               "(G)o back to shop, (L)ook again"]
        print_list(txt)
        action = req_input(["1", "2", "3", "l", "g"])
        if action in ["1", "2", "3"]:
            self.dragons_list.append(l_dragon[int(action)-1])
            print("Dragon bought!!!")
            return self.shop()
        elif action == "l":
            return self.shop_dragon()
        else:
            return self.shop()

    def shop_upgrade(self):
        txt = ["Which upgrade would you like to buy?",
               "You got " + str(self.victory_token) + " Victory Token (VT).",
               "(1) Augment the maximum number of Dragon : 1VT",
               "",
               "(G)o back to shop"]
        print_list(txt)
        action = req_input(["1", "g"])
        if action == "1":
            if self.victory_token >= 1:
                self.victory_token -= 1
                self.maximum_dragons_list += 1
                print("Maximum sized augmented")
            else:
                print("You don't have enough victory token.")
            return self.shop()
        else:
            return self.shop()

    def breed(self):
        print("", "Which Dragon do you want to breed?")
        self.show_owned_dragon()
        txt = ["Expected '1 3' for (1) and (3)",
               "(G)o back to town"]
        print_list(txt)

        action = input()
        if action == "g":
            return self.main_town()
        else:
            if self.maximum_dragons_list == len(self.dragons_list):
                print("You cannot add more Dragon to your team.")
                return self.main_town()
            try:
                d_a, d_b = action.split(" ")
                new_type = self.type_matrix[self.dragons_list[int(d_a)-1].elem_type][self.dragons_list[int(d_b)-1].elem_type]
                # new_type = self.dragons_list[int(d_b)-1].elem_type
                new_d = dragon(generate_dragon_values(elem_type=new_type))
                print(new_d.name + " is born")
                show_all_stats([new_d])
                self.dragons_list.append(new_d)
                return self.main_town()
            except ValueError:
                print("Invalid Input")
                return self.main_town()

        return self.main_town()


if __name__ == "__main__":
    game_world().main_town()
