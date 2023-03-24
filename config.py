TOKEN = "6287364057:AAFmZbogfncnk3r7XR9Tbxuq-XSReYLQ-io"

TOKEN_BD1 = "mongodb+srv://admin:AyGadzhi11@cluster0.3cb1l.mongodb.net/?retryWrites=true&w=majority"
TOKEN_BD2 = "mongodb+srv://admin1:AyGadzhi11@cluster0.krtj0.mongodb.net/?retryWrites=true&w=majority"

PREFIXES = ".|,|*|%|!|%|Бот|бот".split("|")

COMMANDS = {
	1: dict(usage=["баланс", "б"]),
	2: dict(usage=["+"]),
	3: dict(usage=["рулетка", "рул"]),
	4: dict(usage=["крутить", "спин", "^го"]),
	5: dict(usage=["лог"]),
	6: dict(usage=["дать монеты"], call=[1098339945])
}

CHANNEL_NEWS = "@RoyalKavkazNews"

TIMES = {
	0: ["секунда", "секунды", "секунду", "секунд", "сек", "с", "second", "seconds", "sec", "s"],
	1: ["минута", "минуты", "минуту", "минут", "мин", "м", "minute", "minutes", "min", "m"],
	2: ["часа", "часов", "час", "ч", "hour", "hours", "h"],
	3: ["день", "дней", "дня", "д", "day", "days", "d"],
	4: ["неделя", "недели", "неделю", "недель", "нед", "н", "week", "weeks", "w"],
	5: ["месяц", "месяца", "месяцей", "месяцев", "мес", "month", "months", "mon", "mont"],
	6: ["год", "года", "лет"]
}
