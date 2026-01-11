"""导出模型"""

import os
import re
import time
from typing import Literal
from pydantic import BaseModel, field_validator


class VideoFile(BaseModel):
    """视频文件"""

    no: int
    file_name: str
    file_path: str
    start_time: str = "开始"
    end_time: str = "结束"

    def get_full_file_path(self) -> str:
        """获取视频文件完整路径

        Returns:
            str: 视频文件完整路径
        """
        return os.path.join(self.file_path, self.file_name)

    def set_full_file_path(self, full_file_path: str) -> None:
        """设置视频文件完整路径

        Args:
            full_file_path (str): 视频文件完整路径
        """
        self.file_path, self.file_name = os.path.split(full_file_path)

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
            v (str): 时间字符串，要求只能由数字和冒号组成，或为特殊值"开始"/"结束"

        Returns:
            str: 验证通过的时间字符串
        """

        # 去除两端空格
        v = v.strip()

        # 全角替换为半角
        v = v.replace("：", ":")

        # 空格替换冒号
        v = v.replace(" ", ":")

        # 检查是否为特殊值或有效时间格式
        if v != "开始" and v != "结束" and not re.match(r"^[0123456789:]*$", v):
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

    def modify(self, no: int, video: VideoFile):
        self.video_files[no] = video

    def remove(self, no: int):
        # 移除
        self.video_files.pop(no)

        # 排序
        self.video_files.sort(key=lambda x: x.no)

        # 重新编号
        for i, v in enumerate(self.video_files):
            v.no = i + 1

    def insert(self, video: VideoFile, no: int):
        self.video_files.insert(no, video)

    def append(self, video: VideoFile):
        self.video_files.append(video)

    def swap(self, no1: int, no2: int):
        self.video_files[no1], self.video_files[no2] = (
            self.video_files[no2],
            self.video_files[no1],
        )

    def clear(self):
        self.video_files = []


type MultiTrackMode = Literal["first", "amix", "export_both"]
type SizeControlMode = X264Config | MbpsConfig | None


class X264Config(BaseModel):
    pass


class MbpsConfig(BaseModel):
    """Mbps 配置"""

    mbps: float = 6


class ExportConfig(BaseModel):
    """导出配置"""

    multi_track_mode: MultiTrackMode = "first"
    size_control: SizeControlMode = MbpsConfig()


class ExportTask(BaseModel):
    """导出任务"""

    video_sequence: VideoSequence = VideoSequence()
    export_file_name: str = ""
    export_file_path: str = ""
    export_config: ExportConfig = ExportConfig()

    def get_export_full_path(self) -> str:
        """获取导出文件完整路径

        Returns:
            str: 导出文件完整路径
        """
        # 如果 path 为空则使用第一个视频文件的路径
        export_file_path = (
            self.export_file_path
            if self.export_file_path != ""
            else self.video_sequence[0].file_path
        )
        export_file_name = self.export_file_name
        if export_file_name == "":
            export_file_name = time.strftime("No Title %Y.%m.%d - %H.%M.output.mp4")

        # 自动补全后缀扩展
        if "." not in export_file_name:
            export_file_name += ".mp4"

        return os.path.join(export_file_path, export_file_name)
