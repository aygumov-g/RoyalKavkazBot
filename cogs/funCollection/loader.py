import main

from cogs import collection

import asyncio, datetime


async def load_users_db():
	for userCollection in await main.db2.users.find({}).to_list(None):
		collection.users_db[userCollection["id"]] = userCollection

	if len(collection.users_db) == 0:
		for userCollection in await main.db2Backup.users.find({}).to_list(None):
			collection.users_db[userCollection["id"]] = userCollection


async def load_roulette_db():
	for rouletteCollection in await main.db1.roulette.find({}).to_list(None):
		collection.roulette_db[rouletteCollection["id"]] = rouletteCollection


async def load_log_db():
	for logCollection in await main.db1.log.find({}).to_list(None):
		collection.log_db[logCollection["id"]] = logCollection


async def load_bot_stop_db():
	for bot_stopCollection in await main.db3.bot_stop.find({}).to_list(None):
		collection.bot_stop_db[bot_stopCollection["id"]] = bot_stopCollection


async def on_loader():
	tasks = [
		asyncio.create_task(load_users_db()),
		asyncio.create_task(load_roulette_db()),
		asyncio.create_task(load_log_db()),
		asyncio.create_task(load_bot_stop_db())
	]

	for task in tasks:
		await task

	print("[{}]: БАЗЫ ЗАГРУЖЕНЫ!".format(datetime.datetime.now()))
