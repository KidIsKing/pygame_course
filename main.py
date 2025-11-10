from random import randint
import pygame


# Константы
SCREEN_WIDTH = 480
SCREEN_HEIGHT = 270
SCREEN_RIGHT_LIMIT = 250
SCREEN_LEFT_LIMIT = 20

# Цвета
LOSE_TEXT_COLOR = (156, 0, 38)
RESTART_TEXT_COLOR = (7, 130, 31)
RESTART_BACKGROUND_TEXT_COLOR = (85, 230, 114)
INFO_TEXT_COLOR = (255, 255, 255)

# Скорости
SPEED_MOVE_BACKGROUND = 1.5
PLAYER_SPEED = 10

# Размеры текста
MAIN_TEXT_SIZE = 40
BULLET_TEXT_SIZE = 24

# Громкость
BG_SOUND_VOLUME = 0.07
LOSE_SOUND_VOLUME = 0.05

# Таймер врагов
ENEMY_TIMER = 2000

# Константы игрока
PLAYER_START_POS_X = 40
PLAYER_START_POS_Y = 185
JUMP_COUNT = 7
BULLET_COUNT = 10

MIN_ENEMY_DELAY = 1200  # 1.2 секунды
MAX_ENEMY_DELAY = 3500  # 3.5 секунды
DIFFICULTY_INCREASE_RATE = 0.95  # На 5% быстрее каждые 10 очков

pygame.init()
pygame.display.set_caption("PyGame_Course")
clock = pygame.time.Clock()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))


class GameObject:
    """Базовый класс для всех игровых объектов"""

    def __init__(self, x, y, image=None):
        self.x = x
        self.y = y
        self.image = image
        if image:
            self.rect = self.image.get_rect(topleft=(x, y))
        else:
            self.rect = pygame.Rect(x, y, 0, 0)

    def draw(self, surface):
        """Отрисовка объекта на поверхности"""
        if self.image:
            surface.blit(self.image, (self.x, self.y))

    def update(self):
        """Обновление состояния объекта"""
        self.rect.topleft = (self.x, self.y)


class Player(GameObject):
    """Класс игрока"""

    def __init__(self, x, y):
        # Загрузка изображений для анимации
        self.walk_right = [
            pygame.image.load(
                "images/player_right/player_right1.png").convert_alpha(),
            pygame.image.load(
                "images/player_right/player_right2.png").convert_alpha(),
            pygame.image.load(
                "images/player_right/player_right3.png").convert_alpha(),
            pygame.image.load(
                "images/player_right/player_right4.png").convert_alpha(),
        ]
        self.walk_left = [
            pygame.image.load(
                "images/player_left/player_left1.png").convert_alpha(),
            pygame.image.load(
                "images/player_left/player_left2.png").convert_alpha(),
            pygame.image.load(
                "images/player_left/player_left3.png").convert_alpha(),
            pygame.image.load(
                "images/player_left/player_left4.png").convert_alpha(),
        ]
        self.front = pygame.image.load(
            "images/player_front.png").convert_alpha()

        super().__init__(x, y, self.front)

        self.speed = PLAYER_SPEED
        self.is_jumping = False
        self.jump_count = JUMP_COUNT
        self.animation_index = 0
        self.direction = "front"  # Направление взгляда

    def move(self, actions):
        """Движение игрока"""
        moved = False  # Флаг, указывающий, двигался ли игрок

        if actions["right"] and self.x < SCREEN_RIGHT_LIMIT:
            self.x += self.speed
            self.direction = "right"
            moved = True
        elif actions["left"] and self.x > SCREEN_LEFT_LIMIT:
            self.x -= self.speed
            self.direction = "left"
            moved = True

        # Сбрасываем анимацию, если игрок не двигается и не в прыжке
        if not moved and not self.is_jumping:
            self.direction = "front"
            self.animation_index = 0  # Сбрасываем на первый кадр

    def jump(self):
        """Прыжок игрока"""
        if self.is_jumping:
            if self.jump_count >= -JUMP_COUNT:
                if self.jump_count > 0:
                    self.y -= (self.jump_count**2) / 1.8
                else:
                    self.y += (self.jump_count**2) / 1.8
                self.jump_count -= 1
            else:
                self.jump_count = JUMP_COUNT
                self.is_jumping = False

    def start_jump(self):
        """Начало прыжка"""
        if not self.is_jumping:
            self.is_jumping = True
            self.jump_count = JUMP_COUNT

    def draw(self, surface):
        """Отрисовка игрока с анимацией"""
        # Обновление анимации только если игрок движется
        if self.direction in ["right", "left"] and not self.is_jumping:
            self.animation_index = (self.animation_index + 1) % 4

        # Определение кадра для отрисовки
        if self.direction == "right":
            if self.is_jumping:
                # Во время прыжка - используем последний кадр анимации бега
                surface.blit(self.walk_right[1], (self.x, self.y))
            else:
                surface.blit(
                    self.walk_right[self.animation_index], (self.x, self.y))
        elif self.direction == "left":
            if self.is_jumping:
                # Во время прыжка - используем последний кадр анимации бега
                surface.blit(self.walk_left[1], (self.x, self.y))
            else:
                surface.blit(
                    self.walk_left[self.animation_index], (self.x, self.y))
        else:
            surface.blit(self.front, (self.x, self.y))

        self.update()


class Enemy(GameObject):
    """Класс врага"""

    def __init__(self, x, y):
        self.run_frames = [
            pygame.image.load("images/enemy_move/enemy1.png").convert_alpha(),
            pygame.image.load("images/enemy_move/enemy2.png").convert_alpha(),
            pygame.image.load("images/enemy_move/enemy3.png").convert_alpha(),
            pygame.image.load("images/enemy_move/enemy4.png").convert_alpha(),
            pygame.image.load("images/enemy_move/enemy5.png").convert_alpha(),
            pygame.image.load("images/enemy_move/enemy6.png").convert_alpha(),
            pygame.image.load("images/enemy_move/enemy7.png").convert_alpha(),
        ]

        super().__init__(x, y, self.run_frames[0])

        self.speed = 7
        self.animation_index = 0
        self.is_active = True

    def update(self):
        """Обновление положения врага"""
        self.x -= self.speed
        self.animation_index = (self.animation_index + 1) % 7
        self.image = self.run_frames[self.animation_index]
        super().update()

        # Деактивация врага, если он ушел за экран
        if self.x < -50:
            self.is_active = False

    def draw(self, surface):
        """Отрисовка врага"""
        surface.blit(self.image, (self.x, self.y))


class Bullet(GameObject):
    """Класс пули"""

    def __init__(self, x, y):
        image = pygame.image.load("images/bullet.png").convert_alpha()
        super().__init__(x, y, image)
        self.y = y - 7
        self.speed = 20
        self.is_active = True

    def update(self):
        """Обновление положения пули"""
        self.x += self.speed
        super().update()

        # Деактивация пули, если она ушла за экран
        if self.x > SCREEN_WIDTH:
            self.is_active = False


class Game:
    """Основной класс игры"""

    def __init__(self):
        # Загрузка ресурсов
        self.icon = pygame.image.load("images/icon.png").convert_alpha()
        self.bg = pygame.image.load("images/bg.jpg").convert()
        self.lose_bg = pygame.image.load("images/lose_bg.jpg").convert()

        pygame.display.set_icon(self.icon)

        # Звуки
        self.bg_sound = pygame.mixer.Sound("sounds/bg_sound.mp3")
        self.bg_sound.set_volume(BG_SOUND_VOLUME)
        self.lose_sound = pygame.mixer.Sound("sounds/lose_sound.mp3")
        self.lose_sound.set_volume(LOSE_SOUND_VOLUME)

        # Шрифты
        self.main_font = pygame.font.Font("fonts/Bold.ttf", MAIN_TEXT_SIZE)
        self.info_font = pygame.font.Font("fonts/Bold.ttf", BULLET_TEXT_SIZE)

        # Тексты
        self.lose_text = self.main_font.render(
            "Проигрыш!", False, LOSE_TEXT_COLOR)
        self.restart_text = self.main_font.render(
            "Начать заново", True,
            RESTART_TEXT_COLOR, RESTART_BACKGROUND_TEXT_COLOR
        )
        self.restart_text_rect = self.restart_text.get_rect(
            topleft=(SCREEN_HEIGHT // 2 - 30, SCREEN_WIDTH // 2 - 110)
        )

        # Игровые объекты
        self.player = Player(PLAYER_START_POS_X, PLAYER_START_POS_Y)
        self.enemies = []
        self.bullets = []

        # Игровые переменные
        self.score = 0
        self.best_score = 0
        self.bullet_count = BULLET_COUNT
        self.game_status = True
        self.bg_x = 0
        self.lose_sound_playing = False

        # Таймер
        self.enemy_timer = pygame.USEREVENT + 1
        self.min_enemy_delay = MIN_ENEMY_DELAY
        self.max_enemy_delay = MAX_ENEMY_DELAY
        self.update_enemy_timer()
        pygame.time.set_timer(self.enemy_timer, ENEMY_TIMER)

        # Запуск фоновой музыки
        self.bg_sound.play(loops=-1)

    def update_enemy_timer(self):
        """Обновляет интервал появления врагов со случайным значением"""
        delay = randint(self.min_enemy_delay, self.max_enemy_delay)
        pygame.time.set_timer(self.enemy_timer, delay)

    def increase_difficulty(self):
        """Увеличивает сложность игры"""
        if self.score > 0 and self.score % 10 == 0:
            self.min_enemy_delay = max(
                800, int(self.min_enemy_delay * DIFFICULTY_INCREASE_RATE))
            self.max_enemy_delay = max(
                2000, int(self.max_enemy_delay * DIFFICULTY_INCREASE_RATE))

    def handle_events(self):
        """Обработка событий"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (
                event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
            ):
                return False

            if event.type == self.enemy_timer and self.game_status:
                self.enemies.append(Enemy(SCREEN_WIDTH, SCREEN_HEIGHT - 83))
                self.increase_difficulty()  # Проверяем увеличение сложности
                self.update_enemy_timer()   # Обновляем таймер

            if (
                self.game_status
                and event.type == pygame.MOUSEBUTTONDOWN
                and event.button == 1
                and self.bullet_count > 0
            ):
                self.bullets.append(Bullet(
                    self.player.x + 70, self.player.y + 17))
                self.bullet_count -= 1

            if (
                not self.game_status
                and event.type == pygame.MOUSEBUTTONDOWN
                and event.button == 1
                and self.restart_text_rect.collidepoint(pygame.mouse.get_pos())
            ):
                self.reset_game()

        return True

    def get_actions(self):
        """Получение действий игрока"""
        keys = pygame.key.get_pressed()
        return {
            "right": keys[pygame.K_d],
            "left": keys[pygame.K_a],
            "jump": keys[pygame.K_SPACE],
        }

    def update_gameplay(self):
        """Обновление игрового процесса"""
        # Движение фона
        self.bg_x -= SPEED_MOVE_BACKGROUND
        if self.bg_x <= -SCREEN_WIDTH:
            self.bg_x = 0

        # Обновление игрока
        actions = self.get_actions()
        self.player.move(actions)

        if actions["jump"]:
            self.player.start_jump()

        self.player.jump()

        # Обновление врагов
        for enemy in self.enemies[:]:
            enemy.update()
            if not enemy.is_active:
                self.enemies.remove(enemy)
                if self.game_status:
                    self.score += 1

            if self.player.rect.colliderect(enemy.rect):
                self.game_status = False

        # Обновление пуль
        for bullet in self.bullets[:]:
            bullet.update()
            if not bullet.is_active:
                self.bullets.remove(bullet)
            else:
                # Проверка столкновений пуль с врагами
                for enemy in self.enemies[:]:
                    if bullet.rect.colliderect(enemy.rect):
                        if bullet in self.bullets:
                            self.bullets.remove(bullet)
                        if enemy in self.enemies:
                            self.enemies.remove(enemy)
                        break

    def draw_gameplay(self):
        """Отрисовка игрового процесса"""
        # Фон
        screen.blit(self.bg, (self.bg_x, 0))
        screen.blit(self.bg, (self.bg_x + SCREEN_WIDTH, 0))

        # Игровая информация
        self.best_score = max(self.best_score, self.score)

        bullet_text = self.info_font.render(
            f"Патроны: {self.bullet_count}", True, INFO_TEXT_COLOR
        )
        score_text = self.info_font.render(
            f"Очки: {self.score}", True, INFO_TEXT_COLOR)
        best_score_text = self.info_font.render(
            f"Рекорд: {self.best_score}", True, INFO_TEXT_COLOR
        )

        screen.blit(bullet_text, (320, 0))
        screen.blit(score_text, (5, 0))
        screen.blit(best_score_text, (5, 25))

        # Игровые объекты
        for enemy in self.enemies:
            enemy.draw(screen)

        for bullet in self.bullets:
            bullet.draw(screen)

        self.player.draw(screen)

    def draw_game_over(self):
        """Отрисовка экрана проигрыша"""
        screen.blit(self.lose_bg, (-30, -8))
        screen.blit(self.lose_text,
                    (SCREEN_HEIGHT // 2, SCREEN_WIDTH // 2 - 180))
        screen.blit(self.restart_text, self.restart_text_rect)

        # Воспроизведение звука проигрыша
        if not self.lose_sound_playing:
            self.lose_sound.play()
            self.lose_sound_playing = True
            self.bg_sound.stop()

    def reset_game(self):
        """Сброс игры к начальному состоянию"""
        self.player = Player(PLAYER_START_POS_X, PLAYER_START_POS_Y)
        self.enemies.clear()
        self.bullets.clear()
        self.score = 0
        self.bullet_count = BULLET_COUNT
        self.game_status = True
        self.lose_sound_playing = False
        self.bg_sound.play(loops=-1)

    def run(self):
        """Главный игровой цикл"""
        running = True
        while running:
            running = self.handle_events()

            if self.game_status:
                self.update_gameplay()
                self.draw_gameplay()
            else:
                self.draw_game_over()

            pygame.display.update()
            clock.tick(20)

        pygame.quit()


if __name__ == "__main__":
    game = Game()
    game.run()
