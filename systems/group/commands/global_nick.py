from cogs import error, user


CHARS = "йцукенгшщзхъфывапролджэячсмитьбюЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮqwertyuiopasdfghjklzxcvbnm0123456789,. "


async def get_nick_message(user_object):
	output = "Глобальный ник <a href=\"%userLink%\">пользователя</a>:\n<code>></code> %userNick%"

	nickname = "Не установлен ❎"
	if "nick" in user_object:
		nickname = user_object["nick"]

	return output.replace(
		"%userLink%", await user.get_link_user(user_object["username"], user_object["id"])
	).replace(
		"%userNick%", str(nickname)
	)


async def main(message, message_text, numeration_command, command_text):
	usage = await error.check_errors(message, message_text, {
		"arguments": {
			1: ["user"]
		},
		"commands": numeration_command,
		"bot_me": False,
		"repliks": True
	})

	if usage[0] == 1:
		user_object = await user.get_object_user(message.from_user.id)
		if "reply_to_message" in message and not "+" in command_text and not "-" in command_text:  # если смотрим ник пользователя в ответ на сообщение
			user_object = await user.get_object_user(message.reply_to_message.from_user.id)

			await message.reply(await get_nick_message(user_object), parse_mode="HTML", disable_web_page_preview=True)
		
		elif len(usage[1]["users"]) != 0 and not "+" in command_text and not "-" in command_text:  # если смотрим ник пользователя через @пользователь
			user_object = usage[1]["users"][0]

			await message.reply(await get_nick_message(user_object), parse_mode="HTML", disable_web_page_preview=True)

		elif "+" in command_text:  # если пользователь устанавливает себе ник
			if 0 < len(message_text) <= 25:  # проверяем длину устанавливаемого ника
				for char in message_text:  # проходимся по всем символам в Устанавливаемом нике
					if not char in CHARS:  # если символ запрещённый - отрубаем
						await message.reply("❎ В устанавливаемом никнейме присутствует запрещённый символ");return

				user_object["nick"] = message_text

				await message.reply("✅ Ник <a href=\"{}\">пользователя</a> изменён".format(
					await user.get_link_user(user_object["username"], user_object["id"])
				), parse_mode="HTML", disable_web_page_preview=True)
			elif 0 < len(message_text):
				await message.reply("❎ Устанавливаемый никнейм слишком большой")

		elif "-" in command_text:  # если пользователь хочет удалить свой ник
			try:
				del user_object["nick"]
			except KeyError:
				pass
				
			await message.reply("✅ Ник пользователя удалён")

		else:  # если пользователь смотрит свой ник
			await message.reply(await get_nick_message(user_object), parse_mode="HTML", disable_web_page_preview=True)
	else:
		await error.send_errors(message, usage)
