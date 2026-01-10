"""
滤镜构建器

用于构建复杂的滤镜字符串
"""


class FilterBuilder:
    """
    滤镜构建器类，用于构建复杂的滤镜字符串
    """

    def __init__(self):
        """
        创建一个新的滤镜构建器实例
        """
        self.filters = []

    def filter_count(self) -> int:
        """
        获取滤镜数量

        Returns:
            int: 滤镜数量
        """
        return len(self.filters)

    def is_empty(self) -> bool:
        """
        检查是否有滤镜

        Returns:
            bool: 如果没有滤镜返回True，否则返回False
        """
        return len(self.filters) == 0

    def build_to_string(self) -> str:
        """
        构建滤镜字符串

        Returns:
            str: 包含所有滤镜的命令行片段。如果没有滤镜，返回空字符串
        """
        if self.is_empty():
            return ""
        else:
            return f' -filter_complex "{";".join(self.filters)}"'

    def add_merge_amix_filter(
        self, input_index: int, track_count: int, output_alias: str
    ):
        """
        添加合并amix滤镜

        Args:
            input_index (int): 输入索引，对应视频切片的索引
            track_count (int): 音频轨道数量
            output_alias (str): 输出别名，用于引用合并后的音频流
        """
        self.filters.append(build_amix_filter(input_index, track_count, output_alias))

    def add_concat_filter(
        self, inputs: list[str], video_output: str, audio_output: str
    ):
        """
        添加concat滤镜

        Args:
            inputs (list[str]): 输入流列表，包含视频和音频流的索引
            video_output (str): 视频输出别名，用于引用拼接后的视频流
            audio_output (str): 音频输出别名，用于引用拼接后的音频流
        """
        self.filters.append(build_concat_filter(inputs, video_output, audio_output))


def build_amix_filter(input_index: int, track_count: int, output_alias: str) -> str:
    """
    构建amix音频合并滤镜

    Args:
        input_index (int): 输入索引，对应视频切片的索引
        track_count (int): 音频轨道数量
        output_alias (str): 输出别名，用于引用合并后的音频流

    Returns:
        str: 包含amix滤镜的命令行片段
    """
    inputs = []
    for i in range(track_count):
        inputs.append(f"[{input_index}:a:{i}]")

    return f"{' '.join(inputs)} amix=inputs={track_count}[{output_alias}]"


def build_concat_filter(inputs: list[str], video_output: str, audio_output: str) -> str:
    """
    构建concat拼接滤镜

    Args:
        inputs (list[str]): 输入流列表，包含视频和音频流的索引
        video_output (str): 视频输出别名，用于引用拼接后的视频流
        audio_output (str): 音频输出别名，用于引用拼接后的音频流

    Returns:
        str: 包含concat滤镜的命令行片段
    """
    input_count = len(inputs) // 2
    inputs_str = " ".join(f"[{s}]" for s in inputs)

    return (
        f"{inputs_str} concat=n={input_count}:v=1:a=1 [{video_output}] [{audio_output}]"
    )
