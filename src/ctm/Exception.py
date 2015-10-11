# coding: utf-8


class OutOfSessionDurationError(ValueError):
    """单个talk时间大于最大session时间错误"""
    pass


class TotalDurationNotEnough(ValueError):
    """talk时间之和不足最小时间要求错误"""
    pass