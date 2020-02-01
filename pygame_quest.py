import datetime
import os, pygame, random, sys
import sqlite3
from math import sqrt
import math

pygame.init()
size = width, height = 1200, 600
screen = pygame.display.set_mode(size)
count_down = 0
clock = pygame.time.Clock()
FPS = 60
STEP = 3
sounds = [pygame.mixer.Sound('data/lvl1.ogg'), pygame.mixer.Sound('data/lvl2.ogg'), pygame.mixer.Sound('data/lvl3.ogg'),
          pygame.mixer.Sound('data/hit.ogg')]
dct = {}


class FinalBoss(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y, damage, life, region=350):
        super().__init__(all_sprites, boss_gr)
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
        self.life = life
        self.damage = damage
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
        global timer, mode, msh_flag
        dx, dy = player.rect.x - self.rect.x, player.rect.y - self.rect.y
        dist = math.hypot(dx, dy) + 1
        dx, dy = dx / dist, dy / dist

        px, py = player.coord()
        dx2, dy2 = px - self.xd2, py - self.yd2
        dist2 = math.hypot(dx2, dy2) + 1
        coll4 = pygame.sprite.groupcollide(player_group, boss_gr, False, False,
                                           collided=pygame.sprite.collide_mask)
        coll5 = pygame.sprite.groupcollide(shuriken_gr, boss_gr, False, False,
                                           collided=pygame.sprite.collide_mask)

        if abs(dist2) < self.region or abs(dist) < 300:
            if dist < player.dist:
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
                    if pygame.sprite.groupcollide(player_group, boss_gr, False, False,
                                                  collided=pygame.sprite.collide_mask):
                        player.del_life(self.damage)
                        print("здоровье игрока", player.life)
                        timer = True
                        if player.life <= 0:
                            if player.life_count > 1:
                                player.life_count -= 1
                                player.life = 100
                                player.rect.x = spawn.rect.x
                                player.rect.y = spawn.rect.y
                                player.x = spawn.rect.x
                                player.y = spawn.rect.y
                            else:
                                mode = 5
                                return
                else:
                    timer = True
            else:
                if msh_flag and player.flag_sk:  # TODO
                    player.flag_sk = False
                    if dx < 0:
                        if dy < 0:
                            shell = Monstershells(self.rect.x, self.rect.y, -1, -1)
                            shell = Monstershells(self.rect.x, self.rect.y, 0, -1)
                            shell = Monstershells(self.rect.x, self.rect.y, -1, 0)
                        else:
                            shell = Monstershells(self.rect.x, self.rect.y, -1, 1)
                            shell = Monstershells(self.rect.x, self.rect.y, 0, 1)
                            shell = Monstershells(self.rect.x, self.rect.y, -1, 0)
                    else:
                        if dy < 0:
                            shell = Monstershells(self.rect.x, self.rect.y, 0, -1)
                            shell = Monstershells(self.rect.x, self.rect.y, 1, -1)
                            shell = Monstershells(self.rect.x, self.rect.y, 1, 0)
                        else:
                            shell = Monstershells(self.rect.x, self.rect.y, 1, 1)
                            shell = Monstershells(self.rect.x, self.rect.y, 0, 1)
                            shell = Monstershells(self.rect.x, self.rect.y, 1, 0)
                    msh_flag = False
                else:
                    timer = True
        if coll5:
            self.del_life(30)
            print("здоровье босса", self.life)
            if self.life <= 0:
                pygame.sprite.Sprite.kill(self)
                print("u kill boss")
                player.add_money(random.choice((10, 10, 10, 15, 20)))
                player.add_key("bosskey")

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


class Boss(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y, damage, life, speed, num_boss, region=350):
        super().__init__(all_sprites, boss_gr)
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
        global timer, mode
        dx, dy = player.rect.x - self.rect.x, player.rect.y - self.rect.y
        dist = math.hypot(dx, dy) + 1
        dx, dy = dx / dist, dy / dist

        px, py = player.coord()
        dx2, dy2 = px - self.xd2, py - self.yd2
        dist2 = math.hypot(dx2, dy2) + 1
        coll = pygame.sprite.groupcollide(boss_gr, wall_group, False, False,
                                          collided=pygame.sprite.collide_mask)
        coll1 = pygame.sprite.groupcollide(boss_gr, table_group, False, False,
                                           collided=pygame.sprite.collide_mask)
        coll2 = pygame.sprite.groupcollide(boss_gr, door_group, False, False,
                                           collided=pygame.sprite.collide_mask)
        coll3 = pygame.sprite.groupcollide(player_group, boss_gr, False, False,
                                           collided=pygame.sprite.collide_rect)
        coll4 = pygame.sprite.groupcollide(player_group, boss_gr, False, False,
                                           collided=pygame.sprite.collide_mask)
        coll5 = pygame.sprite.groupcollide(shuriken_gr, boss_gr, False, False,
                                           collided=pygame.sprite.collide_mask)

        if abs(dist2) < self.region or abs(dist) < 150:
            if coll or coll1 or coll2:
                if self.num_boss != 2:
                    self.rect.x -= dx * 2 * self.speed
                    self.rect.y -= dy * 2 * self.speed
                    self.x -= dx * 2 * self.speed
                    self.y -= dy * 2 * self.speed
            if dist < player.dist:
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
                    if pygame.sprite.groupcollide(player_group, boss_gr, False, False,
                                                  collided=pygame.sprite.collide_mask):
                        player.del_life(self.damage)
                        print("здоровье игрока", player.life)
                        timer = True
                        if player.life <= 0:
                            if player.life_count > 1:
                                player.life_count -= 1
                                player.life = 100
                                player.rect.x = spawn.rect.x
                                player.rect.y = spawn.rect.y
                                player.x = spawn.rect.x
                                player.y = spawn.rect.y
                            else:
                                mode = 5
                                return
                else:
                    timer = True
            else:
                self.rect.x += dx * 2 * self.speed
                self.rect.y += dy * 2 * self.speed
                self.x += dx * 2 * self.speed
                self.y += dy * 2 * self.speed
        if coll5:
            self.del_life(30)
            print("здоровье босса", self.life)
            if self.life <= 0:
                pygame.sprite.Sprite.kill(self)
                print("u kill boss")
                player.add_money(random.choice((10, 10, 10, 15, 20)))
                player.add_key("bosskey")

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
    def __init__(self, sheet, columns, rows, x, y, damage=5, life=150):
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
        self.life = life
        self.damage = damage
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
        global timer, mode
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
        coll4 = pygame.sprite.groupcollide(player_group, monster_gr, False, False,
                                           collided=pygame.sprite.collide_mask)
        coll5 = pygame.sprite.groupcollide(shuriken_gr, monster_gr, False, False,
                                           collided=pygame.sprite.collide_mask)

        if abs(dist2) < 200 or abs(dist) < 70:
            if coll or coll1 or coll2:
                self.rect.x -= dx * 2
                self.rect.y -= dy * 2
                self.x -= dx * 2
                self.y -= dy * 2
            if dist < player.dist:
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
                        timer = True
                        if player.life <= 0:
                            if player.life_count > 1:
                                player.life_count -= 1
                                player.life = 100
                                player.rect.x = spawn.rect.x
                                player.rect.y = spawn.rect.y
                                player.x = spawn.rect.x
                                player.y = spawn.rect.y
                            else:
                                mode = 5
                                return
                else:
                    timer = True
            else:
                self.rect.x += dx * 2
                self.rect.y += dy * 2
                self.x += dx * 2
                self.y += dy * 2
        if coll5:
            self.del_life(30)
            print("здоровье скелета", self.life)
            if self.life <= 0:
                pygame.sprite.Sprite.kill(self)
                print("u kill skeleton")
                player.add_money(random.choice((10, 10, 10, 15, 20)))
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


class Ghost(Skeleton):
    def move_towards_player(self, player):
        global timer, mode
        dx, dy = player.rect.x - self.rect.x, player.rect.y - self.rect.y
        dist = math.hypot(dx, dy) + 1
        dx, dy = dx / dist, dy / dist

        px, py = player.coord()
        dx2, dy2 = px - self.xd2, py - self.yd2
        dist2 = math.hypot(dx2, dy2) + 1
        coll4 = pygame.sprite.groupcollide(player_group, monster_gr, False, False,
                                           collided=pygame.sprite.collide_mask)
        coll5 = pygame.sprite.groupcollide(shuriken_gr, monster_gr, False, False,
                                           collided=pygame.sprite.collide_mask)

        if abs(dist2) < 200 or abs(dist) < 70:
            if dist < player.dist:
                if player.fight == 1:
                    self.del_life(player.damage)
                    print("здоровье призрака", self.life)
                    player.damage = 0
                    if self.life <= 0:
                        pygame.sprite.Sprite.kill(self)
                        print("u kill ghost")
                        player.add_money(random.choice((10, 10, 10, 15, 20)))

            if coll4:
                if player.flag_sk:
                    player.flag_sk = False
                    if pygame.sprite.groupcollide(player_group, monster_gr, False, False,
                                                  collided=pygame.sprite.collide_mask):
                        player.del_life(self.damage)
                        print("здоровье игрока", player.life)
                        timer = True
                        if player.life <= 0:
                            if player.life_count > 1:
                                player.life_count -= 1
                                player.life = 100
                                player.rect.x = spawn.rect.x
                                player.rect.y = spawn.rect.y
                                player.x = spawn.rect.x
                                player.y = spawn.rect.y
                            else:
                                mode = 5
                                return
                else:
                    timer = True
            else:
                self.rect.x += dx * 1.5
                self.rect.y += dy * 1.5
                self.x += dx * 1.5
                self.y += dy * 1.5
        if coll5:
            self.del_life(30)
            print("здоровье скелета", self.life)
            if self.life <= 0:
                pygame.sprite.Sprite.kill(self)
                print("u kill skeleton")
                player.add_money(random.choice((10, 10, 10, 15, 20)))
        if dx < 0:
            self.change(load_image('ghostL.png'), 4, 1, self.rect.x, self.rect.y)
        else:
            self.change(load_image('ghostR.png'), 4, 1, self.rect.x, self.rect.y)


class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y, rkey=0, ykey=0, bkey=0, bosskey=0, money=0, life_count=1,
                 life=100, dist=70):
        super().__init__(all_sprites, player_group)
        self.frames = []
        self.game_time = datetime.datetime.now()
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)
        self.check_frame = 0
        self.mask = pygame.mask.from_surface(self.image)
        self.rkey = rkey
        self.ykey = ykey
        self.bkey = bkey
        self.bosskey = bosskey
        self.Money = money
        self.life = life
        self.dist = dist
        self.damage = 20
        self.fight = 0
        self.shuriken = 0
        self.sward = False
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
        global kill, level_x, level_y, lvl, mode, spawn
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
        coll4 = pygame.sprite.groupcollide(player_group, shell_gr, False, False,
                                           collided=pygame.sprite.collide_mask)
        if coll or coll1 or coll2:
            return True
        elif coll3:
            kill_all()
            if lvl == 1:
                sounds[0].stop()
                sounds[1].play()
                spawn, level_x, level_y = generate_level(load_level('карта2.txt'), 2)
                self.life = 100
                self.rect.x = 1650
                self.x = 1650
                self.rect.y = 50
                self.y = 50
                lvl += 1
            elif lvl == 2:
                pygame.mixer.stop()
                sounds[2].play()
                spawn, level_x, level_y = generate_level(load_level('карта3.txt'), 3)
                self.life = 100
                self.rect.x = 1200
                self.x = 1200
                self.rect.y = 550
                self.y = 550
                lvl += 1
            elif lvl == 3:
                mode = 4
                return
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

    def get_info(self):
        pygame.font.init()
        myfont = pygame.font.SysFont('arial', 30)
        textsurface = myfont.render('Здоровье: ' + str(self.life), True, (255, 255, 255))
        screen.blit(textsurface, (10, 10))
        pygame.display.flip()

    def clear(self):
        self.rkey = 0
        self.ykey = 0
        self.bkey = 0
        self.bosskey = 0
        self.Money = 0
        self.life = 100
        self.dist = 70
        self.damage = 20
        self.fight = 0
        self.shuriken = 0
        self.sward = False
        self.flag_sk = False


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


class Shuriken(pygame.sprite.Sprite):
    image = load_image("shur.png")

    def __init__(self, plx, ply, x, y):
        super().__init__(all_sprites, shuriken_gr)
        self.image = Shuriken.image
        self.x = x
        self.y = y
        self.rect = self.image.get_rect()
        self.rect.x = plx
        self.rect.y = ply
        self.mask = pygame.mask.from_surface(self.image)
        self.dx, self.dy = self.x - self.rect.x, self.y - self.rect.y
        dist = math.hypot(self.dx, self.dy) + 1
        self.dx, self.dy = self.dx / dist, self.dy / dist

    def update(self):
        global kill, sh_flag
        if kill:
            pygame.sprite.Sprite.kill(self)
        coll = pygame.sprite.groupcollide(shuriken_gr, wall_group, False, False,
                                          collided=pygame.sprite.collide_mask)
        coll1 = pygame.sprite.groupcollide(shuriken_gr, table_group, False, False,
                                           collided=pygame.sprite.collide_mask)
        coll2 = pygame.sprite.groupcollide(shuriken_gr, door_group, False, False,
                                           collided=pygame.sprite.collide_mask)
        coll3 = pygame.sprite.groupcollide(shuriken_gr, monster_gr, False, False,
                                           collided=pygame.sprite.collide_mask)
        coll4 = pygame.sprite.groupcollide(shuriken_gr, boss_gr, False, False,
                                           collided=pygame.sprite.collide_mask)
        if coll or coll1 or coll2 or coll3 or coll4:
            sh_flag = True
            pygame.sprite.Sprite.kill(self)
        self.rect.x += self.dx * 6
        self.rect.y += self.dy * 6


class Monstershells(pygame.sprite.Sprite):
    image = load_image("shur.png")

    def __init__(self, plx, ply, runx=0, runy=0):
        super().__init__(all_sprites, shell_gr)
        self.image = Monstershells.image
        self.rect = self.image.get_rect()
        self.rect.x = plx
        self.rect.y = ply
        self.runx = runx
        self.runy = runy
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        global kill, msh_flag, mode
        if kill:
            pygame.sprite.Sprite.kill(self)
        coll = pygame.sprite.groupcollide(shell_gr, wall_group, False, False,
                                          collided=pygame.sprite.collide_mask)
        coll1 = pygame.sprite.groupcollide(shell_gr, table_group, False, False,
                                           collided=pygame.sprite.collide_mask)
        coll2 = pygame.sprite.groupcollide(shell_gr, door_group, False, False,
                                           collided=pygame.sprite.collide_mask)
        coll3 = pygame.sprite.groupcollide(shell_gr, player_group, False, False,
                                           collided=pygame.sprite.collide_mask)
        if coll or coll1 or coll2 or coll3:
            if coll3:
                player.del_life(10)
                print("здоровье игрока", player.life)
                if player.life <= 0:
                    if player.life_count > 1:
                        player.life_count -= 1
                        player.life = 100
                        player.rect.x = spawn.rect.x
                        player.rect.y = spawn.rect.y
                        player.x = spawn.rect.x
                        player.y = spawn.rect.y
                    else:
                        mode = 5
                        return
            msh_flag = True
            pygame.sprite.Sprite.kill(self)
        self.rect.x += self.runx * 6
        self.rect.y += self.runy * 6


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
    imagegreen = load_image("green.png")

    def __init__(self, x, y, texture=0):
        super().__init__(all_sprites, ladder_gr)
        self.image = Ladder.image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        if texture == 1:
            self.image = self.imagegreen

    def update(self):
        global kill
        if kill:
            pygame.sprite.Sprite.kill(self)


class Spawn1(pygame.sprite.Sprite):
    image = load_image("grass.png")

    def __init__(self, x, y):
        super().__init__(all_sprites, grass_gr)
        self.image = Spawn1.image
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
boss_gr = pygame.sprite.Group()
ladder_gr = pygame.sprite.Group()
grass_gr = pygame.sprite.Group()
shuriken_gr = pygame.sprite.Group()
shell_gr = pygame.sprite.Group()


def generate_level(level, numlvl):
    global spawn
    spawn, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '#':
                wall = Wall(x * 50, y * 50, x * 50 + 50, y * 50 + 50)
            elif level[y][x] == '.':
                grass = Grass(x * 50, y * 50)
            elif level[y][x] == '1':
                spawn = Spawn1(x * 50, y * 50)
            elif level[y][x] == '@':
                wall = Wall(x * 50, y * 50, x * 50 + 50, y * 50 + 50)
                if numlvl == 1:
                    ghost = Ghost(load_image("ghostL.png"), 4, 1, 350, 400)
                    skelet = Skeleton(load_image("skeleton.png"), 4, 1, 700, 100)
                    skelet = Skeleton(load_image("skeleton.png"), 4, 1, 700, 400)
                    boss = Boss(load_image("fBossR.png"), 4, 1, 1500, 400, 20, 1000, 1, 1)
                if numlvl == 2:
                    skelet = Skeleton(load_image("skeleton.png"), 4, 1, 100, 450)
                    skelet = Skeleton(load_image("skeleton.png"), 4, 1, 300, 450)
                    skelet = Skeleton(load_image("skeleton.png"), 4, 1, 300, 700)
                    skelet = Skeleton(load_image("skeleton.png"), 4, 1, 100, 100)
                    skelet = Skeleton(load_image("skeleton.png"), 4, 1, 500, 700)
                    boss = Boss(load_image("skeleton.png"), 4, 1, 800, 400, 25, 900, 1, 2, region=200)
                if numlvl == 3:
                    skelet = Skeleton(load_image("skeleton.png"), 4, 1, 1800, 300)
                    skelet = Skeleton(load_image("skeleton.png"), 4, 1, 1650, 300)
                    skelet = Skeleton(load_image("skeleton.png"), 4, 1, 1650, 50)
                    boss = FinalBoss(load_image("final_boss.png"), 4, 1, 450, 250, 25, 3000)
                    ghost = Ghost(load_image("ghostL.png"), 4, 1, 400, 200, 10, 500)
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
            elif level[y][x] == '0':
                ladder = Ladder(x * 50, y * 50, 1)
            elif level[y][x] == '2':
                grass = Grass(x * 50, y * 50)

    # вернем игрока, а также размер поля в клетках
    return spawn, x, y


def kill_all():
    global kill
    kill = True
    door_group.update(player.rect.x, player.rect.y)
    table_group.update(player.rect.x, player.rect.y)
    wall_group.update()
    monster_gr.update()
    shuriken_gr.update()
    boss_gr.update()
    ladder_gr.update()
    grass_gr.update()
    kill = False


def write_to_db(delta=0):
    con = sqlite3.connect("pygame_quest.db")
    cur = con.cursor()
    if delta != 0:
        result = cur.execute("""INSERT INTO base(Name_ID, highscore, difficulty)
         VALUES((SELECT ID FROM Names WHERE name is ('{}')), {}, {})""".format(player_name, delta, diff)).fetchall()
    else:
        result = cur.execute('''INSERT INTO Names(name) VALUES('{}')'''.format(player_name)).fetchall()
    con.commit()
    con.close()  # TODO


def get_from_db():
    con = sqlite3.connect("pygame_quest.db")
    cur = con.cursor()
    result = cur.execute('''select * from base where highscore in (select MIN(highscore) from base)''').fetchall()
    print(result[-1][0]) # самое быстрое прохождение
    con.commit()
    con.close()
    return


def information():
    intro_text = ["Количество жизней: {}".format(player.life_count),
                  "Жёлтых ключей: {}".format(player.ykey),
                  "Синих ключей: {}".format(player.bkey),
                  "Красных ключей: {}".format(player.rkey),
                  "Босс ключей: {}".format(player.bosskey),
                  "Сюрикенов: {}".format(player.shuriken),
                  "Урон: {}".format(player.damage),
                  "Длинна удара: {}".format(player.dist),
                  "Монет: {}".format(player.Money)]
    pygame.font.init()
    myfont = pygame.font.SysFont('arial', 30)
    textsurface = myfont.render('health: ' + str(player.life), True, (255, 255, 255))
    pygame.display.flip()
    y = 50
    for line in intro_text:
        screen.blit(myfont.render(line, True, (255, 255, 255)), (10, y))
        y += 30


def shop():
    """функция срабатывает, если mode = 2
    если нажать клавишу m, то mode = 2"""
    global keypress, watch, timer, timer_z, kill, lvl, mode, sh_flag, level_x, level_y, player, lvl, spawn, msh_flag
    global error_timer, error_timer_z
    product1 = False
    product2 = False
    product3 = False
    product4 = False
    error_timer = False
    error_timer_z = -1
    fon = pygame.transform.scale(load_image('fon.jpg'), (width, height))
    screen.blit(fon, (0, 0))
    fontB = pygame.font.Font(None, 100)
    fontS = pygame.font.Font(None, 30)
    screen.blit(fontB.render("S H O P", True, (255, 255, 255)), (500, 70))
    screen.blit(fontS.render("Money: {}".format(player.Money), True, (255, 255, 255)), (10, 500))

    while True:
        screen.blit(fon, (0, 0))
        screen.blit(fontB.render("S H O P", True, (255, 255, 255)), (500, 70))
        screen.blit(fontS.render("Money: {}".format(player.Money), True, (255, 255, 255)), (10, 500))
        if error_timer and error_timer_z != -1:
            if wait(1.5, error_timer_z):
                error_timer_z = -1
                error_timer = False
            screen.blit(fontS.render("Вам не хватает монет или вам не доступен данный предмет",
                                     True, (104, 28, 35)), (10, 460))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if x >= 396 and x <= 880 and y >= 372 and y <= 445:
                    mode = 1
                    return
                elif y >= 164 and y <= 341:
                    if x >= 87 and x <= 264:
                        product1 = True
                    elif x >= 396 and x <= 585:
                        product2 = True
                    elif x >= 695 and x <= 880:
                        product3 = True
                    elif x >= 970 and x <= 1135:
                        product4 = True
                if product1:
                    product1 = False
                    product2 = False
                    product3 = False
                    product4 = False
                    if player.Money >= 10 and player.shuriken < 100:
                        player.shuriken += 1
                        player.del_money(10)
                    else:
                        screen.blit(fontS.render("Вам не хватает монет или вам не доступен данный предмет",
                                                 True, (104, 28, 35)), (10, 460))
                        error_timer_z = pygame.time.get_ticks()
                        error_timer = True
                elif product2:
                    product1 = False
                    product2 = False
                    product3 = False
                    product4 = False
                    if player.Money >= 70 and player.life <= 90:
                        player.life += 10
                        player.del_money(70)
                    else:
                        screen.blit(fontS.render("Вам не хватает монет или вам не доступен данный предмет",
                                                 True, (104, 28, 35)), (10, 460))
                        error_timer_z = pygame.time.get_ticks()
                        error_timer = True
                elif product3:
                    product1 = False
                    product2 = False
                    product3 = False
                    product4 = False
                    if player.Money >= 150 and not player.sward:
                        player.sward = True
                        player.damage += 10
                        player.del_money(150)
                    else:
                        screen.blit(fontS.render("Вам не хватает монет или вам не доступен данный предмет",
                                                 True, (104, 28, 35)), (10, 460))
                        error_timer_z = pygame.time.get_ticks()
                        error_timer = True
                elif product4:
                    product1 = False
                    product2 = False
                    product3 = False
                    product4 = False
                    if player.Money >= 100 and player.dist == 70:
                        player.dist += 5
                        player.del_money(100)
                    else:
                        screen.blit(fontS.render("Вам не хватает монет или вам не доступен данный предмет",
                                                 True, (104, 28, 35)), (10, 460))
                        error_timer_z = pygame.time.get_ticks()
                        error_timer = True

        pygame.display.flip()
        clock.tick(FPS)


def win_screen():
    global keypress, watch, timer, timer_z, kill, lvl, mode, sh_flag, level_x, level_y, player, lvl, spawn, msh_flag
    fon = pygame.transform.scale(load_image('box.png'), (width, height))
    screen.blit(fon, (0, 0))
    delta = datetime.datetime.now() - player.game_time
    write_to_db(delta.seconds)
    font = pygame.font.Font(None, 250)
    sfont = pygame.font.Font(None, 40)
    screen.blit(sfont.render("Нажмити на любую клавишу, чтобы продолжить", True, (255, 255, 255)), (250, 500))
    screen.blit(font.render("YOU WIN", True, (255, 0, 0)), (250, 250))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN:
                mode = 3
                return
        pygame.display.flip()
        clock.tick(FPS)


def lose_screen():
    global keypress, watch, timer, timer_z, kill, lvl, mode, sh_flag, level_x, level_y, player, lvl, spawn, msh_flag
    fon = pygame.transform.scale(load_image('green.png'), (width, height))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 250)
    sfont = pygame.font.Font(None, 40)
    screen.blit(sfont.render("Нажмити на любую клавишу, чтобы продолжить", True, (255, 255, 255)), (250, 500))
    screen.blit(font.render("YOU LOSE", True, (255, 0, 0)), (200, 250))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN:
                mode = 3
                return
        pygame.display.flip()
        clock.tick(FPS)


def play(num_play):
    global keypress, watch, timer, timer_z, kill, lvl, mode, sh_flag, level_x, level_y, player, lvl, spawn, msh_flag

    global error_timer_z, error_timer, count_down
    if num_play == 0:
        player = AnimatedSprite(load_image("player_D_inv.png"), 4, 1, 100, 100, rkey=0, ykey=0, bkey=0, bosskey=0,
                                money=0)
        num_play += 1
    if num_play == 1:
        lvl = 1

        sounds[0].play()
        spawn, level_x, level_y = generate_level(load_level('карта.txt'), 1)
        player.rect.x = spawn.rect.x
        player.x = spawn.rect.x
        player.y = spawn.rect.y
        player.rect.y = spawn.rect.y
        player.life_count = diff
        player.clear()
        """
        player.bosskey = 3
        player.ykey = 20
        player.bkey = 20
        player.rkey = 20
        """
    msh_flag = True
    timer = True
    timer_z = -1
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                table_group.update(player.rect.x, player.rect.y, event)
                door_group.update(player.rect.x, player.rect.y, event)
                if keypress == "g" and sh_flag and player.shuriken > 0:
                    sh_flag = False
                    player.shuriken -= 1
                    shx, shy = event.pos
                    shuriken = Shuriken(player.rect.x, player.rect.y, shx, shy)
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
                elif event.key == 9:
                    keypress = "tab"
                elif event.key == 109:
                    keypress = "m"
                elif event.key == 110:
                    keypress = "n"
                elif event.key == 103:
                    keypress = "g"
            elif event.type == pygame.KEYUP:
                keypress = None
                player.fight_flag(False)
                player.damage = 20
                if player.sward:
                    player.damage = 30
        if keypress == "tab":
            information()
        if keypress == "m":
            keypress = ""
            mode = 2
            return
        if keypress == "n":
            keypress = ""
            mode = 6
            return
        if keypress == "r":
            player.rect.x += STEP
            if player.sward:
                player.change(load_image("swplayer_R_inv.png"), 4, 1, player.rect.x, player.rect.y)
            else:
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
            if player.sward:
                player.change(load_image("swplayer_L_inv.png"), 4, 1, player.rect.x, player.rect.y)
            else:
                player.change(load_image("player_L_inv.png"), 4, 1, player.rect.x, player.rect.y)
            collis = player.update()
            watch = "l"
            if collis:
                player.rect.x += STEP
                player.x += STEP
        if keypress == "u":
            player.rect.y -= STEP
            player.y -= STEP
            if player.sward:
                player.change(load_image("swplayer_U_inv.png"), 4, 1, player.rect.x, player.rect.y)
            else:
                player.change(load_image("player_U_inv.png"), 4, 1, player.rect.x, player.rect.y)
            collis = player.update()
            watch = "u"
            if collis:
                player.rect.y += STEP
                player.y += STEP
        if keypress == "d":
            player.rect.y += STEP
            player.y += STEP
            if player.sward:
                player.change(load_image("swplayer_D_inv.png"), 4, 1, player.rect.x, player.rect.y)
            else:
                player.change(load_image("player_D_inv.png"), 4, 1, player.rect.x, player.rect.y)
            collis = player.update()
            watch = "d"
            if collis:
                player.rect.y -= STEP
                player.y -= STEP
        player.get_info()

        if keypress == "f":
            sounds[3].play()
            player.fight_flag(True)
            if watch == "r":
                if player.sward:
                    player.change(load_image("swhitR.png"), 4, 1, player.rect.x, player.rect.y)
                else:
                    player.change(load_image("hitR.png"), 4, 1, player.rect.x, player.rect.y)
                collis = player.update()
                if collis:
                    player.rect.x -= 1
                    player.x -= 1
            elif watch == "l":
                if player.sward:
                    player.change(load_image("swhitL.png"), 4, 1, player.rect.x, player.rect.y)
                else:
                    player.change(load_image("hitL.png"), 4, 1, player.rect.x, player.rect.y)
                collis = player.update()
                if collis:
                    player.rect.x += 1
                    player.x += 1
            elif watch == "u":
                if player.sward:
                    player.change(load_image("swhitU.png"), 4, 1, player.rect.x, player.rect.y)
                else:
                    player.change(load_image("hitU.png"), 4, 1, player.rect.x, player.rect.y)
                collis = player.update()
                if collis:
                    player.rect.y += 1
                    player.y -= 1
            elif watch == "d":
                if player.sward:
                    player.change(load_image("swhitD.png"), 4, 1, player.rect.x, player.rect.y)
                else:
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
            if pygame.time.get_ticks() % 10000 in (range(18)):
                player.add_life(5)
        boss_gr.update()
        shell_gr.update()
        shuriken_gr.update()
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
        if mode == 4 or mode == 5:
            kill_all()
            player.clear()
            return


def rules():
    global mode, game_f, diff
    change = True
    fon1 = pygame.transform.scale(load_image('rules_1.jpg'), (width, height))
    fon2 = pygame.transform.scale(load_image('rules_2.jpg'), (width, height))
    screen.blit(fon1, (0, 0))
    while True:
        if change:
            screen.blit(fon1, (0, 0))
        else:
            screen.blit(fon2, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                print(event.pos)
                x, y = event.pos
                if y >= 429 and y <= 521:
                    if x >= 239 and x <= 595:
                        mode = 3
                        return
                    if x >= 723 and x <= 972:
                        change = not change

        pygame.display.flip()
        clock.tick(FPS)


def setting_menu():
    global mode, game_f, diff, music
    fon1 = pygame.transform.scale(load_image('setting_music.jpg'), (width, height))
    fon2 = pygame.transform.scale(load_image('setting.jpg'), (width, height))
    screen.blit(fon1, (0, 0))
    while True:
        if music:
            screen.blit(fon1, (0, 0))
        else:
            screen.blit(fon2, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                print(event.pos)
                x, y = event.pos
                if x >= 287 and x <= 897:
                    if y >= 135 and y <= 235:
                        mode = 1
                        return
                    elif y >= 273 and y <= 363:
                        mode = 3
                        kill_all()
                        return
                    if y >= 398 and y <= 495 and x <= 424:
                        music = not music
                        if music:
                            if lvl == 1:
                                sounds[0].play()
                            elif lvl == 2:
                                sounds[1].play()
                            elif lvl == 3:
                                sounds[2].play()
                        else:
                            if lvl == 1:
                                sounds[0].stop()
                            elif lvl == 2:
                                sounds[1].stop()
                            elif lvl == 3:
                                sounds[2].stop()
        pygame.display.flip()
        clock.tick(FPS)


def keyboard():
    global mode, game_f, diff, player_name
    fon = pygame.transform.scale(load_image('keyboard.jpg'), (width, height))
    var = ""
    screen.blit(fon, (0, 0))
    fontB = pygame.font.Font(None, 100)
    fontS = pygame.font.Font(None, 40)
    abc = "abcdefghijklmnopqrstuvwxyz"
    numbers = "0123456789"
    w = False

    while True:
        screen.blit(fon, (0, 0))
        screen.blit(fontS.render(var, True, (0, 0, 0)), (350, 180))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                print(event.pos)
                x, y = event.pos
                if x >= 338 and x <= 831:
                    if y >= 163 and y <= 234:
                        w = True
                    else:
                        w = False
                else:
                    w = False
                if x >= 597 and x <= 1024:
                    if y >= 83 and y <= 150 and len(var) > 0:
                        player_name = var
                if x >= 140 and x <= 359:
                    if y >= 81 and y <= 141:
                        mode = 3.1
                        return
            elif event.type == pygame.KEYUP:
                if w:
                    print(event.key)
                    a = event.key
                    n = event.key
                    n -= 48
                    a -= 97
                    if a >= 0 and a <= 26 and len(var) < 20:
                        var += abc[a]
                        print(var)
                    elif event.key >= 48 and event.key <= 57:
                        var += numbers[n]
                        print(var)
                    elif event.key == 8 and len(var) > 0:
                        var = var[:-1]
                        print(var)
                    elif event.key == 32 and len(var) < 20:
                        var += " "
                        print(var)

        pygame.display.flip()
        clock.tick(FPS)


def difficulty_menu():
    global mode, game_f, diff
    fon = pygame.transform.scale(load_image('diff_menu.png'), (width, height))
    screen.blit(fon, (0, 0))
    fontB = pygame.font.Font(None, 100)
    fontS = pygame.font.Font(None, 30)
    while True:
        screen.blit(fon, (0, 0))
        screen.blit(fontS.render("Ник: " + player_name, True, (0, 0, 0)), (350, 180))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                print(event.pos)
                x, y = event.pos
                if x >= 241 and x <= 590:
                    if y >= 424 and y <= 516:
                        mode = 3
                        return
                if x >= 677 and x <= 1009:
                    if y >= 80 and y <= 155:
                        print("easy")
                        diff = 3
                        if game_f:
                            mode = 1.2
                        else:
                            mode = 1.1
                            game_f = True
                        return
                    elif y >= 212 and y <= 279:
                        print("medium")
                        diff = 2
                        if game_f:
                            mode = 1.2
                        else:
                            mode = 1.1
                            game_f = True
                        return
                    elif y >= 318 and y <= 380:
                        print("hard")
                        diff = 1
                        if game_f:
                            mode = 1.2
                        else:
                            mode = 1.1
                            game_f = True
                        return
                    elif y >= 410 and y <= 475:
                        print("random")
                        diff = random.randrange(1, 4)
                        if game_f:
                            mode = 1.2
                        else:
                            mode = 1.1
                            game_f = True
                        return
                if x >= 233 and x <= 527:
                    if y >= 283 and y <= 340:
                        mode = 7
                        return
        pygame.display.flip()
        clock.tick(FPS)


def main_menu():
    global mode
    fon = pygame.transform.scale(load_image('menu.png'), (width, height))
    screen.blit(fon, (0, 0))
    fontB = pygame.font.Font(None, 100)
    fontS = pygame.font.Font(None, 30)

    while True:
        screen.blit(fon, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if x >= 147 and x <= 402:
                    if y >= 137 and y <= 213:
                        terminate()
                if x >= 446 and x <= 936:
                    if y >= 113 and y <= 223:
                        mode = 3.1
                        return
                    elif y >= 277 and y <= 373:
                        print(1)
                        mode = 3.2
                        return
                    elif y >= 420 and y <= 500:
                        mode = 3.3
                        return

        pygame.display.flip()
        clock.tick(FPS)


game_f = False
running = True
keypress = None
camera = Camera()
watch = "d"
timer = False
timer_z = -1
kill = False
lvl = 1
mode = 3
diff = random.randrange(1, 4)
error_timer = False
error_timer_z = -1
music = True
player_name = "player"
"""
mode
1 - игра
2 - магазин
3 - меню
3.1 - выбор сложности
3.2  - правила
3.3 - статистика
4 - win
5 - lose
"""
sh_flag = True
msh_flag = True

while running:
    if mode == 1:

        play(3)
    elif mode == 1.1:
        play(0)
    elif mode == 1.2:
        play(1)
    elif mode == 2:
        shop()
    elif mode == 3:
        main_menu()
    elif mode == 3.1:
        difficulty_menu()
    elif mode == 3.2:
        rules()
    elif mode == 3.3:
        get_from_db()
        mode = 3
    elif mode == 4:
        win_screen()
    elif mode == 5:
        lose_screen()
    elif mode == 6:
        setting_menu()
    elif mode == 7:
        keyboard()
        write_to_db()

pygame.quit()
