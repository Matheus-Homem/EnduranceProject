from libs.font import *

def centralized_text(canvas, up_start, text, pattern):
	# Load font and font size based on the provided pattern
	font, font_size = load_font(pattern)

	# Set the font and font size for the canvas
	canvas.setFont(font, font_size)

	# Calculate the width of the text using the selected font and font size
	text_width = canvas.stringWidth(text, font, font_size)

	# Calculate the left starting position to center the text horizontally
	left_start = (595.276 - text_width) / 2

	# Draw the text on the canvas at the calculated position
	canvas.drawString(left_start, up_start, text)