""" Домашнее задание №11 (курс "Основы языка Python")
== Лото ==
Правила игры в лото.
Игра ведется с помощью специальных карточек, на которых отмечены числа,
и фишек (бочонков) с цифрами.
Количество бочонков — 90 штук (с цифрами от 1 до 90).
Каждая карточка содержит 3 строки по 9 клеток. В каждой строке по 5 случайных цифр,
расположенных по возрастанию. Все цифры в карточке уникальны. Пример карточки:

--------------------------
    9 43 62          74 90
 2    27    75 78    82
   41 56 63     76      86
--------------------------

В игре 2 игрока: пользователь и компьютер. Каждому в начале выдается
случайная карточка.

Каждый ход выбирается один случайный бочонок и выводится на экран.
Также выводятся карточка игрока и карточка компьютера.

Пользователю предлагается зачеркнуть цифру на карточке или продолжить.
Если игрок выбрал "зачеркнуть":
    Если цифра есть на карточке - она зачеркивается и игра продолжается.
    Если цифры на карточке нет - игрок проигрывает и игра завершается.
Если игрок выбрал "продолжить":
    Если цифра есть на карточке - игрок проигрывает и игра завершается.
    Если цифры на карточке нет - игра продолжается.

Побеждает тот, кто первый закроет все числа на своей карточке.
Пример одного хода:
Новый бочонок: 70 (осталось 76)
------ Ваша карточка -----
 6  7          49    57 58
   14 26     -    78    85
23 33    38    48    71
--------------------------
-- Карточка компьютера ---
 7 87     - 14    11
      16 49    55 88    77
   15 20     -       76  -
--------------------------
Зачеркнуть цифру? (y/n)

Подсказка: каждый следующий случайный бочонок из мешка удобно получать
с помощью функции-генератора.

Подсказка: для работы с псевдослучайными числами удобно использовать
модуль random: http://docs.python.org/3/library/random.html """

from random import randint as ri

print('Здравствуйте! Привестствуем Вас в игре "Русское Лото"! ')


def generate_unique_numbers(number_count, minimal_numb, maximal_numb):
    if number_count > maximal_numb - minimal_numb + 1:
        raise ValueError('Введены некорректные исходные данные! Попробуйте еще раз! ')
    our_list = []
    while len(our_list) < number_count:
        again_new_number = ri(minimal_numb, maximal_numb)
        if again_new_number not in our_list:
            our_list.append(again_new_number)
    return our_list


class KegOur:
    __num = None

    def __init__(self):
        self.__num = ri(1, 91)

    @property
    def num(self):
        return self.__num

    def __str__(self):
        return str(self.__num)


class Card:
    __cols = 9
    __rows = 3
    __data = None
    __nums_in_row = 5
    __crossednum = -1
    __emptynum = 0

    def __init__(self):
        count_unique = self.__nums_in_row * self.__rows
        number_unique = generate_unique_numbers(count_unique, 1, 91)

        self.__data = []
        for x in range(0, self.__rows):
            one = sorted(number_unique[x * self.__nums_in_row: (x + 1) * self.__nums_in_row])
            empty_numbers_count = self.__cols - self.__nums_in_row
            for y in range(0, empty_numbers_count):
                keg_index = ri(0, len(one))
                one.insert(keg_index, self.__emptynum)
            self.__data += one

    def __str__(self):
        line_with_delimiter = '--------------------------------------------'
        our_list = line_with_delimiter + '\n'
        for keg_index, num in enumerate(self.__data):
            if num == self.__emptynum:
                our_list += '  '
            elif num == self.__crossednum:
                our_list += ' -'
            elif num < 10:
                our_list += f' {str(num)}'
            else:
                our_list += str(num)

            if (keg_index + 1) % self.__cols == 0:
                our_list += '\n'
            else:
                our_list += ' '

        return our_list + line_with_delimiter

    def __contains__(self, our):
        return our in self.__data

    def cross_num(self, num):
        for keg_index, our in enumerate(self.__data):
            if our == num:
                self.__data[keg_index] = self.__crossednum
                return
        raise ValueError(f'Предупреждение! Номер выпавшего Вам бочонка на карточке отсутствует: {num}')

    def our_error(self) -> bool:
        return set(self.__data) == {self.__emptynum, self.__crossednum}


class LotoGame:
    __numkegs = 90
    __kegs = []
    __gameover = False
    __usercard = None
    __compcard = None

    def __init__(self):
        self.__usercard = Card()
        self.__compcard = Card()
        self.__kegs = generate_unique_numbers(self.__numkegs, 1, 90)

    def player_play(self) -> int:

        keg = self.__kegs.pop()
        print(f'Вам выпал бочонок с новым номером: {keg} (Попыток осталось: {len(self.__kegs)})')
        print(f'-------- Это Ваша карточка игрока ----------\n{self.__usercard}')
        print(f'-- Это карточка противника (компьютера) ---\n{self.__compcard}')

        to_user_request = input('Вы хотите зачеркнуть цифру на карточке? (y/n): ').lower().strip()
        if to_user_request == 'y' and not keg in self.__usercard or \
           to_user_request != 'y' and keg in self.__usercard:
            return 2

        if keg in self.__usercard:
            self.__usercard.cross_num(keg)
            if self.__usercard.our_error():
                return 1
        if keg in self.__compcard:
            self.__compcard.cross_num(keg)
            if self.__compcard.our_error():
                return 2

        return 0


# Вывод сообщения о текущем статусе игры!

if __name__ == '__main__':
    game = LotoGame()
    while True:
        player_step = game.player_play()
        if player_step == 1:
            print('Мы Вас поздравляем! Вы выиграли игру у компьютера! Если Вам понравилась '
                  'игра - попробуйте еще раз сыграть!')
            break
        elif player_step == 2:
            print('Сожалеем, но Вы проиграли компьютеру! Попробуйте сыграть еще раз!')
            break

