#!/usr/bin/python3

"""
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
модуль random: http://docs.python.org/3/library/random.html

"""
import os
import random

import sys


class Graphics(object):
    RULES = """
                        -= Игра Лото =-
    
        В игре 2 игрока: пользователь и компьютер.
        Каждому в начале выдается случайная карта. 
    
        Каждый ход выбирается один случайный бочонок и выводится на экран.
        Также выводятся карты игрока и карточка компьютера.
    
        Вы можете выбрать: зачеркнуть цифру на карточке или продолжить.
    
        Если выбор — зачеркнуть, а числа на карте нет, — проигрыш.
        Если выбор — проложить, а число на карте есть, — проигрыш.
    
        Выигрывает тот, кто зачеркнёт все числа на карте.    
    """


class Bag(object):
    """Generates sequence of barrels"""

    def __init__(self):
        self.barrels = list(range(1, 91))
        random.shuffle(self.barrels)
        self.step = -1

    def __iter__(self):
        # Метод __iter__ должен возвращать объект-итератор
        return self

    def __next__(self):
        self.step += 1
        if self.step < len(self.barrels):
            return self.barrels[self.step]
        else:
            raise StopIteration

    def __str__(self):
        return f"Новый бочонок: {self.barrels[self.step]} (осталось {89 - self.step})"


class Card(object):
    """
    Hold numbers, check for matches and form pretty string to display
    """
    CLEAR_PLACES = "000011111"

    def __init__(self, owner="Карточка компьютера"):
        self.owner = owner
        self.raw_numbers = sorted(random.sample(range(1, 91), 15))

        self.numbers = [random.sample(self.CLEAR_PLACES, 9),
                        random.sample(self.CLEAR_PLACES, 9),
                        random.sample(self.CLEAR_PLACES, 9)
                        ]

        self.populate_list()

    def check_number(self, num):

        for row in self.numbers:
            if num in row:
                row[row.index(num)] = "--"
                return True
        return False

    def make_complete(self):
        """Just for testing"""
        for row in range(3):
            for col in range(9):
                if self.numbers[row][col] != "  ":
                    self.numbers[row][col] = "--"

    @property
    def completed(self):
        for row in self.numbers:
            for item in row:
                if not (item == "--" or item == "  "):
                    return False

        return True

    # Overload __str__ to nicely represent card
    def __str__(self):
        s = f" {self.owner} ".center(43, "-") + "\n"
        for row in self.numbers:
            r_str = "   ".join([str(x).rjust(2) for x in row]) + "\n"
            s += r_str
        s += "-" * 43
        return f"\n{s}\n"

    @property
    def card(self):
        s = f" {self.owner} ".center(43, "-") + "\n"
        for row in self.numbers:
            r_str = "   ".join([str(x).rjust(2) for x in row]) + "\n"
            s += r_str
        s += "-" * 43
        return f"\n{s}\n"

    def populate_list(self):
        cut_numbers = [self.raw_numbers[::3], self.raw_numbers[1::3], self.raw_numbers[2::3]]
        for row in range(3):
            for col in range(9):
                if self.numbers[row][col] == "1":
                    self.numbers[row][col] = cut_numbers[row].pop(0)
                else:
                    self.numbers[row][col] = "  "


class Player(object):
    def __init__(self, is_human=True):
        self.is_human = is_human
        if self.is_human:
            self.card = Card("Ваша карточка")
        else:
            self.card = Card()

    def __str__(self):
        return self.card.card  # С заделом на будущее. Потом выводить сразу несколько карточек

    def check_and_cross(self, num):  # Надо переделать по уму для списка карт. Пока оценивает только первую
        return self.card.check_number(num)

    @property
    def done(self):
        return self.card.completed


class Loto(object):
    """Main game class"""
    GAME_ON = "continue game"
    GAME_OVER_WIN = "Congratulation! You win!"
    GAME_OVER_LOSE = "Bad luck. You lose :("

    def __init__(self):
        self.clear_screen()
        print(Graphics.RULES)
        start = input("Начнём? (y/n) ").lower()  # Задел на будущее, для выбора количества карт и т.п.
        if start == "y" or start == "н":
            self.bag = Bag()
            self.ai = Player(False)
            self.player = Player()
            self.game_state = Loto.GAME_ON
            self.play()
        else:
            sys.exit(1)

    def refresh(self):
        print(Graphics.RULES)
        start = input("Начнём? (y/n) ").lower()  # Задел на будущее, для выбора количества карт и т.п.
        if start == "y" or start == "н":
            self.bag = Bag()
            self.ai = Player(False)
            self.player = Player()
            self.game_state = Loto.GAME_ON
            self.play()
        else:
            sys.exit(1)

    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def play(self):
        for barrel in self.bag:
            if self.player.done:
                self.game_state = Loto.GAME_OVER_WIN
            if self.ai.done:
                self.game_state = Loto.GAME_OVER_LOSE
            self.draw_game_state()
            self.ai.check_and_cross(barrel)
            answer = input("Зачеркнуть цифру? (y/n)\n")
            barrel_in_card = self.player.check_and_cross(barrel)
            if (answer == "y" and barrel_in_card) or (answer == "n" and not barrel_in_card):
                continue
            else:
                self.game_state = Loto.GAME_OVER_LOSE
                self.draw_game_state()

            if not self.game_state == Loto.GAME_ON:
                break

    def draw_game_state(self):
        if self.game_state == Loto.GAME_ON:
            self.clear_screen()
            print(self.bag)
            print(self.player)
            print(self.ai)
        else:
            self.clear_screen()
            print(self.game_state)
            print(self.bag)
            print(self.player)
            if input("Ещё раз? (y/n) ") == "y":
                self.refresh()
            else:
                sys.exit(1)


if __name__ == '__main__':
    game = Loto()
    # b = Bag()
    # print(b.barrels)
    # for brl in b:
    #     print(b)
    #     print(brl)
