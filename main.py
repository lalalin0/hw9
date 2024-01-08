import os
import shutil
import re
import json
import csv
import codecs
from collections import Counter

print('Имя вашей ОС:', os.name)

current_folder = os.getcwd()
print('Текущая папка:', current_folder)

text_folder = os.path.join(current_folder, 'Текстовые файлы')
image_folder = os.path.join(current_folder, 'Изображения')
other_folder = os.path.join(current_folder, 'Прочие файлы')

os.makedirs(text_folder, exist_ok=True)
os.makedirs(image_folder, exist_ok=True)
os.makedirs(other_folder, exist_ok=True)

# сортировка файлов, исключая .py файлы
for file_name in os.listdir(current_folder):
    file_path = os.path.join(current_folder, file_name)

    if os.path.isfile(file_path):
        _, file_extension = os.path.splitext(file_name)
        file_extension = file_extension.lower()

        if file_extension in ('.py', '.json', '.txt', '.csv'):
            continue

        elif file_extension in ('.jpg', '.jpeg', '.png', '.gif'):
            shutil.move(file_path, os.path.join(image_folder, file_name))
        else:
            shutil.move(file_path, os.path.join(other_folder, file_name))


def get_folder_info(folder):
    total_files = len(os.listdir(folder))
    total_size = sum(os.path.getsize(os.path.join(folder, f)) for f in os.listdir(folder))
    return total_files, total_size


text_files, text_size = get_folder_info(text_folder)
image_files, image_size = get_folder_info(image_folder)
other_files, other_size = get_folder_info(other_folder)

print(
    f'В папке с текстовыми файлами перемещено {text_files} файлов, их суммарный размер - '
    f'{text_size / (1024 ** 3):.2f} гигабайт')
print(
    f'В папке с изображениями перемещено {image_files} файлов, их суммарный размер - '
    f'{image_size / (1024 ** 3):.2f} гигабайт')
print(
    f'В папке с прочими файлами перемещено {other_files} файлов, их суммарный размер -'
    f' {other_size / (1024 ** 3):.2f} гигабайт')


def rename_file(directory):
    files = os.listdir(directory)
    if files:
        old_name = files[0]
        new_name = 'some_' + old_name
        old_path = os.path.join(directory, old_name)
        new_path = os.path.join(directory, new_name)
        os.rename(old_path, new_path)
        print(f'Файл {old_name} был переименован в {new_name}')


# переименовывем файлы

rename_file(image_folder)
rename_file(other_folder)


# Task 2
def replace_names(text):
    name_pattern = re.compile(r'\b[А-ЯЁ][а-яё]*(-[А-ЯЁ][а-яё]*)*\s+[А-ЯЁ][а-яё]*\s+[А-ЯЁ][а-яё]*\b')

    # заменяем ФИО на "N"
    replaced_text = name_pattern.sub('N', text)

    return replaced_text


# Вводимый текст
input_text = '''Подсудимая Эверт-Колокольцева Елизавета Александровна
в судебном заседании вину инкриминируемого
правонарушения признала в полном объёме и суду показала,
что 14 сентября 1876 года, будучи в состоянии алкогольного
опьянения от безысходности, в связи с состоянием здоровья
позвонила со своего стационарного телефона в полицию,
сообщив о том, что у неё в квартире якобы заложена бомба.
После чего приехали сотрудники полиции, скорая
и пожарные, которым она сообщила, что бомба — это она.'''

output_text = replace_names(input_text)

print(output_text)


# Task 3


def most_common_word_in_line(line):
    words = line.lower().split()  # чтобы слова мама и Мама считались одинаковыми
    word_counter = Counter(words)
    most_common_word, count = word_counter.most_common(1)[0]
    return most_common_word, count


def process_file(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    with open(output_file, 'w', encoding='utf-8') as output_file:
        for line in lines:
            most_common_word, count = most_common_word_in_line(line)
            output_file.write(f'Самое частое слово: {most_common_word}, Количество повторений: {count}\n')


input_file_path = 'words.txt'
output_file_path = 'most_common_words.txt'

process_file(input_file_path, output_file_path)


# Task 4


def load_stop_words(stop_words_file):
    try:
        with open(stop_words_file, 'r', encoding='utf-8') as stop_words_file:
            stop_words = stop_words_file.read().split()
        return set(stop_words)
    except FileNotFoundError:
        print(f'Файл {stop_words_file} не найден.')
        return set()


def censor_text(input_file, stop_words_file):
    stop_words = load_stop_words(stop_words_file)

    try:
        with open(input_file, 'r', encoding='utf-8') as file:
            text = file.read()

        for word in stop_words:
            # Заменяем найденные слова, игнорируя регистр
            text = re.sub(r'\b' + re.escape(word) + r'\b', '*' * len(word), text, flags=re.IGNORECASE)

        print(text)
    except FileNotFoundError:
        print(f'Файл {input_file} не найден.')


input_file = 'example.txt'
stop_words_file = 'stop_words.txt'
censor_text(input_file, stop_words_file)


# Task 5

def read_grades(file_path):
    students = []

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                parts = line.strip().split()
                if len(parts) == 3:
                    last_name, first_name, grade = parts
                    students.append({'last_name': last_name, 'first_name': first_name, 'grade': int(grade)})
                else:
                    print(f'Ошибка в строке: {line}')
    except FileNotFoundError:
        print(f'Файл {file_path} не найден.')

    return students


def print_students_below_three(students):
    for student in students:
        if student['grade'] < 3:
            print(f"{student['last_name']} {student['first_name']} - Оценка: {student['grade']}")


file_path = 'grades.txt'
students = read_grades(file_path)

if students:
    print('Учащиеся с оценкой меньше трех баллов:')
    print_students_below_three(students)
else:
    print('Нет данных оценок.')


# Task 6


def sum_numbers_in_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()

        numbers = re.findall(r'\d+', content)

        total_sum = sum(map(int, numbers))

        return total_sum
    except FileNotFoundError:
        print(f'Файл {file_path} не найден.')
        return 0


file_path = 'example_with_numbers.txt'
result = sum_numbers_in_file(file_path)

print(f'Сумма всех чисел в файле: {result}')


# Task 7
def encrypt_caesar_cycler(message):
    result = ''
    for i, char in enumerate(message):
        shift = (i // len(message.split('\n'))) + 1
        if char.isalpha():
            if 'a' <= char <= 'z':
                result += chr((ord(char) - ord('a') + shift) % 26 + ord('a'))
            elif 'A' <= char <= 'Z':
                result += chr((ord(char) - ord('A') + shift) % 26 + ord('A'))
            elif 'а' <= char <= 'я':
                result += chr((ord(char) - ord('а') + shift) % 32 + ord('а'))
            elif 'А' <= char <= 'Я':
                result += chr((ord(char) - ord('А') + shift) % 32 + ord('А'))
        elif char.isnumeric():
            result += chr((ord(char) - ord('0') + shift) % 10 + ord('0'))
        else:
            result += char
    return result


def encrypt_file_caesar_cycler(input_file, output_file):
    try:
        with open(input_file, 'r', encoding='utf-8') as file:
            content = file.read()

        encrypted_content = encrypt_caesar_cycler(content)

        with open(output_file, 'w', encoding='utf-8') as encrypted_file:
            encrypted_file.write(encrypted_content)

        print(f'Файл успешно зашифрован. Зашифрованный файл: {output_file}')
    except FileNotFoundError:
        print(f'Файл {input_file} не найден.')


input_file = 'example_ceasar.txt'
output_file = 'encrypted_example_ceasar.txt'

encrypt_file_caesar_cycler(input_file, output_file)


# Task 8

def json_to_csv(json_file, csv_file):
    try:
        with open(json_file, 'r', encoding='utf-8') as json_file:
            data = json.load(json_file)

        with open(csv_file, 'w', encoding='utf-8', newline='') as csv_file:
            csv_writer = csv.writer(csv_file)

            headers = list(data[0].keys())
            csv_writer.writerow(headers)

            for row in data:
                csv_writer.writerow(row.values())

        print(f'Данные преобразованы в CSV. CSV-файл: {csv_file}')
    except FileNotFoundError:
        print(f'Файл {json_file} не найден.')
    except json.JSONDecodeError:
        print('fОшибка декодирования JSON в файле {json_file}.')


json_file = 'some_file.json'
csv_file = 'data.csv'

json_to_csv(json_file, csv_file)


# taaaaaaaaaask 8.2


def add_employee(json_file_path, new_employee):
    try:
        with open(json_file_path, 'r', encoding='utf-8') as json_file:
            data = json.load(json_file)

        data.append(new_employee)

        with open(json_file_path, 'w', encoding='utf-8') as updated_json_file:
            json.dump(data, updated_json_file, indent=2)

        print(f'Новый сотрудник добавлен в JSON-файл: {json_file_path}')
    except FileNotFoundError:
        print(f'Файл {json_file_path} не найден.')
    except json.JSONDecodeError:
        print(f'Ошибка декодирования JSON в файле {json_file_path}. ')


json_file = 'data.json'
csv_file = 'data.csv'

new_employee = {
    "name": "Новый Сотрудник",
    "position": "Должность",
    "salary": 50000
}

add_employee(json_file, new_employee)
json_to_csv(json_file, csv_file)

# Task 8.3
def add_employee_to_json(json_file_path):
    try:
        with open(json_file_path, 'r', encoding='utf-8') as json_file:
            data = json.load(json_file)

        new_employee = {}
        new_employee['name'] = input('Введите имя сотрудника: ')
        new_employee['position'] = input('Введите должность сотрудника: ')
        new_employee['salary'] = float(input('Введите зарплату сотрудника: '))

        data.append(new_employee)

        with open(json_file_path, 'w', encoding='utf-8') as json_file:
            json.dump(data, json_file, indent=2)

        print(f'Новый сотрудник добавлен в JSON-файл: {json_file_path}')
    except FileNotFoundError:
        print(f'Файл {json_file_path} не найден.')
    except json.JSONDecodeError:
        print(f'Ошибка декодирования JSON в файле {json_file_path}.')
    except ValueError:
        print('Ошибка: Некорректный ввод зарплаты. Введите число.')


json_file_path = 'data.json'

add_employee_to_json(json_file_path)

# Task 8.4


def json_to_csv(json_file, csv_file):
    try:
        with codecs.open(json_file, 'r', encoding='utf-8') as json_file:
            data = json.loads(json_file.read())

        with open(csv_file, 'w', encoding='utf-8', newline='') as csv_file:
            csv_writer = csv.writer(csv_file)

            # Если файл пустой, добавляем заголовки
            if len(data) > 0:
                headers = list(data[0].keys())
                csv_writer.writerow(headers)

            # Записываем данные
            for row in data:
                csv_writer.writerow(row.values())

        print(f'Данные успешно преобразованы в CSV. CSV-файл: {csv_file}')
    except FileNotFoundError:
        print(f'Файл {json_file} не найден.')
    except json.JSONDecodeError:
        print(f'Ошибка декодирования JSON в файле {json_file}.')


json_file = 'data.json'
csv_file = 'data.csv'

json_to_csv(json_file, csv_file)


