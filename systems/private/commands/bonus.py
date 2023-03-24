from main import bot

from cogs import user

import config, random


async def send(message):
	user_object, output = await user.get_object_user(message.from_user.id), ""

	if int(user_object["b"]) <= 0:
		member = await bot.get_chat_member(chat_id=config.CHANNEL_NEWS, user_id=message.from_user.id)

		if member["status"] != "left":
			get = random.randint(5000, 10000)
			
			output = "💰 Тебе начислено <code>{}</code> монет".format(get)

			user_object["b"] = str(get)
		else:
			output = "🛑 Подпишись на наш <a href=\"http://t.me/{}\"><b>новостной канал</b></a> а после пропиши команду <b>/bonus</b>".format(
				str(config.CHANNEL_NEWS).replace("@", "")
			)
	else:
		output = "🛑 У тебя и так достаточно монет. Лучше возвращайся когда твой баланс будет на нуле"

	await message.reply(output, parse_mode="HTML", disable_web_page_preview=True)
