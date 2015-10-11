# coding: utf-8
from __future__ import unicode_literals

from unittest import TestCase
from ..ctm.Session import BaseSession, MorningSession, AfternoonSession
from ..ctm.Exception import OutOfSessionDurationError
from ..ctm.Talk import Talk
from ..ctm.setting import AFTERNOON_DURATION, EXTRA_DURATION

import datetime


class TestBaseSession(TestCase):
    def setUp(self):
        test_talk_list = []
        for i in range(1, 4):
            talk = Talk('test{0}'.format(i), '{0}min'.format(i*10), '0{0}:00PM')
            test_talk_list.append(talk)
        self.talk_list = test_talk_list
        self.base_session = BaseSession()

    def test_check_duration(self):
        res = self.base_session.check_duration(datetime.timedelta(minutes=1))
        self.assertEqual(res, False)
        res = self.base_session.check_duration(datetime.timedelta(minutes=0))
        self.assertEqual(res, True)

    def test_check_talk_list(self):
        res = self.base_session._check_talk_list(self.talk_list)
        self.assertEqual(res, False)
        res = self.base_session._check_talk_list([])
        self.assertEqual(res, True)

    def test_format_datetime(self):
        self.assertEqual('05:00PM', self.base_session.format_datetime(datetime.datetime(1900, 1, 1, 17, 0)))


class TestMorningSession(TestCase):
    def setUp(self):
        test_talk_list = []
        for i in range(1, 4):
            talk = Talk('test{0}'.format(i), '{0}min'.format(i*10), '0{0}:00PM')
            test_talk_list.append(talk)
        self.talk_list = test_talk_list
        self.session = MorningSession()
        self.session.talk_list = self.talk_list

    def test_sort_talk_list(self):
        self.session._sort_talk_list()
        self.assertEqual(self.session.talk_list[1].start_at, '09:10AM')

    def test_get_talk_list_duration(self):
        self.assertEqual(self.session.get_talk_list_duration(), 60)


class TestAfternoonSession(TestCase):
    def setUp(self):
        self.session = AfternoonSession()

    def test_check_duration(self):
        res = self.session.check_duration(datetime.timedelta(minutes=AFTERNOON_DURATION+EXTRA_DURATION))
        self.assertEqual(res, True)
        res = self.session.check_duration(datetime.timedelta(minutes=AFTERNOON_DURATION+EXTRA_DURATION+1))
        self.assertEqual(res, False)

