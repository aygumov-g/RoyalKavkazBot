from systems.private.commands import bonus
from systems.private import buttons

from cogs import user, slicer


output = """
👋 Приветствует, <a href="{{userLink}}"><b>{{userName}}</b></a> в нашем проекте. Так как мы только начинаем, проект немного сыроват но это как ты понимаешь временно!
🅾️ Если вдруг у тебя закончаться монеты, то пропиши <b>/bonus</b>
"""


async def send(message):
	message_text_list = message.text.split(" ")
	
	if len(message_text_list) == 1:
		await message.reply(output.replace(
			"{{userLink}}", await user.get_link_user(
				message.from_user.username,
				message.from_user.id
			)
		).replace(
			"{{userName}}", await slicer.slicer(
				await user.get_name_user(
					message.from_user.first_name,
					message.from_user.username,
					message.from_user.id
				), 10
			)
		), parse_mode="HTML", disable_web_page_preview=True, reply_markup=buttons.main)
	elif message_text_list[1] == buttons.BUTTONS["bonus"]:
		await bonus.send(message)
