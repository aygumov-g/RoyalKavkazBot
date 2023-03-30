from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

BUTTONS = {
	"bonus": "bonus",
	"my_bot_stops": "m3y_bot_stops",
	"profile": "👤 Профиль",
	"donate": "🔥 Донат"
}

main = ReplyKeyboardMarkup(resize_keyboard=True)

main.row(
	KeyboardButton(BUTTONS["profile"]),
	KeyboardButton(BUTTONS["donate"])
)
