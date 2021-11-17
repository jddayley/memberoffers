from datetime import time
import datetime
import decimal
import time


class MyJSONEncoder(flask.json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, datetime): return str(obj)
        if isinstance(obj, time.struct_time): return datetime.fromtimestamp(time.mktime(o))
        if isinstance(obj, decimal.Decimal): return str(obj)
        return super(MyJSONEncoder, self).default(obj)
