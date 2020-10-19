#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔╦╗╦═╗╔═╗╔═╗╔═╗╔╗╔  ╔═╗╔═╗  ╔╦╗╔═╗╔═╗╔╦╗
 ║║╠╦╝╠═╣║ ╦║ ║║║║  ║ ║╠╣    ║║║ ║║ ║║║║
═╩╝╩╚═╩ ╩╚═╝╚═╝╝╚╝  ╚═╝╩    ═╩╝╚═╝╚═╝╩ ╩
"""

import os

if __name__ == "__main__":
    # Rustine de l'enfer
    os.chdir(os.getcwd() + "/scripts")
    exec(open("dod.py").read())
