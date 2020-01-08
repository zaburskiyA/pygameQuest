import os, pygame, random, sys

pygame.init()
infoObject = pygame.display.Info()
screen = pygame.display.set_mode((infoObject.current_w - 500, infoObject.current_h - 300))
size = width, height = infoObject.current_w, infoObject.current_h

clock = pygame.time.Clock()
FPS = 60
STEP = 1


class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y):
        super().__init__(all_sprites)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)
        self.check_frame = 0

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
        self.check_frame += 1
        if self.check_frame % 70 == 0:
            self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]


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
               'door': load_image('door.png')}
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
        self.dy = -(target.rect.y + target.rect.h//2 - height // 3) + 25


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = player_image
        self.rect = self.image.get_rect().move(tile_width * pos_x + 15, tile_height * pos_y + 5)


player = None

# группы спрайтов
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()


def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '-':
                Tile('empty', x, y)
            elif level[y][x] == '#':
                Tile('wall', x, y)
            elif level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '1':
                Tile('empty', x, y)
            elif level[y][x] == '@':
                Tile('wall', x, y)
                new_player = AnimatedSprite(load_image("player_D_inv.png"), 4, 1, 100, 100)
            elif level[y][x] == '/':
                Tile('door', x, y)

    # вернем игрока, а также размер поля в клетках
    return new_player, x, y


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
player, level_x, level_y = generate_level(load_level('карта.txt'))
running = True
keypress = None
camera = Camera()

while running:

    for event in pygame.event.get():
        # при закрытии окна
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == 275:
                keypress = "r"
            elif event.key == 276:
                keypress = "l"
            elif event.key == 273:
                keypress = "u"
            elif event.key == 274:
                keypress = "d"
        elif event.type == pygame.KEYUP:
            keypress = None
    if keypress == "r":
        player.rect.x += STEP
        player.change(load_image("player_R_inv.png"), 4, 1, player.rect.x, player.rect.y)
        player.update()
    if keypress == "l":
        player.rect.x -= STEP
        player.change(load_image("player_L_inv.png"), 4, 1, player.rect.x, player.rect.y)
        player.update()
    if keypress == "u":
        player.rect.y -= STEP
        player.change(load_image("player_U_inv.png"), 4, 1, player.rect.x, player.rect.y)
        player.update()
    if keypress == "d":
        player.rect.y += STEP
        player.change(load_image("player_D_inv.png"), 4, 1, player.rect.x, player.rect.y)
        player.update()
    screen.fill((0, 0, 0))
    all_sprites.draw(screen)
    player_group.draw(screen)
    pygame.display.flip()
    # изменяем ракурс камеры
    camera.update(player);
    # обновляем положение всех спрайтов
    for sprite in all_sprites:
        camera.apply(sprite)

pygame.quit()
