from systems.private.commands import (
	start,
	bonus,
	profile
)

from systems.private import buttons


async def check_usage_command(message):
	if "/start" in message.text and message.text[:6] == "/start":
		await start.send(message)
	elif message.text == "/bonus":
		await bonus.send(message)
	elif message.text == "/profile" or message.text == buttons.BUTTONS["profile"]:
		await profile.send(message)
