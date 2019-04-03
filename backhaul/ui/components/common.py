import glooey
from ...util.conf import config
import pyglet

class Text(glooey.Label):
	custom_color = config.style.font_color
	custom_font_size = config.style.font_size
	custom_font_name = config.style.font
	custom_alignment = 'center'


# class DialogBackground(glooey.Background):
# 	custom_center = pyglet.resource.texture('box-center.png')
# 	custom_top = pyglet.resource.texture('box-top.png')
# 	custom_bottom = pyglet.resource.texture('box-bottom.png')
# 	custom_left = pyglet.resource.texture('box-left.png')
# 	custom_right = pyglet.resource.texture('box-right.png')
# 	custom_top_left = pyglet.resource.image('box-top-left.png')
# 	custom_top_right = pyglet.resource.image('box-top-right.png')
# 	custom_bottom_left = pyglet.resource.image('box-bottom-left.png')
# 	custom_bottom_right = pyglet.resource.image('box-bottom-right.png')

class BlackBackground(glooey.Background):
	custom_color = '#2e3131'



class Button(glooey.Button):
	class Base(glooey.Background):
		custom_center = pyglet.resource.texture('button-center.png')
		custom_top = pyglet.resource.texture('button-top.png')
		custom_bottom = pyglet.resource.texture('button-bottom.png')
		custom_left = pyglet.resource.texture('button-left.png')
		custom_right = pyglet.resource.texture('button-right.png')
		custom_top_left = pyglet.resource.image('button-top-left.png')
		custom_top_right = pyglet.resource.image('button-top-right.png')
		custom_bottom_left = pyglet.resource.image('button-bottom-left.png')
		custom_bottom_right = pyglet.resource.image('button-bottom-right.png')

	class Label(Text):
		custom_padding = 10
		custom_left_padding = 12 # Why wont this center ?!?!
		custom_size = 0


# class Box(glooey.Frame):
# 	Decoration = DialogBackground

# class Button(glooey.Button):
# 	pass
	# class Label(Text):
	# 	custom_right_padding = 16
	# 	custom_top_padding = 8
	# 	custom_left_padding = 16
	# 	custom_bottom_padding = 8

	# Base=DialogBackground

	# def __init__(self, text, response):
	# 	super().__init__(text)
	# 	self.response = response

	# def on_click(self, widget):
	# 	print(self.response)
	# custom_right_padding = 0
	# custom_top_padding = 0
	# custom_left_padding = 0
	# custom_bottom_padding = 0
	# custom_padding = 0
	# custom_vert_padding = 0
	# custom_aligment = 'center'
# 	class Over(glooey.Background):
# 		custom_color = '#3465a4'

# 	class Down(glooey.Background):
# 		custom_color = '#729fcff'

# 	# Beyond just setting class variables in our widget subclasses, we can
# 	# also implement new functionality.  Here we just print a programmed
# 	# response when the button is clicked.


# class MainBox(glooey.VBox):
# 	# custom_cell_padding = 4
# 	# custom_padding = 4
# 	custom_alignment = 'center'

# # It's also common to style a widget with existing widgets or with new
# # widgets made just for that purpose.  The button widget is a good example.
# # You can give it a Label subclass (like MyLabel from above) to tell it how
# # to style text, and Background subclasses to tell it how to style the
# # different mouse rollover states:

# class MyButton(glooey.Button):
#     Label = MyLabel
#     custom_alignment = 'fill'

#     # More often you'd specify images for the different rollover states, but
#     # we're just using colors here so you won't have to download any files
#     # if you want to run this code.

#     class Base(glooey.Background):
#         custom_color = '#204a87'

#     class Over(glooey.Background):
#         custom_color = '#3465a4'

#     class Down(glooey.Background):
#         custom_color = '#729fcff'

#     # Beyond just setting class variables in our widget subclasses, we can
#     # also implement new functionality.  Here we just print a programmed
#     # response when the button is clicked.

#     def __init__(self, text, response):
#         super().__init__(text)
#         self.response = response

#     def on_click(self, widget):
#         print(self.response)
