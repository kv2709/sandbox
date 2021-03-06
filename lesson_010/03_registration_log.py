# -*- coding: utf-8 -*-

# Есть файл с протоколом регистраций пользователей на сайте - registrations.txt
# Каждая строка содержит: ИМЯ ЕМЕЙЛ ВОЗРАСТ, разделенные пробелами
# Например:
# Василий test@test.ru 27
#
# Надо проверить данные из файла, для каждой строки:
# - присутсвуют все три поля
# - поле имени содержит только буквы
# - поле емейл содержит @ и .
# - поле возраст является числом от 10 до 99
#
# В результате проверки нужно сформировать два файла
# - registrations_good.log для правильных данных, записывать строки как есть
# - registrations_bad.log для ошибочных, записывать строку и вид ошибки.
#
# Для валидации строки данных написать метод, который может выкидывать исключения:
# - НЕ присутсвуют все три поля: ValueError
# - поле имени содержит НЕ только буквы: NotNameError (кастомное исключение)
# - поле емейл НЕ содержит @ и .(точку): NotEmailError (кастомное исключение)
# - поле возраст НЕ является числом от 10 до 99: ValueError
# Вызов метода обернуть в try-except.

import re

LOG_VALID_EMAIL_RE = r'^.+@.+\..+'
FILE_NAME_OUT_GOOD = 'registrations_good.log'
FILE_NAME_OUT_BAD = 'registrations_bad.log'


class NotNameError(Exception):
    pass


class NotEmailError(Exception):
    pass


class ValueCountError(Exception):
    pass


class ValueAgeError(Exception):
    pass


class ValidatorLog:

    def __init__(self, file_name_log='', file_name_out_good=FILE_NAME_OUT_GOOD, file_name_out_bad=FILE_NAME_OUT_BAD):
        """
        :param file_name_log: имя входного файла лога
        :param file_name_out_good: имя выходгного файла хороших записей
        :param file_name_out_bad: имя выходного файла плохих записей
        """
        self.file_name_log = file_name_log
        self.file_name_out_good = file_name_out_good
        self.file_name_out_bad = file_name_out_bad
        self.line_from_file = ''
        self.file_log = None
        self.file_out_good = None
        self.file_out_bad = None
        self.line_good = False
        self.value_error_message = ''

    def _open_files(self):
        """
        Внутренний метод открытия всех файло: входной файл с логом для чтения
        и два выходных файла для записи ошибочных и верных регистраций
        :return: нет
        """
        self.file_log = open(self.file_name_log,  mode='r', encoding='utf8')
        self.file_out_good = open(self.file_name_out_good,  mode='w', encoding='utf8')
        self.file_out_bad = open(self.file_name_out_bad,  mode='w', encoding='utf8')

    def _close_files(self):
        """
        Внутренний метод закрытия всех файлов
        :return: нет
        """
        self.file_log.close()
        self.file_out_good.close()
        self.file_out_bad.close()

    def execute(self):
        """
        Основной метод класса по валидации читаемых строк из файла лога и
        записи верных и отбракованных строк в разные файлы
        Для самой валидации в цикле чтения ихсодного файла
        вызывается внутренний метод _validate_line(),
        который при отбраковке строки генерирует соотвествующее исключение,
        содержание которого вместе с отбракованной строкой пишем в файл плохих регистраций
        :return: нет
        """
        self._open_files()
        for self.line_from_file in self.file_log:
            try:
                self._validate_line()
            except Exception as ext:
                align_space = (35 - len(self.line_from_file[:-1])) * ' '
                self.file_out_bad.write(f'{self.line_from_file[:-1]} {align_space} ===> {ext} !!!\n')
            else:
                self.file_out_good.write(self.line_from_file)
        self._close_files()

    def _validate_line(self):
        """
        Внутренний метод валидации строки из исходного файла
        выполнятеся четыре типа проверки с генерации пользовательских исключений
        !!! с пробросом содержания исключения в вызывающий метод !!!
        для последующей записи его в файл отбракованных строк лога.
        Проверка корректности E-mail выполенна с помощью простейшего
        регулярного выражения https://regex101.com/r/1WyDiy/1
        :return: нет
        """
        separate_line_lst = self.line_from_file.split(' ')
        if len(separate_line_lst) < 3:
            raise ValueCountError('Не присутствую все поля!')
        elif not separate_line_lst[0].isalpha():
            raise NotNameError('Неверное имя!')
        elif re.match(LOG_VALID_EMAIL_RE, separate_line_lst[1]) is None:
            raise NotEmailError('Некорректный E-mail!')
        elif not 10 <= int(separate_line_lst[2][:-1]) <= 99:
            raise ValueAgeError('Неверный возраст!')


vl = ValidatorLog(file_name_log='registrations.txt')
vl.execute()
