import asyncio
import logging
import os
import random
import re
import io
from datetime import datetime
from ioio import get_exif_coords_from_bytesio

from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.utils.keyboard import InlineKeyboardMarkup
# from aiogram.types import Message, ContentType
from dotenv import load_dotenv

load_dotenv()
bot = Bot(token=os.getenv('TGTOKEN'))
dp = Dispatcher()

logging.basicConfig(level='INFO', datefmt='%Y-%m-%d %H:%M:%S',
                    format='%(asctime)s m:%(module)s l:%(name)s %(levelname)s %(message)s')
logger = logging.getLogger()

def get_random_photo(pic_dir):
    return f'{pic_dir}/{random.choice(os.listdir(pic_dir))}'


async def main():
    for loggers in ['aiogram', 'tzlocal', 'asyncio']:
        logging.getLogger(loggers).setLevel(logging.WARNING)

    logger.info('GPXBaikal bot started successfully!')

    await dp.start_polling(bot)
    return 0


@dp.message(Command('about'))
async def cmd_about(msg: Message):
    pass


@dp.message(Command('help'))
async def cmd_help(msg: Message):

    help_txt = 'HELP TEXT'
    await bot.send_photo(msg.chat.id, types.FSInputFile(get_random_photo('pic')),  caption=help_txt)


@dp.message(Command('start'))
async def cmd_start(msg: Message):
    kb = InlineKeyboardMarkup(inline_keyboard = [
        [types.InlineKeyboardButton(text="\U0001F50E Поехали >", callback_data="letsgo_fwd")],
        [types.InlineKeyboardButton(text="-", callback_data="letsgo_minus"),
         types.InlineKeyboardButton(text="+", callback_data="letsgo_plus")],
        [types.InlineKeyboardButton(text="< Не, лучше туда", callback_data="letsgo_bwd")]
    ])

    start_txt = 'START TEXT'

    # await bot.send_photo(msg.chat.id, types.FSInputFile(get_random_photo('pic')), caption=start_txt, reply_markup=kb_builder.as_markup())
    await bot.send_photo(msg.chat.id, types.FSInputFile(get_random_photo('pic')), caption=start_txt, reply_markup=kb)
    print(f"{datetime.now()} START from {msg.from_user.username} ({msg.from_user.full_name})")


@dp.message(F.document)
async def file_handler(msg: Message):
    with io.BytesIO() as buf2file:
        file_name = msg.document.file_name
        # print(f"{file_name}: {msg.document.mime_type}")
        ff = await bot.get_file(msg.document.file_id)
        file_path = ff.file_path
        await bot.download_file(file_path, buf2file)
        buf2file.seek(0)
        with open(f'upload/{file_name}', 'wb') as f_to_disk:
            f_to_disk.write(buf2file.getbuffer())
        if re.match('^\.jpe?g$',os.path.splitext(file_name)[1].lower()):
            coords = get_exif_coords_from_bytesio(buf2file)
            if coords:
                await msg.reply(f'{coords[0]}, {coords[1]}')
            else:
                await msg.reply(f'Ваш файл не содержит данных о геопозиции')


    # print(ff)
    # '''вставить проверку на соответствие XML-схеме'''
    # if re.search("\.gpx$", file_name.lower()):
    #     await msg.reply(f'Поймал {file_name}')
    #     # ff = await bot.get_file(msg.document.file_id)
    #     # file_path = ff.file_path
    #     await bot.download_file(file_path, f"upload/{file_name}")
    # else:
    #     await msg.reply('Это не GPX-файл... \U0001F92E')


@dp.message(Command('stop'))
async def cmd_stop(msg: Message):
    print(f"{datetime.now()} STOP from {msg.from_user.username} ({msg.from_user.full_name})")
    # await msg.answer('\U0001F644')
    await msg.answer('\U0001F616')


@dp.callback_query(F.data == "letsgo_fwd")
async def inline_letsgo_fwd(callback: types.CallbackQuery):
    await callback.answer('got it!')
    await callback.message.answer('Вперед!')


@dp.callback_query(F.data == "letsgo_bwd")
async def inline_letsgo_bwd(callback: types.CallbackQuery):
    await callback.answer('got it!')
    await callback.message.answer('Назад')


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print('Bot stopped.')
