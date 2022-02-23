from aiogram import types

# Кнопки главного меню
keyboard_main = types.ReplyKeyboardMarkup()
keyboard_main.add('🔑 Запустить переводы')
keyboard_main.add('💰 Проверить баланс', '⚙ Настройки')
keyboard_main.resize_keyboard = True

# Кнопки настроек
keyboard_settings = types.ReplyKeyboardMarkup()
keyboard_settings.add('📋 Список кошельков')
keyboard_settings.add('✅ Добавить кошелек', '❌ Удалить кошелек')
keyboard_settings.add('⬇ Главное меню')
keyboard_settings.resize_keyboard = True

# Кнопки подтверждения
keyboard_confirm = types.ReplyKeyboardMarkup()
keyboard_confirm.add('✔ Да', '❌ Нет')
keyboard_confirm.resize_keyboard = True

# Кнопки остановки
keyboard_cancel = types.ReplyKeyboardMarkup()
keyboard_cancel.add('❌ Остановить')
keyboard_cancel.resize_keyboard = True

# Кнопки выбора действий
keyboard_task = types.ReplyKeyboardMarkup()
keyboard_task.add('🔑 Запустить проверку баланса', '🔑 Запустить переводы')
