import main

from cogs import collection

import asyncio, datetime


SAVE_DB_TIME = datetime.datetime.now()
SAVE_DB_TIMEOUT = 3600


async def unload_users_db():
	if len(collection.users_db) != 0:
		list_unload = [{"id": i, **collection.users_db[i]} for i in collection.users_db]

		await main.db2.users.delete_many({})
		await main.db2.users.insert_many(list_unload)

		await main.db2Backup.users.delete_many({})
		await main.db2Backup.users.insert_many(list_unload)


async def unload_roulette_db():
	if len(collection.roulette_db) != 0:
		list_unload = [{"id": i, **collection.roulette_db[i]} for i in collection.roulette_db]

		await main.db1.roulette.delete_many({})
		await main.db1.roulette.insert_many(list_unload)


async def unload_log_db():
	if len(collection.log_db) != 0:
		list_unload = [{"id": i, **collection.log_db[i]} for i in collection.log_db]

		await main.db1.log.delete_many({})
		await main.db1.log.insert_many(list_unload)


async def on_unloader(reload=None):
	global SAVE_DB_TIME
	
	if SAVE_DB_TIME <= datetime.datetime.now() or reload is not None:
		SAVE_DB_TIME = datetime.datetime.now() + datetime.timedelta(seconds=SAVE_DB_TIMEOUT)
		
		tasks = [
			asyncio.create_task(unload_users_db()),
			asyncio.create_task(unload_roulette_db()),
			asyncio.create_task(unload_log_db())
		]
		
		for task in tasks:
			await task
		
		print("[{}]: ОБНОВЛЕНИЯ ОТПРАВЛЕНЫ!".format(datetime.datetime.now()))
