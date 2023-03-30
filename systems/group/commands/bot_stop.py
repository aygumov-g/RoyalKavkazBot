from cogs import error, user, collection, word

from cogs import timeDecoder

from systems.private import buttons

import datetime, config


async def checker_protection(user_id):
	output = True

	try:
		user_object = await user.get_object_user(user_id)
	
		if await timeDecoder.get_time_is_str(user_object["bs"]) > datetime.datetime.now():
			output = False
		else:
			del user_object["bs"]
	except KeyError:
		pass

	return output


async def checker_reply_stop(message):
	if "reply_to_message" in message and message.reply_to_message.from_user.id in collection.bot_stop_db and message.from_user.id in collection.bot_stop_db[message.reply_to_message.from_user.id]["stop"] and await checker_protection(message.from_user.id) is True:
		try:
			await message.delete()
		except Exception as exception:
			return exception


async def main(message, message_text, numeration_command, command_text):
	params = {
		"arguments": {
			1: ["int|user"],
		},
		"block_errors": ["user_not_in_base"],
		"commands": numeration_command,
		"bot_me": False,
		"me": False
	}

	if not "мои" in command_text and "reply_to_message" in message:
		params["user"] = True
	
	usage = await error.check_errors(message, message_text, params)

	if usage[0] == 1:
		user_object = None
		if len(usage[1]["users"]) != 0 and int(usage[1]["users"][0]["id"]) != 0:
			user_object = usage[1]["users"][0]
		elif "reply_to_message" in message:
			user_object = await user.get_object_user(message.reply_to_message.from_user.id)
			if int(user_object["id"]) == 0:
				user_object = message.reply_to_message.from_user

		if not "-" in command_text and user_object is not None and (not message.from_user.id in collection.bot_stop_db or not user_object["id"] in collection.bot_stop_db[message.from_user.id]["stop"]):  # хочет запретить отвечать на свои сообщения
			if not message.from_user.id in collection.bot_stop_db:
				collection.bot_stop_db[message.from_user.id] = {
					"id": message.from_user.id,
					"stop": []
				}

			output = "🛑 <a href=\"{}\">{}</a> запретил <a href=\"{}\">{}</a> отвечать на свои сообщения".format(
				await user.get_link_user(message.from_user.username, message.from_user.id), await user.get_name_user(message.from_user.first_name, message.from_user.username, message.from_user.id),
				await user.get_link_user(user_object["username"], user_object["id"]), await user.get_name_user(user_object["first_name"], user_object["username"], user_object["id"])
			)

			if "bs" in user_object:
				output += "\n💬 Но, у этого пользователя защита. Возможно, этот запрет мало чем поможет тебе..."

			collection.bot_stop_db[message.from_user.id]["stop"].append(user_object["id"])
			if len(collection.bot_stop_db[message.from_user.id]["stop"]) > 50:  # защита от переполнения (всего запретить человеку отвечать на свои сообщения могут 50 человек)
				del collection.bot_stop_db[message.from_user.id]["stop"][0]

		elif not "-" in command_text and user_object is not None and user_object["id"] in collection.bot_stop_db[message.from_user.id]["stop"]:  # уже запрещал отвечать на свои сообщения
			output = "🚫 Ты уже запрещал этому пользователю отвечать на свои сообщения\n💬 Команда: \"<code>-бот стоп</code>\" — снять запрет на ответы"
		
		elif "мои" in command_text and len(usage[1]["args"]) == 0:  # хочет либо снять, либо посмотреть все свои запреты
			if "-" in command_text and message.from_user.id in collection.bot_stop_db:  # хочет снять все свои запреты
				len_user_bot_stop = len(collection.bot_stop_db[message.from_user.id]["stop"])

				output = "🟢 Освобождено: {} {}".format(
					len_user_bot_stop, await word.ending(
						"пользователь|пользователя|пользователей", len_user_bot_stop
					)
				)

				del collection.bot_stop_db[message.from_user.id]
			elif message.from_user.id in collection.bot_stop_db:  # хочет посмотреть все свои запреты
				output = "✅ <a href=\"{}?start={}\">Нажми</a>, чтобы увидеть всех кому ты запретил отвечать на свои сообщения".format(
					config.BOT_LINK, buttons.BUTTONS["my_bot_stops"]
				)
			else:
				output = "❗️ Ты ещё никому не запрещал отвечать на свои сообщения"
		
		elif "-" in command_text and user_object is not None and message.from_user.id in collection.bot_stop_db and user_object["id"] in collection.bot_stop_db[message.from_user.id]["stop"]:  # хочет снять запрет
			output = "🟢 <a href=\"{}\">{}</a> снова может отвечать на твои сообщения".format(
				await user.get_link_user(user_object["username"], user_object["id"]),
				await user.get_name_user(user_object["first_name"], user_object["username"], user_object["id"])
			)
			
			collection.bot_stop_db[message.from_user.id]["stop"].remove(user_object["id"])
			if len(collection.bot_stop_db[message.from_user.id]["stop"]) == 0:
				del collection.bot_stop_db[message.from_user.id]

		elif "-" in command_text and len(usage[1]["args"]) != 0:  # хочет снять запрет под номером
			if message.from_user.id in collection.bot_stop_db and len(collection.bot_stop_db[message.from_user.id]["stop"]) != 0:
				if 0 < int(usage[1]["args"][0]) <= len(collection.bot_stop_db[message.from_user.id]["stop"]):
					del collection.bot_stop_db[message.from_user.id]["stop"][int(usage[1]["args"][0])-1]

					if len(collection.bot_stop_db[message.from_user.id]["stop"]) == 0:
						del collection.bot_stop_db[message.from_user.id]

					output = "🟢 Запрет на «бот стоп» под номер ({}) удалён".format(
						usage[1]["args"][0]
					)
				else:
					output = "❗️У тебя нет запрета под таким номером. Проверь свои запреты по <a href=\"{}?start={}\">этой ссылке</a>".format(
						config.BOT_LINK, buttons.BUTTONS["my_bot_stops"]
					)
			else:
				output = "❗️Ты ещё никому не запрещал отвечать на твои сообщения"

		elif ("reply_to_message" in message) or (len(usage[1]["args"]) != 0 and not str(usage[1]["args"][0]).isdigit()):  # если не было запрета отвечать на свои сообщения
			output = "❗️Ты не запрещал этому пользователю отвечать на свои сообщения"
		
		else:
			return

		await message.reply(output, parse_mode="HTML", disable_web_page_preview=True)
	else:
		await error.send_errors(message, usage)
