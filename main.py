import telebot
from telebot import types
import pymysql
import random
import requests
from bs4 import BeautifulSoup  # импорт библиотек
import csv

host = 'localhost'
user = 'root'
port = 3306
password = 'root'
db = 'databasekts'  # параметры для подключения БД

connection = pymysql.connect(host=host, user=user, password=password, database=db, port=port)  # подключение к БД

# def get_csv():
#     with open('database.csv') as file:
#         file_reader = csv.reader(file, delimiter=' ')
#         count = 0
#         for row in file_reader:
#             if count == 0:
#                 print(f'Файл содержит строки: {", ".join(row)}')
#
#             else:
#                 print(f'{row[0]}: ')
#
#             count += 1
#
# get_csv()

def get_status(regNumber):  # функция для получения места в рейтинге по рег. номеру
    with connection.cursor() as cur:  # Подключаемся к бд
        rating_list = []  # Создаем пустой массив.
        sql = "SELECT Rating FROM `user` WHERE `IsCopy` = %s"  # Запрос к БД SELECT - выборка, FROM - из какой таблицы, WHERE - условие для сортировки
        cur.execute(sql, ("Нет"))  # выполнение запроса
        result = cur.fetchall()  # считывание результата
        for row in result:  # цикл для перебора данных
            rating_list.append("%s" % row[0])  # добавление данных в массив.

        rating_list.sort(reverse=True)  # Сортировка массива по возростанию.

        if get_rating(regNumber) in rating_list:  # Проверка, что данное значение есть в массиве.
            return rating_list.index(get_rating(regNumber)) + 1  # Определяем индекс массива



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


def is_user_exist(regNumber):  # проверка на пользователя (в БД)
    with connection.cursor() as cur:  # подключение БД
        users = []  # Создаем пустой массив
        sql = "SELECT `RegNumber` FROM `user` WHERE `IsCopy` = %s"  # Запрос
        cur.execute(sql, "Нет")  # выполнения запроса с параметром
        user_find = cur.fetchall()  # нахождения результата
        for row in user_find:  # перебор данных циклом
            users.append("%d" % row[0])  # добавления данных в массив

    if str(regNumber) in users:  # проверка параметра на нахождения пользователя в массиве
        return True  # возвращаем истенное
    else:  # иначе
        return False  # возвращаем ложное


def get_rating(regNumber):  # функция для получения рейтинга
    with connection.cursor() as cur:  # подключение БД
        sql = "SELECT `Rating` FROM `user` WHERE `RegNumber` = %s AND `IsCopy` = %s"  # Запрос к БД SELECT - выборка, FROM - из какой таблицы, WHERE - условие для сортировки
        rating = 0  # создаем переменную
        cur.execute(sql, (regNumber, "Нет"))  # выполнения запроса с параметром
        result = cur.fetchall()  # нахождения результата
        for row in result:  # перебор данных циклом
            rating = "%s" % row[0]  # добавления значения рейтинга
    return rating  # возвращаем рейтинг


def get_specialnost(regNumber):  # функция для получения специальности
    with connection.cursor() as cur:  # подключение БД
        sql = "SELECT `Specialnost` FROM `user` WHERE `RegNumber` = %s"  # Запрос к БД SELECT - выборка, FROM - из какой таблицы, WHERE - условие для сортировки
        cur.execute(sql, (regNumber))  # выполнения запроса с параметром
        result = cur.fetchone()  # нахождения результата

    return result  # возвращаем специальность


def get_FIO(regNumber):  # функция для получения ФИО
    with connection.cursor() as cur:  # подключение БД
        sql = "SELECT `FIO` FROM `user` WHERE `RegNumber` = %s"  # Запрос к БД SELECT - выборка, FROM - из какой таблицы, WHERE - условие для сортировки
        cur.execute(sql, (regNumber))  # выполнения запроса с параметром
        result = cur.fetchone()  # нахождения результата

    return result  # возвращам ФИО


bot = telebot.TeleBot('6000660385:AAFl_hZ11tmBJjuR1W9yYtkLeU2g4y368OI')
print('Success')


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
    bot.send_message(message.chat.id, text=get_information(message.text.split()[0]))


def get_information(regNumber):  # функция для получения информации
    if is_user_exist(regNumber):  # проверка на пользователя
        fio = ''.join(get_FIO(regNumber))  # форматируем имя
        spec = ''.join(get_specialnost(regNumber))  # форматируем  специальность
        rating = get_rating(regNumber)  # форматируем рейтинг
        information = f"👨‍💻 Ваше ФИО: {fio}\n🎓 Ваша специальность: {spec}\n📈 Ваш рейтинг: {rating}\n🏆 Место в общем рейтинге: {get_status(regNumber)}"  # создаем строку с информацией
        return information  # возвращаем информацию
    else:  # иначе
        return "❌ Нет такого пользователя! ❌\n\nПользователь не найден в базе данных, либо присутствует только копия документов!"  # ошибка


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
        bot.send_message(message.chat.id,
                         "👨‍💻 Документы для подачи заявления: \n\n"
                         "\n📃 1. Оригинал или ксерокопия документов, удостоверяющих личность и гражданство"
                         "\n📃 2. Оригинал или ксерокопия документов об образовании и (или) документа об образовании и о квалификации;"
                         "\n📃 3. Согласие на обработку данных;"
                         "\n📃 4. Фотографии – 4 шт. (размер 3х4).")


bot.polling(none_stop=True)  # нон стоп работа бота
