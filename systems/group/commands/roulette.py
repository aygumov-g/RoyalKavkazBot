from cogs import error, collection

import datetime


async def main(message, message_text, numeration_command):
	usage = await error.check_errors(message, message_text, {
		"block_arguments": True,
		"commands": numeration_command,
		"bot_me": False
	})

	if usage[0] == 1:
		if not message.chat.id in collection.roulette_db:
			collection.roulette_db[message.chat.id] = {
				"id": message.chat.id,
				"reg": str(datetime.datetime.now()),
				"rates": []
			}

			output = "▶️ Рулетка запущена. Ставки может делать любой участник чата. Пример: <code>5 на к</code>, <code>100 на чёрное</code>, <code>500 на 0</code>\n🚫 Префиксы в ставках не поддерживаются\n\n💬 Меню с кнопками скоро добавим"
		else:
			output = "🚫 Сделай ставку, в этом чате уже запущена рулетка"
		
		await message.reply(output, parse_mode="HTML")
	else:
		await error.send_errors(message, usage)
