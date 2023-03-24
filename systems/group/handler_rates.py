from cogs import user, collection


max_len_rates = 50

rates_types = {
	1: ["красное", "красно", "красн", "крас", "кра", "кр", "к"],
	2: ["чёрное", "черное", "чёрно", "черно", "чёрн", "черн", "чёр", "чер", "чё", "че", "ч"],
	3: ["зелёное", "зеленое", "зелёно", "зелено", "зелён", "зелен", "зелё", "зеле", "зел", "зе", "з", "0"]
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
		if message.chat.id in collection.roulette_db:
			user_object = await user.get_object_user(message.from_user.id)
			
			if len(collection.roulette_db[message.chat.id]["rates"]) >= max_len_rates:
				await message.reply("🚫 Введи \"<code>!крутить</code>\", в рулетке уже сделано максимальное число ставок", parse_mode="HTML")
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
		
		else:
			await message.reply("🚫 Рулетка не запущена в этом чате")

	return output
