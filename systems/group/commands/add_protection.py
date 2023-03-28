from main import bot

from systems.private import buttons

from cogs import error, user

from cogs import timeDecoder


async def send_user_message_add_protection(user_object, uptime):
	output = False
	
	try:
		await bot.send_message(int(user_object["id"]), "🟣 Тебе была вручена защита от «бот стоп» на {}".format(
			await timeDecoder.decodate(uptime)
		), parse_mode="HTML", disable_web_page_preview=True, reply_markup=buttons.main)
	except Exception as exception:
		output = exception
	
	return output


async def main(message, message_text, numeration_command):
	params = {
		"arguments": {
			1: ["int"],
			2: ["time|user"],
			3: ["user"]
		},
		"commands": numeration_command,
		"bot_me": False
	}

	if not "reply_to_message" in message:
		params["user"] = True
	
	usage = await error.check_errors(message, message_text, params)
	
	if usage[0] == 1:
		if len(usage[1]["users"]) != 0:
			user_object_reply = usage[1]["users"][0]
		else:
			user_object_reply = await user.get_object_user(message.reply_to_message.from_user.id)

		output = "❓На сколько"
		if len(usage[1]["args"]) > 1:  # если время было указано
			if len(usage[1]["args"]) > 2:  # если был указан пользователь то удаляем его
				del usage[1]["args"][len(usage[1]["args"])-1]

			uptime = await timeDecoder.decoder(usage[1]["args"])
			user_object_reply["bs"] = str(uptime)

			status_message_send = await send_user_message_add_protection(user_object_reply, str(uptime))
			output = "🟣 Пользователю успешно вручена защита от бот стоп\n{}".format(
				"✅ Уведомление получено" if status_message_send is False else "❗️Уведомление не получено: {}".format(
					str(status_message_send)
				)
			)

		await message.reply(output, parse_mode="HTML", disable_web_page_preview=True)
	else:
		await error.send_errors(message, usage)