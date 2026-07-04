"""核心控制器 — 纯数据管理 + 线程管理，不依赖任何 UI 框架。"""

import logging
import os
import threading
from collections import deque

from pydantic import ValidationError

import export
from export.model import ExportConfig, ExportTask, VideoFile
from message import ExportMessage, WorkStateEnum


class CoreController:
    """核心控制器（无 UI 依赖）"""

    def __init__(self):
        self.first_select_index: int = 0
        self.task = ExportTask()
        self.working_threads: dict[str, threading.Thread] = {}

        # 线程安全的结果队列，UI 层每帧轮询
        self._export_results: deque[ExportMessage] = deque()
        self._results_lock = threading.Lock()

    # ---- 导出结果轮询接口 ----

    def drain_export_results(self) -> list[ExportMessage]:
        """取出所有待处理的导出结果，线程安全。"""
        with self._results_lock:
            results = list(self._export_results)
            self._export_results.clear()
        return results

    def has_pending_exports(self) -> bool:
        """是否还有导出线程在运行。"""
        return len(self.working_threads) > 0

    # ---- 文件操作 ----

    def get_file(self, index: int) -> VideoFile:
        return self.task.video_sequence[index]

    def set_file(self, index: int, video: VideoFile):
        self.task.video_sequence.modify(index, video)

    def add_file(self, filename: str, path: str):
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
        self.task.video_sequence.remove(index)

    def swap_file(self, index1: int, index2: int):
        self.task.video_sequence.swap(index1, index2)
        self.task.video_sequence[index1].no, self.task.video_sequence[index2].no = (
            self.task.video_sequence[index2].no,
            self.task.video_sequence[index1].no,
        )

    def clear_all_files(self):
        self.task.video_sequence.clear()

    def sequence_length(self) -> int:
        return len(self.task.video_sequence.video_files)

    # ---- 导出配置 ----

    def setup_export_config(self, export_config: ExportConfig):
        self.task.export_config = export_config

    # ---- 导出 ----

    def export_sequence(self):
        """启动导出线程，结果通过 drain_export_results() 获取。"""
        try:
            self.task = ExportTask.model_validate(self.task)
        except ValidationError as e:
            logging.error(f"Export Task Validate Error: {e}")
            return

        tasks = []
        if self.task.export_config.multi_track_mode == "export_both":
            first_only_task = self.task.model_copy(deep=True)
            first_only_task.export_config.multi_track_mode = "first"

            amix_task = self.task.model_copy(deep=True)
            amix_task.export_config.multi_track_mode = "amix"
            header, ext = os.path.splitext(amix_task.get_export_full_path())
            amix_task.export_file_name = header + "_amix" + ext

            tasks.append(first_only_task)
            tasks.append(amix_task)
        else:
            tasks.append(self.task)

        for task in tasks:
            export_path = task.get_export_full_path()
            thread = threading.Thread(
                target=self._export_thread, args=(task, export_path), daemon=True
            )
            self.working_threads[export_path] = thread
            thread.start()

    def _export_thread(self, task: ExportTask, export_path: str):
        """导出线程函数，完成后将结果推入安全队列。"""
        success = export.core.export(task)

        with self._results_lock:
            if success:
                self._export_results.append(
                    ExportMessage(WorkStateEnum.SUCCESS, "导出完成", export_path)
                )
            else:
                self._export_results.append(
                    ExportMessage(WorkStateEnum.FAIL, "导出失败", export_path)
                )

        if export_path in self.working_threads:
            self.working_threads.pop(export_path, None)

    # ---- 工具 ----

    @staticmethod
    def format_time(time_str: str) -> str:
        time_str = time_str.strip().replace("：", ":").replace(" ", ":")
        return time_str
