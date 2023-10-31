import asyncio

from aiogram import Bot, Dispatcher

from aiogram.filters import Command
from aiogram.types import Message
import json
from query import do_group, WrongGroupingRangeException
from db import get_client
from config import settings


bot = Bot(token=settings.bot_token)
dp=Dispatcher()

db_client = get_client()
collection = db_client.test.payments



@dp.message(Command("start"))
async def start(message: Message):
    await message.answer(f"Hello, {message.from_user.first_name}")



@dp.message()
async def echo(message: Message):
    request = message.text

    try:
        request = json.loads(request)
    except Exception as e:
        print(e)

    try :
        result = do_group(collection,request["dt_from"], request["dt_upto"], request["group_type"])

    except WrongGroupingRangeException:
        result = 'Невалидный запос. Пример запроса: \n \
{"dt_from": "2022-09-01T00:00:00", "dt_upto": "2022-12-31T23:59:00", "group_type": "month"}'
    except ValueError:
        result = 'Невалидный запос. Пример запроса: \n \
{"dt_from": "2022-09-01T00:00:00", "dt_upto": "2022-12-31T23:59:00", "group_type": "month"}'
    except TypeError:
        result = 'Невалидный запос. Пример запроса: \n \
{"dt_from": "2022-09-01T00:00:00", "dt_upto": "2022-12-31T23:59:00", "group_type": "month"}'

    await message.answer(json.dumps(result))

    # await message.answer(message.text)



async def main():
    # print("Bot started")
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
