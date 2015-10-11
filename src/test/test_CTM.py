# coding: utf-8
from __future__ import unicode_literals

from unittest import TestCase
from ..ctm.main import CTM
from ..ctm.Talk import Talk
from ..ctm.Exception import OutOfSessionDurationError, TotalDurationNotEnough


class TestCTM(TestCase):
    def setUp(self):
        self.ctm = CTM(10, 50, 60)
        self.read_ctm = CTM(10, 50, 10)
        test_talk_list = []
        for i in range(1, 4):
            talk = Talk('test{0}'.format(i), '{0}min'.format(i*10))
            talk_dict = {'use': False, 'talk': talk}
            test_talk_list.append(talk_dict)
        self.ctm.talk_list = test_talk_list
        self.talk_list = test_talk_list

    def test_check_talk(self):
        res = self.ctm._check_talk(self.talk_list)
        self.assertEqual(res, True)
        self.ctm.afternoon_duration = 0
        self.ctm.extra_duration = 1
        self.assertRaises(OutOfSessionDurationError, self.ctm._check_talk, self.talk_list)
        self.ctm.afternoon_duration = 1000
        self.assertRaises(TotalDurationNotEnough, self.ctm._check_talk, self.talk_list)
        self.ctm.morning_duration = 5
        self.ctm.afternoon_duration = 50
        self.assertRaises(TotalDurationNotEnough, self.ctm._check_talk, self.talk_list)
        self.ctm.afternoon_duration = 30
        self.ctm.morning_duration = 10

    def test_read_sample_input(self):
        self.read_ctm.read_sample_input('test/test_data.txt')
        self.assertEqual(self.read_ctm.talk_list[0]['talk'].title, 'test')

    def test_sort_talk_by_duration(self):
        self.ctm.talk_list = self.ctm._sort_talk_by_duration()
        self.assertEqual(self.ctm.talk_list[0]['talk'].duration_value(), 30)

    def test_create_track(self):
        self.ctm.create_track()
        self.assertEqual(len(self.ctm.track_list), 1)
        self.assertEqual(self.ctm.track_list[0].morning_session.talk_list[0].title, 'test1')

    def test_check_last_track(self):
        self.ctm.create_track()
        res = self.ctm._check_last_track(self.ctm.track_list)
        self.assertEqual(res, True)
