import pygame
import random as rnd

# настройки окна
WIDTH, HEIGHT = 640, 750
RES = 970, 750

# начальный уровень сложности
difficulty = 60

# настройки платформы для всех уровней
platform_w = 120
platform_h = 35
platform_speed = 15
platform = pygame.Rect(WIDTH // 2 - platform_w // 2, HEIGHT - platform_h - 10, platform_w - 2, platform_h - 2)
platform_image = pygame.transform.scale(pygame.image.load('pictures/platform.png'), (platform_w - 2, platform_h - 2))

# настройки мяча для всех уровней
ball_radius = 15
ball_speed = 6
ball_rect = int(ball_radius * 2 ** 0.5)
ball = pygame.Rect(rnd.randrange(ball_rect, WIDTH - ball_rect), HEIGHT - platform_h - 50, ball_rect, ball_rect)
ball_contour = pygame.Rect(ball.x, HEIGHT - platform_h - 50, ball_rect + 1, ball_rect + 1)
dx = rnd.choice([-1, 1])
dy = -1

# создание полей
pygame.mixer.pre_init(44100, -16, 4, 512)
pygame.mixer.init()
pygame.init()
pygame.display.set_icon(pygame.image.load('pictures/favicon.ico'))
pygame.display.set_caption('Arcanoid')
sc = pygame.display.set_mode(RES)
game_sc = pygame.Surface((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# background image
game_right_panel = pygame.image.load('pictures/deckcomplw.jpg').convert()
main_menu = pygame.image.load('pictures/main_menu.png').convert()

# импорт шрифтов
main_font = pygame.font.Font('font/better-vcr.ttf', 40)
main_font_select = pygame.font.Font('font/better-vcr.ttf', 42)
font = pygame.font.Font('font/better-vcr.ttf', 30)
mini_font = pygame.font.Font('font/better-vcr.ttf', 25)
maxi_font = pygame.font.Font('font/better-vcr.ttf', 60)

# импорт звуков
hurt = pygame.mixer.Sound("hurt3.wav")


# считывание рекордов с файла
def get_record(lvl_number):
    if lvl_number == 0:
        with open('record_inf', 'r') as f:
            lines = f.readlines()
            return lines[0].strip()
    else:
        with open('record_lvl', 'r') as f:
            for current_line_number, line in enumerate(f, 1):
                if current_line_number == lvl_number:
                    return line.strip()


# установка рекордов в файл
def set_record(score, lvl_number):
    if lvl_number == 0:
        with open('record_inf', 'r+') as f:
            lines = f.readlines()
            numbers = [int(line.strip()) for line in lines]
            insert_index = 0
            for i in range(len(numbers)):
                if score > numbers[i]:
                    insert_index = i
                    break
            else:
                insert_index = len(numbers)
            numbers.insert(insert_index, score)
            if len(numbers) > 10:
                numbers = numbers[:10]
            f.seek(0)
            f.truncate()
            for number in numbers:
                f.write(str(number) + '\n')
    else:
        with open('record_lvl', 'r+') as f:
            lines = f.readlines()
            if score > int(lines[lvl_number - 1]):
                lines[lvl_number - 1] = str(score) + '\n'
                f.seek(0)
                f.writelines(lines[:10])


# отслеживание столкновения
def detect_collision(dx, dy, ball, rect):
    if dx > 0:
        delta_x = ball.right - rect.left
    else:
        delta_x = rect.right - ball.left
    if dy > 0:
        delta_y = ball.bottom - rect.top
    else:
        delta_y = rect.bottom - ball.top

    if abs(delta_x - delta_y) < 10:
        dx, dy = -dx, -dy
    elif delta_x > delta_y:
        dy = -dy
    elif delta_y > delta_x:
        dx = -dx
    return dx, dy


def switch_scene(scene):
    global current_scene
    current_scene = scene


class Level:
    def __init__(self, block_list, contour_list, contour_colour, glare_list, glare_colour, color_list, png, png_cord,
                 background_img, background_cord):
        self.block_list = block_list
        self.contour_list = contour_list
        self.contour_colour = contour_colour
        self.glare_list = glare_list
        self.glare_colour = glare_colour
        self.color_list = color_list
        self.png = png
        self.png_cord = png_cord
        self.background_img = background_img
        self.background_cord = background_cord

    def draw(self, surface):
        surface.blit(self.background_img, self.background_cord)
        [pygame.draw.rect(surface, self.glare_colour, block) for color, block in enumerate(self.glare_list)]
        [pygame.draw.rect(surface, self.contour_colour, block) for color, block in enumerate(self.contour_list)]
        [pygame.draw.rect(surface, self.color_list[color], block) for color, block in enumerate(self.block_list)]
        surface.blit(platform_image, (platform.left, platform.top))
        pygame.draw.circle(surface, pygame.Color('black'), ball_contour.center, ball_radius + 1.5)
        pygame.draw.circle(surface, pygame.Color('white'), ball.center, ball_radius)
        surface.blit(self.png, self.png_cord)
        return surface


def level0():
    level_block_list = [pygame.Rect(5 + 64 * i, 10 + 40 * j, 51, 21) for i in range(10) for j in range(1, 5)]
    level_contour_list = [pygame.Rect(5 + 64 * i, 10 + 40 * j, 54, 24) for i in range(10) for j in range(1, 5)]
    level_contour_colour = pygame.Color(58, 32, 50)
    level_glare_list = [pygame.Rect(2 + 64 * i, 7 + 40 * j, 57, 27) for i in range(10) for j in range(1, 5)]
    level_glare_colour = pygame.Color('white')
    level_color_list = [rnd.choice(['red', 'blue', 'orange', 'purple', 'green', 'yellow']) for i in range(10) for j in
                        range(1, 5)]
    level_background_img = pygame.image.load('pictures/level0.jpg').convert()
    level_png = pygame.image.load('pictures/png0.png')
    level_png_cord = (620, 230)
    level_background_cord = (0, 0)

    # Создание объекта Level для бесконечного уровня
    level0 = Level(level_block_list, level_contour_list, level_contour_colour, level_glare_list,
                   level_glare_colour,
                   level_color_list, level_png, level_png_cord, level_background_img, level_background_cord)

    return level0


def level1():
    level1_block_list = [pygame.Rect(5 + 64 * i, 10 + 50 * j, 51, 21) for i in range(10) for j in range(1, 5)]
    level1_contour_list = [pygame.Rect(5 + 64 * i, 10 + 50 * j, 50 + 4, 20 + 4) for i in range(10) for j in range(1, 5)]
    level1_contour_colour = pygame.Color(31, 97, 53)
    level1_glare_list = [pygame.Rect(2 + 64 * i, 7 + 50 * j, 50 + 7, 20 + 7) for i in range(10) for j in range(1, 5)]
    level1_glare_colour = pygame.Color(144, 238, 144)
    level1_color_list = [(2, 172, 35) if (i + j) % 2 == 0 else (125, 212, 53) for i in range(10) for j in range(1, 5)]
    level1_background_img = pygame.image.load('pictures/level1.png').convert()
    level1_png = pygame.image.load('pictures/png1.png')
    level1_png_cord = (629, 245)
    level1_background_cord = (0, -200)

    # Создание объекта Level для уровня 1
    level1 = Level(level1_block_list, level1_contour_list, level1_contour_colour, level1_glare_list,
                   level1_glare_colour,
                   level1_color_list, level1_png, level1_png_cord, level1_background_img, level1_background_cord)

    return level1


def level2():
    block_width = 50  # Ширина блока
    block_height = 30  # Высота блока
    gap = 10  # Промежуток между блоками
    rows = 5  # Количество рядов блоков в пирамиде
    start_x = (WIDTH - (10 * (50 + 10) - 10)) // 2  # Начальная позиция X
    start_y = 50  # Начальная позиция Y
    level2_block_list = []
    level2_contour_list = []
    level2_glare_list = []
    level2_color_list = []

    for row in range(rows):
        y = start_y + row * (block_height + gap)  # Вычисление Y-позиции для текущего ряда
        blocks_in_row = 10 - row  # Количество блоков в текущем ряду
        for i in range(blocks_in_row):
            x = start_x + i * (block_width + gap) + (
                    row * (block_width + gap)) // 2  # Вычисление X-позиции для текущего блока
            block_rect = pygame.Rect(x, y, block_width, block_height)
            contour_rect = pygame.Rect(x, y, block_width + 4, block_height + 4)
            glare_rect = pygame.Rect(x - 3, y - 3, block_width + 7, block_height + 7)
            level2_block_list.append(block_rect)
            level2_contour_list.append(contour_rect)
            level2_glare_list.append(glare_rect)
            if row % 2 == 1:
                level2_color_list.append(pygame.Color(140, 106, 69))
            else:
                level2_color_list.append(pygame.Color(223, 176, 115))
    level2_contour_colour = pygame.Color(99, 74, 46)
    level2_glare_colour = pygame.Color(171, 136, 99)
    level2_background_img = pygame.image.load('pictures/level2.jpg')
    level2_png = pygame.image.load('pictures/png2.png')
    level2_png_cord = (653, 295)
    level2_background_cord = (0, -100)

    # Создание объекта Level для уровня 2

    level2 = Level(level2_block_list, level2_contour_list, level2_contour_colour, level2_glare_list,
                   level2_glare_colour, level2_color_list, level2_png, level2_png_cord,
                   level2_background_img, level2_background_cord)
    return level2


def level3():
    gap = 7  # Промежуток между блоками
    rows = 8  # Количество рядов блоков в пирамиде
    start_x = 100  # Начальная позиция X
    start_y = 25  # Начальная позиция Y
    level3_block_list = []
    level3_contour_list = []
    level3_glare_list = []
    level3_color_list = []
    for row in range(rows):
        y = start_y + row * (40)  # Вычисление Y-позиции для текущего ряда
        blocks_in_row = 11  # Количество блоков в каждом ряду
        for i in range(blocks_in_row):
            x = start_x + i * (40)
            if row == 0:
                if i != 2 and i != 8:
                    continue
            elif row == 1:
                if i != 3 and i != 7:
                    continue
            elif row == 2:
                if i == 0 or i == 1 or i == 9 or i == 10:
                    continue
            elif row == 3:
                if i == 0 or i == 3 or i == 7 or i == 10:
                    continue
            elif row == 5:
                if i == 1 or i == 9:
                    continue
            elif row == 6:
                if i != 0 and i != 2 and i != 8 and i != 10:
                    continue
            elif row == 7:
                if i != 3 and i != 4 and i != 6 and i != 7:
                    continue

            block_rect = pygame.Rect(x, y, 40, 40)
            contour_rect = pygame.Rect(x, y, 40 + 3, 40 + 3)
            glare_rect = pygame.Rect(x - 2, y - 2, 40 + 2, 40 + 2)
            level3_block_list.append(block_rect)
            level3_contour_list.append(contour_rect)
            level3_glare_list.append(glare_rect)
            level3_color_list.append(pygame.Color(76, 176, 81))  # Цвет пустого блока

    level3_contour_colour = pygame.Color(31, 97, 53)
    level3_glare_colour = pygame.Color(144, 238, 144)
    level3_background_img = pygame.image.load('pictures/level3.jpg').convert()
    level3_png = pygame.image.load('pictures/png3.png')
    level3_png_cord = (629, 245)
    level3_background_cord = (0, -250)
    # Создание объекта Level для уровня 1
    level3 = Level(level3_block_list, level3_contour_list, level3_contour_colour, level3_glare_list,
                   level3_glare_colour,
                   level3_color_list, level3_png, level3_png_cord, level3_background_img, level3_background_cord)
    return level3


def level4():
    rows = 8  # Количество рядов блоков
    start_x = 20  # Начальная позиция X
    start_y = 20  # Начальная позиция Y
    level4_block_list = []
    level4_contour_list = []
    level4_glare_list = []
    level4_color_list = []
    for row in range(rows):
        y = start_y + row * (40)  # Вычисление Y-позиции для текущего ряда
        blocks_in_row = 15  # Количество блоков в каждом ряду
        for i in range(blocks_in_row):
            x = start_x + i * (40)
            if row == 0:
                continue
            if (row + i) % 2 == 1:
                continue
            block_rect = pygame.Rect(x, y, 40, 40)
            contour_rect = pygame.Rect(x, y, 40 + 3, 40 + 3)
            glare_rect = pygame.Rect(x - 2, y - 2, 40 + 2, 40 + 2)
            level4_block_list.append(block_rect)
            level4_contour_list.append(contour_rect)
            level4_glare_list.append(glare_rect)
            if i % 2 == 0:
                level4_color_list.append(pygame.Color(254, 203, 186))
            else:
                level4_color_list.append(pygame.Color(248, 173, 167))

    level4_contour_colour = pygame.Color(39, 18, 44)
    level4_glare_colour = pygame.Color(248, 208, 234)
    level4_background_img = pygame.image.load('pictures/level4.jpg').convert()
    level4_png = pygame.image.load('pictures/png4.png')
    level4_png_cord = (629, 265)
    level4_background_cord = (0, -250)
    # Создание объекта Level для уровня 1
    level4 = Level(level4_block_list, level4_contour_list, level4_contour_colour, level4_glare_list,
                   level4_glare_colour,
                   level4_color_list, level4_png, level4_png_cord, level4_background_img, level4_background_cord)

    return level4


def level5():
    rows = 7  # Количество рядов
    start_x = 150  # Начальная позиция X
    start_y = 25  # Начальная позиция Y
    level5_block_list = []
    level5_contour_list = []
    level5_glare_list = []
    level5_color_list = []
    for row in range(rows):
        y = start_y + row * 50  # Вычисление Y-позиции для текущего ряда
        blocks_in_row = 7  # Количество блоков в каждом ряду
        for i in range(blocks_in_row):
            x = start_x + i * 50

            if row == 0:
                if i == 2:
                    level5_color_list.append(pygame.Color('yellow'))
                else:
                    continue
            elif row == 1:
                if i == 3:
                    level5_color_list.append(pygame.Color('yellow'))
                else:
                    continue
            elif row == 2:
                if 1 <= i <= 5:
                    level5_color_list.append(pygame.Color('yellow'))
                else:
                    continue
            elif row == 3:
                    level5_color_list.append(pygame.Color('yellow'))
            elif row == 4:
                if i == 0 or i == 2 or i == 4 or i == 6:
                    level5_color_list.append(pygame.Color('yellow'))
                elif i == 1 or i == 5:
                    level5_color_list.append(pygame.Color(44, 43, 44))
                elif i == 3:
                    level5_color_list.append(pygame.Color(255, 144, 36))
            elif row == 5:
                if 2 <= i <= 4:
                    level5_color_list.append(pygame.Color(255, 144, 36))
                else:
                    level5_color_list.append(pygame.Color('yellow'))
            elif row == 6:
                if 1 <= i <= 5:
                    level5_color_list.append(pygame.Color('yellow'))
                else:
                    continue

            block_rect = pygame.Rect(x, y, 50, 50)
            contour_rect = pygame.Rect(x, y,  50 + 4, 50 + 4)
            glare_rect = pygame.Rect(x - 4, y - 4, 50 + 7, 50 + 7)
            level5_block_list.append(block_rect)
            level5_contour_list.append(contour_rect)
            level5_glare_list.append(glare_rect)

    level5_contour_colour = pygame.Color(197, 147, 2)
    level5_glare_colour = pygame.Color(238, 254, 91)
    level5_background_img = pygame.image.load('pictures/level5.jpg').convert()
    level5_png = pygame.image.load('pictures/png5.png')
    level5_png_cord = (545, 200)
    level5_background_cord = (0, 0)
    # Создание объекта Level для уровня 1
    level5 = Level(level5_block_list, level5_contour_list, level5_contour_colour, level5_glare_list,
                   level5_glare_colour, level5_color_list, level5_png, level5_png_cord, level5_background_img,
                   level5_background_cord)
    return level5


def game():
    global WIDTH, HEIGHT, RES, dx, dy, level, lvl_number, difficulty, bonus
    block_list = level.block_list
    contour_list = level.contour_list
    glare_list = level.glare_list
    color_list = level.color_list
    score = 0
    fps = difficulty
    lives = 3
    running = True
    show_game_over_text = False
    game_started = False
    show_start_text = True
    bonuses = []
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                set_record(score, lvl_number)
                exit()
        record = get_record(lvl_number)
        if int(record) < score:
            record = str(score)

        # отрисовка поля
        sc.blit(game_right_panel, (640, 1))
        level.draw(sc)

        # отрисовка мира
        pygame.draw.line(sc, pygame.Color(154, 74, 41), (641, 1), (970, 1), width=6)
        pygame.draw.line(sc, pygame.Color(154, 74, 41), (641, 0), (641, 750), width=7)
        pygame.draw.line(sc, pygame.Color(154, 74, 41), (640, 748), (970, 748), width=6)

        # отрисовка надписей
        sc.blit(main_font.render('ARCANOID', True, pygame.Color(58, 32, 50)), (689, 20))
        sc.blit(main_font.render('ARCANOID', True, pygame.Color(2, 172, 35)), (685, 16))
        sc.blit(font.render(record, True, pygame.Color(58, 32, 50)), (819, 75))
        sc.blit(font.render(record, True, pygame.Color(204, 146, 42)), (817, 73))
        sc.blit(font.render('Best:', True, pygame.Color(58, 32, 50)), (655, 75))
        sc.blit(font.render('Best:', True, pygame.Color(204, 146, 42)), (653, 73))
        sc.blit(font.render('Score:', True, pygame.Color(58, 32, 50)), (655, 128))
        sc.blit(font.render('Score:', True, pygame.Color(29, 170, 69)), (653, 126))
        sc.blit(font.render(str(score), True, pygame.Color(58, 32, 50)), (819, 128))
        sc.blit(font.render(str(score), True, pygame.Color(29, 170, 69)), (817, 126))
        sc.blit(font.render('Lives: ' + str(lives), True, pygame.Color(58, 32, 50)), (655, 183))
        sc.blit(font.render('Lives: ' + str(lives), True, pygame.Color(228, 45, 56)), (653, 181))

        for bonus in bonuses:
            pygame.draw.rect(sc, pygame.Color(29, 170, 69), bonus)

        # столкновение с левой и правой стенкой
        if ball.left < 10 or ball.right > WIDTH - 10:
            dx = -dx

        # столкновение с потолком
        if ball.centery < ball_radius:
            dy = -dy

        # столкновение с платформой
        if ball.colliderect(platform) and dy > 0:
            dx, dy = detect_collision(dx, dy, ball, platform)

        # столкновение с блоками
        hit_index = ball.collidelist(block_list)
        if hit_index != -1:
            hit_rect = block_list.pop(hit_index)
            color_list.pop(hit_index)
            contour_list.pop(hit_index)
            glare_list.pop(hit_index)
            dx, dy = detect_collision(dx, dy, ball, hit_rect)
            hurt.play()
            score += fps * 10
            fps += 1

        if not game_started and show_start_text:
            start_text_line1_c = font.render('press "Enter" key', True, pygame.Color('black'))
            start_text_line2_c = font.render('for start', True, pygame.Color('black'))
            sc.blit(start_text_line1_c, (87, 302))
            sc.blit(start_text_line2_c, (147, 352))
            start_text_line1 = font.render('press "Enter" key', True, pygame.Color('red'))
            start_text_line2 = font.render('for start', True, pygame.Color('red'))
            sc.blit(start_text_line1, (85, 300))
            sc.blit(start_text_line2, (145, 350))

        if not game_started and show_game_over_text:
            start_text_line1_c = mini_font.render('Game over', True, pygame.Color('black'))
            start_text_line2_c = mini_font.render('press "Enter" key for restart', True, pygame.Color('black'))
            start_text_line3_c = mini_font.render('or press "ESC" for exit', True, pygame.Color('black'))
            sc.blit(start_text_line1_c, (248, 302))
            sc.blit(start_text_line2_c, (42, 352))
            sc.blit(start_text_line3_c, (108, 402))
            start_text_line1 = mini_font.render('Game over', True, pygame.Color('red'))
            start_text_line2 = mini_font.render('press "Enter" key for restart', True, pygame.Color('red'))
            start_text_line3 = mini_font.render('or press "ESC" for exit', True, pygame.Color('red'))
            sc.blit(start_text_line1, (246, 300))
            sc.blit(start_text_line2, (40, 350))
            sc.blit(start_text_line3, (106, 400))

        key = pygame.key.get_pressed()
        if not game_started and key[pygame.K_RETURN]:
            if show_game_over_text == True:
                switch_scene(game)
                running = False
            show_game_over_text = False
            game_started = True
            show_start_text = False
        elif key[pygame.K_SPACE]:
            game_started = False
            show_start_text = True
        elif key[pygame.K_ESCAPE]:
            set_record(score, lvl_number)
            drop_poz()
            drop_block_poz()
            switch_scene(menu)
            running = False
        if key[pygame.K_r] and game_started:
            set_record(score, lvl_number)
            drop_poz()
            drop_block_poz()
            Redirect(lvl_number)
            running = False

        if game_started and lives > 0:
            if key[pygame.K_LEFT] and platform.left > 0:
                platform.left -= platform_speed
            if key[pygame.K_RIGHT] and platform.right < WIDTH - 15:
                platform.right += platform_speed

            # движение мяча
            ball.x += ball_speed * dx
            ball.y += ball_speed * dy
            ball_contour.x += ball_speed * dx
            ball_contour.y += ball_speed * dy

        # win, game over
        if ball.bottom > HEIGHT:
            lives -= 1
            drop_poz()
            fps = difficulty
            bonuses.clear()
            game_started = False
            if lives == 0:
                set_record(score, lvl_number)
                Redirect(lvl_number)
                score = 0
                drop_block_poz()
                lives = 3
                show_game_over_text = True
            else:
                show_start_text = True

        elif not len(level.block_list):
            if lvl_number == 0:
                level = level0()
                drop_poz()
                block_list = level.block_list
                contour_list = level.contour_list
                glare_list = level.glare_list
                color_list = level.color_list
                show_start_text = True
                game_started = False
            else:
                set_record(score, lvl_number)
                score = 0
                game_started = False
                running = False
                lives = 3
                switch_scene(win)
                drop_poz()
        # update screen
        pygame.display.flip()
        clock.tick(fps)


def drop_poz():
    global dx, dy
    platform.x = WIDTH // 2 - platform_w // 2
    ball.x = rnd.randrange(ball_rect, WIDTH - ball_rect)
    ball.y = HEIGHT - platform_h - 70
    ball_contour.x = ball.x
    ball_contour.y = HEIGHT - platform_h - 70
    dx, dy = 1, -1


def drop_block_poz():
    block_list = level.block_list
    contour_list = level.contour_list
    glare_list = level.glare_list
    color_list = level.color_list


def Redirect(select):
    global level
    if select == 0:
        level = level0()
    elif select == 1:
        level = level1()
    elif select == 2:
        level = level2()
    elif select == 3:
        level = level3()
    elif select == 4:
        level = level4()
    elif select == 5:
        level = level5()
    else:
        switch_scene(soon)
        return
    switch_scene(game)


def win():
    global lvl_number
    items = ['menu', 'restart', 'next level']
    select_opt = 0
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    select_opt -= 1
                elif event.key == pygame.K_DOWN:
                    select_opt += 1
                elif event.key == pygame.K_RETURN:
                    if items[select_opt] == 'menu':
                        switch_scene(menu)
                        running = False
                    elif items[select_opt] == 'restart':
                        drop_poz()
                        drop_block_poz()
                        Redirect(lvl_number)
                        running = False
                    elif items[select_opt] == 'next level':
                        lvl_number += 1
                        Redirect(lvl_number)
                        running = False

                select_opt = select_opt % len(items)

        sc.blit(main_menu, (-180, 0))
        sc.blit(main_font.render('You win!', True, pygame.Color(58, 32, 50)), (370, 68))
        sc.blit(main_font.render('You win!', True, pygame.Color('red')), (368, 66))

        for i in range(len(items)):
            if i == select_opt:
                text = main_font_select.render(items[i], 1, (244, 255, 155))
                text_contour = main_font_select.render(items[i], 1, (58, 32, 50))
            else:
                text = main_font.render(items[i], 1, (251, 242, 54))
                text_contour = main_font.render(items[i], 1, (58, 32, 50))
            sc.blit(text_contour, (479 - text.get_width() // 2 + 3, 195 + 68 * i))
            sc.blit(text, (479 - text.get_width() // 2, 192 + 68 * i))

        pygame.display.flip()
        clock.tick(60)


def select_mode():
    items = ['infinity', 'levels']
    select_opt = 0
    global current_scene, level, lvl_number
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    select_opt -= 1
                elif event.key == pygame.K_DOWN:
                    select_opt += 1
                elif event.key == pygame.K_RETURN:
                    if items[select_opt] == 'infinity':
                        lvl_number = 0
                        Redirect(lvl_number)
                        running = False
                    elif items[select_opt] == 'levels':
                        switch_scene(select_level)
                        running = False
                elif event.key == pygame.K_ESCAPE:
                    switch_scene(menu)
                    running = False
                select_opt = select_opt % len(items)

        sc.blit(main_menu, (-180, 0))
        sc.blit(main_font.render('Select mode', True, pygame.Color(58, 32, 50)), (311, 68))
        sc.blit(main_font.render('Select mode', True, pygame.Color('red')), (309, 66))
        sc.blit(mini_font.render('Press esc', True, pygame.Color(58, 32, 50)), (12, 17))
        sc.blit(mini_font.render('to go back', True, pygame.Color(58, 32, 50)), (12, 53))
        sc.blit(mini_font.render('Press esc', True, pygame.Color(204, 253, 82)), (10, 15))
        sc.blit(mini_font.render('to go back', True, pygame.Color(204, 253, 82)), (10, 51))

        for i in range(len(items)):
            if i == select_opt:
                text = main_font_select.render(items[i], 1, (244, 255, 155))
                text_contour = main_font_select.render(items[i], 1, (58, 32, 50))
            else:
                text = main_font.render(items[i], 1, (251, 242, 54))
                text_contour = main_font.render(items[i], 1, (58, 32, 50))
            sc.blit(text_contour, (479 - text.get_width() // 2 + 3, 195 + 68 * i))
            sc.blit(text, (479 - text.get_width() // 2, 192 + 68 * i))

        pygame.display.flip()
        clock.tick(60)


def select_level():
    level_select = [[i + 1 + j * 5 for j in range(4)] for i in range(5)]
    select_i = 0
    select_j = 0
    global current_scene, level, lvl_number
    lvl_number = 1
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    select_i += 1
                elif event.key == pygame.K_LEFT:
                    select_i -= 1
                elif event.key == pygame.K_DOWN:
                    select_j += 1
                elif event.key == pygame.K_UP:
                    select_j -= 1
                elif event.key == pygame.K_RETURN:
                    Redirect(lvl_number)
                    running = False
                elif event.key == pygame.K_ESCAPE:
                    switch_scene(select_mode)
                    running = False
            select_i = select_i % 5
            select_j = select_j % 4
            lvl_number = select_i + 1 + select_j * 5

        sc.blit(main_menu, (-180, 0))
        sc.blit(main_font.render('Select level', True, pygame.Color(58, 32, 50)), (311, 68))
        sc.blit(main_font.render('Select level', True, pygame.Color('red')), (309, 66))
        sc.blit(mini_font.render('Press esc', True, pygame.Color(58, 32, 50)), (12, 17))
        sc.blit(mini_font.render('to go back', True, pygame.Color(58, 32, 50)), (12, 53))
        sc.blit(mini_font.render('Press esc', True, pygame.Color(204, 253, 82)), (10, 15))
        sc.blit(mini_font.render('to go back', True, pygame.Color(204, 253, 82)), (10, 51))
        for i in range(5):
            for j in range(4):
                text = main_font.render(str(level_select[i][j]), 1, (251, 242, 54))
                text_contour = main_font.render(str(level_select[i][j]), 1, (58, 32, 50))
                if lvl_number == i + 1 + j * 5:
                    text = main_font_select.render(str(level_select[i][j]), 1, (244, 255, 155))
                    text_contour = main_font_select.render(str(level_select[i][j]), 1, (58, 32, 50))

                sc.blit(text_contour, (258 + 100 * i, 184 + j * 100))
                sc.blit(text, (256 + 100 * i, 182 + j * 100))

        pygame.display.flip()
        clock.tick(60)


def control():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    switch_scene(menu)
                    running = False

        sc.blit(main_menu, (-180, 0))
        sc.blit(main_font.render('Control', True, pygame.Color(58, 32, 50)), (341, 68))
        sc.blit(main_font.render('Control', True, pygame.Color('red')), (339, 66))
        sc.blit(main_font.render('left - movement to the left', True, pygame.Color(58, 32, 50)), (91, 158))
        sc.blit(main_font.render('left - movement to the left', True, pygame.Color(251, 242, 54)), (89, 156))
        sc.blit(main_font.render('Right - movement to the Right', True, pygame.Color(58, 32, 50)), (61, 208))
        sc.blit(main_font.render('Right - movement to the Right', True, pygame.Color(251, 242, 54)), (59, 206))
        sc.blit(main_font.render('Space - pause', True, pygame.Color(58, 32, 50)), (286, 258))
        sc.blit(main_font.render('Space - pause', True, pygame.Color(251, 242, 54)), (284, 256))
        sc.blit(main_font.render('R - restart', True, pygame.Color(58, 32, 50)), (311, 308))
        sc.blit(main_font.render('R - restart', True, pygame.Color(251, 242, 54)), (309, 306))
        sc.blit(main_font.render('Enter - confirm', True, pygame.Color(58, 32, 50)), (261, 358))
        sc.blit(main_font.render('Enter - confirm', True, pygame.Color(251, 242, 54)), (259, 356))
        sc.blit(main_font.render('Esc - exit', True, pygame.Color(58, 32, 50)), (311, 408))
        sc.blit(main_font.render('Esc - exit', True, pygame.Color(251, 242, 54)), (309, 406))
        sc.blit(font.render('warning! If you exit to the menu,', True, pygame.Color(58, 32, 50)), (41, 608))
        sc.blit(font.render('warning! If you exit to the menu,', True, pygame.Color(228, 45, 57)), (39, 606))
        sc.blit(font.render('in the game, you progress', True, pygame.Color(58, 32, 50)), (41, 658))
        sc.blit(font.render('in the game, you progress', True, pygame.Color(228, 45, 57)), (39, 656))
        sc.blit(font.render('will not be saved', True, pygame.Color(58, 32, 50)), (41, 708))
        sc.blit(font.render('will not be saved', True, pygame.Color(228, 45, 57)), (39, 706))
        sc.blit(mini_font.render('Press esc', True, pygame.Color(58, 32, 50)), (12, 17))
        sc.blit(mini_font.render('to go back', True, pygame.Color(58, 32, 50)), (12, 53))
        sc.blit(mini_font.render('Press esc', True, pygame.Color(204, 253, 82)), (10, 15))
        sc.blit(mini_font.render('to go back', True, pygame.Color(204, 253, 82)), (10, 51))

        pygame.display.flip()
        clock.tick(60)


def Scores():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    switch_scene(menu)
                    running = False

        sc.blit(main_menu, (-180, 0))
        lines = []
        with open('record_inf', 'r') as file:
            for line in file:
                lines.append(line.strip())
        for i, line in enumerate(lines):
            text = font.render(line, 1, (251, 242, 54))
            text_contour = font.render(line, 1, (58, 32, 50))
            sc.blit(text_contour, (479 - text.get_width() // 2 + 3, 155 + 50 * i))
            sc.blit(text, (479 - text.get_width() // 2, 152 + 50 * i))
        sc.blit(main_font.render('Rating in infinity mode', True, pygame.Color(58, 32, 50)), (118, 88))
        sc.blit(main_font.render('Rating in infinity mode', True, pygame.Color('red')), (116, 86))
        sc.blit(mini_font.render('Press esc', True, pygame.Color(58, 32, 50)), (12, 17))
        sc.blit(mini_font.render('to go back', True, pygame.Color(58, 32, 50)), (12, 53))
        sc.blit(mini_font.render('Press esc', True, pygame.Color(204, 253, 82)), (10, 15))
        sc.blit(mini_font.render('to go back', True, pygame.Color(204, 253, 82)), (10, 51))

        pygame.display.flip()
        clock.tick(60)


def menu():
    items = ['New game', 'Scores', 'Control', 'Difficulty', 'Exit']
    select_opt = 0
    global current_scene
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    select_opt -= 1
                elif event.key == pygame.K_DOWN:
                    select_opt += 1
                elif event.key == pygame.K_RETURN:
                    if items[select_opt] == 'New game':
                        switch_scene(select_mode)
                        running = False
                    elif items[select_opt] == 'Scores':
                        switch_scene(Scores)
                        running = False
                    elif items[select_opt] == 'Control':
                        switch_scene(control)
                        running = False
                    elif items[select_opt] == 'Difficulty':
                        switch_scene(Difficulty)
                        running = False
                    elif items[select_opt] == 'Exit':
                        running = False
                        current_scene = None

                select_opt = select_opt % len(items)

        sc.blit(main_menu, (-180, 0))

        for i in range(len(items)):
            if i == select_opt:
                text = main_font_select.render(items[i], 1, (244, 255, 155))
                text_contour = main_font_select.render(items[i], 1, (58, 32, 50))
            else:
                text = main_font.render(items[i], 1, (251, 242, 54))
                text_contour = main_font.render(items[i], 1, (58, 32, 50))
            sc.blit(text_contour, (479 - text.get_width() // 2 + 3, 195 + 68 * i))
            sc.blit(text, (479 - text.get_width() // 2, 192 + 68 * i))
        sc.blit(maxi_font.render('Arcanoid', True, pygame.Color(58, 32, 50)), (308, 70))
        sc.blit(maxi_font.render('Arcanoid', True, pygame.Color(209, 214, 41)), (304, 66))
        pygame.display.flip()
        clock.tick(60)


def Difficulty():
    global difficulty
    items = ['Easy', 'Medium', 'Hard']
    selected_opt = 0
    confirmed_opt = None  # Переменная для хранения выбранной опции
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_opt -= 1
                elif event.key == pygame.K_DOWN:
                    selected_opt += 1
                elif event.key == pygame.K_ESCAPE:
                    switch_scene(menu)
                    running = False
                elif event.key == pygame.K_RETURN:
                    if confirmed_opt is None:
                        confirmed_opt = selected_opt
                    else:
                        if selected_opt != confirmed_opt:
                            confirmed_opt = selected_opt

                    if items[selected_opt] == 'Easy':
                        difficulty = 60
                    elif items[selected_opt] == 'Medium':
                        difficulty = 80
                    elif items[selected_opt] == 'Hard':
                        difficulty = 100

        selected_opt = selected_opt % len(items)

        sc.blit(main_menu, (-180, 0))

        for i in range(len(items)):
            if i == confirmed_opt:
                text = main_font_select.render(items[i], 1, (137, 220, 69))
                text_contour = main_font_select.render(items[i], 1, (58, 32, 50))
            elif i == selected_opt:
                text = main_font_select.render(items[i], 1, (244, 255, 155))
                text_contour = main_font_select.render(items[i], 1, (58, 32, 50))
            else:
                text = main_font.render(items[i], 1, (251, 242, 54))
                text_contour = main_font.render(items[i], 1, (58, 32, 50))
            sc.blit(text_contour, (479 - text.get_width() // 2 + 3, 235 + 75 * i))
            sc.blit(text, (479 - text.get_width() // 2, 232 + 75 * i))
        sc.blit(main_font.render('Choose a difficulty', True, pygame.Color(58, 32, 50)), (192, 108))
        sc.blit(main_font.render('Choose a difficulty', True, pygame.Color('red')), (190, 106))
        sc.blit(mini_font.render('Press esc', True, pygame.Color(58, 32, 50)), (12, 17))
        sc.blit(mini_font.render('to go back', True, pygame.Color(58, 32, 50)), (12, 53))
        sc.blit(mini_font.render('Press esc', True, pygame.Color(204, 253, 82)), (10, 15))
        sc.blit(mini_font.render('to go back', True, pygame.Color(204, 253, 82)), (10, 51))

        pygame.display.flip()
        clock.tick(60)


def soon():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    switch_scene(select_level)
                    running = False

        sc.blit(main_menu, (-180, 0))
        sc.blit(main_font.render('Coming soon', True, pygame.Color(58, 32, 50)), (311, 308))
        sc.blit(main_font.render('Coming soon', True, pygame.Color('red')), (309, 306))
        sc.blit(mini_font.render('Press esc', True, pygame.Color(58, 32, 50)), (12, 17))
        sc.blit(mini_font.render('to go back', True, pygame.Color(58, 32, 50)), (12, 53))
        sc.blit(mini_font.render('Press esc', True, pygame.Color(204, 253, 82)), (10, 15))
        sc.blit(mini_font.render('to go back', True, pygame.Color(204, 253, 82)), (10, 51))

        pygame.display.flip()
        clock.tick(60)


current_scene = None
switch_scene(menu)
while current_scene is not None:
    current_scene()

pygame.quit()
