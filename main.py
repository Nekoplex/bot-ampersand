import sqlite3
import random
import time
from datetime import datetime, timedelta
from vkbottle.bot import Bot, Message
from aiohttp.client_exceptions import ClientConnectorError
from loguru import logger
import asyncio
from vkbottle.dispatch.rules.base import FromUserRule
from vkbottle.dispatch.rules.base import CommandRule
from vkbottle import (Keyboard,
                      KeyboardButtonColor,
                      Text,
                      EMPTY_KEYBOARD)
from config import TOKEN
from tools import labelers
bot = Bot(TOKEN)
bot.labeler.vbml_ignore_case = True
bot.labeler.auto_rules = [FromUserRule()]
clubpref="[club224599461|@ampersand_bot]"
for custom_labeler in labelers:
    bot.labeler.load(custom_labeler)
import tools
# Создаем базу данных
conn = sqlite3.connect('database.db')
c = conn.cursor()
c.execute('''
    CREATE TABLE IF NOT EXISTS users
    (id INTEGER PRIMARY KEY,
    drink INTEGER,
    last_request_date INTEGER)
''')
conn.commit()

# Клавиатура
@bot.on.message(text=(",клава","[club224599461|@ampersand_bot] клава"))
async def handle_keyboard(message: Message):
    keyboard = Keyboard()
    keyboard.add(Text("пить"), color=KeyboardButtonColor.NEGATIVE)
    keyboard.add(Text("пить топ"), color=KeyboardButtonColor.NEGATIVE)
    keyboard.add(Text("юникс тайм"), color=KeyboardButtonColor.NEGATIVE)
    keyboard.row()
    keyboard.add(Text("помощь"), color=KeyboardButtonColor.NEGATIVE)
    keyboard.row()
    keyboard.add(Text("убрать клаву"), color=KeyboardButtonColor.POSITIVE)


    await message.answer("клава успешно подключена", keyboard=keyboard)
    
    
@bot.on.message(text=(",убрать клаву","[club224599461|@ampersand_bot] убрать клаву"))
async def remove_keys(message: Message):
    await message.answer("клава была успешно отключена", keyboard=EMPTY_KEYBOARD)


# Функция для обработки команды "пить".
async def handle_drink_command(user_id):
    current_date = int(time.time())
    res = c.execute("SELECT * FROM users WHERE id = ?", (user_id,)) 
    user = res.fetchone()
    
    drink = random.randint(200, 2000)
    total_drink = drink
    if user:
        if datetime.fromtimestamp (user[2]).date() == datetime.now().date():
            return "Вы уже использовали команду 'пить' сегодня."
        c.execute("UPDATE users SET drink = drink + ?, last_request_date = ? WHERE id = ?",
                  (drink, current_date, user_id)
        )
        total_drink += user[1]
    else:
        c.execute(
            "INSERT INTO users (id, drink, last_request_date) VALUES (?, ?, ?)", 
            (user_id, drink, current_date)
        )

    conn.commit()

    return f"Вы выпили {drink} мл спермы. Всего вы выпили : {total_drink} мл спермы."

# Функция для обработки команды "размер моя кружка"
async def handle_count_command(user_id):
    c.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    user = c.fetchone()
    if not user:
        return "Вы еще не использовали команду 'пить'."

    return f"Всего вы выпили: {user[1]} мл."


# Функция для обработки команды "пить топ"
async def handle_top_command(bot):
    # Сортируем пользователей по размеру их "мл" в порядке убывания
    c.execute("SELECT * FROM users ORDER BY drink DESC")
    top_users = c.fetchall()
    top_users = top_users[:10]
    # Получаем имена пользователей
    user_ids = [user[0] for user in top_users]
    user_names = await bot.api.users.get(user_ids=user_ids)
    # Формируем ответ
    response = "общий топ пользователей:\n"
    for i, user in enumerate(top_users, start=1):
        user_name = f'[id{user[0]}|{user_names[i - 1].first_name} {user_names[i - 1].last_name}]'
        response += f"{i}. {user_name}: {user[1]} мл\n"

    return response


# Основная функция бота


@bot.error_handler.register_error_handler(ClientConnectorError)
async def no_internet_error_handler(e: ClientConnectorError):
    logger.warning(f"No internet connection: {e}")
    time.sleep(15)


@bot.on.message(text=(",пить","[club224599461|@ampersand_bot] пить"))
async def drink_handler(message: Message):
    if message.from_id > 0:
        response = await handle_drink_command(message.from_id)
        await message.answer(response)
        await message.answer(sticker_id=58258)


@bot.on.message(CommandRule("пить кружка", [","], 0))
async def drink_count_handler(message: Message):
    response = await handle_count_command(message.from_id)
    await message.answer(response)


@bot.on.message(CommandRule("пить топ",  [",",f"{clubpref} "], 0))
async def top_handler(message: Message):
    response = await handle_top_command(bot)
    await message.answer(response, disable_mentions=True)
    await message.answer(sticker_id=58261)

# Обрабатываем кок инфо
@bot.on.message(CommandRule("пить инфо", [","], 0))
async def kok_info_handler(message: Message):
    return "Модуль пить в боте ampersand\nver.1.0.0,stable \nDerfikop❤️,\nF1zzTao❤️\nampersand gang 4ever🔫"


@bot.on.message(CommandRule("помощь пить", [","], 0))
async def kok_help_handler(message: Message):
    return 'команды модуля пить:\nпить, пить инфо,\nпить топ, пить кружка'

@bot.on.message(text=(",юникс тайм","[club224599461|@ampersand_bot] юникс тайм"))
async def time_handler(message: Message):
    keyboard = (
    Keyboard(inline=True)
    .add(Text("Отформатированный"), color=KeyboardButtonColor.NEGATIVE)
    .row()
    .add(Text("Не форматированный"), color=KeyboardButtonColor.POSITIVE)
    )
    await message.answer("Какой вид юникс тайма вы хотите вывести?", keyboard = keyboard)

@bot.on.message(text=(f"{clubpref} Не форматированный"))
async def time_nonformat(message: Message):
    nf_time=(str(int(time.time())))
    await message.answer(f"Текущее неоотформатированное юникс время : {nf_time}")
    await message.answer(sticker_id=3130)


@bot.on.message(text=(f"{clubpref} Отформатированный"))
async def time_format(message: Message):
    f_time=(time.strftime('%X %x %Z'))
    await message.answer(f"Текущее отформатированное юникс время :\n{f_time}")
    await message.answer(sticker_id=3130)


@bot.on.message(CommandRule("помощь другое", [","], 0))
async def misc_handler(message: Message):
    return "АКА модуль мультутул,\nперечень команд модуля 'другое':\n•юникс тайм\n•клава\n•калькулятор 🤔"

@bot.on.message(CommandRule("помощь мультитул", [","], 0))
async def misc_handler(message: Message):
    return "модуль мультутул,\nперечень команд модуля 'мультитул':\n•юникс тайм\n•клава\n•калькулятор 🤔"


@bot.on.message(text=(",помощь","[club224599461|@ampersand_bot] помощь"))
async def help_handler(message: Message):
    return 'помощь бота амперсанд[&]\nпиши ,помощь <имя_модуля> чтобы узнать о модуле подробнее! \n доступные модули: \n•пить\n•другое(мультитул)'
if __name__ == "__main__":
   bot.run_forever()
