from ecouchbase.bucket import Bucket
from couchbase.connstr import convert_1x_args

class EConnection(Bucket):
    def __init__(self, bucket, **kwargs):
        kwargs = convert_1x_args(bucket, **kwargs)
        super(EConnection, self).__init__(**kwargs)
