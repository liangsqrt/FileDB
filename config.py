import sys,os


BASE_DIR = os.path.dirname(__file__)
sys.path.append(BASE_DIR)

HOST = "0.0.0.0"
PORT = "9999"

CONFIG_PATH = os.path.join(BASE_DIR, "config.json")
