from vkbottle import Keyboard
from vkbottle import KeyboardButtonColor as Color
from vkbottle import Text

MAIN_KBD = (
    Keyboard()
    .add(Text("плыть", payload={"cmd": "sailed"}), color=Color.POSITIVE)
    .row()
    .add(Text("топ регаты", payload={"cmd": "sailed_top"}), color=Color.NEGATIVE)
    .add(Text("юникс тайм", payload={"cmd": "unix_time"}), color=Color.NEGATIVE)
    .row()
    .add(Text("помощь", payload={"cmd": "sailed_help"}), color=Color.NEGATIVE)
    .row()
    .add(Text("убрать клаву", payload={"cmd": "remove_kbd"}), color=Color.POSITIVE)
).get_json()

FORMAT_KBD = (
    Keyboard(inline=True)
    .add(Text("Отформаченный", payload={"cmd": "unix_time_formatted"}), color=Color.POSITIVE)
    .row()
    .add(Text("Неотформаченный", payload={"cmd": "unix_time_unformatted"}), color=Color.NEGATIVE)
)
