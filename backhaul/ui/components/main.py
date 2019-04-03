from .common import Text#, Box
# Define a custom style for text.  We'll inherit the ability to render text
# from the Label widget provided by glooey, and we'll define some class
# variables to customize the text style.
import glooey

class TitleText(Text):
	custom_font_size = 48
	# custom_right_padding = 16
	# custom_top_padding = 20
	custom_left_padding = 12
	custom_bottom_padding = 50



# class TitleFrame(Box):
# 	custom_bottom_padding = 0
# 	custom_top_padding = 0

# If we want another kind of text, for example a bigger font for section
# titles, we just have to derive another class:

# class MyTitle(glooey.Label):
#     custom_color = '#eeeeec'
#     custom_font_size = 12
#     custom_alignment = 'center'
#     custom_bold = True
