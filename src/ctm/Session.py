# coding: utf-8
from __future__ import unicode_literals

from abc import ABCMeta
from Exception import OutOfSessionDurationError
from Talk import Talk
import datetime
import setting


class ExtraDurationMixin(object):
    """额外时间mixin"""
    __metaclass__ = ABCMeta

    extra = datetime.timedelta(minutes=setting.EXTRA_DURATION)

    def check_duration(self, total_duration):
        session_duration = self.extra + self.duration
        if total_duration > session_duration:
            return False
        else:
            return True


class BaseSession(object):
    """
    Session基本类，定义了session的通用属性及方法，用于储存session

    属性：

    start_time:     session起始时间
    name:           session名称(read only)
    duration:       session时长(read only)
    talk_list:      session内的talks


    方法：
    get_talk_list_duration()            获取session包含的talk总时长
    parameter:

    display_talk_list()                 输出session包含的talk
    parameter:

    check_duration(total_duration)      检查total_duration是否小于session duration
    parameter:
        total_duration (integer|Required) -总时长


    """
    def __init__(self):
        super(BaseSession, self).__init__()
        self._name = 'base'
        self._duration = datetime.timedelta(minutes=0)
        self._start_time = datetime.datetime(year=1900, month=1, day=1, hour=0)
        self._talk_list = []

    @property
    def start_time(self):
        return self._start_time

    @start_time.setter
    def start_time(self, value):
        self._start_time = value

    @property
    def name(self):
        return self._name

    @property
    def duration(self):
        return self._duration

    @property
    def talk_list(self):
        return self._talk_list

    @talk_list.setter
    def talk_list(self, talk_list):
        if self._check_talk_list(talk_list):
            self._talk_list = talk_list
        else:
            raise OutOfSessionDurationError('Total durations beyond session duration!')

    def _check_talk_list(self, talk_list):
        """检查talk_list是否符合session限制"""
        total_duration = datetime.timedelta(minutes=0)
        for talk in talk_list:
            total_duration += talk.duration
        return self.check_duration(total_duration)

    def check_duration(self, total_duration):
        if total_duration > self.duration:
            return False
        else:
            return True

    @staticmethod
    def format_datetime(dt_obj):
        """格式化时间为 xx:xx A|PM 格式"""
        return dt_obj.strftime('%I:%M%p')

    def _sort_talk_list(self):
        """对session的talk_list中的talk以start_at属性进行排序"""
        start = self._start_time
        for talk in self.talk_list:
            talk.start_at = self.format_datetime(start)
            start += talk.duration
        self.talk_list = sorted(self.talk_list, key=lambda x: (x.start_at[5:], x.start_at[0:4]))

    def get_talk_list_duration(self):
        total_duration = 0
        for talk in self.talk_list:
            total_duration += talk.duration_value()
        return total_duration

    def display_talk_list(self):
        self._sort_talk_list()
        for talk in self.talk_list:
            display = '{start_at} {title} {duration}min' if talk.duration_display() != 'lightning' \
                else '{start_at} {title} {duration}'
            print display.format(start_at=talk.start_at,
                                 title=talk.title,
                                 duration=talk.duration_display())


class MorningSession(BaseSession):
    """
    早session类
    """
    def __init__(self):
        super(MorningSession, self).__init__()
        self._name = 'Morning Session'
        self._start_time = datetime.datetime(year=1900, month=1, day=1, hour=9)
        self._duration = datetime.timedelta(minutes=setting.MORNING_DURATION)


class AfternoonSession(ExtraDurationMixin, BaseSession):
    """
    下午session类
    """
    def __init__(self):
        super(AfternoonSession, self).__init__()
        self._name = 'Afternoon Session'
        self._start_time = datetime.datetime(year=1900, month=1, day=1, hour=13)
        self._duration = datetime.timedelta(minutes=setting.AFTERNOON_DURATION)


class NoonSession(BaseSession):
    """
    中午session类
    """
    def __init__(self):
        super(NoonSession, self).__init__()
        self._name = 'Noon Session'
        self._start_time = datetime.datetime(year=1900, month=1, day=1, hour=12)
        self._duration = datetime.timedelta(hours=1)
        self._talk_list = [Talk('Lunch', '60min', '12:00PM')]

    def display_talk_list(self):
        self._sort_talk_list()
        print '{start_at} {title}'.format(start_at=self.talk_list[0].start_at,
                                          title=self.talk_list[0].title)


class LastSession(BaseSession):
    """
    networking event session 类
    """
    def __init__(self):
        super(LastSession, self).__init__()
        self._name = 'Last Session'
        self._start_time = datetime.datetime(year=1900, month=1, day=1, hour=17)
        self._duration = datetime.timedelta(minutes=0)
        self._talk_list = [Talk('Networking Event', '0min', '05:00PM')]

    def display_talk_list(self):
        self._sort_talk_list()
        print '{start_at} {title}'.format(start_at=self.talk_list[0].start_at,
                                          title=self.talk_list[0].title)

