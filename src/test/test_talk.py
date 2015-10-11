from unittest import TestCase
from src.ctm.Talk import Talk

import datetime

class TestTalk(TestCase):
    def setUp(self):
        self.talk = Talk(title='test', duration='10min')

    def test_property(self):
        self.talk.duration = 'lightning'
        self.talk.title = 'change title'
        self.assertEqual(self.talk.duration, datetime.timedelta(minutes=5))
        self.assertEqual(self.talk.title, 'change title')

    def test_time_convert(self):
        test_res = self.talk._time_convert('abc')
        self.assertEqual(datetime.timedelta(minutes=0), test_res)
        test_res = self.talk._time_convert('70min')
        self.assertEqual(datetime.timedelta(minutes=70), test_res)
        test_res = self.talk._time_convert('lightning')
        self.assertEqual(datetime.timedelta(minutes=5), test_res)

    def test_duration_value(self):
        self.assertEqual(self.talk.duration_value(), 10)

    def test_duration_display(self):
        self.assertEqual(self.talk.duration_display(), 10)
        self.talk.duration = 5
        self.assertEqual(self.talk.duration_display(), 'lightning')
