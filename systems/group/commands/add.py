from main import bot

from cogs import error, user, word

from cogs import numberDecoder


async def send_user_message_add_money(user_object, money):
	output = False

	try:
		await bot.send_message(int(user_object["id"]), "💰 Ты получил {} {}\n💬 Причина: Вознаграждение от администрации бота".format(
			await numberDecoder.space_decoder(money),
			await word.ending(
				"монету|монеты|монет", int(money)
			)
		), parse_mode="HTML", disable_web_page_preview=True)
	except Exception as exception:
		output = exception
	
	return output


async def main(message, message_text, numeration_command):
	params = {
		"arguments": {
			1: ["int"],
			2: ["user"]
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
			user_object_reply = usage[1]["users"][0]
		else:
			user_object_reply = await user.get_object_user(message.reply_to_message.from_user.id)
		
		output = "❓Сколько"
		if len(usage[1]["args"]) != 0:
			user_object_reply["b"] = str(int(user_object_reply["b"]) + int(usage[1]["args"][0]))
			
			status_message_send = await send_user_message_add_money(user_object_reply, usage[1]["args"][0])

			output = "💰 Пользователю успешно вручены монеты из банка\n{}".format(
				"✅ Уведомление получено" if status_message_send is False else "❗️Уведомление не получено: {}".format(
					str(status_message_send)
				)
			)

		await message.reply(output, parse_mode="HTML", disable_web_page_preview=True)
	else:
		await error.send_errors(message, usage)
