from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

BUTTONS = {
	"bonus": "bonus",
	"profile": "👤 Профиль",
	"donate": "🔥 Донат"
}

main = ReplyKeyboardMarkup(resize_keyboard=True)

main.row(
	KeyboardButton(BUTTONS["profile"]),
	KeyboardButton(BUTTONS["donate"])
)
