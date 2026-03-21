class Anime:
    def __init__ (self,anime_id,anime_name):
        self.anime_id = anime_id
        self.anime_name = anime_name

    def __repr__(self):
        return f"Anime: {self.anime_name}"
    
class Character:
    def __init__ (self,name,famous_dialog, gif):
        self.name = name
        self.famous_dialog = famous_dialog
        self.gif = gif

# main.py
import argparse, sys

def build_parse():
    parser = argparse.ArgumentParser(description="Anime Explorer")
    parser.add_argument("--anime", type=str, help ='Anime title to explore')
    parser.add_argument('--feature', choices=['quize','gif','audio','dialog'],default='dialog')
    parser.add_argument('--list-anime',action='store_true')
    parser.add_argument('--download',choices=['gif','audio'])
    return parser

import random

class Quiz:
    def __init__(self, anime_title,question_bank):
        self.anime_title = anime_title
        self.question_bank = 