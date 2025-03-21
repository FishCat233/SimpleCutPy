"""Subclass of MainFrame, which is generated by wxFormBuilder."""
import os
import subprocess
import time

import wx

import SimpleCutPy
import logging
import threading

from command import concat_filter, merge_filestream_audio_channel
from message import ExportMessage, WorkStateEnum

from pymediainfo import MediaInfo

from src.model import VideoSequenceModel, VideoModel

VERSION = "0.3.4"


class FileDropTarget(wx.FileDropTarget):
    def __init__(self, target):
        wx.FileDropTarget.__init__(self)
        self.target = target

    def OnDropFiles(self, x, y, filenames):
        for file in filenames:
            self.target.append_files(file, file)

        return True


# TODO: 重写配置的参数验证，建立物品类和导出配置 ExportConfig


# Implementing MainFrame
class SimpleCutPyMainFrame(SimpleCutPy.MainFrame):
    def __init__(self, parent=None):
        SimpleCutPy.MainFrame.__init__(self, parent)

        # 设置拖拽文件
        self.list_ctrl.SetDropTarget(FileDropTarget(self))

        self.first_selected_index = 0
        # self.item_list: list[dict] = []  # 列表是控件上的映射，列表的物品顺序就是控件上物品的顺序
        self.video_sequence: VideoSequenceModel = VideoSequenceModel()

        # list_ctrl 控件添加列
        self.list_ctrl.InsertColumn(0, "序号", width=40)
        self.list_ctrl.InsertColumn(1, "文件名", width=280)
        self.list_ctrl.InsertColumn(2, "开始时间", width=65)
        self.list_ctrl.InsertColumn(3, "结束时间", width=65)
        self.list_ctrl.InsertColumn(4, "文件路径", width=238)

        # 标记版本
        self.VersionText.SetLabelText(f"Simple Cut Py 版本号\n{VERSION}")

        # Handlers for MainFrame events.

        # TODO: 参数初始化
        self.ExportBitCtrl.SetValue("6")

    def on_add_file_button_click(self, event):
        # 文件选择对话框
        file_dlg = wx.FileDialog(self, u"选择导入的文件", "", "", "*.mp4", wx.FD_OPEN)
        if file_dlg.ShowModal() == wx.ID_OK:
            # 文件导入
            # {NO, filename, startTime, endTime, path}

            # 将导入文件数据转为字典
            filename = file_dlg.GetFilename()
            path = file_dlg.GetPath()

            self.append_files(filename, path)

            logging.debug("导入文件：{}, {}".format(file_dlg.GetFilename(), file_dlg.GetPath()))

        file_dlg.Destroy()

    def list_ctrl_on_drop_files(self, event):
        files = event.GetFiles()

        # 防止拖空文件
        if len(files) <= 0:
            return

        logging.debug(f"拖拽文件：{files}")

        for filename in files:
            item_no = self.list_ctrl.GetItemCount()
            self.add_files(item_no, filename, filename)

    def on_remove_file_button_click(self, event):
        # 删除列表中的项
        index = self.first_selected_index

        if index <= -1:
            return  # 如果没有选中

        if index >= len(self.video_sequence):
            return  # 如果超出范围

        self.video_sequence.pop_video(index)

        # 删除界面中的项

        self.list_ctrl.DeleteItem(index)

        # 删除以后进行序号重排
        for i in range(len(self.video_sequence)):
            if i < index:
                continue

            # 从删除项开始后面的每一个物品都重新加载
            self.update_video_model_item(i)

        # 选中 index
        self.list_ctrl.Select(index)

    def on_move_up_file_button_click(self, event):
        value = self.first_selected_index

        if value == -1:
            return  # 如果没有选中

        if value == 0:
            wx.MessageBox("选中素材已置顶。", "错误", style=wx.YES_DEFAULT | wx.ICON_QUESTION)
            return  # 如果是第一个物品

        self.video_sequence.swap_item(value, value - 1)

        self.update_video_model_item(value)
        self.update_video_model_item(value - 1)

        self.list_ctrl.Select(self.first_selected_index, on=0)  # 取消原来的选中
        self.list_ctrl.Select(self.first_selected_index - 1)

    def on_move_down_file_button_click(self, event):
        value = self.first_selected_index

        if value == -1:
            return  # 如果没有选中

        if value == self.list_ctrl.GetItemCount() - 1:
            wx.MessageBox("选中素材在最末端。", "错误", style=wx.YES_DEFAULT | wx.ICON_QUESTION)
            return  # 如果是最后一个

        self.video_sequence.swap_item(self.first_selected_index, self.first_selected_index + 1)

        self.update_video_model_item(value)
        self.update_video_model_item(value + 1)

        # 选中转移
        self.list_ctrl.Select(self.first_selected_index, on=0)  # 取消原来的选中
        self.list_ctrl.Select(self.first_selected_index + 1)

    def on_export_button_click(self, event):
        # TODO: 加了码率设置的功能，别忘了测试
        # TODO: item list 重写

        # 从界面读取导出文件名、路径、码率
        export_name = self.ExportNameCtrl.GetValue()
        export_path = self.ExportPathCtrl.GetValue()
        export_mbps = self.ExportBitCtrl.GetValue()
        export_amix = self.AmixCheckBox.IsChecked()

        # 导出码率设置为空则使用 6 mbps
        if export_mbps == '':
            export_mbps = 6

        # 导出文件名为空则使用时间
        if export_name == '':
            export_name = str(time.strftime('No Title %Y.%m.%d - %H.%M.output.mp4'))

        # 导出路径不为空则更改导出目录
        if not export_path == '':
            # os.chdir(export_path)
            export_name = export_path + '/' + export_name
        else:
            # 默认使用第一个文件的目录
            path = os.path.dirname(self.video_sequence[0].path)
            export_name = path + '/' + export_name

        threading.Thread(target=self.export_video_file, args=(export_amix, export_mbps, export_name)).start()
        self.ExportBtn.Disable()

        return

    def export_video_file(self, export_amix, export_mbps, export_name):
        # TODO: item list 重写
        # 导出命令
        console_command = 'ffmpeg '
        filter_complex_string = '-filter_complex '
        filter_complex_filters: list[str] = []
        concat_inputs: list[str] = []
        for index, item in enumerate(self.video_sequence.video_list):
            no = index
            start_time = item.start_time
            end_time = item.end_time
            item_path = item.path

            # 开始、结束时间以及路径的命令行参数生成
            time_param = []
            if start_time != "":
                time_param.append(f'-ss {start_time}')
            if end_time != "":
                time_param.append(f'-to {end_time}')
            time_param.append(f'-i "{item_path}"')
            time_string = " ".join(time_param)

            console_command += time_string + " "

            # concat_inputs 的参数生成
            concat_inputs.append(f'{no}:v')

            media_info = MediaInfo.parse(item_path)
            audio_tracks_number = len(media_info.audio_tracks)
            if audio_tracks_number > 0 and export_amix:
                # 多音轨，合并
                # amix_filter
                filter_complex_filters.append(merge_filestream_audio_channel(f"{no}", audio_tracks_number, f"{no}a"))
                concat_inputs.append(f'{no}a')
            else:
                # 单音轨
                concat_inputs.append(f'{no}:a')
        # 使用 concat 滤镜
        concat_string = concat_filter(concat_inputs, "v", "a")
        filter_complex_filters.append(concat_string)
        # 拼接 filter_complex 命令行参数，拼接滤镜
        console_command += filter_complex_string + f'"{";".join(filter_complex_filters)}"'
        console_command += ' -map "[v]" -map "[a]"'
        # 拼接全指令
        if not export_name.endswith(".mp4"):
            export_name += ".mp4"
        console_command += f' -b:v {export_mbps}M "{export_name}"'
        logging.info(f"导出命令：{console_command}")

        # 执行命令
        try:
            subprocess.run(console_command, shell=False, check=True, creationflags=subprocess.CREATE_NO_WINDOW)

            # 完成命令，发送事件
            wx.CallAfter(self.on_export_done, ExportMessage(WorkStateEnum.SUCCESS, "导出完成"))
        except subprocess.CalledProcessError as e:
            # 导出失败，发送事件
            wx.CallAfter(self.on_export_done, ExportMessage(WorkStateEnum.FAIL, e))

    def on_open_project_website_button_click(self, event):
        # TODO: Implement ProjectWebBtnOnClick
        pass

    def add_files(self, item_no, filename, path):
        """
        添加文件。将文件添加到物品列表，并刷新显示在界面上
        :param item_no: 序号
        :param filename: 文件名
        :param path: 文件路径
        :return: 空
        """
        # 构建物品字典
        item = VideoModel(path, filename)

        # 加到物品表
        self.video_sequence.append_video(item)

        # 显示数据在界面
        index = self.list_ctrl.InsertItem(item_no, item_no)
        self.update_video_model_item(index)

    def append_files(self, filename, path):
        item_no = self.list_ctrl.GetItemCount()
        self.add_files(item_no, filename, path)

    def on_clear_all_button_click(self, event):
        self.video_sequence.clear_all()
        logging.debug(f"clear all video: {self.video_sequence.video_list}")
        self.update_sequence_model()

    def on_start_time_ctrl_text(self, event):
        """修改开始时间输入框的时候修改itemlist的start_time"""
        index = self.first_selected_index
        value = self.StartTimeCtrl.GetValue()

        self.video_sequence[index].start_time = value

        self.update_video_model_item(index)

    def on_end_time_ctrl_text(self, event):
        """修改结束时间输入框的时候修改itemlist的end_time"""
        index = self.first_selected_index
        value = self.EndTimeCtrl.GetValue()

        self.video_sequence[index].end_time = value

        self.update_video_model_item(index)

    def on_list_item_selected(self, event):
        index = self.list_ctrl.GetFirstSelected()
        self.first_selected_index = index

        # 获取选中的物品时间，同步到输入框
        self.StartTimeCtrl.SetValue(self.video_sequence[index].start_time)
        self.EndTimeCtrl.SetValue(self.video_sequence[index].end_time)

        logging.debug(
            f"Selected Item Index: {index}, \
                    Selected Item no: {self.video_sequence[index]}")

    def update_video_model_item(self, no):
        """重载物品"""
        self.load_video_model_item(self.video_sequence[no], no)

    def update_sequence_model(self):
        """重载序列"""
        self.load_sequence_model(self.video_sequence)

    def load_video_model_item(self, load_item: VideoModel, list_ctrl_index: int):
        """
        将 VideoModel 载入到 列表item上
        :param load_item: 载入的物品
        :param list_ctrl_index: 载入在控件的行数
        :return: 无
        """
        self.list_ctrl.SetItem(list_ctrl_index, 0, str(list_ctrl_index))
        self.list_ctrl.SetItem(list_ctrl_index, 1, load_item.filename)

        start_time = "开头" if load_item.start_time == "" else load_item.start_time
        end_time = "结尾" if load_item.end_time == "" else load_item.end_time
        self.list_ctrl.SetItem(list_ctrl_index, 2, start_time)
        self.list_ctrl.SetItem(list_ctrl_index, 3, end_time)
        self.list_ctrl.SetItem(list_ctrl_index, 4, load_item.path)

    def load_sequence_model(self, sequence: VideoSequenceModel):
        """
        把物品列表上的所有物品载入到用户界面的控件上
        :return:
        """
        # 清除控件
        self.list_ctrl.DeleteAllItems()

        # 重新载入
        for index, item in enumerate(sequence.video_list):
            logging.debug(f"load item: {index},{item}")
            self.list_ctrl.InsertItem(index, index)
            self.load_video_model_item(item, index)

    def on_export_done(self, msg: ExportMessage):
        logging.debug(f"Export Done: {msg}")
        if msg.state == WorkStateEnum.SUCCESS:
            wx.MessageBox("导出成功", "提示", wx.OK | wx.ICON_INFORMATION)
        elif msg.state == WorkStateEnum.FAIL:
            logging.error(f"Export Error: {msg.message}")
            wx.MessageBox("导出失败", "提示", wx.OK | wx.ICON_INFORMATION)

        self.ExportBtn.Enable()
        return


if __name__ == '__main__':
    App = wx.App()
    mainFrame = SimpleCutPyMainFrame(None)
    mainFrame.Show(True)
    App.MainLoop()
