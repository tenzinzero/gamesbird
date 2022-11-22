import pygame
import os
import random

def load_image(name, x, y, colorkey=None):
    fullname = os.path.join('image2', name)
    # если файл не существует, то выходим
    try:
        image = pygame.image.load(fullname).convert_alpha()
    except pygame.error as message:
        print(f"Файл с изображением '{fullname}' не найден")
        return SystemExit(message)
    if colorkey is None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return pygame.transform.scale(image, (x, y))


def fps(screen, clock, WIDTH):
    front = pygame.font.SysFont('Arial', 30, bold=True)
    display_fps = str(int(clock.get_fps()))
    render = front.render(display_fps, 0, (255, 0, 0))
    screen.blit(render, (WIDTH - 60, 30))


class Bird(pygame.sprite.Sprite):
    def __init__(self, player_image, pos_x, pos_y):
        super().__init__(bird_sprites)
        self.image = player_image
        self.rect = self.image.get_rect().move(
            pos_x, pos_y)
        self.sostoniye = 'down'
        self.tim_down = 1
        self.tim_up = 1
        self.speeding_up = 1
        self.speeding_down = 2
        self.pozitsiya = self.rect.y
        #self.mask_bird = pygame.mask.from_surface(self.image2)
        self.fly_or_not_fly = True

    def update(self, balki):
        for i in balki:
            if pygame.sprite.collide_mask(self, i):
                self.fly_or_not_fly = False
                break
        if self.fly_or_not_fly:
            if self.sostoniye == 'down':
                self.rect.y = self.pozitsiya + (self.speeding_down * (self.tim_down ** 2) / 2)
                self.tim_down += 0.5
            elif self.sostoniye == 'up':
                if self.tim_up < 0:
                    self.sostoniye = 'down'
                    self.tim_down = 0.5
                    self.pozitsiya = self.rect.y
                else:
                    self.rect.y = self.rect.y - (self.speeding_up * (self.tim_up ** 2) / 2)
                    self.tim_up = self.tim_up - 0.3


class Balki(pygame.sprite.Sprite):
    def __init__(self, image, pos_x, pos_y):
        super().__init__(balki_sprites)
        self.image = pygame.transform.scale(pygame.image.load(image[0]), (image[1], 300))
        self.rect = self.image.get_rect().move(
            pos_x, pos_y)
        self.speed = 5
        self.mask_balka = pygame.mask.from_surface(self.image)

    def update(self):
        if self.rect.x + 200 < 0:
            self.rect.x = 1000
        else:
            self.rect.x -= self.speed

if __name__ == '__main__':
    pygame.init()

    SIZE = (1000, 800)

    kol_balok = 6
    rastoyanie = SIZE[0] // 4
    rastoyanie1 = SIZE[0] // 4

    screen = pygame.display.set_mode(SIZE)

    time = pygame.time.Clock()

    fon = load_image('img_222.png', SIZE[0], SIZE[1])
    ja = 'flappy.png'
    bird_sprites = pygame.sprite.Group()
    balki_sprites = pygame.sprite.Group()
    spisok_balki = []
    down = 'image2/img_111.png'
    up = 'image2/img_333.png'
    for i in range(kol_balok):
        spisok_balki.append(Balki((down, 200, 300), (1500 + rastoyanie), 400))
        rastoyanie += rastoyanie
    for i in range(kol_balok):
        spisok_balki.append(Balki((up, 200, 300), (1500 + rastoyanie1), -20))
        rastoyanie1 += rastoyanie1
    rastoyanie = SIZE[0] // 4
    rastoyanie1 = SIZE[0] // 4
    bird = Bird(load_image(ja, 100, 100), 300, 300)
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bird.sostoniye = 'up'
                    #bird.tim = 0
                    bird.tim_up = 5
                if not bird.fly_or_not_fly and pygame.K_LCTRL:
                    bird.fly_or_not_fly = True
                    for i in range(kol_balok):
                        spisok_balki[i].rect.x, spisok_balki[i].rect.y = 1500 + rastoyanie, 400
                        rastoyanie += rastoyanie
                    for i in range(kol_balok, kol_balok + kol_balok):
                        spisok_balki[i].rect.x, spisok_balki[i].rect.y = 1500 + rastoyanie1, -20
                        rastoyanie1 += rastoyanie1
                    rastoyanie = SIZE[0] // 4
                    rastoyanie1 = SIZE[0] // 4

        screen.fill((0, 0, 0))
        screen.blit(fon, (0, 0))
        bird_sprites.draw(screen)
        balki_sprites.draw(screen)
        if bird.fly_or_not_fly:
            bird_sprites.update(spisok_balki)
            balki_sprites.update()
            pass
        fps(screen, time, SIZE[0])
        pygame.display.flip()
        time.tick(60)
    pygame.quit()