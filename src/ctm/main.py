# coding: utf-8
from __future__ import unicode_literals

from Session import MorningSession, AfternoonSession
from Talk import Talk
from Track import Track
from Exception import OutOfSessionDurationError, TotalDurationNotEnough

import setting
import os
import copy
import codecs
import sys
import argparse


class CTM(object):
    """
    Conference Track Management 处理类，封装了整个问题的操作方法与核心算法

    属性：

    input_path:             输入文本路径
    use_num:                已匹配talk数量(read only)
    talk_list:              文本读取到的所有talk
    track_list:             所有tracks(read only)
    morning_duration:       早上可分配总时间
    afternoon_duration:     下午可分配时间
    extra_duration:         下午额外可分配时间


    方法:

    read_sample_input(file_path)    读取talk数据文件
    parameter:
        file_path(string|Optional) -文件路径，默认为SampleInput.txt

    create_track()                  根据读入talk生成track list
    parameter:

    output_track_arrangement()      输出安排好的tracks
    parameter:

    """
    MORNING = 1
    AFTERNOON = 2

    def __init__(self, morning_duration=0, afternoon_duration=0, extra_duration=0):
        super(CTM, self).__init__()
        self._input_path = '{0}/SampleInput.txt'.format(os.path.dirname(os.path.dirname(sys.path[0])))
        self._use_num = 0
        self._talk_list = None
        self._track_list = None
        self._morning_duration = morning_duration
        self._afternoon_duration = afternoon_duration
        self._extra_duration = extra_duration

    @property
    def input_path(self):
        return self._input_path

    @input_path.setter
    def input_path(self, value):
        self._input_path = value

    @property
    def morning_duration(self):
        return self._morning_duration

    @morning_duration.setter
    def morning_duration(self, value):
        self._morning_duration = value

    @property
    def afternoon_duration(self):
        return self._afternoon_duration

    @afternoon_duration.setter
    def afternoon_duration(self, value):
        self._afternoon_duration = value

    @property
    def extra_duration(self):
        return self._extra_duration

    @extra_duration.setter
    def extra_duration(self, value):
        self._extra_duration = value

    @property
    def talk_list(self):
        return self._talk_list

    @talk_list.setter
    def talk_list(self, value):
        self._talk_list = value

    @property
    def use_num(self):
        return self._use_num

    @property
    def track_list(self):
        return self._track_list

    def _check_talk(self, talk_list):
        """检查talk_list是否能生成track，否则根据原因抛出异常"""
        total_duration = 0
        for talk in talk_list:
            talk = talk['talk']
            total_duration += talk.duration_value()
            if talk.duration_value() > self._morning_duration and talk.duration_value() > \
                    (self._afternoon_duration + self._extra_duration):
                raise OutOfSessionDurationError('''\nSingle talk duration larger than session duration.
                Please change session duration or change your sample input data!''')
        if total_duration < self._afternoon_duration:
            raise TotalDurationNotEnough('''\n Total talk durations must larger than afternoon session duration!
            Please add your sample input or change single talk duration.''')
        mod = total_duration % self._afternoon_duration
        track_num = total_duration / self._afternoon_duration
        if track_num * self._morning_duration < mod:
            raise TotalDurationNotEnough('''\n Total talk durations can not distribute in each tracks impartial''')
        return True

    def _check_last_track(self, track_list):
        """检测极端情况下最后一个track的afternoon_session是否符合条件，否则重写分配talk使其符合条件"""
        last_track = track_list[-1]
        if last_track.afternoon_session.get_talk_list_duration() >= self._afternoon_duration:
            return True
        first_track = track_list[0]
        last_track.afternoon_session.talk_list, first_track.morning_session.talk_list = \
            first_track.morning_session.talk_list, last_track.afternoon_session.talk_list
        for track in track_list:
            for talk in track.morning_session.talk_list:
                last_track.afternoon_session.talk_list.append(talk)
                total_duration = last_track.afternoon_session.get_talk_list_duration()
                if self._afternoon_duration <= total_duration <= (self._afternoon_duration + self._extra_duration):
                    track.morning_session.talk_list.remove(talk)
                    return True
                elif total_duration > (self._afternoon_duration + self._extra_duration):
                    last_track.afternoon_session.talk_list.remove(talk)
                else:
                    track.morning_session.talk_list.remove(talk)

    def read_sample_input(self, file_path=None):
        file_path = file_path if file_path else self.input_path
        talk_list = []
        with codecs.open(file_path, 'r', encoding='utf-8') as f1:
            content = f1.readlines()
            for line in content:
                line = line.strip('\n')
                line_array = line.split(' ')
                duration = line_array[-1]
                title = ' '.join(line_array[0:-1])
                talk = Talk(title, duration)
                talk_dict = {'talk': talk, 'use': False}
                talk_list.append(talk_dict)
        self._check_talk(talk_list)
        self._talk_list = talk_list
        self._talk_list = self._sort_talk_by_duration()


    def _sort_talk_by_duration(self):
        """对读入的talk按duration排序"""
        return sorted(self._talk_list, key=lambda x: x['talk'].duration, reverse=True)

    def _match_session(self, session_type=MORNING):
        """生成track的核心算法"""
        m_duration = 0
        m_talk_list = []
        duration_dict = {self.MORNING: self._morning_duration,
                         self.AFTERNOON: self._afternoon_duration + self._extra_duration}
        duration = duration_dict.get(session_type, self.MORNING)
        for talk in self._talk_list:
            if talk['use']:
                continue
            m_duration += talk['talk'].duration_value()
            if m_duration > duration:
                m_duration -= talk['talk'].duration_value()
                break
            elif m_duration == duration:
                m_talk_list.append(talk['talk'])
                talk['use'] = True
                self._use_num += 1
                return m_talk_list
            m_talk_list.append(talk['talk'])
            talk['use'] = True
            self._use_num += 1
        self._talk_list.reverse()
        for talk in self._talk_list:
            if talk['use']:
                continue
            m_duration += talk['talk'].duration_value()
            if m_duration > duration:
                return m_talk_list
            elif m_duration == duration:
                m_talk_list.append(talk['talk'])
                talk['use'] = True
                self._use_num += 1
                return m_talk_list
            m_talk_list.append(talk['talk'])
            talk['use'] = True
            self._use_num += 1
        self._talk_list.reverse()
        return m_talk_list

    def create_track(self):
        track_list = []
        while self.use_num < len(self.talk_list):
            morning_list = self._match_session(self.MORNING)
            afternoon_list = self._match_session(self.AFTERNOON)
            new_morning = MorningSession()
            new_morning.talk_list = copy.deepcopy(morning_list)
            new_afternoon = AfternoonSession()
            new_afternoon.talk_list = copy.deepcopy(afternoon_list)
            new_track = Track()
            new_track.morning_session = new_morning
            new_track.afternoon_session = new_afternoon
            track_list.append(new_track)
        self._check_last_track(track_list)
        self._track_list = track_list

    def output_track_arrangement(self):
        for i, itm in enumerate(self.track_list):
            print '\nTrack{0}'.format(i+1)
            itm.revise_last_event_time()
            itm.morning_session.display_talk_list()
            itm.noon_session.display_talk_list()
            itm.afternoon_session.display_talk_list()
            itm.last_session.display_talk_list()



if __name__ == '__main__':
    p = argparse.ArgumentParser(
        description=' Conference Track Management ')
    p.add_argument('--f', help='sample input file path, default is ..SampleInput.txt', default=None)
    ctm = CTM(setting.MORNING_DURATION, setting.AFTERNOON_DURATION, setting.EXTRA_DURATION)
    ctm.read_sample_input(p.parse_args().f)
    ctm.create_track()
    ctm.output_track_arrangement()