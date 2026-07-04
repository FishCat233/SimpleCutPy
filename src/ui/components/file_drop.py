"""文件选择与拖放处理。dearpygui 不原生支持 OS 文件拖放，使用 file_dialog 替代。"""

import logging
import os

import dearpygui.dearpygui as dpg

from controller.core import CoreController


def build_file_dialog() -> None:
    """创建多选文件对话框控件。"""
    with dpg.file_dialog(
        directory_selector=False,
        show=False,
        modal=True,
        tag="file_open_dialog",
        width=600,
        height=400,
    ):
        dpg.add_file_extension(".*")
        dpg.add_file_extension(".mp4", color=(0, 255, 0, 255))
        dpg.add_file_extension(".mkv", color=(255, 255, 0, 255))
        dpg.add_file_extension(".mov", color=(0, 255, 255, 255))
        dpg.add_file_extension(".avi", color=(255, 0, 0, 255))


def open_file_dialog() -> None:
    """打开文件选择对话框。"""
    dpg.show_item("file_open_dialog")


def handle_file_selection(_, file_data: dict, controller: CoreController) -> None:
    """文件选择回调 - 将选中文件加入序列。"""
    selections = file_data.get("selections", {})
    for path in selections:
        filepath, filename = os.path.split(path)
        logging.debug(f"导入文件：{path} -> 路径: {filepath}, 文件名: {filename}")
        controller.add_file(filename, filepath)
