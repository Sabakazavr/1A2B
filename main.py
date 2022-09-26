import aioschedule
from aiogram.contrib.middlewares.logging import LoggingMiddleware
import logging
import random
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.types.message import ContentType
from aiogram.utils.exceptions import MessageNotModified
from aiogram.dispatcher.filters.state import State, StatesGroup
import datetime
import time
from contextlib import suppress

import messages
import messages as text
from game_with_bot import *
from utils import *
from users import *


# файл конфигурации и переменные
from config import token

# данные, токены и так далее.
bot = Bot(token=token)
dp = Dispatcher(bot, storage=MemoryStorage())
dp.middleware.setup(LoggingMiddleware())

logging.basicConfig(level=logging.INFO)

class Statements(StatesGroup):
    game_bot = State()
    get_nick = State()

@dp.message_handler(commands='start')
async def cmd_start(message: types.Message):
    await message.answer(text=text.start)

@dp.message_handler(commands='set_nickname')
async def get_nick(message: types.Message):
    await message.answer(text=text.get_nick)
    await Statements.get_nick.set()

@dp.message_handler(state=Statements.get_nick)
async def set_nick(message: types.Message, state: FSMContext):
    if len(message.text) <= 10:
        update_nickname(message.from_user.id, message.text)
        await message.answer(text=text.set_nick)
        await state.finish()
    else:
        await message.answer(text=text.wrong_nick)

@dp.message_handler(commands='profile')
async def get_profile(message: types.Message):
    if find_user(message.from_user.id):
        stat = get_all(message.from_user.id)
        await message.answer(f"Твой профиль:\nНикнейм:\t\t{stat[1]}\nЛучший счёт:\t{stat[2]} {move_list[endings(stat[2])]}\nКол-во побед:\t{stat[3]} {win_list[endings(stat[3])]}\nКол-во поражений:\t{stat[4]} {lose_list[endings(stat[4])]}")
    else:
        await message.answer(text=text.none_nickname)

@dp.message_handler(commands='game_with_bot')
async def start_game_with_bot(message: types.Message):
    if find_user(message.from_user.id):
        await message.answer(text=text.new_game)
        delete_moves(message.from_user.id)
        digits = random.sample("1234567890", 4)
        num = "".join(digits)
        move_to_base(message.from_user.id, num, "0", 0, 0, 0)
        await Statements.game_bot.set()
    else:
        await message.answer(text=text.none_nickname)

@dp.message_handler(state=Statements.game_bot)
async def get_number(message: types.Message, state: FSMContext):
    if try_number(message.text):
        last = get_last(message.from_user.id)
        bc = bulls_and_cows(last[0], message.text)
        if bc[0] == 4:
            await message.answer(text=text.win)
            moves = get_last(message.from_user.id)[1] + 1
            best = get_best(message.from_user.id)
            if best == 0 or moves < best:
                update_best(message.from_user.id, moves)
                await message.answer(f"У тебя новый рекорд: {moves} {move_list[endings(moves)]}")
            delete_moves(message.from_user.id)
            await state.finish()
        else:
            move_to_base(message.from_user.id, last[0], message.text, bc[0], bc[1], last[1] + 1)
            history = get_all_moves(message.from_user.id)
            history_txt = "Ещё не угадал. Твои попытки:\n\n"
            for m in history:
                if m[3] != 0:
                    history_txt += f"{m[3]}) {m[0]} Б: {m[1]} К: {m[2]}\n"
            history_txt += "\nПопробуй ещё."
            await message.answer(history_txt)
    else:
        await message.answer("Некорректный ввод")

@dp.message_handler(commands='help')
async def cmd_help(message: types.message):
    await bot.send_message(message.from_user.id, text.commands)

@dp.message_handler()
async def bugs(message: types.Message):
    await message.answer(text.wrong_command)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)