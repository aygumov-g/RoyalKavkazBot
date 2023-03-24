async def slicer(text, max_chars):
	if len(text) > int(max_chars):
		output = text[:-(len(text) - int(max_chars if len(text) < 3 else max_chars - 3))] + "..."
	else:
		output = text

	return output


async def HTML_slicer(text, max_chars):
	if len(text) > int(max_chars):
		output = text[:-(len(text) - int(max_chars if len(text) < 3 else max_chars - 3))] + "<code>.</code><code>.</code><code>.</code>"
	else:
		output = text

	return output
