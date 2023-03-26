import datetime

from cogs import error, user, slicer, collection

from cogs import numberDecoder

from systems.group.commands.log import get_log
from systems.group.handler_rates import (
	rates_types_chit_not_chit,
	rates_coefficient,
	rates_types_int,
	rates_types
)

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


async def thumbnail_in_output_message(output_message, checker_and_zero):
	output = output_message
	
	if checker_and_zero == 1:
		output += "\n\n💬 Тому кто поставил ставку возврат половины его ставки"
	
	elif checker_and_zero > 1:
		output += "\n\n💬 Другим кто поставил ставки, возврат половины их ставок"

	return output


async def add_in_output_message(output_message, checker, winner_users):
	if checker != 0 and int(checker[0]) in collection.users_db:
		user_object = await user.get_object_user(int(checker[0]))
		
		if not int(checker[0]) in winner_users:
			if len(checker) != 6:
				output_message += "\n{} <a href=\"{}\">{}</a> <code>></code> {} [{}]".format(
					checker[3],
					await user.get_link_user(user_object["username"], user_object["id"]),
					await slicer.slicer(
						await user.get_name_user(user_object["first_name"], user_object["username"], user_object["id"]), 13
					),
					await numberDecoder.space_decoder(checker[2]),
					checker[4]
				)
	
			user_object["b"] = str(int(user_object["b"]) + checker[2])
			
			winner_users.append(int(checker[0]))

		elif int(checker[0]) in winner_users:
			user_object["b"] = str(int(user_object["b"]) + checker[1])

	return output_message, winner_users


async def add_money_winner(message):
	ball = random.randint(1, 37)

	output_message, checker_and_zero, winner_users = "Рулетка: {} {}".format(
		await get_log(ball), ball
	), 0, []

	for rates in collection.roulette_db[message.chat.id]["rates"]:
		list_rates, checker, = rates[2].split("-"), 0

		if not int(ball) in rates_types_int[3]:  # если выпал не 0 "не зелёное"
			if len(list_rates) > 1 and str(ball) in list_rates:  # выигрыш при ставках в диапозоне
				checker = [rates[0], int(rates[1]), int(int(rates[1]) * rates_coefficient[len(list_rates)]), "x{}".format(
					rates_coefficient[len(list_rates)]
				), "на {}-{}".format(
					list_rates[0], list_rates[-1]
				)]
	
			elif len(list_rates) == 1 and str(list_rates[0]).isdigit() and int(list_rates[0]) == ball:  # выигрыш при ставке на одно число
				checker = [rates[0], int(rates[1]), int(rates[1]) * rates_coefficient[1], "x{}".format(
					rates_coefficient[1]
				), "на {}".format(
					list_rates[0]
				)]
	
			elif len(list_rates) == 1 and rates[2] in rates_types[1] and int(ball) in rates_types_int[1]:  # выигрыш при красном
				checker = [rates[0], int(rates[1]), int(rates[1]) * 2, "x2", "на красный"]
			
			elif len(list_rates) == 1 and rates[2] in rates_types[2] and int(ball) in rates_types_int[2]:  # выигрыш при чёрном
				checker = [rates[0], int(rates[1]), int(rates[1]) * 2, "x2", "на чёрный"]
			
			elif len(list_rates) == 1 and rates[2] in rates_types_chit_not_chit[1] and int(ball) % 2 == 0:  # выигрыш при чётном
				checker = [rates[0], int(rates[1]), int(rates[1]) * 2, "2", "на чётное"]
			
			elif len(list_rates) == 1 and rates[2] in rates_types_chit_not_chit[2] and int(ball) % 2 != 0:  # выигрыш при нечётном
				checker = [rates[0], int(rates[1]), int(rates[1]) * 2, "2", "на нечётное"]

		elif len(list_rates) == 1 and rates[2] in rates_types[3] + [str(i) for i in rates_types_int[3]]:  # если выпал 0 и ставка тоже была на него 0
			checker = [rates[0], int(rates[1]), int(rates[1]) * 35, "x35", "на зелёный"]
		
		else:  # если ставка не была на ноль, то возвращаем игроку половину ставки и увеличиваем количество ставок не на 0
			checker = [rates[0], int(rates[1]), int(int(rates[1]) / 2), "x35", "на зелёный", 0]  # 0 в конце означает что не добавлять это в сообщение
			checker_and_zero += 1

		output_message, winner_users = await add_in_output_message(output_message, checker, winner_users)  # получаем обновлённое сообщение и выйгрышных пользователей

	await add_log(message, ball)
	
	return await thumbnail_in_output_message(output_message, checker_and_zero)


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
		
		try:
			await message.reply(output, parse_mode="HTML", disable_web_page_preview=True)
		except Exception as exception:
			await message.reply("❗️Произошла ошибка при отправке сообщения с рулеткой: {}💬\nСообщение не было отправлено но все ставки были засчитаны".format(
				exception
			))
	else:
		await error.send_errors(message, usage)
