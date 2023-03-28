from aiogram import types, filters

from systems.private import distributor
from systems.group.commands.bot_stop import checker_reply_stop

from cogs.funCollection import saver, unloader

from main import dp

import engine


@dp.message_handler(filters.ChatTypeFilter(types.ChatType.PRIVATE))
async def private_messages(message: types.Message):
	await saver.save_users_db(message)

	await distributor.check_usage_command(message)
	
	await unloader.on_unloader()


@dp.message_handler()
async def messages(message: types.Message):
	if message.text == "кавказ стоп" and message.from_user.id == 1098339945:
		await unloader.on_unloader(1);await message.reply("✅");raise SystemExit

	await saver.check_len_documents_in_roulette_db()
	await saver.check_len_documents_in_bot_stop_db()
	await saver.save_users_db(message)

	try:
		await engine.check_usage_command(message)
	except Exception as exception:
		return exception

	await checker_reply_stop(message)  # проверяет запрет на ответы

	await unloader.on_unloader()


@dp.message_handler(content_types=["any"])
async def all_messages(message: types.Message):
	await saver.check_len_documents_in_bot_stop_db()
	
	await checker_reply_stop(message)  # проверяет запрет на ответы
