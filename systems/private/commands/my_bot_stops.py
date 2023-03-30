from systems.private import buttons

from cogs import user, collection, slicer


async def send(message):
	if message.from_user.id in collection.bot_stop_db:
		output = "🛑 Пользователи, которым ты запретил отвечать на свои сообщения:\n"

		for num, user_id in enumerate(collection.bot_stop_db[message.from_user.id]["stop"]):
			user_object = await user.get_object_user(user_id)
			
			pref = ""
			if "bs" in user_object:
				pref = "💎"
			
			output += "\n%num%: <a href=\"%userLink%\">%userName%</a> %pref%".replace(
				"%num%", str(num+1)
			).replace(
				"%pref%", str(pref)
			).replace(
				"%userLink%", await user.get_link_user(user_object["first_name"], user_object["username"])
			).replace(
				"%userName%", await slicer.slicer(
					await user.get_name_user(user_object["first_name"], user_object["username"], user_object["id"]), 20
				)
			)
		
		output += "\n\n💎 — Означает что пользователь приобрёл себе невидимку от «бот стоп» и его сообщения не будут удаляться."
	else:
		output = "⚪️ Ты ещё не запретил ни одному пользователю отвечать на свои сообщения"
	
	await message.reply(output, parse_mode="HTML", disable_web_page_preview=True, reply_markup=buttons.main)
