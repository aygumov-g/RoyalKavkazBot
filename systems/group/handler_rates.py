from cogs import user, collection

import datetime

max_len_rates = 50

rates_coefficient = {
	1: 36,
	2: 18,
	3: 12,
	4: 9,
	5: 7.2,
	6: 6,
	7: 5.1,
	8: 4.5,
	9: 4,
	10: 3.6,
	11: 3.2,
	12: 3,
	13: 2.7,
	14: 2.5,
	15: 2.4,
	16: 2.2,
	17: 2.1,
	18: 2
}

rates_types_int = {
	1: [23, 5, 16, 1, 14, 9, 18, 7, 12, 3, 32, 19, 21, 25, 34, 27, 36, 30],
	2: [10, 24, 33, 20, 31, 22, 29, 28, 35, 26, 15, 4, 2, 17, 6, 13, 11, 8],
	3: [0, 37]
}

rates_types_chit_not_chit = {
	1: ["чётное", "чётный", "чёт", "четное", "четный", "чет"],
	2: ["нечётное", "нечётный", "нечёт", "нечетное", "нечетный", "нечет"]
}

rates_types = {
	1: ["красное", "красно", "красн", "крас", "кра", "кр", "к"],
	2: ["чёрное", "черное", "чёрно", "черно", "чёрн", "черн", "чёр", "чер", "чё", "че", "ч"],
	3: ["зелёное", "зеленое", "зелёно", "зелено", "зелён", "зелен", "зелё", "зеле", "зел", "зе", "з"]
}


async def start_roulette(message):
	if not message.chat.id in collection.roulette_db:
		collection.roulette_db[message.chat.id] = {
			"id": message.chat.id,
			"reg": str(datetime.datetime.now()),
			"rates": []
		}


async def check_rates(message):
	message_text_list, output = message.text.split(" "), False
	
	if len(message_text_list) in [2, 3]:
		if len(message_text_list) == 3 and message_text_list[1] != "на":  # защита от "2 выфвыф 3" и прочего
			return output

		elif str(message_text_list[0]).isdigit() or str(message_text_list[0]) in ["ва-банк", "вабанк"]:
			rate = message_text_list[0]
			if str(message_text_list[0]) in ["ва-банк", "вабанк"]:  # если был прописан ва-банк - ставим все монеты
				rate = (await user.get_object_user(message.from_user.id))["b"]

			message_text_rates_list = message_text_list[-1].replace(" ", "").split("-")
			if 2 < len(message_text_rates_list) <= 8:
				return output  # здесь сделаю ставки на подобии 1-3-6-8-2-10-34-4

			elif len(message_text_rates_list) == 2:
				for checkerInt in message_text_rates_list:  # проходимся по числам в 1-14 (не по диапазону)
					if not str(checkerInt).isdigit():  # если символ не число - отрубаем всю ставку
						return output
				
				if int(message_text_rates_list[0]) <= 0 or int(message_text_rates_list[0]) >= 36 or int(message_text_rates_list[1]) > 36 or not int(message_text_rates_list[1]) - int(message_text_rates_list[0]) + 1 in rates_coefficient:
					error_send = "🚫 Неизвестный диапазон"
					
					if int(message_text_rates_list[1]) > 36:
						error_send = "🚫 Большой диапазон"
					
					await message.reply(error_send);return output
				
				elif int(message_text_rates_list[0]) <= int(message_text_rates_list[1]):  # если второе число меньше первого в конструкции "1-4" то идём дальше
					ratesInt = []
					for i in range(int(message_text_rates_list[1]) - int(message_text_rates_list[0]) + 1):
						ratesInt.append(str(int(message_text_rates_list[0]) + i))
					
					output = [int(rate), "-".join(ratesInt)]
			
			elif len(message_text_rates_list) == 1 and message_text_rates_list[0] in rates_types_chit_not_chit[1] + rates_types_chit_not_chit[2]:  # если ставка была на "чётное" или "нечётное"
				types = rates_types_chit_not_chit[1][0]
				
				if message_text_rates_list[0] in rates_types_chit_not_chit[2]:
					types = rates_types_chit_not_chit[2][0]
				
				output = [int(rate), types]
			
			elif len(message_text_rates_list) == 1 and message_text_rates_list[0] in rates_types[1] + rates_types[2] + rates_types[3]:  # если ставка была на "красный" или "чёрный" или "зелёный"
				output = [int(rate), message_text_list[-1].lower()]
			
			elif len(message_text_rates_list) == 1 and str(message_text_rates_list[0]).isdigit() and int(message_text_rates_list[0]) in rates_types_int[1] + rates_types_int[2] + rates_types_int[3]:  # если была на число
				output = [int(rate), message_text_list[-1].lower()]
	
	return output


async def main(message):
	output = False
	
	rate = await check_rates(message)
	if rate is not False:
		await start_roulette(message)
		
		user_object = await user.get_object_user(message.from_user.id)

		if len(collection.roulette_db[message.chat.id]["rates"]) >= max_len_rates:
			await message.reply("🚫 Введи \"<code>!крутить</code>\", в рулетке уже сделано максимальное число ставок", parse_mode="HTML")
		elif int(user_object["b"]) == 0:
			await message.reply("🚫 У тебя нет монет")
		elif int(rate[0]) <= 0:
			await message.reply("🚫 Такие ставки не принимаются")
		elif int(user_object["b"]) >= rate[0]:
			await message.reply("✅ Ставка принята")
			
			collection.roulette_db[message.chat.id]["rates"].append([
				str(message.from_user.id), str(rate[0]), str(rate[1])
			])
			
			user_object["b"] = str(int(user_object["b"]) - int(rate[0]))
		else:
			await message.reply("🚫 У тебя нет столько монет")
		
		output = True
	
	return output
