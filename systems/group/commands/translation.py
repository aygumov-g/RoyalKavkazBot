import datetime

from cogs import error, user
from cogs import timeDecoder


limit_trans_time = ["20", "часов"]
limit_trans_money = 10000


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
		user_object_reply = None

		if len(usage[1]["users"]) != 0:
			user_object_reply = usage[1]["users"][0]
		elif "reply_to_message" in message:
			user_object_reply = await user.get_object_user(message.reply_to_message.from_user.id)
		user_object = await user.get_object_user(message.from_user.id)

		if user_object_reply is not None and len(usage[1]["args"]) != 0 and int(usage[1]["args"][0]) <= 0:
			await message.reply("🚫 Такие переводы не принимаются")
		elif user_object_reply is not None and len(usage[1]["args"]) != 0 and int(user_object["b"]) >= int(usage[1]["args"][0]):
			if not "trans" in user_object:  # если пользователь никогда не делал переводы, добавляем инфу о его переводах
				user_object["trans"] = [
					str(0), str(datetime.datetime.now())
				]

			if int(user_object["trans"][0]) < limit_trans_money:
				await message.reply("✅ Пользователю успешно начислены монеты")

				user_object["trans"][0] = str(int(user_object["trans"][0]) + int(usage[1]["args"][0]))
				user_object["trans"][1] = str(await timeDecoder.decoder(limit_trans_time))

				user_object["b"] = str(int(user_object["b"]) - int(usage[1]["args"][0]))
				user_object_reply["b"] = str(int(user_object_reply["b"]) + int(usage[1]["args"][0]))
			else:
				await message.reply("🚫 Лимит на количество переведённых монет истрачен. ({})".format(
					await timeDecoder.decodate(user_object["trans"][1])
				))
		elif user_object_reply is not None and len(usage[1]["args"]) != 0:
			await message.reply("🚫 У тебя нет столько монет")
	else:
		await error.send_errors(message, usage)
