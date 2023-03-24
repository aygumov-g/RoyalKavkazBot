from main import bot

from cogs import user, collection


messages = {}


async def check_error_not_commands_usage_me(key):
	try:
		if (messages[key]["params"]["me"] is False and messages[key]["message"].from_user.id in [int(us["id"]) for us in messages[key]["users"]]) or (messages[key]["params"]["me"] is False and messages[key]["message"].from_user.id == messages[key]["message"].reply_to_message.from_user.id):
			messages[key]["errors_message"] = "🚫 Ты не можешь применить эту команду к себе"
			return 0
	except AttributeError:
		pass
	except KeyError:
		pass


async def check_error_commands_not_usage_in_bot(key):
	try:
		if messages[key]["params"]["bot_me"] is False and messages[key]["bot_obj"].id in [int(i["id"]) for i in messages[key]["users"]] or messages[key]["message"].reply_to_message.from_user.id == messages[key]["bot_obj"].id:
			messages[key]["errors_message"] = "🚫 На мне эта команда не работает"
			return 0
	except AttributeError:
		pass
	except KeyError:
		pass


async def check_error_user_not_in_base(key):
	if "reply_to_message" in messages[key]["message"] and not messages[key]["message"].reply_to_message.from_user.id in collection.users_db:
		messages[key]["errors_message"] = "🚫 Пользователь отсутсвует в базе"
		return 0


async def check_error_type_and_users_and_len_arguments(key):
	if "block_arguments" in messages[key]["params"] and len(messages[key]["args"]) != 0:
		"""Были прописаны аргументы в команде в которой не должны были"""
		return 0

	elif "arguments" in messages[key]["params"] and len(messages[key]["params"]["arguments"]) < len(messages[key]["args"]):
		"""Неправильное количество аргументов в команде"""
		return 0
	
	elif len(messages[key]["arguments_types_error"]) != 0:
		"""Неправильный тип аргумента в команде"""
		return 0
	
	elif len(messages[key]["attempt_users"]) != 0:
		messages[key]["errors_message"] = "🚫 Пользователь отсутствует либо в беседе, либо в базе бота"
		return 0


async def set_arguments_in_message(key):
	for index_argument, argument in enumerate(messages[key]["args"]):
		try:
			argument_checker_error = len(messages[key]["params"]["arguments"][messages[key]["argument_len"]][0].split("|"))

			for index, argument_type in enumerate(messages[key]["params"]["arguments"][messages[key]["argument_len"]][0].split("|")):
				if argument_type == "int":
					if not str(argument).isdigit():
						argument_checker_error -= 1
					else:
						break
				
				elif argument_type == "user":
					if "@" in argument:
						us = await user.get_object_user(argument, messages[key]["message"].chat.id)
						
						if us["id"] == 0:
							messages[key]["attempt_users"].append(argument)
						else:
							messages[key]["users"].append(us)
						
						break
					
					elif "entities" in messages[key]["message"]:
						if "user" in messages[key]["message"]["entities"][index_argument]:
							us = await user.get_object_user(
								messages[key]["message"]["entities"][index_argument]["user"].id,
								messages[key]["message"].chat.id
							)
							
							if us["id"] == 0:
								messages[key]["attempt_users"].append(argument)
							else:
								messages[key]["users"].append(us)
							
							break

					messages[key]["arguments_types_error"].append(str(index + 1))
			
			if argument_checker_error == 0:
				messages[key]["arguments_types_error"].append(str(messages[key]["argument_len"]))
			
			messages[key]["argument_len"] += 1
		except KeyError:
			pass


async def check_errors(message, message_text, params):
	key = "{}%{}%{}".format(message.message_id, message.from_user.id, message.chat.id)
	
	messages[key] = {
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
	
	await set_arguments_in_message(key)
	
	if await check_error_type_and_users_and_len_arguments(key) == 0:
		output = [0, messages[key]["errors_message"]]
	elif await check_error_commands_not_usage_in_bot(key) == 0:
		output = [0, messages[key]["errors_message"]]
	elif await check_error_user_not_in_base(key) == 0:
		output = [0, messages[key]["errors_message"]]
	elif await check_error_not_commands_usage_me(key) == 0:
		output = [0, messages[key]["errors_message"]]
	else:
		output = [1, messages[key]]
	
	try:
		del messages[key]
	except KeyError:
		pass
	
	return output


async def send_errors(message, usage):
	if usage[1] is not False:
		await message.reply(usage[1], parse_mode="HTML")
