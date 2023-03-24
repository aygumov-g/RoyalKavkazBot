async def ending(words, tp):
	words_list = words.split("|")

	if tp % 10 == 1 and tp % 100 != 11:
		return words_list[0]
	elif 2 <= tp % 10 <= 4 and (tp % 100 < 10 or tp % 100 > 20):
		return words_list[1]
	else:
		return words_list[2]
