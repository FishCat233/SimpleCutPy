"""
数据模型
"""


class VideoModel:
    path: str
    filename: str
    _start_time: str = ''
    _end_time: str = ''

    def __init__(self, path: str, filename: str, start_time: str = '', end_time: str = ''):
        self.path = path
        self.filename = filename
        self.start_time = start_time
        self.end_time = end_time

    @property
    def start_time(self) -> str:
        return self._start_time

    @start_time.setter
    def start_time(self, time_string: str):
        self._start_time = VideoModel.format_time(time_string)

    @property
    def end_time(self) -> str:
        return self._end_time

    @end_time.setter
    def end_time(self, time_string: str):
        self._end_time = VideoModel.format_time(time_string)

    @staticmethod
    def format_time(time_string: str) -> str:
        # 一些提升体验的小更改
        # 除去两侧空格
        time_string = time_string.strip()

        # 将空格替换为 ":"
        # 将全角 “：” 替换为半角 “:”
        time_string = str.replace(time_string, " ", ":")
        time_string = str.replace(time_string, "：", ":")

        return time_string


class VideoSequenceModel:
    """
    视频序列模型
    """
    video_list: list[VideoModel]

    def __init__(self):
        self.video_list = []

    def __getitem__(self, item):
        return self.video_list[item]

    def __iter__(self):
        return iter(self.video_list)

    def __len__(self):
        return len(self.video_list)

    def pop_video(self, no: int):
        self.video_list.pop(no)

    def insert_video(self, video: VideoModel, no: int):
        self.video_list.insert(no, video)

    def append_video(self, video: VideoModel):
        self.video_list.append(video)

    def swap_item(self, no1: int, no2: int):
        self.video_list[no1], self.video_list[no2] = self.video_list[no2], self.video_list[no1]

    def clear_all(self):
        self.video_list = []
