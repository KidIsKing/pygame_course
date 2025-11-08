import pygame


# Constans
SCREEN_HEIGHT = 600
SCREEN_WIDHT = 300

BACKGROUND_COLOR = (92, 215, 246)


pygame.init()
pygame.display.set_caption("PyGame_Course")

# Если не нужна полоса с кнопкой закрытия окна: дописываем вторым аргументом:
# pygame.display.set_mode((SCREEN_HEIGHT, SCREEN_WIDHT), flags=pygame.NOFRAME)

screen = pygame.display.set_mode((SCREEN_HEIGHT, SCREEN_WIDHT))

# Подгрузка и установка иконки игры
icon = pygame.image.load("images/icon.png")
pygame.display.set_icon(icon)


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
    screen.fill(BACKGROUND_COLOR)

    while True:
        key_control()

        pygame.display.update()


if __name__ == "__main__":
    main()
