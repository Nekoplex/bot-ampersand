from vkbottle import Keyboard
from vkbottle import KeyboardButtonColor as Color
from vkbottle import Text

MAIN_KBD = (
    Keyboard()
    .add(Text("пить"), color=Color.NEGATIVE)
    .add(Text("пить топ"), color=Color.NEGATIVE)
    .add(Text("юникс тайм"), color=Color.NEGATIVE)
    .row()
    .add(Text("помощь"), color=Color.NEGATIVE)
    .row()
    .add(Text("убрать клаву"), color=Color.POSITIVE)
).get_json()

FORMAT_KBD = (
    Keyboard(inline=True)
    .add(Text("Отформатированный"), color=Color.NEGATIVE)
    .row()
    .add(Text("Не форматированный"), color=Color.POSITIVE)
)
