import config

from aiogram import Bot
from aiogram.dispatcher import Dispatcher

from cogs.funCollection import loader, unloader

import motor.motor_asyncio

import datetime

bot = Bot(token=config.TOKEN)
dp = Dispatcher(bot)

db1 = motor.motor_asyncio.AsyncIOMotorClient(config.TOKEN_BD1).Royal
db2 = motor.motor_asyncio.AsyncIOMotorClient(config.TOKEN_BD2).main


async def on_startup(dp):
	print("[{}]: ЗАПУЩЕНО!".format(datetime.datetime.now()))
	
	for numerationCommands in config.COMMANDS:
		newCommandsList = []
		
		for commandSynonyms in config.COMMANDS[numerationCommands]["usage"]:
			if commandSynonyms[0] != "^":
				newCommandsList.append(commandSynonyms)
			else:
				commandSynonyms = commandSynonyms[1:]
			
			for prefix in config.PREFIXES:
				newCommandsList.append("{}{}".format(prefix, commandSynonyms))
		
		config.COMMANDS[numerationCommands]["usage"] = newCommandsList

	await loader.on_loader()


async def on_shutdown(dp):
	print("[{}]: СОХРАНЕНИЕ...".format(datetime.datetime.now()))
	await unloader.on_unloader(1)


if __name__ == "__main__":
	from aiogram.utils import executor
	from handlers import dp
	
	executor.start_polling(dp, on_startup=on_startup, on_shutdown=on_shutdown)
