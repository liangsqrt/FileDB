import sys,os


base_dir = os.path.dirname(__file__)
sys.path.append(base_dir)

HOST = "0.0.0.0"
PORT = "9999"

config_path = os.path.join(base_dir, "config.json")
