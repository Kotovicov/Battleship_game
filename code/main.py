import pygame
import random
import sys
import os


class Board:   # поле кораблей
    # создание поля
    def __init__(self, width1, height1):
        self.width = width1
        self.height = height1
        self.board = [[0 for j in range(self.width)] for _ in range(self.height)]
        # значения по умолчанию
        self.left = 10
        self.top = 10
        self.cell_size = 10

    # настройка внешнего вида
    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self, screen):
        alf = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j"]
        font = pygame.font.Font(None, 30)
        for i in range(9):
            screen.blit(font.render(str(i + 1), True, (50, 50, 50)), (self.left + 10
                                                                      + i * self.cell_size, 5))
        screen.blit(font.render("10", True, (50, 50, 50)), (self.left + 3 + 9 * self.cell_size, 5))
        for i in range(self.width):
            screen.blit(font.render(alf[i], True, (50, 50, 50)), (self.left - 20, self.top + 5
                                                                  + self.cell_size * i))
            for j in range(self.height):
                pygame.draw.rect(screen, (192, 192, 192),
                                 [self.left + i * self.cell_size, self.top + j * self.cell_size,
                                  self.cell_size, self.cell_size], width=0)
                pygame.draw.rect(screen, (96, 96, 96),
                                 [self.left + i * self.cell_size, self.top + j * self.cell_size,
                                  self.cell_size, self.cell_size], width=1)
                # 0 - пусто
                # 1 - свой корабль
                # 2 - чужой корабль
                # 3 - взорваная клетка
                # 4 - взорваная клетка с кораблем
                # 5 - корабль взорван
                if self.board[i][j] == 1:
                    pygame.draw.rect(screen, (0, 0, 205),
                                     [self.left + i * self.cell_size,
                                      self.top + j * self.cell_size,
                                      self.cell_size, self.cell_size], width=3)

                if self.board[i][j] == 3:
                    pygame.draw.rect(screen, (0, 0, 0),
                                     [self.left + i * self.cell_size + 10,
                                      self.top + j * self.cell_size + 10,
                                      self.cell_size - 20, self.cell_size - 20], width=0)

                if self.board[i][j] == 4 or self.board[i][j] == 5:
                    pygame.draw.line(screen, (220, 20, 60),
                                     (self.left + i * self.cell_size + 3,
                                      self.top + j * self.cell_size + 3),
                                     (self.left + (i + 1) * self.cell_size - 3,
                                      self.top + (j + 1) * self.cell_size - 3), width=5)
                    pygame.draw.line(screen, (220, 20, 60),
                                     (self.left + i * self.cell_size + 3,
                                      self.top + (j + 1) * self.cell_size - 3),
                                     (self.left + (i + 1) * self.cell_size - 3,
                                      self.top + j * self.cell_size + 3), width=5)
                    pygame.draw.rect(screen, (0, 0, 205),
                                     [self.left + i * self.cell_size,
                                      self.top + j * self.cell_size,
                                      self.cell_size, self.cell_size], width=3)
                if self.board[i][j] == 4 or self.board[i][j] == 5:
                    pygame.draw.line(screen, (220, 20, 60),
                                     (self.left + i * self.cell_size + 3,
                                      self.top + j * self.cell_size + 3),
                                     (self.left + (i + 1) * self.cell_size - 3,
                                      self.top + (j + 1) * self.cell_size - 3), width=5)
                    pygame.draw.line(screen, (220, 20, 60),
                                     (self.left + i * self.cell_size + 3,
                                      self.top + (j + 1) * self.cell_size - 3),
                                     (self.left + (i + 1) * self.cell_size - 3,
                                      self.top + j * self.cell_size + 3), width=5)
                    pygame.draw.rect(screen, (0, 0, 205),
                                     [self.left + i * self.cell_size,
                                      self.top + j * self.cell_size,
                                      self.cell_size, self.cell_size], width=3)

    def get_cell(self, mouse_pos):  # возвращает координаты клетки в виде кортежа по координатам мыши
        if self.left < mouse_pos[0] < self.left + self.width * self.cell_size and \
                self.top < mouse_pos[1] < self.top + self.height * self.cell_size:
            return ((mouse_pos[0] - self.left) // self.cell_size,
                    (mouse_pos[1] - self.top) // self.cell_size)
        return None

    def on_click(self, cell_coords):  # который как-то изменяет поле, по координатам клетки
        pass

    def get_click(self, pos):  # получает событие нажатия и вызывает первые два метода
        cell = self.get_cell(pos)
        if cell:
            self.on_click(cell)

    def add_ship(self, ship, number_ship):
        x, y = ship.x // 30 - 1, ship.y // 30 - 1
        if ship.rotation % 2 == 0:
            dx = 1
            dy = ship.size
        else:
            dx = ship.size
            dy = 1
        for x in range(x, x + dx):
            for y in range(y, y + dy):
                self.board[x][y] = number_ship


class Ship:  # корабль в клетках, писелей от стенок, 0 по вертикали
    def __init__(self, size_ship, x, y, rotation):
        self.size = size_ship
        self.x = x
        self.y = y
        self.rotation = rotation
        self.width = 30 + self.rotation % 2 * (self.size - 1) * 30
        self.height = 30 + (self.rotation + 1) % 2 * (self.size - 1) * 30


class OurBoard(Board):  # работа нашего поля
    def __init__(self, width1, height1):
        super().__init__(width1, height1)

    def on_click(self, cell_coords):
        if self.board[cell_coords[0]][cell_coords[1]] == 0:
            self.board[cell_coords[0]][cell_coords[1]] = 3
        elif self.board[cell_coords[0]][cell_coords[1]] == 1:
            self.board[cell_coords[0]][cell_coords[1]] = 4
            not_kill = False
            x, y = cell_coords
            while not not_kill and x >= 0 and self.board[x][y] != 0 and self.board[x][y] != 3:
                if self.board[x][y] == 1:
                    not_kill = True
                x -= 1
            x, y = cell_coords
            while not not_kill and x <= 9 and self.board[x][y] != 0 and self.board[x][y] != 3:
                if self.board[x][y] == 1:
                    not_kill = True
                x += 1
            x, y = cell_coords
            while not not_kill and y >= 0 and self.board[x][y] != 0 and self.board[x][y] != 3:
                if self.board[x][y] == 1:
                    not_kill = True
                y -= 1
            x, y = cell_coords
            while not not_kill and y <= 9 and self.board[x][y] != 0 and self.board[x][y] != 3:
                if self.board[x][y] == 1:
                    not_kill = True
                y += 1

            if not not_kill:
                x, y = cell_coords
                while x >= 0 and (self.board[x][y] == 4 or self.board[x][y] == 5):
                    self.board[x][y] = 5
                    if y > 0 and self.board[x][y - 1] != 4 and self.board[x][y - 1] != 5:
                        self.board[x][y - 1] = 3
                    if y < 9 and self.board[x][y + 1] != 4 and self.board[x][y + 1] != 5:
                        self.board[x][y + 1] = 3
                    x -= 1
                if x >= 0:
                    self.board[x][y] = 3
                    if y > 0:
                        self.board[x][y - 1] = 3
                    if y < 9:
                        self.board[x][y + 1] = 3

                x, y = cell_coords
                while x <= 9 and (self.board[x][y] == 4 or self.board[x][y] == 5):
                    self.board[x][y] = 5
                    if y > 0 and self.board[x][y - 1] != 4 and self.board[x][y - 1] != 5:
                        self.board[x][y - 1] = 3
                    if y < 9 and self.board[x][y + 1] != 4 and self.board[x][y + 1] != 5:
                        self.board[x][y + 1] = 3
                    x += 1
                if x < 10:
                    self.board[x][y] = 3
                    if y > 0:
                        self.board[x][y - 1] = 3
                    if y < 9:
                        self.board[x][y + 1] = 3

                x, y = cell_coords
                while y >= 0 and (self.board[x][y] == 4 or self.board[x][y] == 5):
                    self.board[x][y] = 5
                    if x > 0 and self.board[x - 1][y] != 4 and self.board[x - 1][y] != 5:
                        self.board[x - 1][y] = 3
                    if x < 9 and self.board[x + 1][y] != 4 and self.board[x + 1][y] != 5:
                        self.board[x + 1][y] = 3
                    y -= 1
                if y >= 0:
                    self.board[x][y] = 3
                    if x > 0:
                        self.board[x - 1][y] = 3
                    if x < 9:
                        self.board[x + 1][y] = 3

                x, y = cell_coords
                while y <= 9 and (self.board[x][y] == 4 or self.board[x][y] == 5):
                    if x > 0 and self.board[x - 1][y] != 4 and self.board[x - 1][y] != 5:
                        self.board[x - 1][y] = 3
                    if x < 9 and self.board[x + 1][y] != 4 and self.board[x + 1][y] != 5:
                        self.board[x + 1][y] = 3
                    y += 1
                if y < 10:
                    self.board[x][y] = 3
                    if x > 0:
                        self.board[x - 1][y] = 3
                    if x < 9:
                        self.board[x + 1][y] = 3
        else:
            pass


class EnemyBoard(Board):  # работа вражеского поля
    def __init__(self, width1, height1):
        super().__init__(width1, height1)

    def on_click(self, cell_coords):
        if self.board[cell_coords[0]][cell_coords[1]] == 0:
            self.board[cell_coords[0]][cell_coords[1]] = 3
            return 0
        elif self.board[cell_coords[0]][cell_coords[1]] == 2:
            self.board[cell_coords[0]][cell_coords[1]] = 4
            x, y = cell_coords
            not_kill = False
            while not not_kill and x >= 0 and self.board[x][y] != 0 and self.board[x][y] != 3:
                if self.board[x][y] == 2:
                    not_kill = True
                x -= 1
            x, y = cell_coords
            while not not_kill and x <= 9 and self.board[x][y] != 0 and self.board[x][y] != 3:
                if self.board[x][y] == 2:
                    not_kill = True
                x += 1
            x, y = cell_coords
            while not not_kill and y >= 0 and self.board[x][y] != 0 and self.board[x][y] != 3:
                if self.board[x][y] == 2:
                    not_kill = True
                y -= 1
            x, y = cell_coords
            while not not_kill and y <= 9 and self.board[x][y] != 0 and self.board[x][y] != 3:
                if self.board[x][y] == 2:
                    not_kill = True
                y += 1

            if not not_kill:
                x, y = cell_coords
                while x >= 0 and (self.board[x][y] == 4 or self.board[x][y] == 5):
                    self.board[x][y] = 5
                    if y > 0 and self.board[x][y - 1] != 4 and self.board[x][y - 1] != 5:
                        self.board[x][y - 1] = 3
                    if y < 9 and self.board[x][y + 1] != 4 and self.board[x][y + 1] != 5:
                        self.board[x][y + 1] = 3
                    x -= 1
                if x >= 0:
                    self.board[x][y] = 3
                    if y > 0:
                        self.board[x][y - 1] = 3
                    if y < 9:
                        self.board[x][y + 1] = 3

                x, y = cell_coords
                while x <= 9 and (self.board[x][y] == 4 or self.board[x][y] == 5):
                    self.board[x][y] = 5
                    if y > 0 and self.board[x][y - 1] != 4 and self.board[x][y - 1] != 5:
                        self.board[x][y - 1] = 3
                    if y < 9 and self.board[x][y + 1] != 4 and self.board[x][y + 1] != 5:
                        self.board[x][y + 1] = 3
                    x += 1
                if x < 10:
                    self.board[x][y] = 3
                    if y > 0:
                        self.board[x][y - 1] = 3
                    if y < 9:
                        self.board[x][y + 1] = 3

                x, y = cell_coords
                while y >= 0 and (self.board[x][y] == 4 or self.board[x][y] == 5):
                    self.board[x][y] = 5
                    if x > 0 and self.board[x - 1][y] != 4 and self.board[x - 1][y] != 5:
                        self.board[x - 1][y] = 3
                    if x < 9 and self.board[x + 1][y] != 4 and self.board[x + 1][y] != 5:
                        self.board[x + 1][y] = 3
                    y -= 1
                if y >= 0:
                    self.board[x][y] = 3
                    if x > 0:
                        self.board[x - 1][y] = 3
                    if x < 9:
                        self.board[x + 1][y] = 3

                x, y = cell_coords
                while y <= 9 and (self.board[x][y] == 4 or self.board[x][y] == 5):
                    self.board[x][y] = 5
                    if x > 0 and self.board[x - 1][y] != 4 and self.board[x - 1][y] != 5:
                        self.board[x - 1][y] = 3
                    if x < 9 and self.board[x + 1][y] != 4 and self.board[x + 1][y] != 5:
                        self.board[x + 1][y] = 3
                    y += 1
                if y < 10:
                    self.board[x][y] = 3
                    if x > 0:
                        self.board[x - 1][y] = 3
                    if x < 9:
                        self.board[x + 1][y] = 3
            return 1
        else:
            return 0


def terminate():  # закрытие игры
    pygame.quit()
    sys.exit()


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


class Button:  # кнопка
    def __init__(self, x, y, w, h, txt):
        self.x = x
        self.y = y
        self.width = w
        self.height = h
        self.text = txt


def rect_crossing(ship1, ship2):  # проверка накладываются ли корабли
    x1, y1, w1, h1, x2, y2, w2, h2 = ship1.x, ship1.y, ship1.width, ship1.height, ship2.x, ship2.y, \
                                     ship2.width, ship2.height
    if x2 < x1:
        x1, y1, w1, h1, x2, y2, w2, h2 = x2, y2, w2, h2, x1, y1, w1, h1
    return x1 <= x2 <= x1 + w1 and (y1 <= y2 and y1 <= y2 <= y1 + h1 or y2 <= y1 and y2 <= y1 <= y2
                                    + h2)


def ship_in_board(ship, board):  # проверка корабль выходит за поле
    return board.left <= ship.x <= board.left + board.cell_size * 10 and \
           board.left <= ship.x + ship.width <= board.left + board.cell_size * 10 and \
           board.top <= ship.y <= board.height + board.cell_size * 10 and \
           board.top <= ship.y + ship.height <= board.top + board.cell_size * 10


def random_ship(number):  # 1 - свой, 2 чужой
    arr = [[0 for __ in range(10)] for _ in range(10)]   # функция выстрела
    for size_ship in range(4, 0, -1):
        for _ in range(5 - size_ship):
            rotation = random.randint(0, 1)
            x, y, dx, dy = 0, 0, 0, 0
            good = False
            while x + rotation % 2 * size_ship >= 10 or \
                    y + (rotation + 1) % 2 * size_ship >= 10 or not good:
                good = False
                rotation, x, y = random.randint(0, 1), random.randint(0, 9), random.randint(0, 9)
                if x > 9 or y > 9:
                    print(x, y)

                if rotation % 2 == 0:
                    dx = 1
                    dy = size_ship
                else:
                    dx = size_ship
                    dy = 1
                if x + dx > 10 or y + dy > 10:
                    continue

                ok = True
                for x0 in range(x, x + dx):
                    for y0 in range(y, y + dy):
                        if x0 > 0 and (
                                arr[x0 - 1][y0] != 0 or
                                (y0 > 0 and arr[x0 - 1][y0 - 1] != 0) or
                                (y0 < 9 and arr[x0 - 1][y0 + 1] != 0)):
                            ok = False
                            break
                        if x0 < 9 and (
                                arr[x0 + 1][y0] != 0 or
                                (y0 > 0 and arr[x0 + 1][y0 - 1] != 0) or
                                (y0 < 9 and arr[x0 + 1][y0 + 1] != 0)):
                            ok = False
                            break
                        if arr[x0][y0] != 0 or \
                                (y0 > 0 and arr[x0][y0 - 1] != 0) or \
                                (y0 < 9 and arr[x0][y0 + 1] != 0):
                            ok = False
                            break
                    if not ok:
                        break
                if ok:
                    good = True
            for x0 in range(x, x + dx):
                for y0 in range(y, y + dy):
                    arr[x0][y0] = number
    return arr


def random_ship_player(arr_ship):  # работа кнопки рандомного раставления кораблей
    arr = [[0 for __ in range(10)] for _ in range(10)]
    for i in range(len(arr_ship)):
        rotation = random.randint(0, 1)
        size_ship = arr_ship[i].size
        x, y, dx, dy = 0, 0, 0, 0
        good = False
        c = 0
        while x + rotation % 2 * size_ship >= 10 or y + (rotation + 1) % 2 * size_ship >= 10 or \
                not good and c < 2000:
            c += 1
            good = False
            rotation, x, y = random.randint(0, 1), random.randint(0, 9), random.randint(0, 9)
            if rotation % 2 == 0:
                dx = 1
                dy = size_ship
            else:
                dx = size_ship
                dy = 1
            if x + dx > 10 or y + dy > 10:
                continue

            ok = True
            for x0 in range(x, x + dx):
                for y0 in range(y, y + dy):
                    if x0 > 0 and (
                            arr[x0 - 1][y0] != 0 or
                            (y0 > 0 and arr[x0 - 1][y0 - 1] != 0) or
                            (y0 < 9 and arr[x0 - 1][y0 + 1] != 0)):
                        ok = False
                        break
                    if x0 < 9 and (
                            arr[x0 + 1][y0] != 0 or
                            (y0 > 0 and arr[x0 + 1][y0 - 1] != 0) or
                            (y0 < 9 and arr[x0 + 1][y0 + 1] != 0)):
                        ok = False
                        break
                    if arr[x0][y0] != 0 or \
                            (y0 > 0 and arr[x0][y0 - 1] != 0) or \
                            (y0 < 9 and arr[x0][y0 + 1] != 0):
                        ok = False
                        break
                if not ok:
                    break
            if ok:
                good = True
        if c >= 2000:
            return random_ship_player(arr_ship)
        for x0 in range(x, x + dx):
            for y0 in range(y, y + dy):
                arr[x0][y0] = 1
        arr_ship[i].rotation = rotation
        arr_ship[i].x = x * 30 + 30
        arr_ship[i].y = y * 30 + 30
        arr_ship[i].width = dx * 30
        arr_ship[i].height = dy * 30
    return arr_ship


def start_screen():  # начальный экран
    fon = pygame.transform.scale(load_image('ship.png'), (1000, 600))
    screen.blit(fon, (0, 0))

    font = pygame.font.Font(None, 75)
    string_rendered = font.render("МОРСКОЙ БОЙ", True, pygame.Color('white'))
    intro_rect = string_rendered.get_rect()
    intro_rect.top = 450
    intro_rect.x = 500 - intro_rect.width // 2
    screen.blit(string_rendered, intro_rect)

    font = pygame.font.Font(None, 30)
    string_rendered = font.render("Нажмите на экран, чтобы продолжить", True, pygame.Color('white'))
    intro_rect = string_rendered.get_rect()
    intro_rect.top = 510
    intro_rect.x = 500 - intro_rect.width // 2
    screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return screen_arrange()
        pygame.display.flip()
        clock.tick(30)


def screen_arrange():  # растоновка кораблей
    our_board.set_view(30, 30, 30)
    # fon = pygame.transform.scale(load_image('ship.png'), (1000, 600))
    # screen.blit(fon, (0, 0))
    screen.fill((208, 208, 208))
    our_board.render(screen)

    arr_ship = []
    c = 1
    for size_ship in range(1, 5):
        for i in range(5 - size_ship):
            arr_ship.append(Ship(size_ship, c * 32, 360, 0))
            c += 1

    text = ["РАССТАВТЕ КОРАБЛИ НА ПОЛЕ", "",
            "Между кораблями должна быть свободная клетка",
            "Корабли не должны выступать за поле", "",
            "Чтобы передвинуть корабль нажмите левую кнопку мыши",
            "Чтобы перевернуть корабль нажмите правую кнопку мыши"]
    font = pygame.font.Font(None, 30)

    btn_random = Button(600, 200, 300, 80, "Расставить")
    btn_continue = Button(600, 300, 300, 80, "Играть")

    running = True
    drawing = False
    d_x, d_y = 0, 0
    tx, ty = 0, 0
    ind_ship = None
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()

            pos_x, pos_y = pygame.mouse.get_pos()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for i in range(len(arr_ship)):
                    if arr_ship[i].x < pos_x < arr_ship[i].x + arr_ship[i].width and \
                            arr_ship[i].y < pos_y < arr_ship[i].y + arr_ship[i].height:
                        tx, ty = arr_ship[i].x, arr_ship[i].y
                        ind_ship = i
                        d_x = pos_x - arr_ship[i].x
                        d_y = pos_y - arr_ship[i].y
                        drawing = True  # включаем режим рисования
                        break

            if event.type == pygame.MOUSEBUTTONDOWN and not drawing and event.button == 3:
                for i in range(len(arr_ship)):
                    if arr_ship[i].x < pos_x < arr_ship[i].x + arr_ship[i].width and \
                            arr_ship[i].y < pos_y < arr_ship[i].y + arr_ship[i].height:
                        t = Ship(arr_ship[i].size, arr_ship[i].x, arr_ship[i].y,
                                 arr_ship[i].rotation)
                        arr_ship[i].rotation = (arr_ship[i].rotation + 1) % 4
                        arr_ship[i].width = 30 + arr_ship[i].rotation % 2 * (arr_ship[i].size
                                                                             - 1) * 30
                        arr_ship[i].height = 30 + (arr_ship[i].rotation + 1) % 2 * (arr_ship[i].size
                                                                                    - 1) * 30
                        for j in range(len(arr_ship)):
                            if j == i:
                                continue
                            if rect_crossing(arr_ship[i], arr_ship[j]):
                                arr_ship[i] = t
                                break

            if event.type == pygame.MOUSEBUTTONUP and event.button == 1 and drawing:
                # сохраняем нарисованное (на втором холсте)
                if arr_ship[ind_ship].x % 30 > 15:
                    arr_ship[ind_ship].x += 30
                if arr_ship[ind_ship].y % 30 > 15:
                    arr_ship[ind_ship].y += 30
                arr_ship[ind_ship].x = arr_ship[ind_ship].x // 30 * 30
                arr_ship[ind_ship].y = arr_ship[ind_ship].y // 30 * 30
                if arr_ship[ind_ship].x + arr_ship[ind_ship].width > 330 or \
                        arr_ship[ind_ship].x < 30 or \
                        arr_ship[ind_ship].y + arr_ship[ind_ship].height > 330 or \
                        arr_ship[ind_ship].y < 30:
                    arr_ship[ind_ship].x = tx
                    arr_ship[ind_ship].y = ty
                else:
                    for j in range(len(arr_ship)):
                        if j == ind_ship:
                            continue
                        if rect_crossing(arr_ship[ind_ship], arr_ship[j]):
                            arr_ship[ind_ship].x = tx
                            arr_ship[ind_ship].y = ty
                            break
                drawing = False
                ind_ship = None

            if event.type == pygame.MOUSEMOTION:
                # запоминаем текущие размеры
                pos_x, pos_y = pygame.mouse.get_pos()
                if drawing:
                    arr_ship[ind_ship].x, arr_ship[ind_ship].y = pos_x - d_x, pos_y - d_y

            if event.type == pygame.MOUSEBUTTONDOWN:
                for btn in [btn_random, btn_continue]:
                    if btn.x < pos_x < btn.x + btn.width and btn.y < pos_y < btn.y + btn.height:
                        if btn.text == "Расставить":
                            arr_ship = random_ship_player(arr_ship)
                        elif btn.text == "Играть":
                            good = True
                            for ship in arr_ship:
                                good = ship_in_board(ship, our_board)
                                if not good:
                                    break
                            if good:
                                for ship in arr_ship:
                                    our_board.add_ship(ship, 1)
                                screen_game()

        screen.fill((208, 208, 208))
        # screen.blit(fon, (0, 0))
        text_coord = 30
        for line in text:
            string_rendered = font.render(line, True, (0, 0, 0))
            intro_rect = string_rendered.get_rect()
            text_coord += 2
            intro_rect.top = text_coord
            intro_rect.x = 360
            text_coord += intro_rect.height
            screen.blit(string_rendered, intro_rect)
        our_board.render(screen)
        for btn in [btn_random, btn_continue]:
            pygame.draw.rect(screen, (192, 192, 192),
                             [btn.x, btn.y, btn.width, btn.height],
                             width=0)
            pygame.draw.rect(screen, (96, 96, 96),
                             [btn.x, btn.y, btn.width, btn.height],
                             width=2)

            string_rendered = font.render(btn.text, True, (0, 0, 0))
            intro_rect = string_rendered.get_rect()
            intro_rect.top = btn.y + (btn.height - intro_rect.height) // 2
            intro_rect.x = btn.x + (btn.width - intro_rect.width) // 2
            text_coord += intro_rect.height
            screen.blit(string_rendered, intro_rect)
        for ship in arr_ship:
            for x in range(ship.width // 30):
                for y in range(ship.height // 30):
                    pygame.draw.rect(screen, (0, 0, 205),
                                     [ship.x + 30 * x, ship.y + 30 * y,
                                      30, 30],
                                     width=3)
        pygame.display.flip()
        clock.tick(30)


def screen_game():  # основная игра
    enemy_board.set_view(390, 30, 30)
    enemy_board.board = random_ship(2)
    # fon = pygame.transform.scale(load_image('ship.png'), (1000, 600))
    # screen.blit(fon, (0, 0))
    screen.fill((208, 208, 208))
    our_board.render(screen)
    enemy_board.render(screen)
    font = pygame.font.Font(None, 30)

    move_number = 0
    letter = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j"]
    move_arr = [str(i + 1) + "." for i in range(10)]
    btn_new_game = Button(720, 360, 200, 50, "Новая игра")
    winning_me = False
    winning_bot = False
    context = "Ваш ход"

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and not (winning_me or winning_bot):
                    pos = event.pos
                    p = enemy_board.get_cell(pos)

                    if p and (enemy_board.board[p[0]][p[1]] == 0 or
                              enemy_board.board[p[0]][p[1]] == 2):
                        enemy_board.on_click(p)  # наш удар
                        move_number += 1
                        if move_number < 11:
                            move_arr[move_number - 1] = str(move_number) + ". " + letter[p[1]] + str(
                                p[0] + 1) + " - ваш ход"
                        else:
                            for i in range(9):
                                move_arr[i] = move_arr[i + 1]
                            move_arr[9] = str(move_number) + ". " + letter[p[1]] + str(
                                p[0] + 1) + " - ваш ход"
                        context = "Ход компьютера"
                        winning_me = True
                        for x in range(10):
                            for y in range(10):
                                if enemy_board.board[x][y] == 2:
                                    winning_me = False

                        if not winning_me:
                            vertical = horizontal = False
                            found = False
                            for x in range(10):
                                for y in range(10):
                                    if our_board.board[x][y] == 4:
                                        if x > 0 and our_board.board[x - 1][y] == 4:
                                            horizontal = True
                                        elif x < 9 and our_board.board[x + 1][y] == 4:
                                            horizontal = True
                                        elif y > 0 and our_board.board[x][y - 1] == 4:
                                            vertical = True
                                        elif y < 9 and our_board.board[x][y + 1] == 4:
                                            vertical = True

                                        if x > 0 and horizontal and \
                                                (our_board.board[x - 1][y] == 0 or
                                                 our_board.board[x - 1][y] == 1):
                                            our_board.on_click((x - 1, y))
                                            x, y = y, x - 1

                                            move_number += 1
                                            if move_number < 11:
                                                move_arr[move_number - 1] = str(move_number) + \
                                                                            ". " + letter[x] + \
                                                                            str(y + 1) + \
                                                                            " - ход компьютера"
                                            else:
                                                for i in range(9):
                                                    move_arr[i] = move_arr[i + 1]
                                                move_arr[9] = str(move_number) + ". " + letter[
                                                    x] + str(y + 1) + " - ход компьютера"
                                            found = True
                                            break
                                        elif x < 9 and horizontal and \
                                                (our_board.board[x + 1][y] == 0 or
                                                 our_board.board[x + 1][y] == 1):
                                            our_board.on_click((x + 1, y))
                                            x, y = y, x + 1
                                            move_number += 1
                                            if move_number < 11:
                                                move_arr[move_number - 1] = str(move_number) + \
                                                                            ". " + letter[x] + \
                                                                            str(y + 1) + \
                                                                            " - ход компьютера"
                                            else:
                                                for i in range(9):
                                                    move_arr[i] = move_arr[i + 1]
                                                move_arr[9] = str(move_number) + ". " + letter[
                                                    x] + str(y + 1) + " - ход компьютера"
                                            found = True
                                            break
                                        elif x > 0 and not vertical and \
                                                (our_board.board[x - 1][y] == 0 or
                                                 our_board.board[x - 1][y] == 1):
                                            our_board.on_click((x - 1, y))
                                            x, y = y, x - 1
                                            move_number += 1
                                            if move_number < 11:
                                                move_arr[move_number - 1] = str(move_number) + \
                                                                            ". " + letter[x] + \
                                                                            str(y + 1) + \
                                                                            " - ход компьютера"
                                            else:
                                                for i in range(9):
                                                    move_arr[i] = move_arr[i + 1]
                                                move_arr[9] = str(move_number) + ". " + letter[
                                                    x] + str(y + 1) + " - ход компьютера"
                                            found = True
                                            break
                                        elif x < 9 and not vertical and \
                                                (our_board.board[x + 1][y] == 0 or
                                                 our_board.board[x + 1][y] == 1):
                                            our_board.on_click((x + 1, y))
                                            x, y = y, x + 1
                                            move_number += 1
                                            if move_number < 11:
                                                move_arr[move_number - 1] = str(move_number) + \
                                                                            ". " + letter[x] + \
                                                                            str(y + 1) + \
                                                                            " - ход компьютера"
                                            else:
                                                for i in range(9):
                                                    move_arr[i] = move_arr[i + 1]
                                                move_arr[9] = str(move_number) + ". " + letter[
                                                    x] + str(y + 1) + " - ход компьютера"
                                            found = True
                                            break
                                        elif y > 0 and not horizontal and \
                                                (our_board.board[x][y - 1] == 0 or
                                                 our_board.board[x][y - 1] == 1):
                                            our_board.on_click((x, y - 1))
                                            x, y = y - 1, x
                                            move_number += 1
                                            if move_number < 11:
                                                move_arr[move_number - 1] = str(move_number) + \
                                                                            ". " + letter[x] + \
                                                                            str(y + 1) + \
                                                                            " - ход компьютера"
                                            else:
                                                for i in range(9):
                                                    move_arr[i] = move_arr[i + 1]
                                                move_arr[9] = str(move_number) + ". " + letter[
                                                    x] + str(y + 1) + " - ход компьютера"
                                            found = True
                                            break
                                        elif y < 9 and not horizontal and \
                                                (our_board.board[x][y + 1] == 0 or
                                                 our_board.board[x][y + 1] == 1):
                                            our_board.on_click((x, y + 1))
                                            x, y = y + 1, x
                                            move_number += 1
                                            if move_number < 11:
                                                move_arr[move_number - 1] = str(move_number) + \
                                                                            ". " + letter[x] + \
                                                                            str(y + 1) + \
                                                                            " - ход компьютера"
                                            else:
                                                for i in range(9):
                                                    move_arr[i] = move_arr[i + 1]
                                                move_arr[9] = str(move_number) + ". " + letter[
                                                    x] + str(y + 1) + " - ход компьютера"
                                            found = True
                                            break
                                if found:
                                    break
                            if not found:
                                x, y = random.randint(0, 9), random.randint(0, 9)
                                while our_board.board[x][y] != 0 and our_board.board[x][y] != 1:
                                    x, y = random.randint(0, 9), random.randint(0, 9)
                                our_board.on_click((x, y))
                                x, y = y, x
                                move_number += 1
                                if move_number < 11:
                                    move_arr[move_number - 1] = str(move_number) + ". " + letter[
                                        x] + str(y + 1) + " - ход компьютера"
                                else:
                                    for i in range(9):
                                        move_arr[i] = move_arr[i + 1]
                                    move_arr[9] = str(move_number) + ". " + letter[x] + str(
                                        y + 1) + " - ход компьютера"
                            context = "Ваш ход"
                            winning_bot = True
                            for x in range(10):
                                for y in range(10):
                                    if our_board.board[x][y] == 1:
                                        winning_bot = False
                            if winning_bot:
                                for x in range(10):
                                    for y in range(10):
                                        if enemy_board.board[x][y] == 2:
                                            enemy_board.board[x][y] = 1
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos_x, pos_y = event.pos
                for btn in [btn_new_game]:
                    if btn.x < pos_x < btn.x + btn.width and btn.y < pos_y < btn.y + btn.height:
                        if btn.text == "Новая игра":
                            return new_game()

        # screen.blit(fon, (0, 0))
        screen.fill((208, 208, 208))
        our_board.render(screen)
        enemy_board.render(screen)

        text_coord = 30
        for hod in move_arr:
            string_rendered = font.render(hod, True, (0, 0, 0))
            intro_rect = string_rendered.get_rect()
            text_coord += 10
            intro_rect.top = text_coord
            intro_rect.x = 720
            text_coord += intro_rect.height
            screen.blit(string_rendered, intro_rect)

        for btn in [btn_new_game]:
            pygame.draw.rect(screen, (192, 192, 192),
                             [btn.x, btn.y, btn.width, btn.height],
                             width=0)
            pygame.draw.rect(screen, (96, 96, 96),
                             [btn.x, btn.y, btn.width, btn.height],
                             width=2)
            string_rendered = font.render(btn.text, True, (0, 0, 0))
            intro_rect = string_rendered.get_rect()
            intro_rect.top = btn.y + (btn.height - intro_rect.height) // 2
            intro_rect.x = btn.x + (btn.width - intro_rect.width) // 2
            text_coord += intro_rect.height
            screen.blit(string_rendered, intro_rect)

        if winning_bot:
            context = "ВЫИГРАЛ КОМПЬЮТЕР"
        if winning_me:
            context = "ВЫ ВЫИГРАЛИ"
        string_rendered = font.render(context, True, (0, 0, 0))
        intro_rect = string_rendered.get_rect()
        intro_rect.top = 360 + (100 - intro_rect.height) // 2
        intro_rect.x = 390 + (300 - intro_rect.width) // 2
        screen.blit(string_rendered, intro_rect)

        pygame.display.flip()
        clock.tick(30)


def new_game():
    for x in range(10):
        for y in range(10):
            our_board.board[x][y] = 0
            enemy_board.board[x][y] = 0
    screen_arrange()


pygame.init()
pygame.display.set_caption('Battleship')
size = width, height = 1000, 600
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()

our_board = OurBoard(10, 10)

enemy_board = EnemyBoard(10, 10)

start_screen()
