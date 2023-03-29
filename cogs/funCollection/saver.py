import datetime

from cogs import collection

from cogs import timeDecoder


async def save_users_db(message):
	time = datetime.datetime.now()

	if not message.from_user.id in collection.users_db:
		collection.users_db[message.from_user.id] = {
			"id": message.from_user.id,
			"first_name": str(message.from_user.first_name),
			"username": str(message.from_user.username),
			"trans": [str(0), str(time)],
			"bonus": str(time),
			"b": str(5000)
		}

	collection.users_db[message.from_user.id]["first_name"] = message.from_user.first_name
	collection.users_db[message.from_user.id]["username"] = message.from_user.username

	if await timeDecoder.get_time_is_str(collection.users_db[message.from_user.id]["trans"][1]) < time:
		collection.users_db[message.from_user.id]["trans"][1] = str(time)
		collection.users_db[message.from_user.id]["trans"][0] = str(0)


async def check_len_documents_in_roulette_db():
	if not -1 in collection.roulette_db:
		collection.roulette_db[-1] = {
			"id": -1,
			"warning": "Не удалять! Нужен для правильной работы."
		}


async def check_len_documents_in_bot_stop_db():
	if not -1 in collection.bot_stop_db:
		collection.bot_stop_db[-1] = {
			"id": -1,
			"warning": "Не удалять! Нужен для правильной работы."
		}
