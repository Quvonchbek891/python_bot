import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton

# Токен вашего бота (замените на свой)
TOKEN = ""

# Создаем объект бота
bot = telebot.TeleBot(TOKEN)

# Словарь для временного хранения данных регистрации
user_data = {}

# Функция для создания клавиатуры основного меню
def create_main_menu():
    markup = InlineKeyboardMarkup()
    markup.row(InlineKeyboardButton("🍕 Выбрать комбо на большую компанию 3 пиццы от 99 000", callback_data='combo_big'))
    markup.row(InlineKeyboardButton("🍕 100% Халал", callback_data='halal'))
    markup.row(InlineKeyboardButton("🍹 Круглосуточная доставка по Ташкенту", callback_data='delivery'))
    markup.row(InlineKeyboardButton("🍕 35 дақиқада бепул уетказиб бериш ёки пицца совға", callback_data='fast_delivery'))
    markup.row(InlineKeyboardButton("🍕 100% Халал", callback_data='halal_2'))
    markup.row(InlineKeyboardButton("📞 Тошкент бўйича уйгʻун-кун уетказиб бериш", callback_data='tashkent_delivery'))
    markup.row(InlineKeyboardButton("📞 Call-center: +998 93 669 6688", callback_data='call_center'))
    markup.row(InlineKeyboardButton("🚀 Буюртма бериш учун /start тугмасини босинг", callback_data='restart'))
    return markup

# Функция для создания меню пицц
def create_pizza_menu():
    markup = InlineKeyboardMarkup()
    markup.row(InlineKeyboardButton("🍕 Пепперони", callback_data='pizza_pepperoni'))
    markup.row(InlineKeyboardButton("🍕 Маргарита", callback_data='pizza_margherita'))
    markup.row(InlineKeyboardButton("🍕 Четыре сыра", callback_data='pizza_four_cheese'))
    return markup

# Функция для создания клавиатуры с кнопкой "Поделиться номером"
def create_phone_keyboard():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add(KeyboardButton("Поделиться номером телефона", request_contact=True))
    return markup

# Проверка, зарегистрирован ли пользователь
def is_user_registered(user_id):
    try:
        with open("users.txt", "r", encoding="utf-8") as file:
            for line in file:
                if str(user_id) in line:
                    return True
    except FileNotFoundError:
        return False
    return False

# Сохранение данных пользователя
def save_user(user_id, name, phone):
    with open("users.txt", "a", encoding="utf-8") as file:
        file.write(f"UserID: {user_id}, Name: {name}, Phone: {phone}\n")

# Обработчик команды /start
@bot.message_handler(commands=['start1'])
def send_welcome(message):
    user_id = message.from_user.id
    if is_user_registered(user_id):
        bot.reply_to(message, "Вы уже зарегистрированы! ЧТО МОЖЕТ ЭТОТ БОТ?", reply_markup=create_main_menu())
    else:
        bot.reply_to(message, "Добро пожаловать! Давайте зарегистрируем вас. Как вас зовут?")
        bot.register_next_step_handler(message, get_name)

# Получение имени пользователя
def get_name(message):
    user_id = message.from_user.id
    name = message.text
    user_data[user_id] = {"name": name}
    bot.reply_to(message, "Отлично! Теперь поделитесь вашим номером телефона.", reply_markup=create_phone_keyboard())
    bot.register_next_step_handler(message, get_phone)

# Получение номера телефона
@bot.message_handler(content_types=['contact'])
def get_phone(message):
    user_id = message.from_user.id
    if message.contact:
        phone = message.contact.phone_number
        name = user_data.get(user_id, {}).get("name", "Unknown")
        save_user(user_id, name, phone)
        bot.reply_to(message, f"Регистрация завершена, {name}! Теперь вы можете пользоваться ботом.", reply_markup=telebot.types.ReplyKeyboardRemove())
        bot.send_message(message.chat.id, "ЧТО МОЖЕТ ЭТОТ БОТ?", reply_markup=create_main_menu())
    else:
        bot.reply_to(message, "Пожалуйста, отправьте ваш номер телефона, нажав на кнопку.", reply_markup=create_phone_keyboard())

# Обработчик команды /menu
@bot.message_handler(commands=['menu'])
def show_menu(message):
    user_id = message.from_user.id
    if is_user_registered(user_id):
        bot.reply_to(message, "Выберите пиццу:", reply_markup=create_pizza_menu())
    else:
        bot.reply_to(message, "Пожалуйста, сначала зарегистрируйтесь с помощью команды /start.")

# Обработчик команды /order
@bot.message_handler(commands=['order'])
def handle_order(message):
    user_id = message.from_user.id
    if is_user_registered(user_id):
        bot.reply_to(message, "Ваш заказ принят! Мы свяжемся с вами для подтверждения. Call-center: +998 93 669 6688.")
    else:
        bot.reply_to(message, "Пожалуйста, сначала зарегистрируйтесь с помощью команды /start1.")

# Обработчик нажатий на кнопки
@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    user_id = call.from_user.id
    if not is_user_registered(user_id):
        bot.send_message(call.message.chat.id, "Пожалуйста, сначала зарегистрируйтесь с помощью команды /start.")
        return

    if call.data == 'combo_big':
        bot.send_message(call.message.chat.id, "Вы выбрали комбо на большую компанию (3 пиццы от 99 000). Хотите оформить заказ? Напишите /order.")
    elif call.data == 'halal' or call.data == 'halal_2':
        bot.send_message(call.message.chat.id, "Мы предлагаем 100% Халал продукцию! Хотите выбрать пиццу? Напишите /menu.")
    elif call.data == 'delivery':
        bot.send_message(call.message.chat.id, "Круглосуточная доставка по Ташкенту! Оформите заказ с помощью /order.")
    elif call.data == 'fast_delivery':
        bot.send_message(call.message.chat.id, "Доставка за 35 минут или пицца в подарок! Хотите заказать? Напишите /order.")
    elif call.data == 'tashkent_delivery':
        bot.send_message(call.message.chat.id, "Доставка по Ташкенту 24/7. Оформите заказ с помощью /order.")
    elif call.data == 'call_center':
        bot.send_message(call.message.chat.id, "Свяжитесь с нами: Call-center +998 93 669 6688")
    elif call.data == 'restart':
        bot.send_message(call.message.chat.id, "Нажмите /start, чтобы начать заново!")
    elif call.data.startswith('pizza_'):
        pizza_name = call.data.replace('pizza_', '').capitalize()
        bot.send_message(call.message.chat.id, f"Вы выбрали пиццу {pizza_name}. Хотите оформить заказ? Напишите /order.")

# Запуск бота
if __name__ == '__main__':
    print("Бот запущен!")
    bot.polling(none_stop=True)
