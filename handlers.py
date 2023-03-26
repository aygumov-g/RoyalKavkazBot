from aiogram import types, filters

from systems.private import distributor

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
	await saver.save_users_db(message)

	await engine.check_usage_command(message)

	await unloader.on_unloader()
