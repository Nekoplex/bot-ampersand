from vkbottle import Keyboard
from vkbottle import KeyboardButtonColor as Color
from vkbottle import Text

MAIN_KBD = (
    Keyboard()
    .add(Text("пить", payload={"cmd": "drink"}), color=Color.NEGATIVE)
    .add(Text("пить топ", payload={"cmd": "drink_top"}), color=Color.NEGATIVE)
    .add(Text("юникс тайм", payload={"cmd": "unix_time"}), color=Color.NEGATIVE)
    .row()
    .add(Text("помощь", payload={"cmd": "drink_help"}), color=Color.NEGATIVE)
    .row()
    .add(Text("убрать клаву", payload={"cmd": "remove_kbd"}), color=Color.POSITIVE)
).get_json()

FORMAT_KBD = (
    Keyboard(inline=True)
    .add(Text("Отформатированный", payload={"cmd": "unix_time_formatted"}), color=Color.NEGATIVE)
    .row()
    .add(Text("Не форматированный", payload={"cmd": "unix_time_unformatted"}), color=Color.POSITIVE)
)
