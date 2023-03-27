from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from systems.private import buttons

from main import bot

from cogs import error, user

from cogs import numberDecoder


async def main(message, message_text, numeration_command):
	usage = await error.check_errors(message, message_text, {
		"arguments": {
			1: ["user"],
		},
		"commands": numeration_command,
		"bot_me": False
	})

	if usage[0] == 1:
		if len(usage[1]["users"]) != 0:
			user_object = usage[1]["users"][0]
		elif "reply_to_message" in message:
			user_object = await user.get_object_user(message.reply_to_message.from_user.id)
		else:
			user_object = await user.get_object_user(message.from_user.id)

		user_balance, reply_markup = int(user_object["b"]), None
		if user_balance <= 0 and message.from_user.id == int(user_object["id"]):
			bot_obj = await bot.get_me()

			reply_markup = InlineKeyboardMarkup(
				inline_keyboard=[
					[
						InlineKeyboardButton(text="Бонус", url="https://t.me/{}?start={}".format(
							bot_obj["username"], buttons.BUTTONS["bonus"]
						))
					]
				]
			)

		await message.reply("<a href=\"{}\"><b>></b></a> {}".format(
			await user.get_link_user(user_object["username"], user_object["id"]),
			await numberDecoder.space_decoder(user_balance)
		), parse_mode="HTML", disable_web_page_preview=True, reply_markup=reply_markup)
	else:
		await error.send_errors(message, usage)
	