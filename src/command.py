"""
命令生成
"""


def concat_filter(input: list[str], output_video_name: str, output_audio_name: str, v: int = 1, a: int = 1) -> str:
    inputs = []
    input_num = len(input) // 2

    for i in input:
        inputs.append(f'[{i}]')

    inputs = ' '.join(inputs)

    return f'{inputs} concat=n={input_num}:v={v}:a={a} [{output_video_name}] [{output_audio_name}]'


def amix_filter(input: list[str], output: str) -> str:
    """
    amix 滤镜。可以合并多个音轨
    :param input: 要合并的多个音频流
    :param output: 输出的音频流名称
    :return:
    """
    inputs = []
    input_number = len(input)
    for i in input:
        inputs.append(f'[{i}]')
    inputs = ' '.join(inputs)

    return f'{inputs} amix=inputs={input_number}[{output}]'


def merge_filestream_audio_channel(input: str, audio_channel_number: int, output_audio_name: str) -> str:
    """
    混合文件的多轨道
    :param input: 文件流
    :param audio_channel_number: 音频流数量
    :param output_audio_name: 输出音频流名称
    :return:
    """
    inputs = []
    for i in range(audio_channel_number):
        inputs.append(f'{input}:a:{i}')

    return amix_filter(inputs, output_audio_name)
