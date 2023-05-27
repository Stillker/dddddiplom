import pyodbc

connection_string = r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=C:\Users\User\PycharmProjects\diplom\Main_BD.accdb;'
connection = pyodbc.connect(connection_string)
print("Connected")


def get_rating():
    rating = []
    try:
        cursor = connection.cursor()
        cursor.execute('SELECT `средний балл` FROM Абитуриенты WHERE `копия Доо` = False')
        for row in cursor.fetchall():
            rating.append("%s" % round(row[0], 2))

        rating.sort(reverse=True)
        return rating

    except pyodbc.Error as error:
        print("Error", error)


def get_stat(rating, regNumber):
    try:
        if is_user_exist(regNumber):
            cursor = connection.cursor()
            cursor.execute('SELECT `средний балл` FROM Абитуриенты WHERE `регистрационный номер` = ?', regNumber)
            for row in cursor.fetchall():
                student_rating = "%s" % round(row[0], 2)
                if student_rating in rating:
                    return f'📈 Ваш балл аттестата: {student_rating}.\n🏆 Ваше место в рейтинге: {rating.index(student_rating) + 1}'

                else:
                    return "Вас нет в Базе данных. Возможно, Вы принесли только копию документа."
        else:
            return "❌ Нет такого пользователя! ❌\n\nПользователь не найден в базе данных, либо присутствует только копия документов!"

    except pyodbc.Error as error:
        print("Error", error)


def is_user_exist(regNumber):
    try:
        users = []
        cursor = connection.cursor()
        cursor.execute('SELECT `регистрационный номер` FROM Абитуриенты WHERE `копия Доо` = False')
        user_find = cursor.fetchall()
        for row in user_find:
            users.append("%s" % row[0])

        if regNumber in users:
            return True

        else:
            return False

    except pyodbc.Error as error:
        print("Error", error)
