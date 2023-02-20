import config
from aiogram import Bot, Dispatcher, executor, types
import get_info
import time
bot = Bot(token=config.API_TOKEN)

dp = Dispatcher(bot)


update_list = []

@dp.message_handler(commands=['start'])
async def main_bot_work(message:types.Message):
	while True:
		print("started parsing")
		links = get_info.parse()
		count = 0
		for i in links:
			if i in update_list:
				print('already in update_list')
				continue
			else:
				update_list.append(i)
				await message.answer(i)
				count += 1
		await message.answer(f"Новых объявлений: {count}")
		print("going to sleep")
		time.sleep(10)                             

if __name__ == '__main__':
	executor.start_polling(dp,skip_updates=True)
    














