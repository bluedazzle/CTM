# coding: utf-8
from __future__ import unicode_literals
import datetime
from Session import NoonSession, LastSession

class BaseTrack(object):
    """
    Track 基本类，定义了track的通用属性及方法

    属性：
    morning_session:        早session
    noon_session:           午session(read only)
    afternoon_session:      下午session
    last_session:           最后的session(read only)


    方法：
    revise_last_event_time()    根据afternoon session 的结束时间重新定义last session的开始时间
    parameter:
    """
    def __init__(self):
        super(BaseTrack, self).__init__()
        self._morning_session = None
        self._noon_session = None
        self._afternoon_session = None
        self._last_session = None

    @property
    def morning_session(self):
        return self._morning_session

    @morning_session.setter
    def morning_session(self, session):
        self._morning_session = session

    @property
    def afternoon_session(self):
        return self._afternoon_session

    @afternoon_session.setter
    def afternoon_session(self, session):
        self._afternoon_session = session


class Track(BaseTrack):
    """track类,用于表示本问题的track"""
    def __init__(self):
        super(Track, self).__init__()
        self._noon_session = NoonSession()
        self._last_session = LastSession()

    @property
    def noon_session(self):
        return self._noon_session

    @property
    def last_session(self):
        return self._last_session

    def revise_last_event_time(self):
        total_duration = datetime.timedelta(minutes=0)
        for itm in self.afternoon_session.talk_list:
            total_duration += itm.duration
        last_start_time = self.afternoon_session.start_time + total_duration
        self.last_session.start_time = last_start_time