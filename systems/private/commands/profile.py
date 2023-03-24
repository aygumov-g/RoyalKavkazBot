from cogs import user

from cogs import numberDecoder


async def send(message):
	user_object = await user.get_object_user(message.from_user.id)

	output = "💰 Твой баланс: {}".format(
		await numberDecoder.space_decoder(user_object["b"])
	)
	
	await message.reply(output, parse_mode="HTML", disable_web_page_preview=True)
