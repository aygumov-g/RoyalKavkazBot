import main

from cogs import collection

import asyncio, datetime


async def load_users_db():
	for userCollection in await main.db2.users.find({}).to_list(None):
		collection.users_db[userCollection["id"]] = userCollection


async def load_roulette_db():
	for rouletteCollection in await main.db1.roulette.find({}).to_list(None):
		collection.roulette_db[rouletteCollection["id"]] = rouletteCollection


async def on_loader():
	tasks = [
		asyncio.create_task(load_users_db()),
		asyncio.create_task(load_roulette_db())
	]

	for task in tasks:
		await task

	print("[{}]: БАЗЫ ЗАГРУЖЕНЫ!".format(datetime.datetime.now()))
