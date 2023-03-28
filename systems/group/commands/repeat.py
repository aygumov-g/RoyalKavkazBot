from cogs import error, user, collection

from systems.group import handler_rates


async def main(message, message_text, numeration_command):
	usage = await error.check_errors(message, message_text, {
		"block_arguments": True,
		"commands": numeration_command
	})

	if usage[0] == 1:
		user_object = await user.get_object_user(message.from_user.id)

		if "last_rate" in user_object:
			check_errors_rates = await handler_rates.check_errors_rates(message, user_object, user_object["last_rate"])

			if check_errors_rates is False:
				user_rate = user_object["last_rate"][1]
				if "-" in user_rate:
					user_rate_list = user_rate.split("-")
					user_rate = "{}-{}".format(
						user_rate_list[0],
						user_rate_list[-1]
					)

				output = "✅ Твоя последняя ставка [{} на {}] принята".format(
					user_object["last_rate"][0], user_rate
				)

				collection.roulette_db[message.chat.id]["rates"].append([
					str(message.from_user.id), str(user_object["last_rate"][0]), str(user_object["last_rate"][1])
				])

				user_object["b"] = str(int(user_object["b"]) - int(user_object["last_rate"][0]))
			else:
				output = check_errors_rates
		else:
			output = "❎ Твоя последняя ставка не найдена"

		await message.reply(output, parse_mode="HTML", disable_web_page_preview=True)
	else:
		await error.send_errors(message, usage)