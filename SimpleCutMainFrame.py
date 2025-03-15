"""Subclass of MainFrame, which is generated by wxFormBuilder."""
import os
import time

import wx

import SimpleCutPy
import logging

from command import concat_filter, merge_filestream_audio_channel
from pymediainfo import MediaInfo


class FileDropTarget(wx.FileDropTarget):
    def __init__(self, target):
        wx.FileDropTarget.__init__(self)
        self.target = target

    def OnDropFiles(self, x, y, filenames):
        for file in filenames:
            self.target.append_files(file, file)

        return True


# TODO: 重写配置的参数验证，建立物品类和导出配置 ExportConfig
# TODO: 多线程剪辑


# Implementing MainFrame
class SimpleCutPyMainFrame(SimpleCutPy.MainFrame):
    def __init__(self, parent=None):
        SimpleCutPy.MainFrame.__init__(self, parent)

        # 设置拖拽文件
        self.list_ctrl.SetDropTarget(FileDropTarget(self))

        self.first_selected_index = 0
        self.item_list: list[dict] = []  # 列表是控件上的映射，列表的物品顺序就是控件上物品的顺序

        # list_ctrl 控件添加列
        self.list_ctrl.InsertColumn(0, "序号", width=40)
        self.list_ctrl.InsertColumn(1, "文件名", width=280)
        self.list_ctrl.InsertColumn(2, "开始时间", width=65)
        self.list_ctrl.InsertColumn(3, "结束时间", width=65)
        self.list_ctrl.InsertColumn(4, "文件路径", width=238)

        # Handlers for MainFrame events.

        # TODO: 参数初始化
        self.ExportBitCtrl.SetValue("6")

    @staticmethod
    def format_time(time_string: str) -> str:
        # 一些提升体验的小更改
        # 将空格替换为 ":"
        # 将全角 “：” 替换为半角 “:”
        time_string = str.replace(time_string, " ", ":")
        time_string = str.replace(time_string, "：", ":")
        return time_string

    def ApplyTimeButtonOnClick(self, event):
        apply_time_item_index = self.first_selected_index

        # 从控件上读取时间
        start_time = self.StartTimeCtrl.GetValue()
        end_time = self.EndTimeCtrl.GetValue()

        start_time = self.format_time(start_time)
        end_time = self.format_time(end_time)

        # 设置物品列表的参数，如果为空就不更改
        if not start_time == '':
            self.item_list[apply_time_item_index]["start_time"] = start_time
        if not end_time == '':
            self.item_list[apply_time_item_index]["end_time"] = end_time

        # 更新界面
        self.list_load_item(self.item_list[apply_time_item_index], apply_time_item_index)

    def AddFileBtnOnClick(self, event):
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

    def RemoveBtnOnClick(self, event):
        # 删除列表中的项
        delete_index = self.first_selected_index
        self.item_list.pop(delete_index)

        # 删除界面中的项

        self.list_ctrl.DeleteItem(delete_index)

        # 删除以后进行序号重排
        for i in range(len(self.item_list)):
            if i < delete_index:
                continue

            # 从删除项以后的每一个项的序号都要 -1
            self.item_list[i]["no"] -= 1

            # 从删除项开始后面的每一个物品都重新加载
            self.list_load_item(self.item_list[i], i)

    def MovUpBtnOnClick(self, event):
        if self.first_selected_index == -1:
            return  # 如果没有选中

        if self.first_selected_index == 0:
            wx.MessageBox("选中素材已置顶。", "错误", style=wx.YES_DEFAULT | wx.ICON_QUESTION)
            return  # 如果是第一个物品

        self.item_swap(self.first_selected_index, self.first_selected_index - 1)

        self.list_ctrl.Select(self.first_selected_index, on=0)  # 取消原来的选中
        self.list_ctrl.Select(self.first_selected_index - 1)

    def MovDownBtnOnClick(self, event):
        if self.first_selected_index == -1:
            return  # 如果没有选中

        if self.first_selected_index == self.list_ctrl.GetItemCount() - 1:
            wx.MessageBox("选中素材在最末端。", "错误", style=wx.YES_DEFAULT | wx.ICON_QUESTION)
            return  # 如果是最后一个

        self.item_swap(self.first_selected_index, self.first_selected_index + 1)

        # 选中转移
        self.list_ctrl.Select(self.first_selected_index, on=0)  # 取消原来的选中
        self.list_ctrl.Select(self.first_selected_index + 1)

    def ExportBtnOnClick(self, event):
        # TODO: Implement ExportBtnOnClick
        # TODO: 加了码率设置的功能，别忘了测试

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

        # 导出路径不为空则更改工作路径
        if not export_path == '':
            os.chdir(export_path)

        # 导出命令
        console_command = 'ffmpeg '
        filter_complex_string = '-filter_complex '
        filter_complex_filters: list[str] = []
        concat_inputs: list[str] = []

        for item in self.item_list:
            no = item["no"]
            start_time = item["start_time"]
            end_time = item["end_time"]
            item_path = item["path"]

            # 防止一些奇怪的东西
            if start_time == '':
                start_time = "开头"
            if end_time == '':
                end_time = "结尾"

            # 开始、结束时间以及路径的命令行参数生成
            time_param = []
            if start_time != "开头":
                time_param.append(f'-ss {start_time}')
            if end_time != "结尾":
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

        # os.system(console_command)
        return

    def ProjectWebBtnOnClick(self, event):
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
        item_dict = {"no": item_no,
                     "filename": filename,
                     "start_time": "开头",
                     "end_time": "结尾",
                     "path": path
                     }

        # 加到物品表
        self.item_list.append(item_dict)

        # 显示数据在界面
        index = self.list_ctrl.InsertItem(item_dict["no"], item_dict["no"])
        self.list_load_item(item_dict, index)

        pass

    def append_files(self, filename, path):
        item_no = self.list_ctrl.GetItemCount()
        self.add_files(item_no, filename, path)

    def OnStartTimeCtrlText(self, event):
        first_selected_index = self.first_selected_index
        self.item_list[first_selected_index]["start_time"] = self.format_time(self.StartTimeCtrl.GetValue())

        self.list_load_item(self.item_list[first_selected_index], first_selected_index)

    def OnEndTimeCtrlText(self, event):
        first_selected_index = self.first_selected_index
        self.item_list[first_selected_index]["end_time"] = self.format_time(self.EndTimeCtrl.GetValue())

        self.list_load_item(self.item_list[first_selected_index], first_selected_index)

    def list_ctrl_on_selected(self, event):
        first_selected_index = self.list_ctrl.GetFirstSelected()
        self.first_selected_index = first_selected_index

        # 获取选中的物品时间，同步到输入框
        self.StartTimeCtrl.SetValue(self.item_list[first_selected_index]["start_time"])
        self.EndTimeCtrl.SetValue(self.item_list[first_selected_index]["end_time"])

        logging.debug(
            f"Selected Item Index: {self.first_selected_index}, \
                    Selected Item no: {self.item_list[self.first_selected_index]}")

    def item_swap(self, item1_index, item2_index):
        """
        交换物品函数。会交换物品在列表的序号，位置，并更新控件上的位置
        :param item1_index: 交换的物品 1
        :param item2_index: 交换的物品 2
        :return:
        """

        # 更新物品列表的序号
        temp = self.item_list[item1_index]["no"]
        self.item_list[item1_index]["no"] = self.item_list[item2_index]["no"]
        self.item_list[item2_index]["no"] = temp

        # 更新物品列表的位置
        temp = self.item_list[item1_index]
        self.item_list[item1_index] = self.item_list[item2_index]
        self.item_list[item2_index] = temp

        # 交换用户界面上的显示
        self.list_load_item(self.item_list[item1_index], self.item_list[item1_index]["no"])
        self.list_load_item(self.item_list[item2_index], self.item_list[item2_index]["no"])

    def list_load_item(self, load_item, list_ctrl_index):
        """
        把物品列表上的物品载入到用户界面的控件上
        :param load_item: 载入的物品
        :param list_ctrl_index: 载入在控件的行数
        :return: 无
        """
        self.list_ctrl.SetItem(list_ctrl_index, 0, str(load_item["no"]))
        self.list_ctrl.SetItem(list_ctrl_index, 1, load_item["filename"])
        self.list_ctrl.SetItem(list_ctrl_index, 2, load_item["start_time"])
        self.list_ctrl.SetItem(list_ctrl_index, 3, load_item["end_time"])
        self.list_ctrl.SetItem(list_ctrl_index, 4, load_item["path"])


if __name__ == '__main__':
    App = wx.App()
    mainFrame = SimpleCutPyMainFrame(None)
    mainFrame.Show(True)
    App.MainLoop()
