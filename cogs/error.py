from main import bot

from cogs import user, collection


async def check_error_not_commands_usage_me(obj):
	if "me" in obj["params"] and obj["params"]["me"] is False:
		if (obj["message"].from_user.id in [int(us["id"]) for us in obj["users"]]) or ("reply_to_message" in obj["message"] and obj["message"].from_user.id == obj["message"].reply_to_message.from_user.id):
			obj["errors_message"] = "🚫 Ты не можешь применить эту команду к себе"
			return 0


async def check_error_commands_not_usage_in_bot(obj):
	if "bot_me" in obj["params"] and obj["params"]["bot_me"] is False:
		if (obj["bot_obj"].id in [int(i["id"]) for i in obj["users"]]) or ("reply_to_message" in obj["message"] and obj["message"].reply_to_message.from_user.id == obj["bot_obj"].id):
			obj["errors_message"] = "🚫 На мне эта команда не работает"
			return 0


async def check_error_user_not_in_base(obj):
	if "reply_to_message" in obj["message"]:
		if obj["message"].reply_to_message.from_user.id != obj["bot_obj"].id and not obj["message"].reply_to_message.from_user.id in collection.users_db:
			obj["errors_message"] = "🚫 Пользователь отсутсвует в базе"
			return 0


async def check_error_type_and_users_and_len_arguments(obj):
	if "block_arguments" in obj["params"] and len(obj["args"]) != 0:
		"""Были прописаны аргументы в команде в которой не должны были"""
		return 0
	
	elif "arguments" in obj["params"] and len(obj["params"]["arguments"]) < len(obj["args"]) and not "repliks" in obj["params"]:
		"""Неправильное количество аргументов в команде"""
		return 0
	
	elif len(obj["arguments_types_error"]) != 0 and not "repliks" in obj["params"]:
		"""Неправильный тип аргумента в команде"""
		return 0
	
	elif len(obj["attempt_users"]) != 0:
		obj["errors_message"] = "🚫 Пользователь отсутствует либо в беседе, либо в базе бота"
		return 0


async def set_arguments_in_message(obj):
	for index_argument, argument in enumerate(obj["args"]):
		try:
			argument_checker_error = len(obj["params"]["arguments"][obj["argument_len"]][0].split("|"))
			
			for index, argument_type in enumerate(obj["params"]["arguments"][obj["argument_len"]][0].split("|")):
				if argument_type == "int":
					if not str(argument).isdigit():
						argument_checker_error -= 1
					else:
						break
				
				elif argument_type == "user":
					if "@" in argument:
						us = await user.get_object_user(argument, obj["message"].chat.id)
						
						if us["id"] == 0:
							obj["attempt_users"].append(argument)
						else:
							obj["users"].append(us)
						
						break
					
					elif "entities" in obj["message"]:
						if "user" in obj["message"]["entities"][index_argument]:
							us = await user.get_object_user(
								obj["message"]["entities"][index_argument]["user"].id,
								obj["message"].chat.id
							)
							
							if us["id"] == 0:
								obj["attempt_users"].append(argument)
							else:
								obj["users"].append(us)
							
							break
					
					obj["arguments_types_error"].append(str(index + 1))
			
			if argument_checker_error == 0:
				obj["arguments_types_error"].append(str(obj["argument_len"]))
			
			obj["argument_len"] += 1
		except KeyError:
			pass
	
	return obj


async def check_errors(message, message_text, params):
	obj = {
		"errors_message": False,
		"args": list(filter(None, message_text.split(" "))),
		"message": message,
		"message_text": message_text,
		"params": params,
		"users": [],
		"attempt_users": [],
		"times_interval": [],
		"argument_len": 1,
		"arguments_types_error": [],
		"bot_obj": await bot.get_me()
	}
	
	obj = await set_arguments_in_message(obj)
	
	if await check_error_type_and_users_and_len_arguments(obj) == 0:
		output = [0, obj["errors_message"]]
	elif await check_error_commands_not_usage_in_bot(obj) == 0:
		output = [0, obj["errors_message"]]
	elif await check_error_user_not_in_base(obj) == 0:
		output = [0, obj["errors_message"]]
	elif await check_error_not_commands_usage_me(obj) == 0:
		output = [0, obj["errors_message"]]
	else:
		output = [1, obj]
	
	return output


async def send_errors(message, usage):
	if usage[1] is not False:
		await message.reply(usage[1], parse_mode="HTML")
