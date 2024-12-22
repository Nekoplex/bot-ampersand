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

from config import CLUBPREF, TOKEN
from db import (
    create_tables,
    create_user,
    get_user,
    top_sailed_users,
    update_sailed_status
)
from keyboards import FORMAT_KBD, MAIN_KBD
from tools import labelers

bot = Bot(TOKEN)
bot.labeler.vbml_ignore_case = True
bot.labeler.auto_rules = [FromUserRule()]


async def handle_sailed_command(user_id: int) -> str:
    """
    Handles "плыть" command.
    """
    current_date = int(time.time())
    user = await get_user(user_id)
    chance_seed = 0.3
    chance_seed2 = 0.5
    chance_throw = float("%.2f" % random.random())
    if chance_throw <= chance_seed:
        print(chance_throw)
        sailed: int = random.randint(70, 130)
        throw_message = "С шансом в 30% вы проплыли больше."
    elif chance_throw >= chance_seed and chance_throw <= chance_seed2:
        print(chance_throw)
        sailed: int = random.randint(1, 49)
        throw_message = "С шансом в 20% вы проплыли меньше."
    elif chance_throw > chance_seed2:
        print(chance_throw)
        sailed: int = random.randint(50, 70)
        throw_message = "С шансом в 50% вы проплыли нормальное расстояние."
    total_sailed = sailed
    if user:
        if datetime.fromtimestamp(user[2]).date() == datetime.now().date():
            return "Вы уже использовали команду 'плыть' сегодня."

        await update_sailed_status(user_id, sailed, current_date)
        total_sailed += user[1]
    else:
        await create_user(user_id, sailed, current_date)

    return f"Вы проплыли {sailed} сантиметров.{throw_message} Всего вы проплыли : {total_sailed} см."


async def handle_count_command(user_id: int) -> str:
    """
    Handles ",плыть статы" command.
    """
    user = await get_user(user_id)
    if not user:
        return "Вы еще ни разу не плыли."

    return f"Всего вы проплыли: {user[1]} см."


async def handle_top_command(api: API) -> str:
    """
    Handles "плыть топ" command.
    """

    # Sort users by their ml in descending order
    top_users = await top_sailed_users()
    top_users = top_users[:10]

    # Getting users' full names
    user_ids = [user[0] for user in top_users]
    user_names = await api.users.get(user_ids=user_ids)

    # Creating response
    response = "общий топ регаты:\n"
    for i, user in enumerate(top_users, 1):
        user_name = f"[id{user[0]}|{user_names[i - 1].first_name} {user_names[i - 1].last_name}]"
        response += f"{i}. {user_name}: {user[1]} см\n"

    return response


#
# Main bot handlers
#


@bot.on.message(CommandRule("клава", [",", f"{CLUBPREF} "], 0))
async def kbd_handler(message: Message):
    await message.answer("клава успешно подключена", keyboard=MAIN_KBD)


@bot.on.message(CommandRule(",убрать клаву", [",", f"{CLUBPREF} "], 0))
@bot.on.message(payload={"cmd": "remove_kbd"})
async def remove_kbd_handler(message: Message):
    await message.answer("клава была успешно отключена", keyboard=EMPTY_KEYBOARD)


@bot.on.message(CommandRule(",плыть", [",", f"{CLUBPREF} "], 0))
@bot.on.message(payload={"cmd": "sailed"})
async def sailed_handler(message: Message):
    if message.from_id < 1:
        # Bots not allowed!
        return

    response = await handle_sailed_command(message.from_id)
    await message.answer(response)


@bot.on.message(CommandRule("плыть статы", [",", f"{CLUBPREF} "], 0))
async def sailed_count_handler(message: Message):
    response = await handle_count_command(message.from_id)
    await message.answer(response)


@bot.on.message(CommandRule("топ регаты", [",", f"{CLUBPREF} "], 0))
@bot.on.message(payload={"cmd": "sailed_top"})
async def top_handler(message: Message):
    response = await handle_top_command(message.ctx_api)
    await message.answer(response, disable_mentions=True)

@bot.on.message(CommandRule("плыть инфо", [",", f"{CLUBPREF} "], 0))
@bot.on.message(payload={"cmd": "sailed_info"})
async def kok_info_handler(_: Message):
    return (
        "Модуль плыть в боте ampersand"
        "\nver.1.0.3, UNstable"
        "\nrecreated from drink sim!!"
        "\nDerfikop❤️Rip(((,"
        "\n@F1zzTao❤️Alive :)"
        "\n&[?]"
    )


@bot.on.message(CommandRule("помощь плыть", [",", f"{CLUBPREF} "], 0))
@bot.on.message(payload={"cmd": "sailed_help"})
async def kok_help_handler(_: Message):
    return "команды модуля плыть:\nплыть, плыть инфо,\nтоп регаты, плыть статы"


@bot.on.message(CommandRule("юникс тайм", [",", f"{CLUBPREF} "], 0))
@bot.on.message(payload={"cmd": "unix_time"})
async def unix_time_handler(message: Message):
    await message.answer("Какой вид юникс тайма вы хотите вывести?", keyboard=FORMAT_KBD)


@bot.on.message(text=(f"{CLUBPREF} Отформаченный"))
@bot.on.message(payload={"cmd": "unix_time_formatted"})
async def time_format_handler(message: Message):
    f_time = time.strftime("%X %x %Z")
    await message.answer(f"Текущее отформатированное юникс время :\n{f_time}")


@bot.on.message(text=(f"{CLUBPREF} Не формаченный"))
@bot.on.message(payload={"cmd": "unix_time_unformatted"})
async def time_nonformat_handler(message: Message):
    nf_time = str(int(time.time()))
    await message.answer(f"Текущее неоотформаченное юникс время : {nf_time}")
    


@bot.on.message(CommandRule("помощь другое", [","], 0))
async def help_misc_handler(_: Message):
    return (
        "АКА модуль мультутул,"
        "\nсписок команд модуля 'другое':"
        "\n•юникс тайм"
        "\n•клава"
        "\n•калькулятор 🤔"
    )


@bot.on.message(CommandRule("помощь инструменты", [","], 0))
async def help_multitool_handler(_: Message):
    return (
        "модуль мультутул,"
        "\nперечень команд модуля 'инструменты':"
        "\n•юникс тайм"
        "\n•клава"
        "\n•калькулятор(говно)"
    )


@bot.on.message(text=(",помощь", f"{CLUBPREF} помощь"))
async def help_handler(_: Message):
    return (
        "помощь амперсанда[&]"
        "\nпиши ,помощь [имя_модуля] чтобы узнать о модуле всё!"
        "\nдоступные модули:"
        "\n•плыть - МОДУЛЬ НЕСТАБИЛЕН"
        "\n•другое(инструменты)"
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
    logger.info("Starting [&] bot")
    bot.run_forever()
