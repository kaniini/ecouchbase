import eventlet
from eventlet import greenthread as GT
from eventlet.hub import get_hub

from couchbase.async.bucket import AsyncBucket
from ecouchbase.iops import IOPS

class Bucket(AsyncBucket):
    def __init__(self, *args, **kwargs):
        """
        This class is an eventlet-optimized subclass of libcouchbase
        which utilizes the underlying IOPS structures and the eventlet
        event primitives to efficiently utilize couroutine switching.
        """
        super(Bucket, self).__init__(IOPS(), *args, **kwargs)

    def _waitwrap(self, cbasync):
        cur_thread = GT.getcurrent()
        cbasync.callback = cur_thread.switch
        cbasync.errback = lambda r, x, y, z: cur_thread.throw(x, y, z)
        return get_hub().switch()

    def _meth_factory(meth, name):
        def ret(self, *args, **kwargs):
            return self._waitwrap(meth(self, *args, **kwargs))
        return ret

    locals().update(AsyncBucket._gen_memd_wrappers(_meth_factory))
