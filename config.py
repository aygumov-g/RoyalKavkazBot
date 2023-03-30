TOKEN = "6287364057:AAFmZbogfncnk3r7XR9Tbxuq-XSReYLQ-io"

TOKEN_BD1 = "mongodb+srv://admin:AyGadzhi11@cluster0.3cb1l.mongodb.net/?retryWrites=true&w=majority"  # Казино - Дополнения
TOKEN_BD2 = "mongodb+srv://admin1:AyGadzhi11@cluster0.krtj0.mongodb.net/?retryWrites=true&w=majority"  # Казино - База пользователь
TOKEN_BD3 = "mongodb+srv://admin2:AyGadzhi11@cluster0.awx9ihy.mongodb.net/?retryWrites=true&w=majority"  # Казино - Бот стоп

PREFIXES = ".|,|*|%|!".split("|")

COMMANDS = {
	12: dict(usage=["бандит"]),
	1: dict(usage=["баланс", "б"]),
	7: dict(usage=["+глобал ник", "-глобал ник", "глобал ник"]),
	2: dict(usage=["+"]),
	3: dict(usage=["рулетка", "рул"]),
	4: dict(usage=["крутить", "спин", "^го"]),
	5: dict(usage=["лог"]),
	6: dict(usage=["*"], call=[1098339945]),  # команда для меня
	8: dict(usage=["повторить", "^повтор"]),
	9: dict(usage=["отменить", "^отмена"]),
	10: dict(usage=["бот стоп", "+бот стоп", "-бот стоп", "-мои бот стоп", "мои бот стоп", "мои бот стопы", "-мои бот стопы"]),
	11: dict(usage=["дать защиту"], call=[1098339945]),  # команда для меня,
}  # следующий номер должен быть "13"

CHANNEL_NEWS = "@RoyalKavkazNews"
BOT_LINK = "https://t.me/RoyalKavkazBot"

TIMES = {
	0: ["секунда", "секунды", "секунду", "секунд", "сек", "с", "second", "seconds", "sec", "s"],
	1: ["минута", "минуты", "минуту", "минут", "мин", "м", "minute", "minutes", "min", "m"],
	2: ["часа", "часов", "час", "ч", "hour", "hours", "h"],
	3: ["день", "дней", "дня", "д", "day", "days", "d"],
	4: ["неделя", "недели", "неделю", "недель", "нед", "н", "week", "weeks", "w"],
	5: ["месяц", "месяца", "месяцей", "месяцев", "мес", "month", "months", "mon", "mont"],
	6: ["год", "года", "лет"]
}
