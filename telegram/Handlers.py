from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.dispatcher.filters import Text, Command

import telegram.Keyboards
import asyncio
from telegram.States import StatesBot
from yoomoney.API import *

bot = Bot(Config.bot_token)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


@dp.message_handler(commands=['start'], state=None)
async def start(message: types.Message):
    await bot.send_message(message.from_user.id, 'Made by FROFY', reply_markup=telegram.Keyboards.keyboard_main)


@dp.message_handler(commands=['balance'], state=None)
async def bal(message: types.Message):
    for token in SQLite.db_get_all():
        await bot.send_message(message.from_user.id, balance(token[0]), get_number(token[0]))


@dp.message_handler(commands=['cancel', 'menu'], state='*')
@dp.message_handler(Text(equals='⬇ Главное меню', ignore_case=True), state='*')
@dp.message_handler(Text(equals='❌ Остановить', ignore_case=True), state='*')
async def mainMenu(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        await bot.send_message(message.from_user.id, 'Главное меню', reply_markup=telegram.Keyboards.keyboard_main)
    else:
        await state.finish()
        await bot.send_message(message.from_user.id, 'Главное меню', reply_markup=telegram.Keyboards.keyboard_main)


@dp.message_handler(Text(equals='✅ Добавить кошелек', ignore_case=True), state=None)
async def add_token(message: types.Message):
    await bot.send_message(message.from_user.id, 'Введите redirect_uri', reply_markup=types.ReplyKeyboardRemove())
    await StatesBot.token_add.set()


@dp.message_handler(Text(equals='💰 Проверить баланс', ignore_case=True), state=None)
async def check_balance(message: types.Message):
    for access_token in SQLite.db_get_all():
        await bot.send_message(message.from_user.id, f'Кошелек {SQLite.db_get_account(access_token[0])}\n'
                                                     f'Баланс {balance(access_token[0])}')
        await asyncio.sleep(1)


@dp.message_handler(Text(equals='📋 Список кошельков', ignore_case=True), state=None)
async def show_wallets(message: types.Message):
    for access_token in SQLite.db_get_all():
        await bot.send_message(message.from_user.id, f'{SQLite.db_get_account(access_token[0])}')


@dp.message_handler(Text(equals='⚙ Настройки', ignore_case=True), state=None)
async def settings(message: types.Message):
    await bot.send_message(message.from_user.id, 'Настройки', reply_markup=telegram.Keyboards.keyboard_settings)


@dp.message_handler(Text(equals='❌ Удалить кошелек', ignore_case=True), state=None)
async def delete_wallet(message: types.Message):
    await bot.send_message(message.from_user.id, 'Введите номер кошелька для удаления',
                           reply_markup=types.ReplyKeyboardRemove())

    await StatesBot.token_delete.set()


@dp.message_handler(Text(equals='🔑 Запустить переводы', ignore_case=True), state=None)
async def checking(message: types.Message):
    access_tokens = SQLite.db_get_all()

    if access_tokens[0] is None:
        await bot.send_message(message.from_user.id, 'У вас нет добавленных кошельков')
        return

    await bot.send_message(message.from_user.id, 'Вы уверены?',
                           reply_markup=telegram.Keyboards.keyboard_confirm)

    await StatesBot.balance_checking.set()


@dp.message_handler(state=StatesBot.balance_checking)
async def balance_checking(message: types.Message, state: FSMContext):
    if message.text == '❌ Нет':
        await bot.send_message(message.from_user.id, 'Проверка отменена', reply_markup=telegram.Keyboards.keyboard_main)
        await state.finish()
        return
    elif message.text == '✔ Да':
        await bot.send_message(message.from_user.id, 'Была запущена проверка',
                               reply_markup=telegram.Keyboards.keyboard_cancel)

        access_tokens = SQLite.db_get_all()

        while await state.get_state() is not None:
            for access_token in access_tokens:
                if int(balance(access_token[0]) > 10):
                    success, status = transfer(access_token[0])
                    if not success:
                        await bot.send_message(message.from_user.id,
                                               f'Произошла ошибка при переводе с кошелька '
                                               f'{get_number(access_token[0])}\n{status}\n')
                        # await state.finish()
                    else:
                        await bot.send_message(message.from_user.id, f'Выполнен перевод с кошелька '
                                                                     f'{get_number(access_token[0])}\n'
                                                                     f'Баланс {status}')
                        await asyncio.sleep(10)
                else:
                    await bot.send_message(message.from_user.id, 'Баланс меньше 10р')
                    await asyncio.sleep(5)
            await asyncio.sleep(5)


@dp.message_handler(state=StatesBot.token_delete)
async def delete(message: types.Message, state: FSMContext):

    await state.finish()

    await bot.send_message(message.from_user.id, SQLite.db_table_delete(message.text), reply_markup=telegram.Keyboards.keyboard_main)
