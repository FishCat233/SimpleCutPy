import logging
import subprocess
from pymediainfo import MediaInfo

from tools.path import PathHelper

from .model import (
    ExportConfig,
    ExportTask,
    MbpsConfig,
    MultiTrackMode,
    VideoFile,
    X264Config,
)
from .filter_builder import FilterBuilder


def export(task: ExportTask) -> bool:
    """导出视频切片

    Args:
        task (ExportTask): 导出任务

    Returns:
        bool: 导出是否成功
    """

    ffmpeg_path = PathHelper.get_ffmpeg_path()

    # 构建命令
    command = build_command_header(ffmpeg_path)

    for video_file in task.video_sequence.get_video_list():
        command += build_video_input(video_file)

    try:
        filter_complex = build_filter_complex(
            task.video_sequence.get_video_list(),
            task.export_config.multi_track_mode,
        )
    except Exception as e:
        logging.error("build filter complex error: {:?}", e)
        return False

    command += filter_complex

    command += build_command_tail(task.get_export_full_path(), task.export_config)

    logging.info("导出命令: %s", command)

    # 执行命令
    try:
        subprocess.run(
            command, shell=False, check=True, creationflags=subprocess.CREATE_NO_WINDOW
        )
        logging.info("export one success")
        return True
    except subprocess.CalledProcessError as e:
        logging.error("export one failed with error: {:?}", e)
        return False


def build_command_header(ffmpeg_path: str) -> str:
    """构建ffmpeg命令头

    Args:
        ffmpeg_path (str): ffmpeg可执行文件路径

    Returns:
        str: 构建后的ffmpeg命令头字符串
    """
    return ffmpeg_path + " -y"


def build_command_header_without_executeable() -> str:
    """构建不带执行文件路径的ffmpeg命令头

    Returns:
        str: 构建后的不带执行文件路径的ffmpeg命令头字符串
    """
    return " -y"


def build_video_input(video_file: VideoFile) -> str:
    """构建视频输入参数

    Args:
        video_file (VideoFile): 视频文件信息

    Returns:
        str: 构建后的视频输入参数字符串
    """

    start_time_string = (
        "" if video_file.start_time == "开始" else f" -ss {video_file.start_time}"
    )
    end_time_string = (
        "" if video_file.end_time == "结束" else f" -to {video_file.end_time}"
    )

    ret = f"{start_time_string}{end_time_string} -i {video_file.get_full_file_path()}"

    return ret


def build_filter_complex(
    video_files: list[VideoFile], audio_merge_type: MultiTrackMode
) -> str:
    """构建滤镜复杂链

    Args:
        video_files (list[VideoFile]): 视频文件列表
        audio_merge_type (MultiTrackMode): 音频合并类型

    Returns:
        str: 构建后的滤镜复杂链字符串
    """

    if not video_files:
        return ""

    concat_inputs = []
    filter_builder = FilterBuilder()

    for i, v in enumerate(video_files):
        concat_inputs.append(f"{i}:v")

        multi_track_mode = get_audio_track_count(v.get_full_file_path())
        if multi_track_mode > 1 and audio_merge_type == "amix":
            # 多音轨且需要合并
            output_alias = f"{i}a"  # 为每个音频流创建唯一别名

            # 添加合并amix滤镜
            filter_builder.add_merge_amix_filter(i, multi_track_mode, output_alias)

            concat_inputs.append(output_alias)
        else:
            # 单音轨或不需要合并
            concat_inputs.append(f"{i}:a")

    # 在所有文件处理完毕后添加concat滤镜
    filter_builder.add_concat_filter(concat_inputs, "v", "a")

    filter_complex = filter_builder.build_to_string()

    if filter_complex:
        filter_complex += " -map [v] -map [a]"

    return filter_complex


def build_command_tail(output_path: str, config: ExportConfig) -> str:
    """构建命令尾

    Args:
        output_path (str): 导出路径
        config (ExportConfig): 导出配置

    Returns:
        str: 构建后的命令尾字符串
    """

    match config.size_control:
        case X264Config():
            return f' -c:v libx264 -crf 23.5 -preset veryslow -keyint_min 600 -g 600 -refs 4 -bf 3 -me_method umh -sc_threshold 60 -b_strategy 1 -qcomp 0.5 -psy-rd 0.3:0 -aq-mode 2 -aq-strength 0.8 -c:a aac -b:a 128k -movflags faststart "{output_path}"'
        case MbpsConfig():
            return f' -b:v {config.size_control.mbps}M "{output_path}"'
        case _:
            return f' "{output_path}"'


# 工具函数
def get_audio_track_count(file_path: str) -> int:
    """MediaInfo 获取音频轨道数量

    Args:
        file_path (str): 视频文件路径

    Returns:
        int: 音频轨道数量
    """

    media_info = MediaInfo.parse(file_path)
    return len(media_info.audio_tracks)
