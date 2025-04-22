from telebot import TeleBot, types

TOKEN = "7536710828:AAHpiG5XkjH4ysvh_x87qmKkeVYLergvk_U"
bot = TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    buttons = [types.KeyboardButton(text) for text in ["Salom", "Xayr"]]
    markup.add(*buttons)
    bot.send_message(
        chat_id=message.chat.id,
        text="Tugmalardan birini tanlang:",
        reply_markup=markup
    )

@bot.message_handler(func=lambda message: True)
def reply_to_button(message):
    responses = {
        "Salom": "Salom yaxshimisiz?",
        "Xayr": "Xayr yana ko'rishamiz"
    }
    response = responses.get(
        message.text,
        "Men bu tugmani tushinmadim"
    )
    bot.send_message(chat_id=message.chat.id, text=response)

if name == "main":
    bot.polling()
