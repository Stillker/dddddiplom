import telebot
from telebot import types
import requests
from bs4 import BeautifulSoup  # импорт библиотек
from csv_helper import get_information
from AccessHelper import get_stat, get_rating


def get_documents():  # Парсинг документов.
    url = "https://техникумсвязи.рф/abiturientu/documentsforaccept/"
    page = requests.get(url)
    document_list = []
    soup = BeautifulSoup(page.text, "html.parser")
    docs = soup.find('ol', class_='list-group list-group-numbered')
    for doc in docs:
        document_list.append((doc.text)
                             .replace('\n ', '').replace(';\r\n      ', '')
                             .replace(';\r     ', '')
                             .replace('.\r     ', ''))

    document_list.remove('\n')
    document_list.remove('\n')
    document_list.remove('\n')
    document_list.remove('\n')
    document_list.remove('\n')

    return document_list


def get_links():
    url = "https://техникумсвязи.рф/blog/"  # адрес страницы
    page = requests.get(url)  # получине структуры страницы
    link_list = []  # создаем пустой массив
    soup = BeautifulSoup(page.text, "html.parser")  # указываем тип парсера
    news = soup.findAll('h3', class_='post-title')  # ищем теги страницы в классе
    for data in news:
        links = data.findAll('a')
        for link in links:
            link_list.append("https://техникумсвязи.рф" + link.get('href'))  # добавление в массив

    return link_list


def parserKTS():  # функция для парсинга
    url = "https://техникумсвязи.рф/blog/"  # адрес страницы
    page = requests.get(url)  # получине структуры страницы
    strings = ""  # создаем пустую строку
    news_list = []  # создаем пустой массив
    link_list = []  # создаем пустой массив
    soup = BeautifulSoup(page.text, "html.parser")  # указываем тип парсера

    news = soup.findAll('h3', class_='post-title')  # ищем теги страницы в классе
    for data in news:  # перебор данных циклом
        news_list.append(data.text)  # добавления данных в массив

    return news_list  # возвращаем строку


bot = telebot.TeleBot('6000660385:AAFl_hZ11tmBJjuR1W9yYtkLeU2g4y368OI')
print('[LOG] Start success')


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Привет, я умник КТС!', reply_markup=main_markup())
    file = open('./logo.jpg', 'rb')
    bot.send_photo(message.chat.id, file)


def main_markup():
    markup = types.ReplyKeyboardMarkup()
    btn1 = types.KeyboardButton('Информация о месте в общем рейтинге ')
    btn2 = types.KeyboardButton('Информация о расположении учебного заведения, площадках и т.п.')
    markup.row(btn1, btn2)
    btn3 = types.KeyboardButton('Новости техникума')
    btn4 = types.KeyboardButton('Перечень специальностей и профессий ')
    btn5 = types.KeyboardButton('Сведения о времени подачи заявлений и необходимом комплекте документов')
    markup.row(btn3, btn4, btn5)

    return markup


def send_information(message):  # функция отправления данных
    bot.send_message(message.chat.id, text=get_stat(get_rating(), message.text.split()[0]))


@bot.message_handler(content_types=['text'])
def send_message(message):
    if message.text == "Перечень специальностей и профессий":
        bot.send_message(message.chat.id, text="Информация о специальностях)")
        markup = types.ReplyKeyboardMarkup()
        item1 = types.KeyboardButton('09.02.07 Информационные системы и программирование')
        item2 = types.KeyboardButton('42.02.01 Реклама ')
        item3 = types.KeyboardButton('11.02.15 Инфокоммуникационные сети и системы связи')
        item4 = types.KeyboardButton('09.02.06 Сетевое и системное администрирование')
        item5 = types.KeyboardButton('09.01.01 Наладчик аппаратного и программного обеспечения')
        item6 = types.KeyboardButton('15.01.21 Электромонтер охранно-пожарной сигнализации')
        item7 = types.KeyboardButton('11.02.12 Почтовая связь')
        item8 = types.KeyboardButton('На главную')
        markup.row(item1, item2, item3)
        markup.row(item4, item5, item6)
        markup.row(item7, item8)
        bot.send_message(message.chat.id, '😇', reply_markup=markup)


    elif message.text == "09.02.07 Информационные системы и программирование":
        bot.send_message(message.chat.id, text="09.02.07")
        file = open('./infoseti.mp4', 'rb')
        bot.send_video(message.chat.id, file)


    elif message.text == "42.02.01 Реклама":
        bot.send_message(message.chat.id, text="42.02.01")
        file = open('./42.02.01.mp4', 'rb')
        bot.send_video(message.chat.id, file)

    elif message.text == "11.02.15 Инфокоммуникационные сети и системы связи":
        bot.send_message(message.chat.id, text="11.02.15 ")
        file = open('./0_Поступай в КТС! - _11.02.15 Инфокоммуникационные сети и системы связи.mp4', 'rb')
        bot.send_video(message.chat.id, file)


    elif message.text == "09.02.06 Сетевое и системное администрирование":
        bot.send_message(message.chat.id, text="09.02.06")
        file = open('./09.02.06.mp4', 'rb')
        bot.send_video(message.chat.id, file)

    elif message.text == "09.01.01 Наладчик аппаратного и программного обеспечения":
        bot.send_message(message.chat.id, text="09.01.01")
        file = open('./09.01.01.mp4', 'rb')
        bot.send_video(message.chat.id, file)


    elif message.text == "15.01.21 Электромонтер охранно-пожарной сигнализации":
        bot.send_message(message.chat.id, text="15.01.21")
        file = open('./15.01.21.mp4', 'rb')
        bot.send_video(message.chat.id, file)

    elif message.text == "11.02.12 Почтовая связь":
        bot.send_message(message.chat.id, text="11.02.12")
        file = open('./11.02.12.mp4', 'rb')
        bot.send_video(message.chat.id, file)

    elif message.text == "На главную":
        bot.send_message(message.chat.id, "Главное меню", reply_markup=main_markup())

    elif message.text == "Информация о месте в общем рейтинге":
        send = bot.send_message(message.chat.id, text="Введите уникальный номер:")
        bot.register_next_step_handler(send, send_information)

    elif message.text == "Информация о расположении учебного заведения, площадках и т.п.":
        bot.send_message(message.chat.id, "✌️ Мы расположены тут! 👇")
        file = open('./metka.jpg', 'rb')
        bot.send_photo(message.chat.id, file)
        markup = types.InlineKeyboardMarkup()
        btn11 = types.InlineKeyboardButton('Группа ВК', url='https://vk.com/ktskursk')
        btn12 = types.InlineKeyboardButton('Сайт техникума', url='https://техникумсвязи.рф')
        markup.add(btn11)
        markup.add(btn12)
        bot.send_message(message.chat.id, "Ссылки на ресурсы", reply_markup=markup)

    elif message.text == "Новости техникума":
        for i in range(len(get_links())):
            markup = types.InlineKeyboardMarkup()
            bot.send_message(message.chat.id, parserKTS()[i])
            btn = types.InlineKeyboardButton('Перейти', url=get_links()[i])
            markup.add(btn)
            bot.send_message(message.chat.id, "Для прочтения новости нажмите на кнопку.", reply_markup=markup)

    elif message.text == "Сведения о времени подачи заявлений и необходимом комплекте документов":
        document_list = "👨‍💻 Документы для подачи заявления: \n\n"
        for i in range(len(get_documents())):
            document_list += f"📃 {i + 1}. {get_documents()[i]}\n"

        bot.send_message(message.chat.id, document_list)


bot.polling(none_stop=True)  # нон стоп работа бота
