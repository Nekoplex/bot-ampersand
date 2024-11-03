#custom imports
import random
import time
from datetime import datetime

from aiohttp.client_exceptions import ClientConnectorError
#logger imports, in code it's usage is marked as #logging levels set... 
import sys
from loguru import logger
#main imports
from vkbottle import API, EMPTY_KEYBOARD
from vkbottle.bot import Bot, Message
from vkbottle.dispatch.rules.base import CommandRule, FromUserRule
import asyncio
from config import CLUBPREF, TOKEN
from db import (
    create_tables,
    create_user,
    get_user,
    top_drink_users,
    update_drink_status
)
from keyboards import FORMAT_KBD, MAIN_KBD
from tools import labelers

bot = Bot(TOKEN)
bot.labeler.vbml_ignore_case = True
bot.labeler.auto_rules = [FromUserRule()]


async def handle_drink_command(user_id: int) -> str:
    """
    Handles "пить" command.
    """
    current_date = int(time.time())
    user = await get_user(user_id)

    drink: int = random.randint(200, 2000)
    total_drink = drink
    if user:
        if datetime.fromtimestamp(user[2]).date() == datetime.now().date():
            return "Вы уже использовали команду 'пить' сегодня."

        await update_drink_status(user_id, drink, current_date)
        total_drink += user[1]
    else:
        await create_user(user_id, drink, current_date)

    return f"Вы выпили {drink} мл спермы. Всего вы выпили : {total_drink} мл спермы."


async def handle_count_command(user_id: int) -> str:
    """
    Handles "размер моя кружка" command.
    """
    user = await get_user(user_id)
    if not user:
        return "Вы еще не использовали команду 'пить'."

    return f"Всего вы выпили: {user[1]} мл."


async def handle_top_command(api: API) -> str:
    """
    Handles "пить топ" command.
    """

    # Sort users by their ml in descending order
    top_users = await top_drink_users()
    top_users = top_users[:10]

    # Getting users' full names
    user_ids = [user[0] for user in top_users]
    user_names = await api.users.get(user_ids=user_ids)

    # Creating response
    response = "общий топ пользователей:\n"
    for i, user in enumerate(top_users, 1):
        user_name = f"[id{user[0]}|{user_names[i - 1].first_name} {user_names[i - 1].last_name}]"
        response += f"{i}. {user_name}: {user[1]} мл\n"

    return response


#
# Main bot handlers
#


@bot.on.message(text=(",клава", f"{CLUBPREF} клава"))
async def kbd_handler(message: Message):
    await message.answer("клава успешно подключена", keyboard=MAIN_KBD)


@bot.on.message(text=(",убрать клаву", f"{CLUBPREF} убрать клаву"))
@bot.on.message(payload={"cmd": "remove_kbd"})
async def remove_kbd_handler(message: Message):
    await message.answer("клава была успешно отключена", keyboard=EMPTY_KEYBOARD)


@bot.on.message(text=(",пить", f"{CLUBPREF} пить"))
@bot.on.message(payload={"cmd": "drink"})
async def drink_handler(message: Message):
    if message.from_id < 1:
        # Bots not allowed!
        return

    response = await handle_drink_command(message.from_id)
    await message.answer(response)
    await message.answer(sticker_id=58258)


@bot.on.message(CommandRule("пить кружка", [","], 0))
async def drink_count_handler(message: Message):
    response = await handle_count_command(message.from_id)
    await message.answer(response)


@bot.on.message(CommandRule("пить топ", [",", f"{CLUBPREF} "], 0))
@bot.on.message(payload={"cmd": "drink_top"})
async def top_handler(message: Message):
    response = await handle_top_command(message.ctx_api)
    await message.answer(response, disable_mentions=True)
    await message.answer(sticker_id=65653)
#TODO : DELETE STICKERS

@bot.on.message(CommandRule("пить инфо", [","], 0))
@bot.on.message(payload={"cmd": "drink_info"})
async def kok_info_handler(_: Message):
    return (
        "Модуль пить в боте ampersand"
        "\nver.1.0.0, stable"
        "\nDerfikop❤️,"
        "\nF1zzTao❤️"
        "\nampersand gang 4ever🔫"
    )


@bot.on.message(CommandRule("помощь пить", [","], 0))
@bot.on.message(payload={"cmd": "drink_help"})
async def kok_help_handler(_: Message):
    return "команды модуля пить:\nпить, пить инфо,\nпить топ, пить кружка"


@bot.on.message(text=(",юникс тайм", f"{CLUBPREF} юникс тайм"))
@bot.on.message(payload={"cmd": "unix_time"})
async def unix_time_handler(message: Message):
    await message.answer("Какой вид юникс тайма вы хотите вывести?", keyboard=FORMAT_KBD)


@bot.on.message(text=(f"{CLUBPREF} Отформатированный"))
@bot.on.message(payload={"cmd": "unix_time_formatted"})
async def time_format_handler(message: Message):
    f_time = time.strftime("%X %x %Z")
    await message.answer(f"Текущее отформатированное юникс время :\n{f_time}")
    await message.answer(sticker_id=3130)


@bot.on.message(text=(f"{CLUBPREF} Не форматированный"))
@bot.on.message(payload={"cmd": "unix_time_unformatted"})
async def time_nonformat_handler(message: Message):
    nf_time = str(int(time.time()))
    await message.answer(f"Текущее неоотформатированное юникс время : {nf_time}")
    # Sticker below is not available (error 100) - its cuz you don't have stickerpack
    # await message.answer(sticker_id=3130)


@bot.on.message(CommandRule("помощь другое", [","], 0))
async def help_misc_handler(_: Message):
    return (
        "АКА модуль мультутул,"
        "\nперечень команд модуля 'другое':"
        "\n•юникс тайм"
        "\n•клава"
        "\n•калькулятор 🤔"
    )


@bot.on.message(CommandRule("помощь мультитул", [","], 0))
async def help_multitool_handler(_: Message):
    return (
        "модуль мультутул,"
        "\nперечень команд модуля 'мультитул':"
        "\n•юникс тайм"
        "\n•клава"
        "\n•калькулятор 🤔"
    )


@bot.on.message(text=(",помощь", f"{CLUBPREF} помощь"))
async def help_handler(_: Message):
    return (
        "помощь бота амперсанд[&]"
        "\nпиши ,помощь <имя_модуля> чтобы узнать о модуле подробнее!"
        "\nдоступные модули:"
        "\n•пить"
        "\n•другое(мультитул)"
    )


@bot.error_handler.register_error_handler(ClientConnectorError)
async def no_internet_error_handler(e: ClientConnectorError):
    """
    No internet handler.
    The entire bot waits 15 seconds if there's no internet.
    """
    logger.warning(f"No internet connection: {e}")
    time.sleep(15)  
    # ^^^^ 
    #blocking non-async function, 
    #if it's async, then it'll spam in console


if __name__ == "__main__":
    bot.loop_wrapper.on_startup.append(create_tables())

    for custom_labeler in labelers:
        bot.labeler.load(custom_labeler)
    
    #logging levels set, to keep console clean
    logger.remove()
    logger.add(sys.stderr, level="INFO")
    
    #starting bot
    logger.info("Starting bot ampersand")
    bot.run_forever()
