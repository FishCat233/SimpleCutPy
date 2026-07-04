"""关于 Tab — 版本信息、项目链接、检查更新。"""

import logging
import threading
import webbrowser

import dearpygui.dearpygui as dpg

import meta
import tools.version


def build() -> None:
    """构建关于 tab（仅调用一次）。"""
    with dpg.tab(label="关于", tag="tab_about"):
        dpg.add_text(
            "关于 Simple Cut Py：\n"
            "一个用于进行简单剪切工作的开源迷你剪辑软件。\n"
            "\n"
            "项目地址：\n"
            "\n"
            "--FishCat233\n"
            "2024.2.27",
            wrap=460,
        )

        dpg.add_text(f"Simple Cut Py 版本号\n{meta.VERSION}", tag="version_text")

        with dpg.group(horizontal=True):
            dpg.add_button(
                label="访问项目",
                callback=lambda: webbrowser.open(
                    "https://github.com/FishCat233/SimpleCutPy"
                ),
            )
            dpg.add_button(
                label="检查更新",
                tag="check_update_btn",
                callback=_on_check_update,
            )

        dpg.add_text("", tag="check_update_result")


def _on_check_update() -> None:
    """异步检查更新，避免阻塞渲染循环。"""
    dpg.disable_item("check_update_btn")

    def check() -> None:
        try:
            update_info = tools.version.check_update()
            if update_info.has_new_version:
                dpg.set_value(
                    "check_update_result",
                    f"发现新版本 {update_info.latest_version}！\n"
                    f"当前版本：{update_info.current_version}",
                )
            else:
                dpg.set_value(
                    "check_update_result",
                    f"当前已是最新版本 {update_info.current_version}！",
                )
        except Exception as e:
            logging.error(f"检查更新失败：{e}")
            dpg.set_value("check_update_result", "检查更新失败，请稍后再试！")
        finally:
            dpg.enable_item("check_update_btn")

    threading.Thread(target=check, daemon=True).start()
