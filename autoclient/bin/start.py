import os,sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

os.environ['USER_SETTINGS'] = "config.settings"
from src import script

if __name__ == "__main__":
    script.run()
