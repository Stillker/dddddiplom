import csv

def get_information(regNumber): # Получить инфу.
    with open("student_list.csv") as file:
        file_reader = csv.reader(file, delimiter=";")
        next(file_reader)
        for row in file_reader:
            if row[1] == str(regNumber):
                if row[3] == 'Да' or row[4] == 'Null':
                    return "Вас нет в Базе данных. Возможно, Вы принесли только копию документа."
                else:
                    return f"📈 Ваш балл аттестата: {row[2]}\n🏆 Ваше место в рейтинге: {row[4]}"

        return "Такого номера не существует."
