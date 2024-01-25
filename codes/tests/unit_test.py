import json
from config.settings import Config
import os

config = Config("dev")


#

#print(config.get_file("config", "morning_routine_v2.xlsx"))
print(os.path.join(config.paths.misc_dir, 'font_patterns.json'))
