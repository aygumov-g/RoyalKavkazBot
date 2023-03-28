from cogs import error, user, collection


async def checker_reply_stop(message):
	if "reply_to_message" in message and message.from_user.id in collection.bot_stop_db and message.reply_to_message.from_user.id in collection.bot_stop_db[message.from_user.id]["stop"]:
		try:
			await message.delete()
		except Exception as exception:
			return exception


async def main(message, message_text, numeration_command, command_text):
	params = {
		"arguments": {
			1: ["user"]
		},
		"commands": numeration_command,
		"bot_me": False,
		"me": False
	}
	
	if not "reply_to_message" in message:
		params["user"] = True
	
	usage = await error.check_errors(message, message_text, params)
	
	if usage[0] == 1:
		if len(usage[1]["users"]) != 0:
			user_object = usage[1]["users"][0]
		else:
			user_object = await user.get_object_user(message.reply_to_message.from_user.id)

		if not "-" in command_text and (not user_object["id"] in collection.bot_stop_db or not message.from_user.id in collection.bot_stop_db[user_object["id"]]["stop"]):  # хочет запретить отвечать на свои сообщения
			if not int(user_object["id"]) in collection.bot_stop_db:
				collection.bot_stop_db[user_object["id"]] = {
					"id": int(user_object["id"]),
					"stop": []
				}

			output = "🛑 <a href=\"{}\">{}</a> запретил <a href=\"{}\">{}</a> отвечать на свои сообщения".format(
				await user.get_link_user(message.from_user.username, message.from_user.id), await user.get_name_user(message.from_user.first_name, message.from_user.username, message.from_user.id),
				await user.get_link_user(user_object["username"], user_object["id"]), await user.get_name_user(user_object["first_name"], user_object["username"], user_object["id"])
			)

			collection.bot_stop_db[user_object["id"]]["stop"].append(message.from_user.id)
			if len(collection.bot_stop_db[user_object["id"]]["stop"]) > 50:  # защита от переполнения (всего запретить человеку отвечать на свои сообщения могут 50 человек)
				del collection.bot_stop_db[user_object["id"]]["stop"][0]

		elif not "-" in command_text and message.from_user.id in collection.bot_stop_db[user_object["id"]]["stop"]:  # уже запрещал отвечать на свои сообщения
			output = "🚫 Ты уже запрещал этому пользователю отвечать на свои сообщения\n💬 Команда: \"<code>-бот стоп</code>\" — снять запрет на ответы"
		
		elif "-" in command_text and user_object["id"] in collection.bot_stop_db and message.from_user.id in collection.bot_stop_db[user_object["id"]]["stop"]:  # хочет снять запрет
			output = "🟢 <a href=\"{}\">{}</a> снова может отвечать на твои сообщения".format(
				await user.get_link_user(user_object["username"], user_object["id"]), await user.get_name_user(user_object["first_name"], user_object["username"], user_object["id"])
			)
			
			collection.bot_stop_db[user_object["id"]]["stop"].remove(message.from_user.id)
			if len(collection.bot_stop_db[user_object["id"]]["stop"]) == 0:
				del collection.bot_stop_db[user_object["id"]]

		else:  # если не было запрета отвечать на свои сообщения
			output = "❗️Ты не запрещал этому пользователю отвечать на свои сообщения"

		await message.reply(output, parse_mode="HTML", disable_web_page_preview=True)
	else:
		await error.send_errors(message, usage)
