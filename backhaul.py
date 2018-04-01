import click
from backhaul.util.conf import config
from backhaul.ui import ViewPort
import pyglet

@click.group()
def backhaul():
	pass


@backhaul.command()
def start():
	resolution = [int(x) for x in config.graphics.resolution.split('x')]
	vp = ViewPort(size = resolution, fullscreen = config.graphics.fullscreen)

	pyglet.clock.schedule_interval(vp.update, 1/60.0)

	pyglet.app.run()
	
if __name__ == '__main__':
	backhaul()