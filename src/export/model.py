"""导出模型"""

import re
from typing import Literal
from pydantic import BaseModel, field_validator


class VideoFile(BaseModel):
    """视频文件"""

    no: int
    file_path: str
    start_time: str
    end_time: str

    @field_validator("no")
    def validate_no(cls, v: int) -> int:
        """验证视频文件序号是否合法

        Args:
            v (int): 视频文件序号

        Returns:
            int: 验证通过的视频文件序号
        """
        if v < 0:
            raise ValueError("视频文件序号必须为非负数")
        return v

    @field_validator("start_time", "end_time")
    def validate_time(cls, v: str) -> str:
        """
        验证时间字符串是否合法，并进行格式化

        Args:
            v (str): 时间字符串，要求只能由数字和冒号组成

        Returns:
            str: 验证通过的时间字符串
        """

        # 去除两端空格
        v = v.strip()

        # 全角替换为半角
        v = v.replace("：", ":")

        # 空格替换冒号
        v = v.replace(" ", ":")

        if v == "开始" or v == "结束" or not re.match(r"^[0123456789:]*$", v):
            raise ValueError("时间格式错误")

        return v

    @field_validator("file_path")
    def validate_none_path(cls, v: str) -> str:
        """验证文件路径是否为空

        Args:
            v (str): 文件路径

        Returns:
            str: 验证通过的文件路径
        """
        if v == "":
            raise ValueError("文件路径不能为空")
        return v


class VideoSequence(BaseModel):
    """视频序列"""

    video_files: list[VideoFile] = []

    def __getitem__(self, item):
        return self.video_files[item]

    def __len__(self):
        return len(self.video_files)

    def get_video_list(self) -> list[VideoFile]:
        return self.video_files

    def pop_video(self, no: int):
        self.video_files.pop(no)

    def insert_video(self, video: VideoFile, no: int):
        self.video_files.insert(no, video)

    def append_video(self, video: VideoFile):
        self.video_files.append(video)

    def swap_item(self, no1: int, no2: int):
        self.video_files[no1], self.video_files[no2] = (
            self.video_files[no2],
            self.video_files[no1],
        )

    def clear_all(self):
        self.video_files = []


type MultiTrackMode = Literal["first", "amix", "export_both"]
type SizeControlMode = X264Config | MbpsConfig


class X264Config(BaseModel):
    pass


class MbpsConfig(BaseModel):
    """Mbps 配置"""

    mbps: int = 6


class ExportConfig(BaseModel):
    """导出配置"""

    amix_mode: MultiTrackMode = "first"
    size_control: SizeControlMode = MbpsConfig()


class ExportTask(BaseModel):
    """导出任务"""

    video_sequence: VideoSequence
    export_file_name: str
    export_file_path: str
    export_config: ExportConfig
