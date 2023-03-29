from cogs import error, user

from cogs import numberDecoder

import random


EMOJIS = list("🍏🍎🍐🍊🍋🍌🍉🍇🍓🫐🍈🍒🍑🥭🍍🥥🥝🍅🍆🥑🥦🥬🥒🌽🥕")


async def update_user_balance(user_object, check_winner, rate):
	if check_winner is True:
		user_object["b"] = str(int(user_object["b"]) + int(rate))
	else:
		user_object["b"] = str(int(user_object["b"]) - int(rate))


async def main(message, message_text, numeration_command):
	usage = await error.check_errors(message, message_text, {
		"arguments": {
			1: ["int"],
		},
		"commands": numeration_command
	})

	if usage[0] == 1:
		if len(usage[1]["args"]) != 0:
			user_object = await user.get_object_user(message.from_user.id)

			if str(usage[1]["args"][0]) != "0":
				if int(user_object["b"]) >= int(usage[1]["args"][0]):
					randomEmoji = random.choice(EMOJIS)
					messageEmoji = [randomEmoji] * 3
					ball = random.randint(1, 4)
		
					check_winner = True
					if ball != 3:
						for i in range(3):
							lossEmoji = randomEmoji
							for j in range(10):
								if lossEmoji != randomEmoji:
									break
								lossEmoji = random.choice(EMOJIS)
							messageEmoji[random.randint(1, 3) - 1] = lossEmoji
						check_winner = False
		
					output = "[%emoji%]: %result%\n<code>%resultSim%</code> <a href=\"%userLink%\">%userName%</a> <code>></code> %rate%".replace(
						"%emoji%", " | ".join(messageEmoji)
					).replace(
						"%result%", "ВЫИГРЫШ" if check_winner is True else "ПРОИГРЫШ"
					).replace(
						"%resultSim%", "+" if check_winner is True else "-"
					).replace(
						"%userLink%", str(await user.get_link_user(message.from_user.username, message.from_user.id))
					).replace(
						"%userName%", str(await user.get_name_user(message.from_user.first_name, message.from_user.username, message.from_user.id))
					).replace(
						"%rate%", str(await numberDecoder.space_decoder(
							usage[1]["args"][0] if check_winner is False else int(usage[1]["args"][0]) * 2
						))
					)

					await update_user_balance(user_object, check_winner, int(usage[1]["args"][0]))
				elif int(user_object["b"]) == "0":
					output = "🚫 У тебя нет монет"
				else:
					output = "🚫 У тебя нет столько монет"
			else:
				output = "🚫 Такие ставки не принимаются"

			await message.reply(output, parse_mode="HTML", disable_web_page_preview=True)
			
	else:
		await error.send_errors(message, error)
