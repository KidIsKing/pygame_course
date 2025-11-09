import pygame


# Константы
SCREEN_WIDHT = 480
SCREEN_HEIGHT = 270

# Координатные границы передвижения игрока
SCREEN_RIGHT_LIMIT = 250
SCREEN_LEFT_LIMIT = 20

# Цвета
LOSE_TEXT_COLOR = (156, 0, 38)  # бардовый
RESTART_TEXT_COLOR = (7, 130, 31)  # тёмно-зелёный
RESTART_BACKGROUND_TEXT_COLOR = (85, 230, 114)  # светло-зелёный

# Скорость движения заднего фона
SPEED_MOVE_BACKGROUND = 1.5

# Размер текста
MAIN_TEXT_SIZE = 40

# Громкость звуков
BG_SOUND_VOLUME = 0.07
LOSE_SOUND_VOLUME = 0.05

# Параметры игрока
PLAYER_START_POS_X = 40
PLAYER_START_POS_Y = 185
PLAYER_HEIGHT = 54
PLAYER_WIDTH = 50
PLAYER_SPEED = 10

# Таймер для появления врагов
ENEMY_TIMER = 2000

# Численные константы
JUMP_COUNT = 7
BULLET_COUNT = 10

pygame.init()
pygame.display.set_caption("PyGame_Course")

# Инициация часов в игре
clock = pygame.time.Clock()

# Установка размерности экрана игры
screen = pygame.display.set_mode((SCREEN_WIDHT, SCREEN_HEIGHT))

# Подгрузка иконки игры
icon = pygame.image.load("images/icon.png").convert_alpha()
pygame.display.set_icon(icon)

# Изображения игрока и врага для анимация
player_walk_right = [
    pygame.image.load(
        "images/player_right/player_right1.png").convert_alpha(),
    pygame.image.load(
        "images/player_right/player_right2.png").convert_alpha(),
    pygame.image.load(
        "images/player_right/player_right3.png").convert_alpha(),
    pygame.image.load(
        "images/player_right/player_right4.png").convert_alpha(),
]
player_walk_left = [
    pygame.image.load(
        "images/player_left/player_left1.png").convert_alpha(),
    pygame.image.load(
        "images/player_left/player_left2.png").convert_alpha(),
    pygame.image.load(
        "images/player_left/player_left3.png").convert_alpha(),
    pygame.image.load(
        "images/player_left/player_left4.png").convert_alpha(),
]
player_front = pygame.image.load(
    "images//player_front.png").convert_alpha()
enemy_run = [
    pygame.image.load("images/enemy_move/enemy1.png").convert_alpha(),
    pygame.image.load("images/enemy_move/enemy2.png").convert_alpha(),
    pygame.image.load("images/enemy_move/enemy3.png").convert_alpha(),
    pygame.image.load("images/enemy_move/enemy4.png").convert_alpha(),
    pygame.image.load("images/enemy_move/enemy5.png").convert_alpha(),
    pygame.image.load("images/enemy_move/enemy6.png").convert_alpha(),
    pygame.image.load("images/enemy_move/enemy7.png").convert_alpha()
]

# Подгрузка изображения врага и заднего фона игры
bullet = pygame.image.load("images/bullet.png").convert_alpha()
bg = pygame.image.load("images/bg.jpg").convert()
lose_bg = pygame.image.load("images/lose_bg.jpg").convert()

# Создание таймера для появления врагов
enemy_timer = pygame.USEREVENT + 1  # +1 - обязательно
pygame.time.set_timer(enemy_timer, ENEMY_TIMER)

# Инициализация и проигрывание фоновой музыки и музыки поражения
bg_sound = pygame.mixer.Sound("sounds/bg_sound.mp3")
bg_sound.set_volume(BG_SOUND_VOLUME)
bg_sound.play(loops=-1)

lose_sound = pygame.mixer.Sound("sounds/lose_sound.mp3")
lose_sound.set_volume(LOSE_SOUND_VOLUME)

# Тексты
text = pygame.font.Font("fonts/Bold.ttf", MAIN_TEXT_SIZE)
lose_text = text.render("Проигрыш!", False, LOSE_TEXT_COLOR)
restart_text = text.render(
    "Начать заново", False, RESTART_TEXT_COLOR, RESTART_BACKGROUND_TEXT_COLOR)
restart_text_rect = restart_text.get_rect(
    topleft=(SCREEN_HEIGHT // 2 - 30, SCREEN_WIDHT // 2 - 110))

# Глобальные переменные
is_jumping = False
jump_count = JUMP_COUNT


def key_control():
    """Отслеживание нажатых клавиш."""
    keys = pygame.key.get_pressed()

    action = {
        "right": keys[pygame.K_d],
        "left": keys[pygame.K_a],
        "space": keys[pygame.K_SPACE]
    }

    return action


def reset_game():
    """Сброс состояния игры к начальным значениям."""
    global is_jumping, jump_count
    game_status = True
    is_jumping = False
    jump_count = JUMP_COUNT
    bg_sound.play(loops=-1)
    return game_status, PLAYER_START_POS_X, PLAYER_START_POS_Y


def move(x, y, speed, pose_player, action):
    """Перемещение персонажа."""
    global is_jumping, jump_count

    action = key_control()

    if action["right"] and x < SCREEN_RIGHT_LIMIT:
        screen.blit(player_walk_right[pose_player], (x, y))
        x += speed
    elif action["left"] and x > SCREEN_LEFT_LIMIT:
        screen.blit(player_walk_left[pose_player], (x, y))
        x -= speed
    else:
        screen.blit(player_front, (x, y))

    if action["space"] and not is_jumping:
        is_jumping = True
        jump_count = JUMP_COUNT

    return x, y


def jump(y):
    """Механика прыжка."""
    global is_jumping, jump_count

    if is_jumping:
        if jump_count >= -JUMP_COUNT:
            if jump_count > 0:
                y -= (jump_count ** 2) / 1.8
            else:
                y += (jump_count ** 2) / 1.8

            jump_count -= 1
        else:
            jump_count = JUMP_COUNT
            is_jumping = False

    return y


def main():
    """Главная функция игры."""
    bg_x = 0
    player_animation_index = 0
    enemy_animation_index = 0

    bullet_count = BULLET_COUNT

    player_x = PLAYER_START_POS_X
    player_y = PLAYER_START_POS_Y
    player_speed = PLAYER_SPEED

    enemy_list = []
    bullet_list = []

    game_status = True

    while True:
        if game_status:
            # Отображение динамического заднего фона
            screen.blit(bg, (bg_x, 0))
            screen.blit(bg, (bg_x + SCREEN_WIDHT, 0))
            bg_x += -SPEED_MOVE_BACKGROUND
            if bg_x == -SCREEN_WIDHT:
                bg_x = 0

            # Постоянное отслеживание хитбокса игрока
            player_rect = player_front.get_rect(topleft=(player_x, player_y))

            if player_animation_index == 3:
                player_animation_index = 0
            else:
                player_animation_index += 1

            if enemy_list:
                for i, el in enumerate(enemy_list):
                    if enemy_animation_index == 6:
                        enemy_animation_index = 0
                    else:
                        enemy_animation_index += 1

                    screen.blit(enemy_run[enemy_animation_index], el)
                    el.x -= 7

                    if el.x < -50:
                        enemy_list.pop(i)

                    if player_rect.colliderect(el):
                        game_status = False

            if bullet_list:
                for i, bullet_el in enumerate(bullet_list):
                    screen.blit(bullet, bullet_el)
                    bullet_el.x += 10

                    if bullet_el.x > 480:
                        bullet_list.pop(i)

                    if enemy_list:
                        for index, enemy_el in enumerate(enemy_list):
                            if bullet_el.colliderect(enemy_el):
                                enemy_list.pop(index)
                                bullet_list.pop(i)

            action = key_control()

            player_x, player_y = move(
                player_x,
                player_y,
                player_speed,
                player_animation_index,
                action
            )

            player_y = jump(player_y)

        else:
            bg_sound.stop()

            screen.blit(lose_bg, (-30, -8))

            screen.blit(
                lose_text,
                (SCREEN_HEIGHT // 2, SCREEN_WIDHT // 2 - 180)
            )

            screen.blit(restart_text, (restart_text_rect))

            # Переменная для отслеживания позиции мышки
            mouse = pygame.mouse.get_pos()

            if (restart_text_rect.collidepoint(mouse) and
                    pygame.mouse.get_pressed()[0]):
                game_status, player_x, player_y = reset_game()
                bullet_count = BULLET_COUNT
                enemy_list.clear()
                bullet_list.clear()

        # Обновление экрана игры при каком-либо изменении
        pygame.display.update()

        # fps в игре
        clock.tick(20)

        for event in pygame.event.get():
            # Обработка нажатия клавиш для выхода из игры
            if event.type == pygame.QUIT or (
                event.type == pygame.KEYDOWN and
                event.key == pygame.K_ESCAPE
            ):
                pygame.quit()
                raise SystemExit
            # Создание врагов, когда срабатывает таймер
            if event.type == enemy_timer:
                enemy_list.append(enemy_run[3].get_rect(
                    topleft=(481, SCREEN_WIDHT // 2 - PLAYER_WIDTH // 2 - 30)))
            if (game_status and
                    event.type == pygame.KEYUP and
                    event.key == pygame.K_b and
                    bullet_count > 0):
                bullet_list.append(bullet.get_rect(
                    topleft=(player_x + 70, player_y + 17)))
                bullet_count -= 1


if __name__ == "__main__":
    main()
