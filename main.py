import pygame


# Константы
SCREEN_WIDHT = 480
SCREEN_HEIGHT = 270

SCREEN_RIGHT_LIMIT = 400
SCREEN_LEFT_LIMIT = 20

BACKGROUND_COLOR = (92, 215, 246)

SPEED_MOVE_BACKGROUND = 1.5

BG_SOUND_VOLUME = 0.07

PLAYER_HEIGHT = 54
PLAYER_WIDTH = 50
PLAYER_SPEED = 20

JUMP_COUNT = 6


pygame.init()
pygame.display.set_caption("PyGame_Course")

clock = pygame.time.Clock()

screen = pygame.display.set_mode((SCREEN_WIDHT, SCREEN_HEIGHT))

icon = pygame.image.load("images/icon.png")
pygame.display.set_icon(icon)

player_walk_right = [
    pygame.image.load("images/player_right/player_right1_small.png"),
    pygame.image.load("images/player_right/player_right2_small.png"),
    pygame.image.load("images/player_right/player_right3_small.png"),
    pygame.image.load("images/player_right/player_right4_small.png"),
]
player_walk_left = [
    pygame.image.load("images/player_left/player_left1_small.png"),
    pygame.image.load("images/player_left/player_left2_small.png"),
    pygame.image.load("images/player_left/player_left3_small.png"),
    pygame.image.load("images/player_left/player_left4_small.png"),
]
player_front = pygame.image.load("images/player_front/player_front1_small.png")

bg = pygame.image.load("images/bg.jpg")

# Инициализация и проигрывание фоновой музыки
bg_sound = pygame.mixer.Sound("sounds/bg_sound.mp3")
bg_sound.set_volume(BG_SOUND_VOLUME)
bg_sound.play()

# Глобальные переменные
jump_count = JUMP_COUNT
is_jumping = False


def key_control():
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (
                event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            pygame.quit()
            raise SystemExit

    keys = pygame.key.get_pressed()

    action = {
        "right": keys[pygame.K_d],
        "left": keys[pygame.K_a],
        "space": keys[pygame.K_SPACE]
    }

    return action


def move(x, y, speed, pose_player, action):
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
    global jump_count, is_jumping

    if is_jumping:
        if jump_count >= -JUMP_COUNT:
            if jump_count > 0:
                y -= (jump_count ** 2) / 1.3
            else:
                y += (jump_count ** 2) / 1.3

            jump_count -= 1
        else:
            jump_count = JUMP_COUNT
            is_jumping = False

    return y


def main():
    bg_x = 0
    player_animation_index = 0

    player_x = SCREEN_WIDHT // 2 - PLAYER_WIDTH // 2
    player_y = 185
    player_speed = PLAYER_SPEED

    while True:
        # Отображение динамического заднего фона
        screen.blit(bg, (bg_x, 0))
        screen.blit(bg, (bg_x + SCREEN_WIDHT, 0))

        if player_animation_index == 3:
            player_animation_index = 0
        else:
            player_animation_index += 1

        bg_x += -SPEED_MOVE_BACKGROUND
        if bg_x == -SCREEN_WIDHT:
            bg_x = 0

        action = key_control()

        player_x, player_y = move(
            player_x, player_y, player_speed, player_animation_index, action)

        player_y = jump(player_y)

        pygame.display.update()

        clock.tick(15)


if __name__ == "__main__":
    main()
