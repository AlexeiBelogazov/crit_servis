import telebot
from telebot import types
from db_pony import *
from keyboa import Keyboa


global chat
global a
global b
a = '🔰 Зарегестрироваться'
b = "♻ Войти"
token = API_TOKEN
bot = telebot.TeleBot(token)
init_db()
chat = {}
class Chat:
    secret_cod = ""
    cod_cart = ""
    password = ""
    user = ""
    IDmes_1 = 0
    IDmes_text = 0
    IDmes_2 = 0
    IDmes_st = 0
    flag_s1 = False
    yroven_menu_text = 0
    sticer_update= False

    def __init__(self, cat_id, first_name, last_name):
        self.caT_id = cat_id
        self.first_name = first_name
        self.last_name = last_name


@bot.message_handler(commands=['start'])

def start_message(message):
    global chat


    chat["{0}".format(message.chat.id)] = Chat(message.chat.id, message.from_user.first_name,message.from_user.first_name)

    chatUs = chat["{0}".format(message.chat.id)]

    bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    itembtna = types.KeyboardButton(a)
    itembtnv = types.KeyboardButton(b)
    markup.row(itembtna, itembtnv)
    idmesss = bot.send_message(message.chat.id, f"Здравствуйте {chatUs.first_name} выберете действие ", reply_markup=markup)

    chatUs.flag_s1 = True
    chatUs.IDmes_1 = idmesss

@bot.message_handler(content_types=["text"])
def text_us(message):
    chatUs = chat["{0}".format(message.chat.id)]
    print("text")
    print(message.text)



    if message.text == a:
        print(a)
        if chatUs.IDmes_text != 0:
            bot.delete_message(chat_id=chatUs.IDmes_text.chat.id, message_id=chatUs.IDmes_text.message_id)
        bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
        chatUs.IDmes_text=bot.send_message(chat_id=chatUs.IDmes_1.chat.id,
                              text=f"{chatUs.first_name} введите секретный код ")
        chatUs.yroven_menu_text = 1
    elif message.text == b:
        if chatUs.IDmes_text != 0:
            bot.delete_message(chat_id=chatUs.IDmes_text.chat.id, message_id=chatUs.IDmes_text.message_id)
        print(b)
        bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
        chatUs.IDmes_text=bot.send_message(chat_id=chatUs.IDmes_1.chat.id,
                              text=f"{chatUs.first_name} введите пароль ")
        chatUs.yroven_menu_text = 2

    elif chatUs.yroven_menu_text == 1:
        print("y1")
        chatUs.secret_cod = message.text
        bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
        bot.edit_message_text(chat_id=chatUs.IDmes_text.chat.id, message_id=chatUs.IDmes_text.message_id,
                              text=f"{chatUs.first_name} введите новый пароль")
        chatUs.yroven_menu_text = 3
    elif chatUs.yroven_menu_text == 2:
        print("y2")
        chatUs.secret_cod = message.text
        bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
        bot.edit_message_text(chat_id=chatUs.IDmes_text.chat.id, message_id=chatUs.IDmes_text.message_id,
                              text=f"{chatUs.first_name} введите ваш секретный код")
        chatUs.yroven_menu_text = 4

    elif chatUs.yroven_menu_text == 4:
        print("y4")
        chatUs.password = message.text
        with pony.orm.db_session:
            print(f"{chatUs.first_name} {chatUs.secret_cod} {message.text}")
            users = pony.orm.select(p for p in User if p.name == chatUs.first_name and
                   p.s_code == chatUs.secret_cod and
                   p.passw == message.text)[:]
        print(len(users))
        print(users)
        if len(users) == 1:

            bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
            bot.delete_message(chat_id=chatUs.IDmes_text.chat.id, message_id=chatUs.IDmes_text.message_id)
            bot.delete_message(chat_id=chatUs.IDmes_1.chat.id, message_id=chatUs.IDmes_1.message_id)
            items = [[{"↩ Сменить мой стикер": "s1"}, {"✴Показать мой стикер": "s2"}],{"Сменить скретный код и пароль": "s4"}, {"❌ Удалить мой стикер": "s3"}]
            kb = Keyboa(items).keyboard
            tetxt = f"{chatUs.first_name} можете выбрать далнейшее действие"
            chatUs.IDmes_2 = bot.send_message(message.chat.id, tetxt, reply_markup=kb)
            chatUs.yroven_menu_text = 5
        else:
            bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
            bot.edit_message_text(chat_id=chatUs.IDmes_text.chat.id, message_id=chatUs.IDmes_text.message_id,
                                  text=f"{chatUs.first_name}вы вели данные которые не существуют\n снова введите пароль")
            chatUs.yroven_menu_text = 2

    elif chatUs.yroven_menu_text == 3:
        print("y3")
        chatUs.password = message.text
        with pony.orm.db_session:
            users= pony.orm.select(p for p in User if p.name == chatUs.first_name and
                   p.s_code == chatUs.secret_cod and
                   p.passw == message.text)[:]
        if len(users) == 0:
            with pony.orm.db_session:
                st_none = Stickerr["1"]
                p1 = User(name=chatUs.first_name, s_code=chatUs.secret_cod, passw=message.text, sticker=st_none)
                pony.orm.commit()

            bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
            bot.delete_message(chat_id=chatUs.IDmes_1.chat.id, message_id=chatUs.IDmes_1.message_id)
            bot.delete_message(chat_id=chatUs.IDmes_text.chat.id, message_id=chatUs.IDmes_text.message_id)
            items = [ [{"↩ Сменить мой стикер": "s1"}, {"✴Показать мой стикер": "s2"}],{"Сменить скретный код и пароль": "s4"}, {"❌ Удалить мой стикер": "s3"}]
            kb = Keyboa(items).keyboard
            tetxt = f"Поздравляю {chatUs.first_name} вы зарегестрировались \n можете выбрать далнейшее действие"
            chatUs.IDmes_2 = bot.send_message(message.chat.id, tetxt, reply_markup=kb)
            chatUs.yroven_menu_text = 5
        else:
            bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
            bot.edit_message_text(chat_id=chatUs.IDmes_text.chat.id, message_id=chatUs.IDmes_text.message_id,
                                  text=f"{chatUs.first_name}вы вели данные которые уже существуют\n введите новый секретный код из 3 цифр")
            chatUs.yroven_menu_text = 1

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    chatUs = chat["{0}".format(call.message.chat.id)]
    if call.data == 's1':
        if chatUs.IDmes_st != 0:
            bot.delete_message(chat_id=chatUs.IDmes_st.chat.id, message_id=chatUs.IDmes_st.message_id)
            chatUs.IDmes_st = 0
        batton = ["Назад"]
        kb = Keyboa(batton).keyboard
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text=f"отправте мне стикер на который хотите сменить свой",
                              reply_markup=kb)
        chatUs.sticer_update = True


    if call.data == 's2':
        with pony.orm.db_session:
            users = User.get(name=chatUs.first_name, s_code=chatUs.secret_cod, passw=chatUs.password)
            st_id = users.sticker.sticker_id
        if st_id == " ":
            batton = ["Назад"]
            kb = Keyboa(batton).keyboard
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text=f"{chatUs.first_name} вам сначало необходимо добавить стикер\nотправте мне стикер на который хотите сменить свой",
                                  reply_markup=kb)
            chatUs.sticer_update = True
        else:
            if chatUs.IDmes_st != 0:
                bot.delete_message(chat_id=chatUs.IDmes_st.chat.id, message_id=chatUs.IDmes_st.message_id)
                chatUs.IDmes_st = 0
            chatUs.IDmes_st=bot.send_sticker(call.message.chat.id, users.sticker.sticker_id)

    if call.data == 's3':
        if chatUs.IDmes_st != 0:
            bot.delete_message(chat_id=chatUs.IDmes_st.chat.id, message_id=chatUs.IDmes_st.message_id)
            chatUs.IDmes_st = 0
        with pony.orm.db_session:
            st_none = Stickerr["1"]
            users = User.get(name=chatUs.first_name, s_code=chatUs.secret_cod, passw=chatUs.password)
            users.sticker = st_none
            pony.orm.commit()

    if call.data == 'Назад':
        items = [[{"↩ Сменить мой стикер": "s1"}, {"✴Показать мой стикер": "s2"}],
                 {"Сменить скретный код и пароль": "s4"}, {"❌ Удалить мой стикер": "s3"}]
        kb = Keyboa(items).keyboard
        tetxt = f"{chatUs.first_name} можете выбрать далнейшее действие"
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text=tetxt,
                              reply_markup=kb)


   # if call.data == 's4':

@bot.message_handler(content_types=['sticker'])
def handle_sticker(message):
    chatUs = chat["{0}".format(message.chat.id)]
    # получаем информацию о стикере
    sticker_id = message.sticker.file_id
    sticker_unique_id = message.sticker.file_unique_id
    bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    with pony.orm.db_session:
        users = User.get(name=chatUs.first_name, s_code=chatUs.secret_cod, passw=chatUs.password)
        try:
            S3 = Stickerr[sticker_unique_id]
        except:
            S3 = Stickerr(sticker_unique_id=sticker_unique_id, sticker_id=sticker_id)
        users.sticker = S3
        pony.orm.commit()
    # отправляем ответное сообщение
    items = [[{"↩ Сменить мой стикер": "s1"}, {"✴Показать мой стикер": "s2"}], {"Сменить скретный код и пароль": "s4"},
             {"❌ Удалить мой стикер": "s3"}]
    kb = Keyboa(items).keyboard
    bot.edit_message_text(chat_id=chatUs.IDmes_2.chat.id, message_id=chatUs.IDmes_2.message_id,
                                  text=f"{chatUs.first_name} ваш стикер добавлен \nможете выбрать далнейшее действие",
                                  reply_markup=kb)
# запускаем бота
bot.polling()