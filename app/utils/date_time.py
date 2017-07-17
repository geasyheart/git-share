import datetime
import pytz


class DateTimeMixin(object):
    @classmethod
    def utcnow(cls):
        return datetime.datetime.utcnow()

    @classmethod
    def now(cls):
        return datetime.datetime.now(tz=pytz.timezone("Asia/Shanghai"))

    @classmethod
    def today(cls):
        _utcnow = cls.utcnow()
        return _utcnow.year * 10000 + _utcnow.month * 100 + _utcnow.day

    @classmethod
    def from_timestamp(cls, timestamp):
        return datetime.datetime.fromtimestamp(timestamp, tz=pytz.timezone("Asia/Shanghai"))
