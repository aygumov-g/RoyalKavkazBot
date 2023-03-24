import datetime

from cogs import collection


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

	if datetime.datetime.strptime(collection.users_db[message.from_user.id]["trans"][1], "%Y-%m-%d %H:%M:%S.%f") < time:
		collection.users_db[message.from_user.id]["trans"][1] = str(time)
		collection.users_db[message.from_user.id]["trans"][0] = str(0)
