import hashlib
str_to_crypt = 'Начинаем игру "Быки и Коровы". Я задумываю четырехзначное число, ' \
               'все цифры которого различны (первая цифра числа отлична от нуля).' \
               'Вам необходимо разгадать задуманное число. Вы вводите четырехзначное ' \
               'число c неповторяющимися цифрами, я сообщаю о количестве «быков» и «коров» ' \
               'в названном числе. «Бык» — цифра есть в записи задуманного числа и стоит ' \
               'в той же позиции, что и в задуманном числе, «Корова» — цифра есть в записи' \
               'задуманного числа, но не стоит в той же позиции, что в задуманном числе.'

print(hashlib.sha3_224(str_to_crypt.encode('utf-8')).hexdigest())


# 85d85ee3b565a4acd756169aec695102afda7534fbbfa6a7d591516ec91adb915d4981f4354204c1bb03f514eb6bf7214948f53bc3767823522e96ed685f6999
# 93061fdc4a581b01aeef3f9a6539c01eaa7a6fb4318fa0af41435af350ce9d18b0df2847974b162289a92d661dc29419d609e5858402f1499a4965b74ca5a7db