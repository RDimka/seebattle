#SeaBattle
import random
import copy

#Классы исключений
#Например, когда игрок пытается выстрелить в клетку за пределами поля, во внутренней логике должно
#выбрасываться соответствующее исключение BoardOutException, а потом отлавливаться во внешней логике,
#выводя сообщение об этой ошибке пользователю.
class MyError(Exception):
    def __init__(self, text):
        self.txt = text

#Использование в коде
#except MyError as mr:
#   print(mr)

#класс Dot — класс точек на поле
class Dot():
    x, y = None, None
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

#    def __str__(self):
#        return f'Dot: {self.x, self.y}'

#тест Dot
#f = Dot(1,1)
#s = Dot(1,1)
#if f == s:
#    print ("Равны")
#else:
#    print ("Не равны")

# Класс Ship — корабль на игровом поле, который описывается параметрами:
# Длина.
# Точка, где размещён нос корабля.
# Направление корабля (вертикальное/горизонтальное).
# Количеством жизней (сколько точек корабля ещё не подбито).
# И имеет метод dots, который возвращает список всех точек корабля.
class Ship():
    long, bow_dot, direction, life_num = None, None, None, None
    def __init__(self, *args):
        self.long = args[0]
        self.bow_dot = args[1]
        self.direction = args[2]
        self.life_num = args[3]

    def dots(self):
        ship_dot_list = []
        i = self.long
        x = self.bow_dot.x
        y = self.bow_dot.y
        while i:
            ship_dot_list.append(Dot(x, y))
            if self.direction == "v":
                y += 1
            else:
                x += 1
            i -= 1
        return ship_dot_list #список всех точек корабля

#Тест Ship
#start = Dot(1,1)
#sh = Ship(4, start, "h", 4)
#ship_dots = sh.dots()
#for dot in ship_dots:
#    print(f"{dot.x} {dot.y}")



# Самый важный класс во внутренней логике — класс Board — игровая доска.

class Board():
    def __init__(self, hid=True, alive=6):
        # двумерный списко состояний каждой из клеток, инициализация
        self.board_state = [["O"] * 6 for i in range(6)]

        # Список кораблей доски.
        self.board_ships = [Ship(3, Dot(-1, -1), 'v', 3),
                            Ship(2, Dot(-1, -1), 'v', 2),
                            Ship(2, Dot(-1, -1), 'v', 2),
                            Ship(1, Dot(-1, -1), 'v', 1),
                            Ship(1, Dot(-1, -1), 'v', 1),
                            Ship(1, Dot(-1, -1), 'v', 1)]

        # Параметр hid типа bool — информация о том, нужно ли скрывать корабли на доске (для вывода доски врага) или нет (для своей доски).
        self.hid = True

        # Количество живых кораблей на доске.
        self.alive_ships = alive

        # Метод add_ship, который ставит корабль на доску (если ставить не получается, выбрасываем исключения).
#    def add_ships(self, ship):
#        ship_dots = ship.dots()
#        try:
    #    #проверка, нет ли вокруг других кораблей
    #    for i in ship_dots:
    #      self.board_state[i.x][i.y] = "s"
    #
    #  except

    #  else:#если все хорошо в try
    #    return()
    # Метод contour, который обводит корабль по контуру. Он будет полезен и в ходе самой игры, и в при расстановке кораблей (помечает соседние точки, где корабля по правилам быть не может).
    # def contour(self, ship):



    # Метод, который выводит доску в консоль в зависимости от параметра hid.
    def board_layout(self):
        if self.hid:
            print()
            print("    | 1 | 2 | 3 | 4 | 5 | 6  ")
            print("  -------------------------- ")
            for i, row in enumerate(self.board_state):
                row_str = f"  {i + 1} | {' | '.join(row)} | "
                print(row_str)

    # Метод out, который для точки (объекта класса Dot) возвращает True, если точка выходит за пределы поля, и False, если не выходит.
    def out(self, dot):
        # проверка в поле?
        return True if dot.x > 5 or dot.y > 5 else False

# Метод shot, который делает выстрел по доске (если есть попытка выстрелить за пределы и в использованную точку, нужно выбрасывать исключения).
#выстрел
    def shot(self, dot):
        #try:
        if self.out(dot):
            raise MyError("BoardOutException")
        if self.board_state[dot.x][dot.y] == 'X' or self.board_state[dot.x][dot.y] == 'T':
            raise MyError("UsedPointException")
        #except MyError as err:
        #    print(err)
        #else:
            # помечаем Т (промах), Х (попал)
        self.board_state[dot.x][dot.y] = "T" if self.board_state[dot.x][dot.y] == "O" else "X"
            # Если попал вернем True
        return True if self.board_state[dot.x][dot.y] == "X" else False
#Тест Board
#brd = Board()
#brd.board_layout()
#d = Dot(0, 0)
#print("Промазал" if brd.out(d) else "Попал")
#print(brd.shot(d))
#brd.board_layout()


# класс Player — класс игрока в игру (и AI, и пользователь). Этот класс будет родителем для классов с AI и с пользователем.
class Player():
    def __init__(self, board_player, board_enemy):
        self.board_player = board_player
        self.board_enemy = board_enemy

    # ask — метод, который «спрашивает» игрока, в какую клетку он делает выстрел.
    def ask(self):
        pass

    # move — метод, который делает ход в игре. Тут мы вызываем метод ask, делаем выстрел по вражеской доске (метод Board.shot), отлавливаем исключения, и если они есть, пытаемся повторить ход. Метод должен возвращать True, если этому игроку нужен повторный ход (например, если он выстрелом подбил корабль).
    def move(self):
        i = 1000
        while i:
            dot_shot = self.ask()
            try:
                return self.board_enemy.shot(dot_shot)
            except MyError as err:
                print(err)
                i -= 1
        print("Использовал 1000 ходов, следующий )")
        return False

#тест Player
# player = Player(Board(), Board())
# if player.move():
#     print ("Еще один ход")
# else:
#     print ("Следующий")

# унаследовать классы AI и User от Player и переопределить в них метод ask. Для AI это будет выбор случайной точки, а для User этот метод будет спрашивать координаты точки из консоли.
class AI(Player):
    def ask(self):
        # случайные координаты точки
        return Dot(random.randint(0, 5), random.randint(0, 5))

#Тест AI
#player = AI(Board(), Board())
#i=100
#while i:
#    dot = player.ask()
#    print(f'{dot.x} {dot.y}')
#    i -= 1

class User(Player):
    def ask(self):
        # Запросить точки
        shot_point = Dot()
        print(" формат ввода координат выстрела: x y ")
        print(" x - номер строки  ")
        print(" y - номер столбца ")

        while True:
            cords = input("         Ваш ход: ").split()
            if len(cords) != 2:
                print(" Введите 2 координаты! ")
                continue

            if not (cords[0].isdigit()) or not (cords[1].isdigit()):
                print(" Введите числа! ")
                continue

            shot_point.x, shot_point.y = int(cords[0]), int(cords[1])
            return shot_point

#Тест User
# player = User(Board(), Board())
# dot = player.ask()
# print(f'{dot.x} {dot.y}')

class Game():
    def __init__(self, user, user_board, ai, ai_board):
        self.user = user
        self.user_board = user_board
        self.ai = ai
        self.ai_board = ai_board

    # random_board — метод генерирует случайную доску. Для этого мы просто пытаемся в случайные клетки изначально пустой доски расставлять корабли (в бесконечном цикле пытаемся поставить корабль в случайную доску, пока наша попытка не окажется успешной). Лучше расставлять сначала длинные корабли, а потом короткие. Если было сделано много (несколько тысяч) попыток установить корабль, но это не получилось, значит доска неудачная и на неё корабль уже не добавить. В таком случае нужно начать генерировать новую доску.
    def random_board(self):
        pass

    # greet — метод, который в консоли приветствует пользователя и рассказывает о формате ввода.
    def greet(self):
        pass

    # loop — метод с самим игровым циклом. Там мы просто последовательно вызываем метод mode для игроков и делаем проверку, сколько живых кораблей осталось на досках, чтобы определить победу.
    def loop(self):
        pass

    # start — запуск игры. Сначала вызываем greet, а потом loop.
    def start(self):
        self.greet()
        self.loop()
        pass


#board = Board()
#print(board.board_state)

#board.board_state[5][5] = "X"
#board.board_layout()