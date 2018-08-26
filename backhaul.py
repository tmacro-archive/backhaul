import click
from backhaul.util.conf import config
from backhaul.entry import entrypoint

@click.group()
def backhaul():
	pass


@backhaul.command()
def start():
	entrypoint()
	
if __name__ == '__main__':
	backhaul()