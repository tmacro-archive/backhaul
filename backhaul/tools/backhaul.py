from ..util.arg import option, flag
from ..entry import entrypoint

@flag('-v', '--verbose', dest='logging.loglvl')
def verbose(*args, **kwargs):
	return 'debug'

def main():
	entrypoint()
