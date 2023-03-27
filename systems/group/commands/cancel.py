from cogs import error, user, collection


async def main(message, message_text, numeration_command):
	usage = await error.check_errors(message, message_text, {
		"commands": numeration_command
	})

	if usage[0] == 1:
		output = "❎ У тебя нет активных ставок в этой беседе"

		if message.chat.id in collection.roulette_db and len(collection.roulette_db[message.chat.id]["rates"]) != 0:
			for rate in reversed(collection.roulette_db[message.chat.id]["rates"]):
				if int(rate[0]) == message.from_user.id:
					user_object = await user.get_object_user(message.from_user.id)

					user_rate = rate[2]
					if "-" in user_rate:
						user_rate_list = user_rate.split("-")
						user_rate = "{}-{}".format(
							user_rate_list[0],
							user_rate_list[-1]
						)

					output = "✅ Твоя ставка [{} на {}] отменена".format(
						rate[1], user_rate
					)

					user_object["b"] = str(int(user_object["b"]) + int(rate[1]))
					collection.roulette_db[message.chat.id]["rates"].remove(rate)

					break

		try:
			if len(collection.roulette_db[message.chat.id]["rates"]) == 0:
				del collection.roulette_db[message.chat.id]
		except KeyError:
			pass

		await message.reply(output, parse_mode="HTML", disable_web_page_preview=True)
	else:
		await error.send_errors(message, usage)
