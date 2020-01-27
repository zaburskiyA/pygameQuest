import os, pygame, random, sys
from math import sqrt
import math

pygame.init()
infoObject = pygame.display.Info()
screen = pygame.display.set_mode((infoObject.current_w - 500, infoObject.current_h - 300))
size = width, height = infoObject.current_w, infoObject.current_h

clock = pygame.time.Clock()
FPS = 60
STEP = 3


class Boss(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y, damage, life, speed, num_boss, region=350):
        super().__init__(all_sprites, monster_gr)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)
        self.xd2 = x
        self.region = region
        self.yd2 = y
        self.x = x
        self.y = y
        self.speed = speed
        self.life = life
        self.damage = damage
        self.check_update = 0
        self.mask = pygame.mask.from_surface(self.image)
        self.num_boss = num_boss

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def move_towards_player(self, player):
        global timer
        dx, dy = player.rect.x - self.rect.x, player.rect.y - self.rect.y
        dist = math.hypot(dx, dy) + 1
        dx, dy = dx / dist, dy / dist

        px, py = player.coord()
        dx2, dy2 = px - self.xd2, py - self.yd2
        dist2 = math.hypot(dx2, dy2) + 1
        coll = pygame.sprite.groupcollide(monster_gr, wall_group, False, False,
                                          collided=pygame.sprite.collide_mask)
        coll1 = pygame.sprite.groupcollide(monster_gr, table_group, False, False,
                                           collided=pygame.sprite.collide_mask)
        coll2 = pygame.sprite.groupcollide(monster_gr, door_group, False, False,
                                           collided=pygame.sprite.collide_mask)
        coll3 = pygame.sprite.groupcollide(player_group, monster_gr, False, False,
                                           collided=pygame.sprite.collide_rect)
        coll4 = pygame.sprite.groupcollide(player_group, monster_gr, False, False,
                                           collided=pygame.sprite.collide_mask)

        if abs(dist2) < self.region or abs(dist) < 150:
            if coll or coll1 or coll2:
                if self.num_boss != 2:
                    self.rect.x -= dx * 2
                    self.rect.y -= dy * 2
                    self.x -= dx * 2
                    self.y -= dy * 2
            if dist < 70:
                if player.fight == 1:
                    self.del_life(player.damage)
                    print("здоровье босса", self.life)
                    player.damage = 0
                    if self.life <= 0:
                        pygame.sprite.Sprite.kill(self)
                        print("u kill boss")
                        player.add_money(random.choice((10, 10, 10, 15, 20)))
                        player.add_key("bosskey")

            if coll4:
                if player.flag_sk:
                    player.flag_sk = False
                    if pygame.sprite.groupcollide(player_group, monster_gr, False, False,
                                                  collided=pygame.sprite.collide_mask):
                        player.del_life(self.damage)
                        print(player.life)
                        self.rect.x -= dx * 2
                        self.rect.y -= dy * 2
                        self.x -= dx * 2
                        self.y -= dy * 2
                        timer = True
                        """
                        if player.life <= 0:
                            if player.life_count > 0:
                                player.life_count -= 1
                                player.rect.x = 100
                                player.x = 100
                                player.rect.y = 100
                                player.y = 100
                        """
                else:
                    timer = True
            else:
                self.rect.x += dx * 2
                self.rect.y += dy * 2
                self.x += dx * 2
                self.y += dy * 2
        if dx < 0:
            if self.num_boss == 1:
                self.change(load_image('fBossL.png'), 4, 1, self.rect.x, self.rect.y)
            elif self.num_boss == 2:
                self.change(load_image('sBossL.png'), 4, 1, self.rect.x, self.rect.y)

        else:
            if self.num_boss == 1:
                self.change(load_image('fBossR.png'), 4, 1, self.rect.x, self.rect.y)
            elif self.num_boss == 2:
                self.change(load_image('sBossL.png'), 4, 1, self.rect.x, self.rect.y)

    def update(self):
        global kill
        self.check_update += 1
        self.move_towards_player(player)
        if self.check_update % 30 == 0:
            self.cur_frame = (self.cur_frame + 1) % len(self.frames)
            self.image = self.frames[self.cur_frame]
        if kill:
            pygame.sprite.Sprite.kill(self)

    def change(self, sheet, columns, rows, x, y):
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame %= 4
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)

        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def del_life(self, num):
        self.life -= num

    def add_life(self, num):
        self.life += num


class Skeleton(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y):
        super().__init__(all_sprites, monster_gr)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)
        self.xd2 = x
        self.yd2 = y
        self.x = x
        self.y = y
        self.life = 150
        self.damage = 5
        self.check_update = 0
        self.mask = pygame.mask.from_surface(self.image)

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def move_towards_player(self, player):
        global timer
        dx, dy = player.rect.x - self.rect.x, player.rect.y - self.rect.y
        dist = math.hypot(dx, dy) + 1
        dx, dy = dx / dist, dy / dist

        px, py = player.coord()
        dx2, dy2 = px - self.xd2, py - self.yd2
        dist2 = math.hypot(dx2, dy2) + 1
        coll = pygame.sprite.groupcollide(monster_gr, wall_group, False, False,
                                          collided=pygame.sprite.collide_mask)
        coll1 = pygame.sprite.groupcollide(monster_gr, table_group, False, False,
                                           collided=pygame.sprite.collide_mask)
        coll2 = pygame.sprite.groupcollide(monster_gr, door_group, False, False,
                                           collided=pygame.sprite.collide_mask)
        coll3 = pygame.sprite.groupcollide(player_group, monster_gr, False, False,
                                           collided=pygame.sprite.collide_rect)
        coll4 = pygame.sprite.groupcollide(player_group, monster_gr, False, False,
                                           collided=pygame.sprite.collide_mask)

        if abs(dist2) < 200 or abs(dist) < 70:
            if coll or coll1 or coll2:
                self.rect.x -= dx * 2
                self.rect.y -= dy * 2
                self.x -= dx * 2
                self.y -= dy * 2
            if dist < 70:
                if player.fight == 1:
                    self.del_life(player.damage)
                    print("здоровье скелета", self.life)
                    player.damage = 0
                    if self.life <= 0:
                        pygame.sprite.Sprite.kill(self)
                        print("u kill skeleton")
                        player.add_money(random.choice((10, 10, 10, 15, 20)))

            if coll4:
                if player.flag_sk:
                    player.flag_sk = False
                    if pygame.sprite.groupcollide(player_group, monster_gr, False, False,
                                                  collided=pygame.sprite.collide_mask):
                        player.del_life(self.damage)
                        print("здоровье игрока", player.life)
                        self.rect.x -= dx * 2
                        self.rect.y -= dy * 2
                        self.x -= dx * 2
                        self.y -= dy * 2
                        timer = True
                        """
                        if player.life <= 0:
                            if player.life_count > 0:
                                player.life_count -= 1
                                player.rect.x = 100
                                player.x = 100
                                player.rect.y = 100
                                player.y = 100
                        """


                else:
                    timer = True



            else:
                self.rect.x += dx * 2
                self.rect.y += dy * 2
                self.x += dx * 2
                self.y += dy * 2
        if dx < 0:
            self.change(load_image('skeletonL.png'), 4, 1, self.rect.x, self.rect.y)
        else:
            self.change(load_image('skeleton.png'), 4, 1, self.rect.x, self.rect.y)

    def update(self):
        global kill
        self.check_update += 1
        self.move_towards_player(player)
        if self.check_update % 30 == 0:
            self.cur_frame = (self.cur_frame + 1) % len(self.frames)
            self.image = self.frames[self.cur_frame]
        if kill:
            pygame.sprite.Sprite.kill(self)

    def change(self, sheet, columns, rows, x, y):
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame %= 4
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)

        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def del_life(self, num):
        self.life -= num

    def add_life(self, num):
        self.life += num


class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y, rkey=0, ykey=0, bkey=0, bosskey=0, money=0, life_count=1, life=100):
        super().__init__(all_sprites, player_group)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)
        self.check_frame = 0
        self.mask = pygame.mask.from_surface(self.image)
        self.mask2 = pygame.mask.from_surface(self.image)
        self.rkey = rkey
        self.ykey = ykey
        self.bkey = bkey
        self.bosskey = bosskey
        self.Money = money
        self.life = life
        self.damage = 20
        self.fight = 0
        self.x = x
        self.y = y
        self.flag_sk = False
        self.life_count = life_count

    def change(self, sheet, columns, rows, x, y):
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame %= 4
        self.check_frame += 1
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)

        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self):
        global kill, level_x, level_y, lvl
        if kill:
            pygame.sprite.Sprite.kill(self)
        self.check_frame += 1
        if self.check_frame % 40 == 0:
            self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]
        coll = pygame.sprite.groupcollide(player_group, wall_group, False, False,
                                          collided=pygame.sprite.collide_mask)
        coll1 = pygame.sprite.groupcollide(player_group, table_group, False, False,
                                           collided=pygame.sprite.collide_mask)
        coll2 = pygame.sprite.groupcollide(player_group, door_group, False, False,
                                           collided=pygame.sprite.collide_mask)
        coll3 = pygame.sprite.groupcollide(player_group, ladder_gr, False, False,
                                           collided=pygame.sprite.collide_rect)
        if coll or coll1 or coll2:
            return True
        elif coll3:
            kill_all()
            if lvl == 1:
                level_x, level_y = generate_level(load_level('карта2.txt'), 2)
                self.rect.x = 1650
                self.x = 1650
                self.rect.y = 50
                self.y = 50
                lvl += 1
        else:
            return False

    def add_money(self, num):
        """увеличивает количество денег персонажа на num"""
        self.Money += num

    def del_money(self, num):
        """уменьшает количество денег персонажа на num"""
        self.Money -= num

    def check_money(self):
        return self.Money

    def check_key(self, tipe):
        """просматривает количесво ключей нужного типа"""
        if tipe == "r":
            return self.rkey
        elif tipe == "y":
            return self.ykey
        elif tipe == "b":
            return self.bkey
        elif tipe == "bosskey":
            return self.bosskey

    def add_key(self, tipe):
        """добавляет персонажу нужный тип ключа"""
        if tipe == "r":
            self.rkey += 1
        elif tipe == "y":
            self.ykey += 1
        elif tipe == "b":
            self.bkey += 1
        elif tipe == "bosskey":
            self.bosskey += 1

    def del_key(self, tipe):
        """Отбирает у персонажа нужный тип ключа"""
        if tipe == "r":
            self.rkey -= 1
        elif tipe == "y":
            self.ykey -= 1
        elif tipe == "b":
            self.bkey -= 1
        elif tipe == "bosskey":
            self.bosskey -= 1

    def coord(self):
        return self.x, self.y

    def del_life(self, num):
        self.life -= num

    def add_life(self, num):
        self.life += num

    def fight_flag(self, flag):
        if flag:
            self.fight = 1
        else:
            self.fight = 0


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print("Cannot")
        raise SystemExit(message)
    if colorkey is -1:
        colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    image = image.convert_alpha()
    return image


def wait(second, now):
    return pygame.time.get_ticks() - now > second * 1000 - 100 and \
           pygame.time.get_ticks() - now < second * 1000 + 100


def terminate():
    pygame.quit()
    sys.exit()


def load_level(filename):
    filename = "data/" + filename
    # читаем уровень, убирая символы перевода строки
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    # и подсчитываем максимальную длину
    max_width = max(map(len, level_map))

    # дополняем каждую строку пустыми клетками ('.')
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


tile_images = {'wall': load_image('box.png'), 'empty': load_image('grass.png'),
               'door': load_image('door.png'), 'table': load_image('table.png'),
               'Nstand': load_image('nightstand_close.png'), 'ladder': load_image('ladder.png')}
player_image = load_image('mar.png', -1)

tile_width = tile_height = 50


class Camera:
    # зададим начальный сдвиг камеры
    def __init__(self):
        self.dx = 0
        self.dy = 0

    # сдвинуть объект obj на смещение камеры
    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    # позиционировать камеру на объекте target
    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - width // 3 - 100)
        self.dy = -(target.rect.y + target.rect.h // 2 - height // 3) + 25


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)


class Wall(pygame.sprite.Sprite):
    image = load_image("box.png")

    def __init__(self, x1, y1, x2, y2):
        super().__init__(all_sprites, wall_group)
        self.image = Wall.image
        self.rect = pygame.Rect(x1 + 1, y1 + 1, x2 - 1, y2 - 1)
        # вычисляем маску для эффективного сравнения
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        global kill
        if kill:
            pygame.sprite.Sprite.kill(self)


class Nightstand(pygame.sprite.Sprite):
    image = load_image("nightstand_close.png")
    imageclose = load_image("nightstand_close.png")
    imageopen = load_image("nightstand_open.png")
    maskim = load_image("mask.png")
    Mimage = load_image("Mnightstand_close.png")
    imageopenR = load_image("nightstandR_open.png")
    imageopenB = load_image("nightstandB_open.png")
    imageopenY = load_image("nightstandY_open.png")

    def __init__(self, x, y, Money=0, rkey=False, bkey=False, ykey=False):
        """Money - количество денег на умбочке, по умолчанию 0,
        rkey, bkey, ykey - это ключи, которые находятся на тумбочке. красный, синий, желтый ключь соответственно.
        True - ключ есть, False - ключа нет. по умолчанию ключей нет"""
        super().__init__(all_sprites, table_group)
        self.image = Nightstand.image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.ykey = ykey
        self.rkey = rkey
        self.bkey = bkey
        self.Money = Money
        self.mask = pygame.mask.from_surface(self.maskim)
        self.close = 2  # степень закрытости 2 - закрыт полностью, 1 - закрыт, но там есть лут, 0 - открыт и пуст
        if self.Money > 0:
            self.image = self.Mimage

    def update(self, plx, ply, *args):
        global kill
        dist = sqrt((int(plx) - int(self.rect.x)) ** 2 + (int(ply) - int(self.rect.y)) ** 2) < 60  # флаг дистанция
        # проверяет дистанцию между объетом и игроком
        if args and args[0].type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(args[0].pos) and dist:
            if self.close == 2:
                if self.rkey:
                    self.image = self.imageopenR
                    self.close = 1
                elif self.ykey:
                    self.image = self.imageopenY
                    self.close = 1
                elif self.bkey:
                    self.image = self.imageopenB
                    self.close = 1
                else:
                    self.image = self.imageopen
                    self.close = 0
                player.add_money(self.Money)
                self.Money = 0
            elif self.close == 1:
                if self.ykey:
                    self.ykey = False
                    player.add_key("y")
                elif self.rkey:
                    self.rkey = False
                    player.add_key("r")
                elif self.bkey:
                    self.bkey = False
                    player.add_key("b")
                self.image = self.imageopen
                self.close = 0
            elif self.close == 0:
                self.image = self.imageclose
                self.close = 2
        if kill:
            pygame.sprite.Sprite.kill(self)


class Table(pygame.sprite.Sprite):
    # картинки, которые используются в классе
    image = load_image("table.png")
    maskim = load_image("mask.png")
    image2 = load_image("table.png")
    imageM = load_image("Mtable.png")
    imageY = load_image("ktableY.png")
    imageR = load_image("ktableR.png")
    imageB = load_image("ktableB.png")
    imageYM = load_image("MktableY.png")
    imageRM = load_image("MktableR.png")
    imageBM = load_image("MktableB.png")

    def __init__(self, x, y, Money=0, rkey=False, bkey=False, ykey=False):
        """Money - количество денег на столе, по умолчанию 0,
        rkey, bkey, ykey - это ключи, которые находятся на столе. красный, синий, желтый ключь соответственно.
        True - ключ есть, False - ключа нет. по умолчанию ключей нет"""
        super().__init__(all_sprites, table_group)
        self.image = Table.image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.ykey = ykey
        self.rkey = rkey
        self.bkey = bkey
        self.Money = Money
        self.mask = pygame.mask.from_surface(self.maskim)
        # идет нахождение нужной картинки в зависимости от значений
        if self.rkey:
            if self.Money == 0:
                self.image = self.imageR
            else:
                self.image = self.imageRM
        elif self.ykey:
            if self.Money == 0:
                self.image = self.imageY
            else:
                self.image = self.imageYM
        elif self.bkey:
            if self.Money == 0:
                self.image = self.imageB
            else:
                self.image = self.imageBM
        else:
            if self.Money == 0:
                self.image = self.image2
            else:
                self.image = self.imageM

    def update(self, plx, ply, *args):
        global kill
        dist = sqrt((int(plx) - int(self.rect.x)) ** 2 + (int(ply) - int(self.rect.y)) ** 2) < 60  # флаг дистанция
        # проверяет дистанцию между объетом и игроком
        if args and args[0].type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(args[0].pos) and dist:
            self.image = self.image2
            if self.ykey:
                self.ykey = False
                player.add_key("y")
            elif self.rkey:
                self.rkey = False
                player.add_key("r")
            elif self.bkey:
                self.bkey = False
                player.add_key("b")
            player.add_money(self.Money)
            self.Money = 0
            print(player.check_key("r"))
            print(player.check_key("b"))
            print(player.check_key("y"))
            print(player.check_money())
        if kill:
            pygame.sprite.Sprite.kill(self)


class Ladder(pygame.sprite.Sprite):
    image = load_image("ladder.png")

    def __init__(self, x, y):
        super().__init__(all_sprites, ladder_gr)
        self.image = Ladder.image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        global kill
        if kill:
            pygame.sprite.Sprite.kill(self)


class Grass(pygame.sprite.Sprite):
    image = load_image("grass.png")

    def __init__(self, x, y):
        super().__init__(all_sprites, grass_gr)
        self.image = Grass.image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        global kill
        if kill:
            pygame.sprite.Sprite.kill(self)


class Door(pygame.sprite.Sprite):
    image = load_image("door.png")
    Yimage = load_image("Ydoor.png")
    Bimage = load_image("Bdoor.png")
    Rimage = load_image("Rdoor.png")
    openi = load_image("grass.png")
    emptmask = load_image("emptymask.png")
    bossdoor = load_image("Bossdoor.png")

    def __init__(self, x, y, tipe, open=False):
        """x, y - координаты верхнего левого угла картинки
        col - это цвет двери
        open - открыта или закрыта дверь. по умолчанию False"""
        super().__init__(all_sprites, door_group)
        self.image = Door.image
        self.rect = self.image.get_rect()
        self.open = open
        if not self.open:
            self.mask = pygame.mask.from_surface(self.image)
        self.tipe = tipe
        self.rect.x = x
        self.rect.y = y
        if self.tipe == "Y":
            self.image = self.Yimage
        elif self.tipe == "R":
            self.image = self.Rimage
        elif self.tipe == "B":
            self.image = self.Bimage
        elif self.tipe == "Boss":
            self.image = self.bossdoor

    def update(self, plx, ply, *args):
        global kill
        dist = sqrt((int(plx) - int(self.rect.x)) ** 2 + (int(ply) - int(self.rect.y)) ** 2) < 60  # флаг дистанция
        # проверяет дистанцию между объетом и игроком
        if args and args[0].type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(
                args[0].pos) and dist and not self.open:
            if self.tipe == "Y" and player.check_key("y") > 0:
                player.del_key("y")
                self.open = True
                self.image = self.openi
                self.mask = pygame.mask.from_surface(self.emptmask)
            elif self.tipe == "R" and player.check_key("r") > 0:
                player.del_key("r")
                self.open = True
                self.image = self.openi
                self.mask = pygame.mask.from_surface(self.emptmask)
            elif self.tipe == "B" and player.check_key("b") > 0:
                player.del_key("b")
                self.open = True
                self.image = self.openi
                self.mask = pygame.mask.from_surface(self.emptmask)
            elif self.tipe == "Boss" and player.check_key("bosskey") > 0:
                player.del_key("bosskey")
                self.open = True
                self.image = self.openi
                self.mask = pygame.mask.from_surface(self.emptmask)
        if kill:
            pygame.sprite.Sprite.kill(self)

    def chek_open(self):
        """проверяет открыта ли дверь, возвращает True/False"""
        return self.open


player = None

# группы спрайтов
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
wall_group = pygame.sprite.Group()
table_group = pygame.sprite.Group()
door_group = pygame.sprite.Group()
monster_gr = pygame.sprite.Group()
ladder_gr = pygame.sprite.Group()
grass_gr = pygame.sprite.Group()


def generate_level(level, numlvl):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '#':
                wall = Wall(x * 50, y * 50, x * 50 + 50, y * 50 + 50)
            elif level[y][x] == '.':
                grass = Grass(x * 50, y * 50)
            elif level[y][x] == '1':
                grass = Grass(x * 50, y * 50)
            elif level[y][x] == '@':
                wall = Wall(x * 50, y * 50, x * 50 + 50, y * 50 + 50)
                if numlvl == 1:
                    skelet = Skeleton(load_image("skeleton.png"), 4, 1, 350, 400)
                    skelet = Skeleton(load_image("skeleton.png"), 4, 1, 700, 100)
                    skelet = Skeleton(load_image("skeleton.png"), 4, 1, 700, 400)
                    skelet = Skeleton(load_image("skeleton.png"), 4, 1, 500, 700)
                    boss = Boss(load_image("skeleton.png"), 4, 1, 1500, 400, 20, 1000, 0, 1)
                if numlvl == 2:
                    skelet = Skeleton(load_image("skeleton.png"), 4, 1, 100, 450)
                    skelet = Skeleton(load_image("skeleton.png"), 4, 1, 300, 450)
                    skelet = Skeleton(load_image("skeleton.png"), 4, 1, 300, 700)
                    skelet = Skeleton(load_image("skeleton.png"), 4, 1, 100, 100)
                    skelet = Skeleton(load_image("skeleton.png"), 4, 1, 500, 700)
                    skelet = Skeleton(load_image("skeleton.png"), 4, 1, 1600, 700)
                    boss = Boss(load_image("skeleton.png"), 4, 1, 800, 400, 20, 1000, 0, 2, region=200)
            elif level[y][x] == 'Y':
                door = Door(x * 50, y * 50, "Y")
            elif level[y][x] == '=':
                door = Door(x * 50, y * 50, "Boss")
            elif level[y][x] == 'B':
                door = Door(x * 50, y * 50, "B")
            elif level[y][x] == 'R':
                door = Door(x * 50, y * 50, "R")
            elif level[y][x] == '&':
                table = Table(x * 50, y * 50, Money=random.choice((0, 0, 10)), ykey=True)
            elif level[y][x] == '+':
                table = Table(x * 50, y * 50, Money=random.choice((0, 0, 10)), rkey=True)
            elif level[y][x] == '$':
                table = Table(x * 50, y * 50, Money=random.choice((0, 0, 10)), bkey=True)
            elif level[y][x] == 't':
                table = Table(x * 50, y * 50, Money=random.choice((0, 0, 10)))
            elif level[y][x] == 'c':
                Nstand = Nightstand(x * 50, y * 50, Money=random.choice((0, 0, 10)))
            elif level[y][x] == 's':
                Nstand = Nightstand(x * 50, y * 50, Money=random.choice((0, 0, 10)), ykey=True)
            elif level[y][x] == '-':
                Nstand = Nightstand(x * 50, y * 50, Money=random.choice((0, 0, 10)), bkey=True)
            elif level[y][x] == '%':
                Nstand = Nightstand(x * 50, y * 50, Money=random.choice((0, 0, 10)), rkey=True)
            elif level[y][x] == '*':
                ladder = Ladder(x * 50, y * 50)
            elif level[y][x] == '2':
                grass = Grass(x * 50, y * 50)

    # вернем игрока, а также размер поля в клетках
    return x, y


def kill_all():
    global kill
    kill = True
    door_group.update(player.rect.x, player.rect.y)
    table_group.update(player.rect.x, player.rect.y)
    wall_group.update()
    monster_gr.update()
    ladder_gr.update()
    grass_gr.update()
    kill = False


def start_screen():
    intro_text = ["ЗАСТАВКА", "",
                  "Правила игры",
                  "Если в правилах несколько строк,",
                  "приходится выводить их построчно"]

    fon = pygame.transform.scale(load_image('fon.jpg'), (width, height))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                return  # начинаем игру
        pygame.display.flip()
        clock.tick(FPS)


start_screen()
player = AnimatedSprite(load_image("player_D_inv.png"), 4, 1, 100, 100, rkey=10, ykey=10, bkey=10, bosskey=1)
level_x, level_y = generate_level(load_level('карта.txt'), 1)
running = True
keypress = None
camera = Camera()
watch = "d"
timer = False
timer_z = -1
kill = False
lvl = 1

while running:

    for event in pygame.event.get():
        # при закрытии окна
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            table_group.update(player.rect.x, player.rect.y, event)
            door_group.update(player.rect.x, player.rect.y, event)
        elif event.type == pygame.KEYDOWN:
            if event.key == 275:
                keypress = "r"
            elif event.key == 276:
                keypress = "l"
            elif event.key == 273:
                keypress = "u"
            elif event.key == 274:
                keypress = "d"
            elif event.key == 102:
                keypress = "f"
        elif event.type == pygame.KEYUP:
            keypress = None
            player.fight_flag(False)
            player.damage = 20
    if keypress == "r":
        player.rect.x += STEP
        player.change(load_image("player_R_inv.png"), 4, 1, player.rect.x, player.rect.y)
        collis = player.update()
        watch = "r"
        player.x += STEP
        if collis:
            player.rect.x -= STEP
            player.x -= STEP
    if keypress == "l":
        player.rect.x -= STEP
        player.x -= STEP
        player.change(load_image("player_L_inv.png"), 4, 1, player.rect.x, player.rect.y)
        collis = player.update()
        watch = "l"
        if collis:
            player.rect.x += STEP
            player.x += STEP
    if keypress == "u":
        player.rect.y -= STEP
        player.y -= STEP
        player.change(load_image("player_U_inv.png"), 4, 1, player.rect.x, player.rect.y)
        collis = player.update()
        watch = "u"
        if collis:
            player.rect.y += STEP
            player.y += STEP
    if keypress == "d":
        player.rect.y += STEP
        player.y += STEP
        player.change(load_image("player_D_inv.png"), 4, 1, player.rect.x, player.rect.y)
        collis = player.update()
        watch = "d"
        if collis:
            player.rect.y -= STEP
            player.y -= STEP

    if keypress == "f":
        player.fight_flag(True)
        if watch == "r":
            player.change(load_image("hitR.png"), 4, 1, player.rect.x, player.rect.y)
            collis = player.update()
            if collis:
                player.rect.x -= 1
                player.x -= 1
        elif watch == "l":
            player.change(load_image("hitL.png"), 4, 1, player.rect.x, player.rect.y)
            collis = player.update()
            if collis:
                player.rect.x += 1
                player.x += 1
        elif watch == "u":
            player.change(load_image("hitU.png"), 4, 1, player.rect.x, player.rect.y)
            collis = player.update()
            if collis:
                player.rect.y += 1
                player.y -= 1
        elif watch == "d":
            player.change(load_image("hitD.png"), 4, 1, player.rect.x, player.rect.y)
            collis = player.update()
            if collis:
                player.rect.y -= 1
                player.y -= 1
    if timer:
        if timer_z == -1:
            timer_z = pygame.time.get_ticks()
        if wait(2, timer_z):
            player.flag_sk = True
            timer = False
            timer_z = -1
    if player.life < 95:
        if pygame.time.get_ticks() % 5000 == 1:
            player.add_life(5)

    monster_gr.update()
    screen.fill((0, 0, 0))
    all_sprites.draw(screen)
    player_group.draw(screen)
    pygame.display.flip()
    clock.tick(FPS)
    # изменяем ракурс камеры
    camera.update(player);
    # обновляем положение всех спрайтов
    for sprite in all_sprites:
        camera.apply(sprite)

pygame.quit()
