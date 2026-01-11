import os
import threading
from typing import TYPE_CHECKING

import wx

from export.model import ExportConfig, ExportTask, VideoFile
import export
from message import ExportMessage, WorkStateEnum

if TYPE_CHECKING:
    from SimpleCutMainFrame import SimpleCutPyMainFrame


class CoreController:
    """核心控制器"""

    def __init__(self, view: "SimpleCutPyMainFrame"):
        self.view = view
        self.first_select_index: int = 0
        self.task = ExportTask()

        self.working_thread = {}

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
        # 更新编号
        self.task.video_sequence[index1].no, self.task.video_sequence[index2].no = (
            self.task.video_sequence[index2].no,
            self.task.video_sequence[index1].no,
        )

    def clear_all_files(self):
        """清除所有文件"""
        self.task.video_sequence.clear()

    def sequence_length(self) -> int:
        """获取视频序列长度

        Returns:
            int: 视频序列长度
        """
        return len(self.task.video_sequence.video_files)

    def setup_export_config(self, export_config: ExportConfig):
        """设置导出配置

        Args:
            export_config (ExportConfig): 导出配置对象
        """
        self.task.export_config = export_config

    def export_sequence(self):
        """导出视频序列"""

        # 预处理，将多导出化为单导出
        tasks = []
        if self.task.export_config.multi_track_mode == "export_both":
            first_only_task = self.task.model_copy()
            first_only_task.export_config.multi_track_mode = "first"

            amix_task = self.task.model_copy()
            amix_task.export_config.multi_track_mode = "amix"
            # 添加后缀
            origin_name, ext = os.path.splitext(amix_task.export_file_name)
            amix_task.export_file_name = origin_name + "_amix" + ext

            tasks.append(first_only_task)
            tasks.append(amix_task)
        else:
            tasks.append(self.task)

        def export_thread(task):
            """导出线程函数"""
            success = export.core.export(task)
            export_path = task.get_export_full_path()

            # 从工作线程字典中移除
            if export_path in self.working_thread:
                self.working_thread.pop(export_path)

            # 使用wx.CallAfter在主线程中更新UI
            if success:
                wx.CallAfter(
                    self.view.on_export_done,
                    ExportMessage(WorkStateEnum.SUCCESS, "导出完成", export_path),
                )
            else:
                wx.CallAfter(
                    self.view.on_export_done,
                    ExportMessage(WorkStateEnum.FAIL, "导出失败", export_path),
                )

        for task in tasks:
            export_path = task.get_export_full_path()
            # 创建线程
            thread = threading.Thread(target=export_thread, args=(task,))
            # 保存线程引用
            self.working_thread[export_path] = thread
            # 启动线程
            thread.start()
