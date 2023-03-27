import config

from systems.group import handler_rates

from systems.group.commands import (
	balance, translation, roulette, twist, log, add, global_nick, repeat, cancel
)


async def usage_command(message, message_text, numeration_command, command_text):
	if numeration_command == 1:
		await balance.main(message, message_text, numeration_command)
	elif numeration_command == 2:
		await translation.main(message, message_text, numeration_command)
	elif numeration_command == 3:
		await roulette.main(message, message_text, numeration_command)
	elif numeration_command == 4:
		await twist.main(message, message_text, numeration_command)
	elif numeration_command == 5:
		await log.main(message, message_text, numeration_command)
	elif numeration_command == 6:
		await add.main(message, message_text, numeration_command)
	elif numeration_command == 7:
		await global_nick.main(message, message_text, numeration_command, command_text)
	elif numeration_command == 8:
		await repeat.main(message, message_text, numeration_command)
	elif numeration_command == 9:
		await cancel.main(message, message_text, numeration_command)


async def check_call_usage_command(message, numeration_command):
	output = True

	if "call" in config.COMMANDS[numeration_command] and not message.from_user.id in config.COMMANDS[numeration_command]["call"]:
		output = False
	
	return output


async def check_command_in_message_text(command, message_text):
	message_text_lower, commandOutput = message_text.lower(), ""
	
	if message_text_lower[:len(command) + 1] == "{} ".format(command):
		commandOutput = command
		command = "{} ".format(command)
	
	elif message_text_lower[:len(command)] == command:
		commandOutput = command

	return [message_text[len(command):], commandOutput]


async def dell_space_in_prefix(message_text):
	for i in range(len(message_text)):
		for prefix in config.PREFIXES:
			if message_text[:len(prefix) + 1] == "{} ".format(prefix):
				message_text = "{}{}".format(prefix, message_text[len(prefix) + 1:])
	
	return message_text


async def message_text_format(message_text):
	for i in range(len(message_text)):
		if "  " in message_text:
			message_text = message_text.replace("  ", " ")
		
		if "\n" in message_text:
			message_text = message_text.replace("\n", " ")
	
	return message_text


async def check_usage_command(message):
	message_text = await message_text_format(message.text)
	message_text = await dell_space_in_prefix(message_text)

	if await handler_rates.main(message) is False:
		for numerationCommands in config.COMMANDS:
			for commandSynonyms in config.COMMANDS[numerationCommands]["usage"]:
				check_command_in_message_text_output = await check_command_in_message_text(
					commandSynonyms, message_text
				)

				if check_command_in_message_text_output[1] == commandSynonyms and await check_call_usage_command(message, numerationCommands):
					await usage_command(
						message, check_command_in_message_text_output[0], numerationCommands, check_command_in_message_text_output[1]
					);return
