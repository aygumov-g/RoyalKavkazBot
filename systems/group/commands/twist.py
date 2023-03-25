import datetime

from cogs import error, user, slicer, collection

from cogs import numberDecoder

from systems.group import handler_rates

from systems.group.commands.log import get_log
from systems.group.handler_rates import rates_types_int

import random


max_logs_elem = 20


async def add_log(message, ball):
	if not message.chat.id in collection.log_db:
		collection.log_db[message.chat.id] = {
			"id": message.chat.id,
			"uptime": "",
			"logs": []
		}

	elif len(collection.log_db[message.chat.id]["logs"]) >= max_logs_elem:
		del collection.log_db[message.chat.id]["logs"][0]
	
	collection.log_db[message.chat.id]["logs"].append(str(ball))
	collection.log_db[message.chat.id]["uptime"] = str(datetime.datetime.now())


async def add_money_winner(message):
	ball = random.randint(1, 37)

	output_message = "Рулетка: {} {}".format(
		await get_log(ball), ball
	)
	
	for rates in collection.roulette_db[message.chat.id]["rates"]:
		checker = 0

		if rates[2] in handler_rates.rates_types[1] and int(ball) in rates_types_int[1]:
			checker = [rates[0], int(rates[1]) * 2]
		elif rates[2] in handler_rates.rates_types[2] and int(ball) in rates_types_int[2]:
			checker = [rates[0], int(rates[1]) * 2]
		elif rates[2] in handler_rates.rates_types[3] and int(ball) in rates_types_int[3]:
			checker = [rates[0], int(rates[1]) * len(collection.roulette_db[message.chat.id]["rates"])]
		
		if checker != 0 and int(checker[0]) in collection.users_db:
			user_object = await user.get_object_user(int(checker[0]))

			output_message += "\n<code>+</code> <a href=\"{}\">{}</a> <code>></code> {}".format(
				await user.get_link_user(user_object["username"], user_object["id"]),
				await slicer.slicer(
					await user.get_name_user(user_object["first_name"], user_object["username"], user_object["id"]), 13
				),
				await numberDecoder.space_decoder(checker[1])
			)
			
			user_object["b"] = str(int(user_object["b"]) + checker[1])
	
	await add_log(message, ball)
	
	return output_message


async def main(message, message_text, numeration_command):
	usage = await error.check_errors(message, message_text, {
		"block_arguments": True,
		"commands": numeration_command
	})
	
	if usage[0] == 1:
		if message.chat.id in collection.roulette_db:
			if message.from_user.id in [int(rates[0]) for rates in collection.roulette_db[message.chat.id]["rates"]]:
				output = await add_money_winner(message)
			
				del collection.roulette_db[message.chat.id]
			else:
				output = "🚫 Сделай ставку, потом крути"
		else:
			output = "🚫 Нету ставок чтобы крутить"

		await message.reply(output, parse_mode="HTML", disable_web_page_preview=True)
	else:
		await error.send_errors(message, usage)
