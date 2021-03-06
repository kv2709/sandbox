# -*- coding: utf-8 -*-

# Подземелье было выкопано ящеро-подобными монстрами рядом с аномальной рекой, постоянно выходящей из берегов.
# Из-за этого подземелье регулярно затапливается, монстры выживают, но не герои, рискнувшие спуститься к ним в поисках
# приключений.
# Почуяв безнаказанность, ящеры начали совершать набеги на ближайшие деревни. На защиту всех деревень не хватило
# солдат и вас, как известного в этих краях героя, наняли для их спасения.
#
# Карта подземелья представляет собой json-файл под названием rpg.json. Каждая локация в лабиринте описывается объектом,
# в котором находится единственный ключ с названием, соответствующем формату "Location_<N>_tm<T>",
# где N - это номер локации (целое число), а T (вещественное число) - это время,
# которое необходимо для перехода в эту локацию. Например, если игрок заходит в локацию "Location_8_tm30000",
# то он тратит на это 30000 секунд.
# По данному ключу находится список, который содержит в себе строки с описанием монстров а также другие локации.
# Описание монстра представляет собой строку в формате "Mob_exp<K>_tm<M>", где K (целое число) - это количество опыта,
# которое получает игрок, уничтожив данного монстра, а M (вещественное число) - это время,
# которое потратит игрок для уничтожения данного монстра.
# Например, уничтожив монстра "Boss_exp10_tm20", игрок потратит 20 секунд и получит 10 единиц опыта.
# Гарантируется, что в начале пути будет две локации и один монстр
# (то есть в коренном json-объекте содержится список, содержащий два json-объекта, одного монстра и ничего больше).
#
# На прохождение игры игроку дается 123456.0987654321 секунд.
# Цель игры: за отведенное время найти выход ("Hatch")
#
# По мере прохождения вглубь подземелья, оно начинает затапливаться, поэтому
# в каждую локацию можно попасть только один раз,
# и выйти из нее нельзя (то есть двигаться можно только вперед).
#
# Чтобы открыть люк ("Hatch") и выбраться через него на поверхность, нужно иметь не менее 280 очков опыта.
# Если до открытия люка время заканчивается - герой задыхается и умирает, воскрешаясь перед входом в подземелье,
# готовый к следующей попытке (игра начинается заново).
#
# Гарантируется, что искомый путь только один, и будьте аккуратны в рассчетах!
# При неправильном использовании библиотеки decimal человек, играющий с вашим скриптом рискует никогда не найти путь.
#
# Также, при каждом ходе игрока ваш скрипт должен запоминать следущую информацию:
# - текущую локацию
# - текущее количество опыта
# - текущие дату и время (для этого используйте библиотеку datetime)
# После успешного или неуспешного завершения игры вам необходимо записать
# всю собранную информацию в csv файл dungeon.csv.
# Названия столбцов для csv файла: current_location, current_experience, current_date
#
#
# Пример взаимодействия с игроком:
#
# Вы находитесь в Location_0_tm0
# У вас 0 опыта и осталось 123456.0987654321 секунд до наводнения
# Прошло времени: 00:00
#
# Внутри вы видите:
# — Вход в локацию: Location_1_tm1040
# — Вход в локацию: Location_2_tm123456
# Выберите действие:
# 1.Атаковать монстра
# 2.Перейти в другую локацию
# 3.Сдаться и выйти из игры
#
# Вы выбрали переход в локацию Location_2_tm1234567890
#
# Вы находитесь в Location_2_tm1234567890
# У вас 0 опыта и осталось 0.0987654321 секунд до наводнения
# Прошло времени: 20:00
#
# Внутри вы видите:
# — Монстра Mob_exp10_tm10
# — Вход в локацию: Location_3_tm55500
# — Вход в локацию: Location_4_tm66600
# Выберите действие:
# 1.Атаковать монстра
# 2.Перейти в другую локацию
# 3.Сдаться и выйти из игры
#
# Вы выбрали сражаться с монстром
#
# Вы находитесь в Location_2_tm0
# У вас 10 опыта и осталось -9.9012345679 секунд до наводнения
#
# Вы не успели открыть люк!!! НАВОДНЕНИЕ!!! Алярм!
#
# У вас темнеет в глазах... прощай, принцесса...
# Но что это?! Вы воскресли у входа в пещеру... Не зря матушка дала вам оберег :)
# Ну, на этот-то раз у вас все получится! Трепещите, монстры!
# Вы осторожно входите в пещеру... (текст умирания/воскрешения можно придумать свой ;)
#
# Вы находитесь в Location_0_tm0
# У вас 0 опыта и осталось 123456.0987654321 секунд до наводнения
# Прошло уже 0:00:00
# Внутри вы видите:
#  ...
#  ...
#
# и так далее...
# Учитывая время и опыт, не забывайте о точности вычислений!
import csv
import json
import os
from decimal import *
import re
import datetime


def calculate_change_time_experience(killed_mob=None, input_loc=None):
    global game_experience, remaining_time, game_time
    re_tm = r'_tm'
    re_exp = r'_exp'
    if killed_mob:
        separation_tm = re.split(re_tm, killed_mob)
        remaining_time = Decimal(remaining_time) - Decimal(separation_tm[1])
        game_time = Decimal(game_time) + Decimal(separation_tm[1])
        acquired_experience = re.split(re_tm, re.split(re_exp, killed_mob)[1])[0]
        game_experience += int(acquired_experience)
    if input_loc:
        separation = re.split(re_tm, input_loc)
        remaining_time = Decimal(remaining_time) - Decimal(separation[1])
        game_time = Decimal(game_time) + Decimal(separation[1])


def final_approach(msg=None):
    global game_experience, remaining_time, game_time
    game_time = '0.0'
    game_experience = 0
    remaining_time = '123456.0987654321'
    print(msg)
    action_in_location(map_locations_act=map_locations)


def finish_game_winner_or_no():
    if float(remaining_time) >= 0.0 and game_experience >= 280:
        print("Поздравляю с победой! Вы сумели выбраться из подземелья!")
        log_file_csv.close()
        exit(0)
    elif float(remaining_time) >= 0.0 and game_experience < 280:
        final_approach(msg="Вы не набрали достаточно опыта, чтобы открыть люк!!!\n"
                           "Такая нелепая смерть в такой близи от выхода!")


def action_in_location(map_locations_act=None):
    name_loc = ''
    for name_loc in map_locations_act.keys():
        pass
    input_loc_lst = map_locations_act[name_loc]
    if float(remaining_time) <= 0.0:
        final_approach(msg="Вы не успели открыть люк!!! НАВОДНЕНИЕ!!!\n"
                           "Такая нелепая смерть в самом рассвете сил!")
    if name_loc == "Hatch_tm159.098765432":
        finish_game_winner_or_no()
    mob_lst = []
    keys_locs_lst = []
    dicts_locs_lst = []
    for item in input_loc_lst:
        if type(item) == dict:
            for key_loc in item:
                keys_locs_lst.append(key_loc)
                dicts_locs_lst.append(item)
        elif type(item) == str:
            mob_lst.append(item)
    count_mobs = len(mob_lst)
    count_locs = len(keys_locs_lst)
    while True:
        # ----------------------------
        print(f"Вы находитесь в {name_loc}\n"
              f"У вас {game_experience} опыта и осталось {remaining_time} секунд до наводнения\n"
              f"Прошло времени: {game_time}\n")
        # -------------------------
        print("Внутри вы видите:")
        num_mob = 1
        for mob in mob_lst:
            print(f"— Монстра №{str(num_mob)} - {mob}")
            num_mob += 1
        if len(mob_lst) > 0:
            menu_str = MENU_LST[0] + MENU_LST[1] + MENU_LST[2] + MENU_LST[3]
        else:
            menu_str = MENU_LST[0] + MENU_LST[2] + MENU_LST[3]
        num_loc = 1
        for key_loc in keys_locs_lst:
            print(f"— Вход в локацию №{num_loc} - {key_loc}")
            num_loc += 1

        select = input(menu_str)

        if select == '1' and count_mobs > 0:
            # TODO Обработку ответов пользователя нужно валидировать (падает если ответ выходит за рамки ожидаемого
            #  числа), а также вынесите обработку "атаки", "перехода" и т.п. в отдельные методы - очень большой цикл
            #  вышел
            num_selected_mob = input("Укажите номер монстра для атаки ")
            try:
                num_selected_mob_int = int(num_selected_mob)
                if num_selected_mob_int <= count_mobs:
                    print(f"Атакован монстр под номером {num_selected_mob}")
                    del_mob = mob_lst[int(num_selected_mob) - 1]
                    calculate_change_time_experience(killed_mob=del_mob)
                    log_str = {'current_location': name_loc,
                               'current_experience': str(game_experience),
                               'current_date': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                               'game_time': game_time,
                               'remaining_time': remaining_time}
                    writer_log_csv.writerow(log_str)
                    del mob_lst[int(num_selected_mob) - 1]
                    count_mobs -= 1
                    print(f"Уничтожен монстр {del_mob}")
                else:
                    print(f"Все монстры уничтожены!")
            except ValueError as exc:
                print(f'Ошибка типа данных: {exc}, введите число')
        elif select == '2':
            num_selected_loc = input("Укажите номер локации для входа ")
            try:
                num_selected_loc_int = int(num_selected_loc)
                if num_selected_loc_int <= count_locs:
                    name_col_for_new_level = keys_locs_lst[num_selected_loc_int - 1]
                    print(f"Выбрана локация {name_col_for_new_level} под номером {num_selected_loc}")
                    print(f"{'-'*50}")
                    calculate_change_time_experience(input_loc=name_col_for_new_level)
                    log_str = {'current_location': name_col_for_new_level,
                               'current_experience': str(game_experience),
                               'current_date': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                               'game_time': game_time,
                               'remaining_time': remaining_time}
                    writer_log_csv.writerow(log_str)
                    new_level_map = dicts_locs_lst[int(num_selected_loc) - 1]
                    action_in_location(map_locations_act=new_level_map)
            except ValueError as exc:
                print(f'Ошибка типа данных: {exc}, введите число')
        elif select == '3':
            log_file_csv.close()
            exit(0)


if __name__ == '__main__':
    MENU_LST = ["Выберите действие:\n",
                "1.Атаковать монстра\n",
                "2.Перейти в другую локацию\n",
                "3.Сдаться и выйти из игры\n"]
    MAP_FILE_NAME = "rpg.json"
    LOG_FILE_NAME = 'dungeon.csv'
    FILED_NAMES = ['current_location', 'current_experience', 'current_date', 'game_time', 'remaining_time']

    game_time = '0.0'
    remaining_time = '123456.0987654321'
    game_experience = 0
    log_file_csv = open(LOG_FILE_NAME, 'a')
    writer_log_csv = csv.DictWriter(log_file_csv, fieldnames=FILED_NAMES)

    if not os.path.exists(LOG_FILE_NAME):
        writer_log_csv.writeheader()
    with open(MAP_FILE_NAME, "r") as rpg_json_file:
        map_locations = json.load(rpg_json_file)
    action_in_location(map_locations_act=map_locations)
