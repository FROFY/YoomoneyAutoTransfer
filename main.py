import telegram.Handlers

from aiogram.utils import executor


if __name__ == '__main__':
    executor.start_polling(telegram.Handlers.dp)
