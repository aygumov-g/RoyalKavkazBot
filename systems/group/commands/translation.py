from cogs import error, user, collection
from cogs import timeDecoder


limit_trans_money_in_day = 10000


async def main(message, message_text, numeration_command):
	params = {
		"arguments": {
			1: ["int"],
			2: ["user"]
		},
		"commands": numeration_command,
		"bot_me": False,
		"me": False
	}
	
	if not "reply_to_message" in message:
		params["user"] = True
	
	usage = await error.check_errors(message, message_text, params)

	if usage[0] == 1:
		if len(usage[1]["users"]) != 0:
			user_object_reply = usage[1]["users"][0]
		else:
			user_object_reply = await user.get_object_user(message.reply_to_message.from_user.id)
		user_object = await user.get_object_user(message.from_user.id)
		
		if int(usage[1]["args"][0]) <= 0:
			await message.reply("🚫 Такие переводы не принимаются")
		if int(user_object["b"]) >= int(usage[1]["args"][0]):
			if int(user_object["trans"][0]) < limit_trans_money_in_day:
				await message.reply("✅ Пользователю успешно начислены монеты")
				
				user_object["trans"][0] = str(int(user_object["trans"][0]) + int(usage[1]["args"][0]))
				user_object["trans"][1] = str(await timeDecoder.decoder(["1", "день"]))

				user_object["b"] = str(int(collection.users_db[message.from_user.id]["b"]) - int(usage[1]["args"][0]))
				user_object_reply["b"] = str(int(user_object_reply["b"]) + int(usage[1]["args"][0]))
			else:
				await message.reply("🚫 Лимит на количество переведённых монет за сутки истрачен. ({})".format(
					await timeDecoder.decodate(user_object["trans"][1])
				))
		else:
			await message.reply("🚫 У тебя нет столько монет")
	else:
		await error.send_errors(message, usage)
