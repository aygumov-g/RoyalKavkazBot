from main import bot

from cogs import collection

import fonts


async def get_link_user(username, ids):
	return "tg://user?id={}".format(ids) if username is None else "https://t.me/{}".format(username)


async def get_name_user(first_name, username, ids):
	if int(ids) in collection.users_db and "nick" in collection.users_db[int(ids)]:
		return collection.users_db[int(ids)]["nick"]
	elif not first_name in [".", ","]:
		check = 1

		for char in first_name:
			if not char in fonts.CHARS:
				check = 0
				break

		if check == 1:
			return str(first_name)
		elif username is not None:
			return str(username)
		else:
			return str(ids)
	elif username is not None:
		return str(username)
	else:
		return str(ids)


async def get_object_user(user, chat_id=None):
	output, user_string = {
		"id": 0,
		"first_name": "Неизвестный человек",
		"last_name": "None",
		"username": "None"
	}, str(user) if str(user)[0] != "@" else str(user)[1:]

	if not str(user_string).isdigit():
		for userID in collection.users_db:
			if str(collection.users_db[userID]["first_name"]) == str(user_string) or str(collection.users_db[userID]["username"]) == str(user_string):
				try:
					get_chat_member = await bot.get_chat_member(chat_id=chat_id, user_id=int(userID))
					
					if not get_chat_member["status"] in ["left", "kicked", "banned"]:
						output = collection.users_db[userID];break
				except Exception as exception:
					return {**output, **{
						"exception": exception
					}}
	elif str(user_string).isdigit() and int(user_string) in collection.users_db:
		output = collection.users_db[int(user_string)]

	return output
