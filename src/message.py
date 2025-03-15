"""
多线程的 message
"""
from enum import Enum


class WorkStateEnum(Enum):
    SUCCESS = "成功"
    FAIL = "失败"


class ExportMessage:
    def __init__(self, state: WorkStateEnum, message: any):
        self.state = state
        self.message = message