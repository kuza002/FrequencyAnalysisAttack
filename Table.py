import random
import csv

alphabet = "А Б В Г Д Е Ё Ж З И Й К Л М Н О П Р С Т У Ф Х Ц Ч Ш Щ Ъ Ы Ь Э Ю Я " \
           "а б в г д е ё ж з и й к л м н о п р с т у ф х ц ч ш щ ъ ы ь э ю я"


class Table(object):

    # path - путь к месту сохранения таблицы в csv файл
    # table - словарь

    def __init__(self, path, table=""):
        self.path = path

        # Если в конструктор передали таблицу, то используем её

        if table != "":
            self.table = table

        # Если таблицу не передали, то создаёем таблицу шифрования, а именно
        # словарь, где key - буква алфавита, а value - его зашифрованная версия того же алфавита
        else:
            mixed_alphabet = alphabet.split().copy()
            random.shuffle(mixed_alphabet)

            self.table = dict(zip(alphabet.split(), mixed_alphabet))

    def print(self):
        print("Path = " + self.path)
        print("Table = " + str(self.table))

    # Шифрует по таблице файл из path_in и сохраняет зашифрованну версию в path_out

    def encrypt(self, path_in, path_out):
        with open(path_in, 'r', encoding="Windows 1251") as source:
            with open(path_out, 'w', encoding="Windows 1251") as encoded_file:
                for line in source:
                    for char in line:
                        if char in self.table:
                            encoded_char = self.table.get(char)
                            encoded_file.write(encoded_char)
                        else:
                            encoded_file.write(char)

    # Сохраняет таблицу в csv файл

    def save(self):
        with open(self.path, 'w', newline="", encoding='Windows 1251') as file:
            writer = csv.DictWriter(file, fieldnames=['decode', 'encode'], delimiter=";")
            writer.writeheader()

            for key, value in self.table.items():
                writer.writerow({'decode': key, 'encode': value})

    def get(self, key):
        return self.table.get(key)

    def get_by_value(self, needed_value):
        for key, value in self.table.items():
            if value == needed_value:
                return key

        return ""

    # Считает коэфициент совападения с переданной таблицей

    def number_of_coincidences(self, second):
        rating = 0
        for key, value in self.table.items():
            if second.get(key) == value:
                rating += 1
        return round(rating * 100 / len(alphabet.split()))

    # Расшифровывает по таблице файл из path_in и сохраняет расшифрованную версию в path_out

    def spell_out(self, path_in, path_out="decoded.txt"):
        with open(path_in, 'r', encoding="Windows 1251") as encodedFile:
            with open(path_out, 'w', encoding="Windows 1251") as decodedFile:
                for line in encodedFile:
                    for char in line:
                        value = self.get_by_value(char)
                        if value != "":
                            decodedFile.write(value)
                        else:
                            decodedFile.write(char)

    def add_element(self, key, value):
        self.table[key] = value
        self.save()

    # Редактирует таблицу, меняя местами элементы

    def change_by_key(self, a, b):
        c = self.get(a)
        d = self.get(b)

        self.table[a], self.table[b] = d, c

        self.save()
