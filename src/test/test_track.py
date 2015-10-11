# coding: utf-8
from __future__ import unicode_literals

from unittest import TestCase
from ..ctm.Talk import Talk
from ..ctm.Session import AfternoonSession
from ..ctm.Track import Track

import datetime


class TestTrack(TestCase):
    def setUp(self):
        test_talk_list = []
        for i in range(1, 4):
            talk = Talk('test{0}'.format(i), '{0}min'.format(i*10))
            test_talk_list.append(talk)
        self.talk_list = test_talk_list
        self.afternoon_session = AfternoonSession()
        self.afternoon_session.talk_list = self.talk_list
        self.track = Track()
        self.track.afternoon_session = self.afternoon_session

    def test_revise_last_event_time(self):
        self.track.revise_last_event_time()
        self.assertEqual(self.track.last_session.start_time,
                         datetime.datetime(1900, 1, 1, 14, 0))