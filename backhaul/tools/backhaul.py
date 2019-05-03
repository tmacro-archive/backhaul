from ..util.arg import option, flag
from ..entry import entrypoint

def register_args():
	@flag('-v', '--verbose', dest='logging.loglvl')
	def verbose(*args, **kwargs):
		return 'debug'

def main():
	register_args()
	from ..util.log import setupLogging
	from ..util.conf import config
	setupLogging(config.meta.name, config.meta.version, **config.logging._asdict())
	entrypoint()
