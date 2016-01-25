import eventlet
eventlet.monkey_patch(select=True)

from eventlet import greenthread as GT
from time import time

from couchbase.iops.base import (
    IOEvent, TimerEvent,
    PYCBC_EVACTION_WATCH, PYCBC_EVACTION_UNWATCH
)


class EventletTimer(TimerEvent):
    def __init__(self):
        self._evhandle = None

    def ready_proxy(self, *args):
        self.ready(0)

    def schedule(self, usecs):
        seconds = usecs / 1000000.0
        self._evhandle = eventlet.spawn_after(seconds, self.ready_proxy)


class IOPS(SelectIOPS):
    def update_timer(self, event, action, usecs):
        if action == PYCBC_EVACTION_UNWATCH:
            GT.cancel(self._evhandle)
            self._evhandle = None
            return

        elif action == PYCBC_EVACTION_WATCH:
            event.schedule(usecs)

    def timer_event_factory(self):
        return EventletTimer()
