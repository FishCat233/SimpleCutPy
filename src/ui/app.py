"""dearpygui 应用入口 — context 创建、viewport 配置、渲染循环。"""

import dearpygui.dearpygui as dpg

import meta
from controller.core import CoreController
from ui.tabs import about_tab, export_tab, help_tab, source_tab
from ui.tabs.status_bar import build_status_bar

VIEWPORT_WIDTH = 750
VIEWPORT_HEIGHT = 550


def run(controller: CoreController) -> None:
    """启动 dearpygui 应用主循环。"""
    dpg.create_context()

    dpg.create_viewport(
        title=f"Simple Cut Py {meta.VERSION}",
        width=VIEWPORT_WIDTH,
        height=VIEWPORT_HEIGHT,
        min_width=VIEWPORT_WIDTH,
        min_height=VIEWPORT_HEIGHT,
    )

    _setup_theme()
    _build_ui(controller)

    dpg.setup_dearpygui()
    dpg.show_viewport()

    # 渲染循环
    while dpg.is_dearpygui_running():
        _render_frame(controller)
        dpg.render_dearpygui_frame()

    dpg.destroy_context()


# ---- 内部 ----


def _setup_theme() -> None:
    """设置全局字体与样式 — 加载中文字体。"""
    with dpg.font_registry():
        # 尝试加载微软雅黑（Windows 自带中文字体）
        font_paths = [
            "C:/Windows/Fonts/msyh.ttc",
            "C:/Windows/Fonts/simhei.ttf",
        ]
        font_loaded = False
        for fp in font_paths:
            try:
                default_font = dpg.add_font(fp, 16)
                dpg.bind_font(default_font)
                font_loaded = True
                break
            except SystemError:
                continue
        if not font_loaded:
            # 回退到默认字体
            pass


def _build_ui(controller: CoreController) -> None:
    """一次性构建所有 UI 控件。"""
    with dpg.window(
        label="main",
        tag="main_window",
        no_title_bar=True,
        no_move=True,
        no_resize=True,
        no_close=True,
        no_collapse=True,
    ):
        # 调整窗口占满 viewport
        dpg.set_primary_window("main_window", True)

        # Tab 切换区
        with dpg.tab_bar(tag="main_tabs"):
            source_tab.build(controller)
            export_tab.build(controller)
            help_tab.build()
            about_tab.build()

        # 底部状态条
        build_status_bar()


def _render_frame(controller: CoreController) -> None:
    """每帧调用 — 轮询 controller 状态并刷新 UI。"""
    # 处理导出结果
    all_done = False
    for msg in controller.drain_export_results():
        export_tab.handle_export_result(msg)
        all_done = True

    # 所有导出线程结束时重新启用导出按钮
    if all_done and not controller.has_pending_exports():
        export_tab.enable_export_button()

    # 渲染各 tab 的动态内容
    source_tab.render(controller)
    export_tab.render(controller)
