import config

from systems.group import handler_rates

from systems.group.commands import (
	balance, translation, roulette, twist
)


async def usage_command(message, message_text, numeration_command):
	if numeration_command == 1:
		await balance.main(message, message_text, numeration_command)
	elif numeration_command == 2:
		await translation.main(message, message_text, numeration_command)
	elif numeration_command == 3:
		await roulette.main(message, message_text, numeration_command)
	elif numeration_command == 4:
		await twist.main(message, message_text, numeration_command)


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
	
				if check_command_in_message_text_output[1] == commandSynonyms:
					await usage_command(
						message, check_command_in_message_text_output[0], numerationCommands
					);return
