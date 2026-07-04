"""导出设置 Tab — 导出配置与导出按钮。"""

import logging

import dearpygui.dearpygui as dpg

from controller.core import CoreController
from export.model import ExportConfig, MbpsConfig, X264Config
from ui.tabs.status_bar import set_status_export_fail, set_status_export_success

# 缓存的 mbps 值（当控件被隐藏时保留）
_cached_mbps: float = 6.0


def build(controller: CoreController) -> None:
    """构建导出设置 tab 的全部控件（仅调用一次）。"""
    with dpg.tab(label="导出设置", tag="tab_export"):
        # 导出文件名
        with dpg.group(horizontal=True):
            dpg.add_text("导出文件名（带扩展名）：")
            dpg.add_input_text(tag="export_name", width=270, default_value="")

        # 导出路径 + 浏览按钮
        with dpg.group(horizontal=True):
            dpg.add_text("导出路径：")
            dpg.add_input_text(tag="export_path", width=350, default_value="")
            dpg.add_button(label="浏览...", callback=_on_browse_path)

        # 目录选择对话框
        with dpg.file_dialog(
            directory_selector=True,
            show=False,
            modal=True,
            tag="export_path_dialog",
            width=500,
            height=400,
            callback=_on_path_selected,
        ):
            pass

        # 大小控制模式
        with dpg.group(horizontal=True):
            dpg.add_text("文件大小控制：")
            dpg.add_combo(
                items=["x264", "mbps", "不控制"],
                default_value="x264",
                tag="size_control_mode",
                width=200,
                callback=lambda _, v: _on_size_mode_change(v),
            )

        # mbps 输入（条件渲染）
        with dpg.group(horizontal=True):
            dpg.add_text("导出码率（Mbps）：")
            dpg.add_input_text(
                tag="mbps_input", width=295, default_value=str(_cached_mbps)
            )

        # 多音轨处理
        with dpg.group(horizontal=True):
            dpg.add_text("多音轨处理：")
            dpg.add_combo(
                items=[
                    "只选择第一个音轨",
                    "全部合并为单音轨",
                    "上面两个都要（两次输出）",
                ],
                default_value="只选择第一个音轨",
                tag="multi_track_mode",
                width=200,
            )

        # 导出按钮
        dpg.add_button(
            label="导出",
            tag="export_btn",
            callback=lambda: _on_export(controller),
        )

        # 默认隐藏 mbps 输入（x264 是默认模式）
        _on_size_mode_change("x264")


def render(controller: CoreController) -> None:
    """每帧渲染 — 无动态内容需刷新。"""
    pass


def handle_export_result(msg) -> None:
    """处理导出结果 — 更新状态条。"""
    from message import WorkStateEnum

    if msg.state == WorkStateEnum.SUCCESS:
        logging.info(f"导出成功：{msg.export_name}")
        set_status_export_success(msg.export_name)
    else:
        logging.error(f"导出失败：{msg.export_name}")
        set_status_export_fail(f"导出失败：{msg.export_name}")


def enable_export_button() -> None:
    """重新启用导出按钮。"""
    dpg.enable_item("export_btn")


# ---- 内部 ----


def _on_browse_path() -> None:
    """打开目录选择对话框。"""
    dpg.show_item("export_path_dialog")


def _on_path_selected(_, file_data: dict) -> None:
    """目录选择回调。"""
    path = file_data.get("file_path_name", "")
    if path:
        dpg.set_value("export_path", path)


def _on_size_mode_change(mode: str) -> None:
    """大小控制模式切换 — 条件显示/隐藏 mbps 输入。"""
    global _cached_mbps
    if mode == "mbps":
        dpg.show_item("mbps_input")
    else:
        # 隐藏前缓存当前值
        try:
            _cached_mbps = float(dpg.get_value("mbps_input"))
        except (ValueError, TypeError):
            pass
        dpg.hide_item("mbps_input")


def _on_export(controller: CoreController) -> None:
    """导出按钮回调 — 收集配置并启动导出。"""
    # 收集配置
    controller.task.export_file_name = dpg.get_value("export_name")
    controller.task.export_file_path = dpg.get_value("export_path")

    size_mode = dpg.get_value("size_control_mode")
    if size_mode == "x264":
        size_control = X264Config()
    elif size_mode == "mbps":
        try:
            mbps_value = float(dpg.get_value("mbps_input") or _cached_mbps)
        except (ValueError, TypeError):
            mbps_value = _cached_mbps
        size_control = MbpsConfig(mbps=mbps_value)
    else:
        size_control = None

    multi_mode_map = {
        "只选择第一个音轨": "first",
        "全部合并为单音轨": "amix",
        "上面两个都要（两次输出）": "export_both",
    }
    multi_mode = multi_mode_map.get(dpg.get_value("multi_track_mode"), "first")

    controller.setup_export_config(
        ExportConfig(multi_track_mode=multi_mode, size_control=size_control)
    )

    # 禁用导出按钮，启动导出
    dpg.disable_item("export_btn")
    set_status_export_success(None)  # 清除旧状态
    controller.export_sequence()
