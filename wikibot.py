import logging, telebot, wikipediaapi, random
from telebot import types
token=""
bot=telebot.TeleBot(token)
logger=logging.getLogger(__name__)
lang='ru'

def pagefunc(text, lang):
    wiki_wiki = wikipediaapi.Wikipedia(lang)
    page_py = wiki_wiki.page(text)
    return page_py



@bot.message_handler(commands=['start'])
def startBot(message):
    keyboard=types.InlineKeyboardMarkup()
    en=types.InlineKeyboardButton(text="English", callback_data='en')
    ru = types.InlineKeyboardButton(text="Русский", callback_data='ru')
    keyboard.add(en,ru)
    logger.warning("СТАРТОВАЛ БОТ")
    logger.info(message)
    bot.send_message(message.chat.id,"Привет! Я wikiбот. Выберите язык поиска:",reply_markup=keyboard)


@bot.message_handler(commands=['extra'])
def getMenu(message):
    logger.warning("EXTRA")
    logger.info(message)
    keyboard=types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    id=types.KeyboardButton(text="/id")
    memes=types.KeyboardButton(text="/memes")
    cats=types.KeyboardButton(text="/котики")
    keyboard.add(id, memes, cats)
    bot.send_message(message.chat.id,"extraМЕНЮ",reply_markup=keyboard)

@bot.message_handler(commands=['id'])
def showid(message):
    logger.warning("id")
    logger.info(message)
    bot.send_message(message.chat.id, f'ID нашего чата: {message.chat.id}')

@bot.message_handler(commands=['memes'])
def showmeme(message):
    logger.warning("memes")
    logger.info(message)
    num=random.randint(1,4)
    bot.send_photo(message.chat.id,photo=open(f'memes/meme{num}.png','rb'))

@bot.message_handler(commands=['котики'])
def showmeme(message):
    logger.warning("cats")
    logger.info(message)
    num=random.randint(1,6)
    bot.send_photo(message.chat.id,photo=open(f'cats/cat{num}.jpg','rb'))

@bot.message_handler(commands=['review'])
def review(message):
    logger.warning("отзыв")
    logger.info(message)
    bot.send_message(message.chat.id,'Далее вы можете оставить отзыв или предложения:')
    bot.register_next_step_handler(message,send_review)

def send_review(message):
    bot.send_message(message.chat.id,'Спасибо!')
    bot.send_message(449332008,f'ОТЗЫВ: {message.text}')



@bot.message_handler(commands=['help'])
def startBot(message):
    logger.warning("HELP")
    logger.info(message)
    keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    help = types.KeyboardButton(text="/help")
    info = types.KeyboardButton(text="/info")
    start = types.KeyboardButton(text="/start")
    keyboard.add(help, info, start)
    bot.send_message(message.chat.id, 
                     '''
    /info - информация о боте, описание работы
    /help - описание функций команд
    /start - выбор/смена языка
    /extra - отображает список дополнительных команд''', reply_markup=keyboard)


@bot.message_handler(commands=['info'])
def startBot(message):
    logger.warning("INFO")
    logger.info(message)
    bot.send_message(message.chat.id,'''
    Этот бот выводит отрывки из статей википедии на заданный запрос, а также ссылки к полным версиям. 
    Доступны два языка для поиска: английский и русский. 
    Дополнительный перечень команд доступен по вызову /extra.
    Краткое описание всех команд содержится в /help
    Данный бот является ученическим проектом и может дорабатываться с течением времени. 
    Автор: @zhumzhumay''')

@bot.callback_query_handler(func=lambda c:True)
def inlin(c):
    global lang
    if c.data == 'en':
        lang = 'en'
        bot.send_message(c.message.chat.id, 'Теперь вы можете ввести интересующее понятие на английском языке')
    elif c.data == 'ru':
        lang = 'ru'
        bot.send_message(c.message.chat.id, 'Теперь вы можете ввести интересующее понятие на русском языке')

@bot.message_handler(content_types=['text'])
def repeatMe(message):

    page=pagefunc(message.text, lang)
    if page.exists()==True:
        keyboard = types.InlineKeyboardMarkup()
        url = types.InlineKeyboardButton(text="Ссылка на полную статью", url=page.fullurl)
        keyboard.add(url)
        bot.send_message(message.chat.id,page.summary, reply_markup=keyboard)
    else:
        bot.send_message(message.chat.id, 'Такой статьи не существует')



if __name__=="__main__":
    logger.warning("ЗАПУСК БОТА")
    bot.infinity_polling()



    