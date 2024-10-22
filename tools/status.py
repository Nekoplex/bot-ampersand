import subprocess
import sys
import time

import msgspec
from vkbottle import API
from vkbottle.bot import BotLabeler, Message

bl = BotLabeler()


async def get_vk_time_diff(api: API) -> float:
    """
    Gets difference between VK time and local time.
    >>> get_vk_time_diff()
    >>> 314.15
    """
    server_time = await api.utils.get_server_time()
    current_time = time.time()
    ping_s = abs(current_time-server_time)
    ping_ms = round(ping_s*1000, 2)
    return ping_ms


def get_python_ver() -> str:
    """
    Returns Python version.
    >>> get_python_ver()
    >>> 'Python 3.11.9'
    """
    python_version = sys.version_info
    major = python_version.major
    minor = python_version.minor
    micro = python_version.micro
    return f"Python {major}.{minor}.{micro}"


def get_battery_status() -> dict | str | None:
    """
    Returns phone's battery status if the program is running on Android.
    >>> get_battery_status()
    >>> {'health': 'GOOD', 'percentage': 86, ...}
    """
    if not hasattr(sys, 'getandroidapilevel'):
        return None

    try:
        battery_info_raw = subprocess.check_output(
            "termux-battery-status", shell=True
        ).decode("utf-8")
    except subprocess.CalledProcessError as e:
        return e

    battery_info = msgspec.json.decode(battery_info_raw)
    return battery_info


@bl.message(text=",статус")
async def status_handler(message: Message):
    ping_ms = await get_vk_time_diff(message.ctx_api)
    python_ver = get_python_ver()

    msg = (
        f"Версия ЯП: {python_ver}"
        f"\nПинг: {ping_ms}"
    )

    battery_stats = get_battery_status()
    if not battery_stats:
        return msg

    if isinstance(battery_stats, str):
        msg = f"Не удалось получить заряд батери телефона: {battery_stats}\n" + msg
    else:
        percentage = battery_stats["percentage"]
        msg = f"Заряд: {percentage}%\n" + msg

    return msg
