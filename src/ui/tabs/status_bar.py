"""状态条 — 底部导出状态反馈。"""

import dearpygui.dearpygui as dpg


def build_status_bar() -> None:
    """构建底部状态条（仅调用一次）。"""
    with dpg.group(horizontal=True, tag="status_bar"):
        dpg.add_text("就绪", tag="status_text", color=(128, 128, 128, 255))


def set_status_export_success(msg: str | None) -> None:
    """显示导出成功信息（绿色）。"""
    if msg:
        dpg.set_value("status_text", f"导出成功：{msg}")
        dpg.configure_item("status_text", color=(0, 200, 0, 255))
    else:
        dpg.set_value("status_text", "就绪")
        dpg.configure_item("status_text", color=(128, 128, 128, 255))


def set_status_export_fail(msg: str) -> None:
    """显示导出失败信息（红色，持久显示）。"""
    dpg.set_value("status_text", msg)
    dpg.configure_item("status_text", color=(255, 60, 60, 255))
