"""
命令生成
"""


def concat_filter(
    input: list[str],
    output_video_name: str,
    output_audio_name: str,
    v: int = 1,
    a: int = 1,
) -> str:
    """
    拼接滤镜。可以拼接多个视频流和音频流。

    Args:
        input ([str]): 输入的视频流和音频流
        output_video_name (str): 输出的视频流名称
        output_audio_name (str): 输出的音频流名称
        v (int, optional): 是否拼接视频流。Defaults to 1.
        a (int, optional): 是否拼接音频流。Defaults to 1.

    Returns:
        str: 生成的指令
    """
    inputs = []
    input_num = len(input) // 2

    for i in input:
        inputs.append(f"[{i}]")

    inputs = " ".join(inputs)

    return f"{inputs} concat=n={input_num}:v={v}:a={a} [{output_video_name}] [{output_audio_name}]"


def amix_filter(input: list[str], output: str) -> str:
    """
    amix 滤镜。可以合并多个音轨

    Args:
        input (list[str]): 要合并的多个音频流
        output (str): 输出的音频流名称

    Returns:
        str: amix 滤镜命令
    """
    inputs = []
    input_number = len(input)
    for i in input:
        inputs.append(f"[{i}]")
    inputs = " ".join(inputs)

    return f"{inputs} amix=inputs={input_number}[{output}]"


def merge_filestream_audio_channel(
    input: str, audio_channel_number: int, output_audio_name: str
) -> str:
    """
    混合文件的多轨道
    Args:
        input (str): 文件流
        audio_channel_number (int): 音频流数量
        output_audio_name (str): 输出音频流名称

    Returns:
        str: 生成的指令
    """
    inputs = []
    for i in range(audio_channel_number):
        inputs.append(f"{input}:a:{i}")

    return amix_filter(inputs, output_audio_name)
