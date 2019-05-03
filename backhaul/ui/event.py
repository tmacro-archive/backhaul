from pyglet.event import EventDispatcher as EventDispatcher
from functools import partial
from ..util.log import Log
from collections import defaultdict


_log = Log('ui.event')


def interact(**kwargs):
    import code
    code.InteractiveConsole(locals=kwargs).interact()

# Simple method rename and auto-adding self to handler args
class EventEmitter():
    def __init__(self):
        self.__emitter = None
        self.__handlers = defaultdict(list)
        
    @property
    def _emitter(self):
        if self.__emitter is None:
            class _Emitter(EventDispatcher):
                pass
            for htype in self.__handlers.keys():
                _Emitter.register_event_type(htype)
            self.__emitter = _Emitter()
            for event, handlers in self.__handlers.items():
                for handler in handlers:
                    self.__emitter.push_handlers(**{event: handler})
        return self.__emitter

    def register(self, **kwargs):
        for event, handler in kwargs.items():
            if event not in self.__handlers and self.__emitter is not None:
                raise Exception('Cannot add event types after first emission!') 
            _log.debug('Registering handler %s for event %s'%(event, handler))
            self.__handlers[event].append(handler)

    def emit(self, event, *args):
        _log.debug('Emitting Event %s'%event)
        return self._emitter.dispatch_event(event, self, *args)        

    def _lazy_emit(self, event, *args):
        _log.debug('Emitting lazy event %s'%event)
        return self.emit(event, *args)

    def lazy_emit(self, event, *args):
        _log.debug('Creating lazy event %s'%event)
        return partial(self._lazy_emit, event, *args)