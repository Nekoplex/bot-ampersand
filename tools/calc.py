import math
from vkbottle.bot import BotLabeler, Message
from simpleeval import simple_eval
bl=BotLabeler()
bl.vbml_ignore_case = True
@bl.message(text=",калькулятор <expression>")
async def calculator_handler(message: Message, expression: str):
    try:
        result = simple_eval(expression)
        await message.answer(f"Результат: {result}")
    except Exception as err:
        await message.answer(f"Ошибка расчёта, неверно введено выражение: {err}")

