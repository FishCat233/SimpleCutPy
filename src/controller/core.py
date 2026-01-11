from typing import TYPE_CHECKING

from export.model import ExportTask, VideoFile

if TYPE_CHECKING:
    from SimpleCutMainFrame import SimpleCutPyMainFrame


class CoreController:
    """核心控制器"""

    def __init__(self, view: "SimpleCutPyMainFrame"):
        self.view = view
        self.first_select_index: int = 0
        self.task = ExportTask()

    def add_files(self, filenames: list[str], path: str):
        """添加文件

        Args:
            filenames (list[str]): 文件名列表
            path (str): 文件路径
        """
        for filename in filenames:
            self.task.video_sequence.append_video(
                VideoFile(
                    no=len(self.task.video_sequence.video_files) + 1,
                    file_name=filename,
                    file_path=path,
                    start_time="开始",
                    end_time="结束",
                )
            )
