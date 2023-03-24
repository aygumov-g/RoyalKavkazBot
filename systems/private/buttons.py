from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

BUTTONS = {
	"bonus": "bonus",
	"profile": "👤 Профиль"
}

main = ReplyKeyboardMarkup(resize_keyboard=True)

main.row(
	KeyboardButton(BUTTONS["profile"])
)
