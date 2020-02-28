import random
import os
import pygame

pygame.init()
size = width, height = 500, 500
screen = pygame.display.set_mode(size)
count = 0


def draw(h):
    screen.fill((0, 0, 0))
    font = pygame.font.Font(None, 50)
    text = font.render(h, 1, (100, 255, 100))
    text_x = width // 2 - text.get_width() // 2
    text_y = height // 2 - text.get_height() // 2
    text_w = text.get_width()
    text_h = text.get_height()
    screen.blit(text, (text_x, text_y))
    pygame.draw.rect(screen, (0, 255, 0), (text_x - 10, text_y - 10,
                                           text_w + 20, text_h + 20), 1)


def load_image(name, color_key=None):
    fullname = os.path.join('data', name)
    image = pygame.image.load(fullname).convert()
    if color_key is not None:
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    else:
        image = image.convert_alpha()
    return image


class Bomb(pygame.sprite.Sprite):
    image = load_image("bomb.png")
    boom_image = load_image("boom.png")

    def __init__(self, group):
        super().__init__(group)
        self.count = False
        self.image = Bomb.image
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(width - self.rect.w)
        self.rect.y = random.randrange(height - self.rect.h)

    def clicked(self, y, x):
        # if self.rect.x <= x <= self.rect.x + self.rect.w and self.rect.y <= y <= self.rect.y + self.rect.h:
        #     self.image = Bomb.boom_image
        x1, y1, w1, h1 = self.rect.x, self.rect.y, self.rect.w, self.rect.h
        x2, y2, w2, h2 = x, y, create.rect.w, create.rect.h
        x1m, y1m, x2m, y2m = x1 + w1, y1 + h1, x2 + w2, y2 + h2
        kv1 = x1 + w1
        kn1 = y1 + h1
        kv2 = x2 + w2
        kn2 = y2 + h2
        if not (x1 > kv2 or x2 > kv1 or y1 > kn2 or y2 > kn1):
            self.image = Bomb.boom_image
            self.count = True


all_sprites = pygame.sprite.Group()

bombs = [Bomb(all_sprites) for _ in range(20)]


class Sprite(pygame.sprite.Sprite):
    image = load_image("creature.png")

    def __init__(self, group):
        super().__init__(group)
        self.image = Sprite.image
        self.rect = self.image.get_rect()
        self.x = 0
        self.y = 0

    def update(self, ev):
        if ev == "u":
            self.y += 10
        if ev == "d":
            self.y -= 10
        if ev == "l":
            self.x += 10
        if ev == "r":
            self.x -= 10
        k = self.image.get_rect()
        self.rect = k.move((self.y, self.x))


gr = pygame.sprite.Group()
create = Sprite(gr)
gr.add(create)
fps = 60
clock = pygame.time.Clock()
running = True
start_ticks = pygame.time.get_ticks()
game = True
while running:

    for event in pygame.event.get():
        # при закрытии окна
        if event.type == pygame.QUIT:
            running = False
        screen.fill((255, 255, 255))
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                gr.update("r")
            if event.key == pygame.K_DOWN:
                gr.update("l")
            if event.key == pygame.K_LEFT:
                gr.update("d")
            if event.key == pygame.K_RIGHT:
                gr.update("u")
            for bomb in bombs:
                bomb.clicked(create.x, create.y)
        count = 0
        for bomb in bombs:
            if bomb.count:
                count += 1
        if count == 20:
            draw("winner")
            pygame.display.flip()
            game = False
            break
        seconds = (pygame.time.get_ticks() - start_ticks) / 1000
        if seconds > 60 and game:
            draw("loser")
            pygame.display.flip()
            game = False
            break
        if game:
            screen.fill((255, 255, 255))
            all_sprites.draw(screen)
            all_sprites.update()
            clock.tick(fps)
            gr.draw(screen)
            pygame.display.flip()
