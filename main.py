import pygame


# Константы
SCREEN_WIDHT = 480
SCREEN_HEIGHT = 270

BACKGROUND_COLOR = (92, 215, 246)

SPEED_MOVE_BACKGROUND = 2

BG_SOUND_VOLUME = 0.07

PLAYER_HEIGHT = 54
PLAYER_WIDTH = 50


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

bg = pygame.image.load("images/bg.jpg")

# Инициализация и проигрывание фоновой музыки
bg_sound = pygame.mixer.Sound("sounds/bg_sound.mp3")
bg_sound.set_volume(BG_SOUND_VOLUME)
bg_sound.play()


def key_control():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                raise SystemExit


def main():
    bg_x = 0
    player_animation_index = 0

    while True:
        # Отображение динамического заднего фона
        screen.blit(bg, (bg_x, 0))
        screen.blit(bg, (bg_x + SCREEN_WIDHT, 0))

        screen.blit(
            player_walk_right[player_animation_index],
            (SCREEN_WIDHT // 2 - PLAYER_WIDTH // 2, 185)
        )

        if player_animation_index == 3:
            player_animation_index = 0
        else:
            player_animation_index += 1

        bg_x += -SPEED_MOVE_BACKGROUND
        if bg_x == -SCREEN_WIDHT:
            bg_x = 0

        key_control()

        pygame.display.update()

        clock.tick(4)


if __name__ == "__main__":
    main()
