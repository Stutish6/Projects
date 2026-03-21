
import argparse

parser = argparse.ArgumentParser(description="Anime Explorer")
parser.add_argument("--anime", type=str, help ='Anime title to explore')
parser.add_argument('--feature', choices=['quize','gif','audio','dialog'],default='dialog')
parser.add_argument('--list-anime',action='store_true')
parser.add_argument('--download',choices=['gif','audio'])