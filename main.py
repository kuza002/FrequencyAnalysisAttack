from Table import Table
import random

alphabet = "А Б В Г Д Е Ё Ж З И Й К Л М Н О П Р С Т У Ф Х Ц Ч Ш Щ Ъ Ы Ь Э Ю Я " \
           "а б в г д е ё ж з и й к л м н о п р с т у ф х ц ч ш щ ъ ы ь э ю я"


# Возвращает словарь с данными о колличестве встречаемых символов в файле

def calculate_statistics(path, limit=0):
    statistics = dict.fromkeys(alphabet.split(), 0)

    with open(path, 'r', encoding="Windows 1251") as file:
        i = 0
        for line in file:
            for char in line:
                if limit != 0 and limit == i:
                    return statistics
                if char in statistics:
                    statistics[char] += 1
                i += 1

    return statistics


# Возвращает элемент словаря с максимальным значением

def max_by_value(dictionary):
    max_value = 0
    max_key = ""

    for key, value in dictionary.items():
        if value >= max_value:
            max_value = value
            max_key = key

    return max_key


# Создаёт словарь сопоставляя ключи двух других словарей, по принципу возврастания их значений

def create_my_table(db_statistics, encrypted_file_statistics):
    new_table = {}

    for i in range(len(alphabet.split())):
        max_in_db = max_by_value(db_statistics)
        max_in_encrypted_file = max_by_value(encrypted_file_statistics)

        new_table[max_in_db] = max_in_encrypted_file

        del db_statistics[max_in_db]
        del encrypted_file_statistics[max_in_encrypted_file]

    return new_table

# d = {'a': 10, 'b': 20, 'c': 15}
# d2 = {'a': 10, 'b': 0, 'c': 15}
#
# def sort_keys_by_val(d):
#     return sorted(d.keys(), key=lambda k: d[k])
#
# dict(zip(sort_keys_by_val(d), sort_keys_by_val(d2)))

print("Create encryption table...\n")
table = Table("TopSecret/table.csv")

print("Save this table...\n")
table.save()

print("Encrypt the file...\n")
table.encrypt("TopSecret/original.txt", "encoded.txt")

print("Analyzing the database...\n")
db_statistics = calculate_statistics("Data.txt")

statistic = Table("Statistic.csv", {})

# Анализируем схожесть новой таблицы с оригинальной,
# постепенно увеличивая объём зашфированного файла от 10 тыс. до 40 тыс.

for i in range(1, 41):
    print("Analyzing the encrypted file " + str(i) + "0000 characters long\n")
    encrypted_file_statistics = calculate_statistics("encoded.txt", i * 10000)

    print("Create a test decryption table")
    my_table = Table("MyTable.csv", create_my_table(db_statistics.copy(), encrypted_file_statistics.copy()))
    print("Save a test decryption table \n")
    my_table.save()

    p = str(table.number_of_coincidences(my_table))

    print("Percentage of correct letters: " + p + "\n")
    statistic.add_element(str(i) + "0000", p)

# Расшифровываем файл по новой таблице

my_table.spell_out('encoded.txt', 'decoded.txt')

# Даём возможность пользователю изменить таблицу

answer = input("Enter 0 if you want to end the program "
               "or change table: ")

while answer != 0:
    my_table.change_by_key(answer[0], answer[1])
    my_table.spell_out('encoded.txt', 'decoded.txt')
    print("Now the number of coincidences : " + str(table.number_of_coincidences(my_table)))

    answer = input("Enter 0 if you want to end the program "
                   "or change table: ")
