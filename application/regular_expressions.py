import csv
import re
from application.logger import logger


logger_path = logger('application/db/log.txt')

# читаем адресную книгу в формате CSV в список contacts_list
@logger_path
def get_phonebook():
    with open("application/db/phonebook_raw.csv", encoding="utf-8") as f:
        rows = csv.reader(f, delimiter=",")
        contacts_list = list(rows)
    return contacts_list


# разбиваем имена по строкам
@logger_path
def corrected_structure():
    phone_pattern = r"(\+7|8)*[\s\(]*(\d{3})[\)\s-]*(\d{3})[-]*(\d{2})[-]*(\d{2})[\s\(]*(доб\.)*[\s]*(\d+)*[\)]*"
    phone_correct = r"+7(\2)\3-\4-\5 \6\7"
    corrected_list = []
    for string in get_phonebook():
        fullname = " ".join(string[0:3]).split(" ")
        result = [fullname[0], fullname[1], fullname[2], string[3],
                  string[4], re.sub(phone_pattern, phone_correct, string[5]), string[6]]
        corrected_list.append(result)
    return corrected_list



# удаляем повторения
@logger_path
def remove_duplicate():
    phonebook = list(map(list, corrected_structure()))
    for string in phonebook:
        lastname = string[0]
        firstname = string[1]
        for item in phonebook:
            new_lastname = item[0]
            new_firstname = item[1]
            if firstname == new_firstname and lastname == new_lastname:
                if string[2] == "":
                    string[2] = item[2]
                if string[3] == "":
                    string[3] = item[3]
                if string[4] == "":
                    string[4] = item[4]
                if string[5] == "":
                    string[5] = item[5]
                if string[6] == "":
                    string[6] = item[6]
    result_list = list()
    for i in phonebook:
        if i not in result_list:
            result_list.append(i)
    return result_list


    # код для записи файла в формате CSV
@logger_path
def write_csv():
    with open("application/db/phonebook.csv", "w", newline="", encoding="utf-8") as f:
        datawriter = csv.writer(f, delimiter=',')
        datawriter.writerows(remove_duplicate())
