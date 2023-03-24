async def space_decoder(num):
	reversed_num, len_space, output = str(num)[::-1], 0, ""
	
	for index, char in enumerate(reversed_num):
		output += char
		
		if (index + 1) % 3 == 0 and len(output) != len(reversed_num) + len_space:
			len_space += 1
			output += " "
	
	return output[::-1]
