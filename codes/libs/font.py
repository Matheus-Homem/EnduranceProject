import json
import os

def load_font(font_type):
	# Get the path to the parent directory of the current file
	parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
	
	# Create a variable with the relative path to the font patterns file
	FONT_PATTERNS_FILE = os.path.join(parent_dir, "files", "misc", "font_patterns.json")
	
	# Read font patterns from the JSON file
	with open(FONT_PATTERNS_FILE, 'r') as f:
		font_patterns = json.load(f)
	
	# Extract font and font size based on the provided font_type
	font = font_patterns[font_type]["font"]
	font_size = font_patterns[font_type]["font_size"]
	
	# Return the selected font and font size
	return font, font_size

def translate_weekday(english_weekday):
	# Get the path to the parent directory of the current file
	parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
	
	# Create a variable with the relative path to the font patterns file
	WEEKDAY_NAME_FILE = os.path.join(parent_dir, "files", "misc", "ptbr_weekday_name.json")
	
	# Read font patterns from the JSON file
	with open(WEEKDAY_NAME_FILE, 'r') as f:
		translate_ptbr = json.load(f)

	# Return the translated version of the weekday to PT-BR
	return translate_ptbr[english_weekday]