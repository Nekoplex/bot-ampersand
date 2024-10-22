from simpleeval import simple_eval
from vkbottle.bot import BotLabeler, Message

bl = BotLabeler()
bl.vbml_ignore_case = True


@bl.message(text=",калькулятор <expression>")
async def calculator_handler(_: Message, expression: str):
    try:
        result = simple_eval(expression)
    except Exception as err:
        return f"Ошибка расчёта, неверно введено выражение: {err}"
    return f"Результат: {result}"
