import pygame


# Константы
SCREEN_HEIGHT = 600
SCREEN_WIDHT = 300

BACKGROUND_COLOR = (92, 215, 246)

SQUARE_HEIGHT = 100
SQUARE_WIDTH = 80
SQUARE_COLOR = (255, 255, 255)

CIRCLE_COLOR = "Red"
CIRCLE_RADIUS = 22

MAIN_FONT_SIZE = 30

JAPAN_TEXT_COLOR = (188, 126, 230)


pygame.init()
pygame.display.set_caption("PyGame_Course")

# Если не нужна полоса с кнопкой закрытия окна: дописываем вторым аргументом:
# pygame.display.set_mode((SCREEN_HEIGHT, SCREEN_WIDHT), flags=pygame.NOFRAME)

screen = pygame.display.set_mode((SCREEN_HEIGHT, SCREEN_WIDHT))

# Подгрузка и установка иконки игры
icon = pygame.image.load("images/icon.png")
pygame.display.set_icon(icon)

# Создание квадрата, как объекта игры, в несколько строк
square = pygame.Surface((SQUARE_HEIGHT, SQUARE_WIDTH))
square.fill(SQUARE_COLOR)

# Создание текста
main_font = pygame.font.Font("fonts/Bold.ttf", MAIN_FONT_SIZE)
japan_text = main_font.render("Japan", False, JAPAN_TEXT_COLOR)


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
        screen.blit(square, (SCREEN_HEIGHT // 2, SQUARE_WIDTH // 2))
        screen.blit(japan_text, (SQUARE_HEIGHT + 200, SQUARE_WIDTH - 80))

        # Рисуем круг одной* строкой в квадрате
        pygame.draw.circle(
            square,
            CIRCLE_COLOR,
            (SQUARE_HEIGHT // 2, SQUARE_WIDTH // 2),
            CIRCLE_RADIUS
        )

        key_control()

        pygame.display.update()


if __name__ == "__main__":
    main()
