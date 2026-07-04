"""素材设置 Tab — 视频序列列表、时间编辑、操作按钮。"""

import dearpygui.dearpygui as dpg

from controller.core import CoreController
from ui.components.file_drop import (
    build_file_dialog,
    handle_file_selection,
    open_file_dialog,
)

# 渲染状态（跨帧保持）
_selected_idx: int = -1
_sequence_len: int = 0


def build(controller: CoreController) -> None:
    """构建素材设置 tab 的全部控件（仅调用一次）。"""
    global _selected_idx, _sequence_len
    _selected_idx = -1
    _sequence_len = 0

    with dpg.tab(label="素材设置", tag="tab_source"):
        # 文件对话框
        build_file_dialog()

        # 视频序列表
        with dpg.table(
            tag="source_table",
            header_row=True,
            borders_innerH=True,
            borders_outerH=True,
            borders_innerV=True,
            borders_outerV=True,
            policy=dpg.mvTable_SizingStretchProp,
            height=200,
        ):
            dpg.add_table_column(
                label="序号", width_fixed=True, init_width_or_weight=45
            )
            dpg.add_table_column(
                label="文件名", width_fixed=True, init_width_or_weight=260
            )
            dpg.add_table_column(
                label="开始时间", width_fixed=True, init_width_or_weight=75
            )
            dpg.add_table_column(
                label="结束时间", width_fixed=True, init_width_or_weight=75
            )
            dpg.add_table_column(
                label="文件路径", width_fixed=True, init_width_or_weight=230
            )

        # 时间输入行
        with dpg.group(horizontal=True):
            dpg.add_text("开始时间")
            dpg.add_input_text(
                tag="input_start_time",
                width=100,
                callback=lambda s, v: _on_start_time(v, controller),
            )
            dpg.add_text("结束时间")
            dpg.add_input_text(
                tag="input_end_time",
                width=100,
                callback=lambda s, v: _on_end_time(v, controller),
            )

        # 按钮行
        with dpg.group(horizontal=True):
            dpg.add_button(label="添加文件", callback=lambda: open_file_dialog())
            dpg.add_button(label="移除文件", callback=lambda: _on_remove(controller))
            dpg.add_button(label="向上移动", callback=lambda: _on_move_up(controller))
            dpg.add_button(label="向下移动", callback=lambda: _on_move_down(controller))
            dpg.add_button(label="清除全部", callback=lambda: _on_clear_all(controller))

        # 文件对话框回调
        dpg.set_item_callback(
            "file_open_dialog",
            lambda s, d: handle_file_selection(s, d, controller),
        )


def render(controller: CoreController) -> None:
    """每帧渲染 — 刷新表格和时间输入框。"""
    global _selected_idx, _sequence_len
    seq_len = controller.sequence_length()

    # 选择变化时同步时间输入框
    current_selected = controller.first_select_index
    if current_selected != _selected_idx:
        _selected_idx = current_selected
        if 0 <= _selected_idx < seq_len:
            f = controller.get_file(_selected_idx)
            dpg.set_value("input_start_time", f.start_time)
            dpg.set_value("input_end_time", f.end_time)
        else:
            dpg.set_value("input_start_time", "")
            dpg.set_value("input_end_time", "")

    # 序列长度变化时重建表格行
    if seq_len != _sequence_len:
        _rebuild_table(controller, seq_len)
        _sequence_len = seq_len


# ---- 内部 ----


def _on_row_select(idx: int, controller: CoreController) -> None:
    """表格行选中回调。"""
    global _selected_idx, _sequence_len
    controller.first_select_index = idx
    _selected_idx = idx
    _sequence_len = 0  # 强制下次重建以更新高亮


def _rebuild_table(controller: CoreController, seq_len: int) -> None:
    """清空并重建表格所有行。"""
    dpg.delete_item("source_table", children_only=True)
    sequence = controller.task.video_sequence.get_video_list()
    for i, item in enumerate(sequence):
        with dpg.table_row():
            dpg.add_selectable(
                label=str(i + 1),
                tag=f"table_row_{i}",
                callback=lambda s, d, idx=i: _on_row_select(idx, controller),
            )
            dpg.add_text(item.file_name)
            dpg.add_text(item.start_time)
            dpg.add_text(item.end_time)
            dpg.add_text(item.file_path)


def _on_start_time(value: str, controller: CoreController) -> None:
    global _selected_idx
    if 0 <= _selected_idx < controller.sequence_length():
        vf = controller.get_file(_selected_idx)
        vf.start_time = controller.format_time(value)
        controller.set_file(_selected_idx, vf)


def _on_end_time(value: str, controller: CoreController) -> None:
    global _selected_idx
    if 0 <= _selected_idx < controller.sequence_length():
        vf = controller.get_file(_selected_idx)
        vf.end_time = controller.format_time(value)
        controller.set_file(_selected_idx, vf)


def _on_remove(controller: CoreController) -> None:
    global _selected_idx, _sequence_len
    if _selected_idx < 0 or _selected_idx >= controller.sequence_length():
        return
    controller.remove_file(_selected_idx)
    _sequence_len = 0  # 强制下次重建


def _on_move_up(controller: CoreController) -> None:
    global _selected_idx, _sequence_len
    if _selected_idx <= 0:
        return
    controller.swap_file(_selected_idx, _selected_idx - 1)
    _selected_idx -= 1
    _sequence_len = 0


def _on_move_down(controller: CoreController) -> None:
    global _selected_idx, _sequence_len
    if _selected_idx >= controller.sequence_length() - 1:
        return
    controller.swap_file(_selected_idx, _selected_idx + 1)
    _selected_idx += 1
    _sequence_len = 0


def _on_clear_all(controller: CoreController) -> None:
    global _selected_idx, _sequence_len
    controller.clear_all_files()
    _selected_idx = -1
    _sequence_len = 0
