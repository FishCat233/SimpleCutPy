from dataclasses import dataclass
import logging
import requests

import meta

CHECK_URL = "https://api.github.com/repos/FishCat233/SimpleCutPy/releases/latest"


@dataclass
class UpdateInfo:
    """更新信息"""

    has_new_version: bool
    current_version: str
    latest_version: str
    release_url: str


def check_update() -> UpdateInfo:
    """检查更新

    Returns:
        UpdateInfo: 更新信息

    Raises:
        Exception: 反正会发出异常就对了
    """
    response = requests.get(CHECK_URL, timeout=10)
    response.raise_for_status()
    json_data = response.json()

    logging.debug(
        f"检查更新，当前版本：{meta.VERSION}，最新版本：{json_data['tag_name']}"
    )

    update_info = UpdateInfo(
        has_new_version=is_new_version(meta.VERSION, json_data["tag_name"]),
        current_version=meta.VERSION,
        latest_version=json_data["tag_name"],
        release_url=json_data["html_url"],
    )

    logging.debug(f"检查更新: {update_info}")

    return update_info


def is_new_version(current_version: str, latest_version: str) -> bool:
    """判断是否有新版本

    Args:
        current_version (str): 当前版本号
        latest_version (str): 最新版本号

    Returns:
        bool: 是否有新版本
    """
    current_version_numbers, current_build = resolve_version(current_version)
    latest_version_numbers, latest_build = resolve_version(latest_version)

    for current, latest in zip(current_version_numbers, latest_version_numbers):
        if latest > current:
            return True
        elif latest < current:
            return False

    return latest_build > current_build


def resolve_version(version: str) -> tuple[list[int], int]:
    """解析版本号

    Args:
        version (str): 版本号字符串，例如 "v1.2.3-0000" 或 "1.2.3"

    Returns:
        tuple[list[int], int]: 版本号的整数列表和构建号，例如 ([1, 2, 3], 0) 或 ([1, 2, 3], -1)
    """
    version = version.lstrip("v")

    # 安全地分割版本号和构建号
    if "-" in version:
        version_part, build_part = version.split("-", 1)  # 只分割一次
        build_number = int(build_part) if build_part.isdigit() else -1
    else:
        version_part = version
        build_number = -1

    # 安全地分割版本号部分
    try:
        version_numbers = [int(part) for part in version_part.split(".")]
    except ValueError:
        # 如果版本号部分包含非数字，返回默认值
        version_numbers = [0]

    return version_numbers, build_number
