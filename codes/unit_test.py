import json
from config.settings import Config
import os

config = Config("dev")

#font_patterns_path = os.path.join(config.paths.misc_dir, 'font_patterns.json')
#with open(font_patterns_path, 'r') as f:
#	font_patterns = json.load(f)
#
#
##print(font_patterns["TITLE"])
#
#font_type = input("Digite o tipo: ")
#
#font = font_patterns[font_type]["font"]
#font_size = font_patterns[font_type]["font_size"]
#
#def fontType(self, canvas, font_patterns, font_type):
#	font = font_patterns[font_type]["font"]
#	font_size = font_patterns[font_type]["font_size"]
#	print(font, font_size)
#	canvas.setFont("Times-Bold", 24)
#

print(config.get_file("config", "morning_routine_v2.xlsx"))
