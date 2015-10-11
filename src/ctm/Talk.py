# coding:utf-8
from __future__ import unicode_literals

import datetime
import re


class Talk(object):
    """
    储存单个talk的talk类，本问题的最基本数据

    属性：

    title:          talk标题
    duration:       talk时长
    start_at:       talk开始时间


    方法：

    duration_value()        输出talk duration数值
    parameter:

    duration_display()      输出talk duration数据
    parameter:

    """
    def __init__(self, title='', duration=0, start_at=''):
        self._title = title
        self._duration = self._time_convert(duration)
        self._start_at = start_at
        super(Talk, self).__init__()

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, title):
        self._check_number(title)
        self._title = title

    @property
    def duration(self):
        return self._duration

    @duration.setter
    def duration(self, duration):
        self._duration = self._time_convert(duration)

    @property
    def start_at(self):
        return self._start_at

    @start_at.setter
    def start_at(self, value):
        self._start_at = value

    @staticmethod
    def _check_number(value):
        """检测title中是否包含数字"""
        result = re.findall(r'(\d+)', value)
        if result:
            raise ValueError('talk title can not contain number')
        else:
            return True

    @staticmethod
    def _time_convert(duration):
        """转换duration格式"""
        duration = unicode(duration).lower()
        if duration == 'lightning':
            return datetime.timedelta(minutes=5)
        else:
            try:
                duration = duration.split('min')[0]
                duration = int(duration)
                return datetime.timedelta(minutes=duration)
            except ValueError, e:
                print 'invalid input time str, duration will be set as 0'
                return datetime.timedelta(minutes=0)

    def duration_value(self):
        total_minutes = int(self.duration.total_seconds() / 60)
        return total_minutes

    def duration_display(self):
        return self.duration_value() if self.duration_value() != 5 else 'lightning'