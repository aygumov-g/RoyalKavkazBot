from cogs import word

import datetime, random, re

import config


async def decoder(time_array):
	if time_array[1] in config.TIMES[0]:
		retTime = datetime.datetime.now() + datetime.timedelta(seconds=int(time_array[0]))
	elif time_array[1] in config.TIMES[1]:
		retTime = datetime.datetime.now() + datetime.timedelta(minutes=int(time_array[0]))
	elif time_array[1] in config.TIMES[2]:
		retTime = datetime.datetime.now() + datetime.timedelta(hours=int(time_array[0]))
	elif time_array[1] in config.TIMES[3]:
		retTime = datetime.datetime.now() + datetime.timedelta(hours=24*int(time_array[0]))
	elif time_array[1] in config.TIMES[4]:
		retTime = datetime.datetime.now() + datetime.timedelta(hours=168*int(time_array[0]))
	elif time_array[1] in config.TIMES[5]:
		retTime = datetime.datetime.now() + datetime.timedelta(hours=720*int(time_array[0]))
	elif time_array[1] in config.TIMES[6]:
		retTime = datetime.datetime.now() + datetime.timedelta(hours=8760*int(time_array[0]))
	else:
		retTime = datetime.datetime.now()

	return retTime


async def decodate(date):
	date_now = datetime.datetime.now()
	result = []

	if datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S.%f") > date_now:
		date_obj = re.split(", |:|\.| ", str(datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S.%f") - date_now))
	else:
		date_obj = re.split(", |:|\.| ", str(date_now - datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S.%f")))

	if len(date_obj) == 6:
		del date_obj[5]

	if len(date_obj) == 5:
		days = int(date_obj[0])

		if days >= 30:
			result.append("{} {}".format(days // 30, await word.ending("месяц|месяца|месяцев", days // 30)))
			days %= 30 * (days // 30)
		elif days >= 7:
			result.append("{} {}".format(days // 7, await word.ending("неделя|недели|недель", days // 7)))
			days %= 7 * (days // 7)
		if days != 0:
			result.append("{} {}".format(days, await word.ending("день|дня|дней", days)))

		del date_obj[1]
		del date_obj[0]

	if int(date_obj[0]) > 0:
		result.append("{} {}".format(int(date_obj[0]), await word.ending("час|часа|часов", int(date_obj[0]))))
	if int(date_obj[1]) > 0:
		result.append("{} {}".format(int(date_obj[1]), await word.ending("минута|минуты|минут", int(date_obj[1]))))
	if int(date_obj[2]) > 0:
		result.append("{} {}".format(int(date_obj[2]), await word.ending("секунда|секунды|секунд", int(date_obj[2]))))

	if len(result) == 0:
		milliseconds = random.randint(1, 1000)

		return "{} {}".format(
			milliseconds, await word.ending("миллисекунда|миллисекунды|миллисекунд", milliseconds)
		)
	else:
		return "{}".format(result[0]) if len(result) == 1 else "{} {}".format(result[0], result[1])


async def get_time_is_str(time_str):
	try:
		time_str_output = datetime.datetime.strptime(str(time_str), "%Y-%m-%d %H:%M:%S.%f")
	except ValueError:
		time_str_output = datetime.datetime.strptime(str(time_str), "%Y-%m-%d %H:%M:%S")
	
	return time_str_output
