from cogs import error, user, slicer, collection

from cogs import numberDecoder

from systems.group import handler_rates

import random


async def add_money_winner(message):
	output_message = ""

	for rates in collection.roulette_db[message.chat.id]["rates"]:
		checker, ball = 0, random.randint(1, 37)

		if rates[2] in handler_rates.rates_types[1] and ball in range(1, 19):
			checker = [rates[0], int(rates[1]) * 2]
		elif rates[2] in handler_rates.rates_types[2] and ball in range(19, 37):
			checker = [rates[0], int(rates[1]) * 2]
		elif rates[2] in handler_rates.rates_types[3] and ball == 37:
			checker = [rates[0], int(rates[1]) * len(collection.roulette_db[message.chat.id]["rates"])]

		if checker != 0 and int(checker[0]) in collection.users_db:
			user_object = await user.get_object_user(int(checker[0]))

			output_message += "<code>+</code> <a href=\"{}\">{}</a> <code>></code> {} \n".format(
				await user.get_link_user(user_object["username"], user_object["id"]),
				await slicer.slicer(
					await user.get_name_user(user_object["first_name"], user_object["username"], user_object["id"]), 13
				),
				await numberDecoder.space_decoder(checker[1])
			)

			user_object["b"] = str(int(user_object["b"]) + checker[1])
	
	return output_message


async def main(message, message_text, numeration_command):
	usage = await error.check_errors(message, message_text, {
		"block_arguments": True,
		"commands": numeration_command,
		"bot_me": False
	})
	
	if usage[0] == 1:
		if message.chat.id in collection.roulette_db:
			output = await add_money_winner(message)
			
			del collection.roulette_db[message.chat.id]
		else:
			output = "🚫 Рулетка не запущена в этом чате"
		
		await message.reply(output if output != "" else "👏🏿 Никто не выйграл", parse_mode="HTML", disable_web_page_preview=True)
	else:
		await error.send_errors(message, usage)
