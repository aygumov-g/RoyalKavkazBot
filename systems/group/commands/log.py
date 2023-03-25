from cogs import error, collection


async def get_log(log_int):
	emoji = "💚"

	if int(log_int) in range(1, 19):
		emoji = "🔴"
	elif int(log_int) in range(19, 37):
		emoji = "⚫️"
	
	return emoji


async def main(message, message_text, numeration_command):
	usage = await error.check_errors(message, message_text, {
		"arguments": {
			1: ["user"],
		},
		"commands": numeration_command
	})
	
	if usage[0] == 1:
		output = "🚫 Лог группы не получен"

		if message.chat.id in collection.log_db and len(collection.log_db[message.chat.id]["logs"]) != 0:
			output = ""
			
			for log in reversed(collection.log_db[message.chat.id]["logs"]):
				output += "{} {}\n".format(
					await get_log(log), str(log).replace("37", "0")
				)

		await message.reply(output, parse_mode="HTML", disable_web_page_preview=True)
	else:
		await error.send_errors(message, usage)
