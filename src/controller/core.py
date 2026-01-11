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

    def get_file(self, index: int) -> VideoFile:
        """获取文件

        Args:
            index (int): 文件索引

        Returns:
            VideoFile: 文件对象
        """
        return self.task.video_sequence[index]

    def set_file(self, index: int, video: VideoFile):
        """设置文件

        Args:
            index (int): 文件索引
            video (VideoFile): 文件对象
        """
        self.task.video_sequence.modify(index, video)

    def add_file(self, filename: str, path: str):
        """添加文件

        Args:
            filename (str): 文件名
            path (str): 文件路径
        """
        self.task.video_sequence.append(
            VideoFile(
                no=self.sequence_length() + 1,
                file_name=filename,
                file_path=path,
                start_time="开始",
                end_time="结束",
            )
        )

    def remove_file(self, index: int):
        """删除文件

        Args:
            index (int): 文件索引
        """
        self.task.video_sequence.remove(index)

    def swap_file(self, index1: int, index2: int):
        """交换文件

        Args:
            index1 (int): 文件索引1
            index2 (int): 文件索引2
        """
        self.task.video_sequence.swap(index1, index2)

    def clear_all_files(self):
        """清除所有文件"""
        self.task.video_sequence.clear()

    def sequence_length(self) -> int:
        """获取视频序列长度

        Returns:
            int: 视频序列长度
        """
        return len(self.task.video_sequence.video_files)

    def export_sequence(self):
        """导出视频序列"""

        # 加载 view 上的导出配置
        export_config = self.view.export_config
        self.task.export_config = export_config
