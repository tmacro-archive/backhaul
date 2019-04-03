
class BackhaulError(Exception):
	'''Root exception for all macrup errors'''
	pass

class UnknownError(BackhaulError):
	'''You done fucked up. something happened, probably in a catch all'''
	pass

class ConfigError(BackhaulError):
	'''Error regarding configuration'''
	pass

class InvalidConfigError(ConfigError):
	'''Error parsing a users configuration'''
	pass

class NoConfigError(ConfigError):
	'''Error locating a users config'''
	pass

class ConfigImportError(ConfigError):
	'''Error locating a child config file'''


class ObjectError(BackhaulError):
	'''Base exception for all object related errors'''

class ObjectConstructionError(ObjectError):
	'''Base exception for all launch time object construction errors'''

class DuplicatePropertyError(ObjectConstructionError):
	'''A property key has been registered more than once, or a esisting key is being overwritten'''

class PropertyOverwriteError(ObjectError):
	'''A property is being overwrttien without an explicit overwrite = True'''

class InvalidPositionError(ObjectError):
	pass
