from cogs import error


async def main(message, message_text, numeration_command):
	usage = await error.check_errors(message, message_text, {
		"block_arguments": True,
		"commands": numeration_command
	})

	if usage[0] == 1:
		await message.reply("✅ Эту команду больше не нужно использовать. Для упрощения, смысл рулетки был чуть изменён. 💬 Теперь ты можешь сразу делать любую ставку и крутить рулетку без её запуска", parse_mode="HTML")
	else:
		await error.send_errors(message, usage)
