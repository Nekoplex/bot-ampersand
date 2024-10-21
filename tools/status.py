from vkbottle.bot import BotLabeler, Message
import subprocess
import asyncio
from ping3 import ping
import msgspec
bl=BotLabeler()

def get_battery_status() -> dict | str:
    try:
        battery_info_raw = subprocess.check_output("termux-battery-status", shell=True).decode("utf-8")
    except subprocess.CalledProcessError as e:
        return e
    battery_info = msgspec.json.decode(battery_info_raw)
    return battery_info

async def vk_ping():
    ping1 = ping('google.ru', unit="ms")
    return ping1

def get_python_status() -> dict | str:
    battery_info_raw = subprocess.check_output("python --version", shell=True).decode("utf-8")
    return battery_info_raw

@bl.message(text=",статус")
async def handle_status(message: Message):
    zaryad = get_battery_status()
    procenti = zaryad["percentage"]
    python_ver = get_python_status()
    avg_ping = await vk_ping()
    await message.answer(f"Заряд: {procenti}% \nВерсия ЯП:{python_ver}пинг к google.ru: {avg_ping:.2f} мс")


