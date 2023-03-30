import datetime

from main import bot

from systems.private import buttons

from cogs import user

from cogs import timeDecoder

import config, random


async def send(message):
	user_object, output = await user.get_object_user(message.from_user.id), ""

	if int(user_object["b"]) <= 0:
		if not "bonus" in user_object:  # если пользователь никогда не брал бонусов, то добавляем инфу о его бонусах
			user_object["bonus"] = str(
				datetime.datetime.now()
			)

		if await timeDecoder.get_time_is_str(user_object["bonus"]) <= datetime.datetime.now():
			member = await bot.get_chat_member(chat_id=config.CHANNEL_NEWS, user_id=message.from_user.id)
	
			if member["status"] != "left":
				get = random.randint(5000, 6000)
				
				output = "💰 Тебе начислено <code>{}</code> монет".format(get)
	
				user_object["b"] = str(get)
				user_object["bonus"] = str(await timeDecoder.decoder(["5", "часов"]))
			else:
				output = "🛑 Подпишись на наш <a href=\"http://t.me/{}\"><b>новостной канал</b></a> а после пропиши команду <b>/bonus</b>".format(
					str(config.CHANNEL_NEWS).replace("@", "")
				)
		else:
			output = "🛑 Ты сможешь взять бонус сразу как только пройдет {}".format(
				await timeDecoder.decodate(user_object["bonus"])
			)
	else:
		output = "🛑 У тебя и так достаточно монет. Лучше возвращайся когда они закончаться"

	await message.reply(output, parse_mode="HTML", disable_web_page_preview=True, reply_markup=buttons.main)
