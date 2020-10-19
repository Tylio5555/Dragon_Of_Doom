#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔╦╗╦═╗╔═╗╔═╗╔═╗╔╗╔  ╔═╗╔═╗  ╔╦╗╔═╗╔═╗╔╦╗
 ║║╠╦╝╠═╣║ ╦║ ║║║║  ║ ║╠╣    ║║║ ║║ ║║║║
═╩╝╩╚═╩ ╩╚═╝╚═╝╝╚╝  ╚═╝╩    ═╩╝╚═╝╚═╝╩ ╩
"""

import scripts.dod as dod
import os

if __name__ == "__main__":
    # Rustine de l'enfer
    os.chdir(os.getcwd() + "/scripts")
    # game_world() crée l'instance du jeu.
    dod.game_world().main_town()
