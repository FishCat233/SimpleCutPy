import os
import sys
from typing import Optional


class PathHelper:
    """路径助手"""

    ffmpeg_path: Optional[str] = None

    @staticmethod
    def get_ffmpeg_path() -> str:
        """
        获取ffmpeg可执行文件的路径

        Returns:
            str: ffmpeg可执行文件的完整路径
        """
        if PathHelper.ffmpeg_path:
            return PathHelper.ffmpeg_path

        if getattr(sys, "frozen", False):
            # 打包后环境
            base_path = sys._MEIPASS  # type: ignore
        else:
            # 开发环境
            base_path = os.path.dirname(
                os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            )

        return os.path.join(base_path, "assets", "ffmpeg.exe")
