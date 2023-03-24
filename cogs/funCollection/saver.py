from cogs import collection


async def save_users_db(message):
	if not message.from_user.id in collection.users_db:
		collection.users_db[message.from_user.id] = {
			"id": message.from_user.id,
			"first_name": str(message.from_user.first_name),
			"username": str(message.from_user.username),
			"b": str(5000)
		}

	collection.users_db[message.from_user.id]["first_name"] = message.from_user.first_name
	collection.users_db[message.from_user.id]["username"] = message.from_user.username
	