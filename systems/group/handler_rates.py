from cogs import user, collection

import datetime


max_len_rates = 50

rates_types_int = {
	1: [23, 5, 16, 1, 14, 9, 18, 7, 12, 3, 32, 19, 21, 25, 34, 27, 36, 30],
	2: [10, 24, 33, 20, 31, 22, 29, 28, 35, 26, 15, 4, 2, 17, 6, 13, 11, 8],
	3: [0, 37]
}

rates_types = {
	1: ["красное", "красно", "красн", "крас", "кра", "кр", "к"] + [str(num) for num in rates_types_int[1]],
	2: ["чёрное", "черное", "чёрно", "черно", "чёрн", "черн", "чёр", "чер", "чё", "че", "ч"] + [str(num) for num in rates_types_int[2]],
	3: ["зелёное", "зеленое", "зелёно", "зелено", "зелён", "зелен", "зелё", "зеле", "зел", "зе", "з"] + [str(num) for num in rates_types_int[3]]
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

	if len(message_text_list) in [2, 3] and str(message_text_list[0]).isdigit():
		for rate_type in rates_types:
			if message_text_list[-1].lower() in rates_types[rate_type]:
				output = [int(message_text_list[0]), message_text_list[-1].lower()];break

	return output


async def main(message):
	output = False

	rate = await check_rates(message)
	if rate is not False:
		await start_roulette(message)

		user_object = await user.get_object_user(message.from_user.id)
		
		if len(collection.roulette_db[message.chat.id]["rates"]) >= max_len_rates:
			await message.reply("🚫 Введи \"<code>!крутить</code>\", в рулетке уже сделано максимальное число ставок", parse_mode="HTML")
		elif int(rate[0]) <= 0:
			await message.reply("🚫 Такие ставки не принимаются")
		elif int(user_object["b"]) >= rate[0]:
			await message.reply("✅ Ставка принята")
			
			collection.roulette_db[message.chat.id]["rates"].append([
				str(message.from_user.id), str(rate[0]), str(rate[1])
			])

			user_object["b"] = str(int(user_object["b"]) - int(rate[0]))
		elif int(user_object["b"]) == 0:
			await message.reply("🚫 У тебя нет монет")
		else:
			await message.reply("🚫 У тебя нет столько монет")
		
		output = True

	return output
