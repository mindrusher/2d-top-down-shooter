import pygame
import random
import math

from pygame.locals import (
    RLEACCEL,
    K_w,
    K_s,
    K_a,
    K_d,
    K_ESCAPE,
    KEYDOWN,
    QUIT
)

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.image.load('Sprite-hero.png').convert()
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        self.rect = self.surf.get_rect(center=(400,550))

        self.angle = 0

    def update(self, pressed_keys):
        if pressed_keys[K_w]:
            self.rect.move_ip(0, -4)
        if pressed_keys[K_s]:
            self.rect.move_ip(0, 4)
        if pressed_keys[K_a]:
            self.rect.move_ip(-4, 0)
        if pressed_keys[K_d]:
            self.rect.move_ip(4, 0)

        mouse_x_pos, mouse_y_pos = pygame.mouse.get_pos()
        rads = math.atan2(mouse_x_pos - self.rect.x, mouse_y_pos - self.rect.y)
        self.angle = math.degrees(rads)

        w, h       = self.surf.get_size()
        originPos = (w/2, h/2)
        box        = [pygame.math.Vector2(p) for p in [(0, 0), (w, 0), (w, -h), (0, -h)]]
        box_rotate = [p.rotate(self.angle) for p in box]
        min_box    = (min(box_rotate, key=lambda p: p[0])[0], min(box_rotate, key=lambda p: p[1])[1])
        max_box    = (max(box_rotate, key=lambda p: p[0])[0], max(box_rotate, key=lambda p: p[1])[1])

        pivot        = pygame.math.Vector2(originPos[0], -originPos[1])
        pivot_rotate = pivot.rotate(self.angle)
        pivot_move   = pivot_rotate - pivot

        origin = (round(self.rect.x - originPos[0] + min_box[0] - pivot_move[0]), round(self.rect.y - originPos[1] - max_box[1] + pivot_move[1]))

        rotated_image = pygame.transform.rotate(self.surf, self.angle)

        screen.blit(rotated_image, origin)

class Missle(pygame.sprite.Sprite):
    def __init__(self):
        super(Missle, self).__init__()
        self.surf = pygame.image.load('Sprite-missle.png').convert()
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        self.rect = self.surf.get_rect()
        self.rect.x = turret.rect.x # перенести в аргумент инит
        self.rect.y = turret.rect.y # перенести в аргумент инит
        self.speed = 12
        self.angle = turret.angle # перенести в аргумент инит

    def update(self):
        w, h       = self.surf.get_size()
        originPos = (w/2, h/2)
        box        = [pygame.math.Vector2(p) for p in [(0, 0), (w, 0), (w, -h), (0, -h)]]
        box_rotate = [p.rotate(self.angle) for p in box]
        min_box    = (min(box_rotate, key=lambda p: p[0])[0], min(box_rotate, key=lambda p: p[1])[1])
        max_box    = (max(box_rotate, key=lambda p: p[0])[0], max(box_rotate, key=lambda p: p[1])[1])

        pivot        = pygame.math.Vector2(originPos[0], -originPos[1])
        pivot_rotate = pivot.rotate(self.angle)
        pivot_move   = pivot_rotate - pivot

        origin = (round(self.rect.x - originPos[0] + min_box[0] - pivot_move[0]), round(self.rect.y - originPos[1] - max_box[1] + pivot_move[1]))

        rotated_image = pygame.transform.rotate(self.surf, self.angle)

        screen.blit(rotated_image, origin)
               
        ang = math.radians(self.angle)
        if 0 < self.angle < 90 or 90 < self.angle < 180 or -90 < self.angle < 0 or -180 < self.angle < -90:
            self.rect.x += round(self.speed * math.sin(ang))
            self.rect.y += round(self.speed * math.cos(ang))
        elif self.angle == 0 or self.angle == 180:
            self.rect.y += round(self.speed * math.cos(ang))
        elif self.angle == 90 or self.angle == -90:
            self.rect.x += round(self.speed * math.sin(ang))

        self.destroy()

    def destroy(self):
        if 850 < self.rect.x or self.rect.x < -850 or 650 < self.rect.y or self.rect.y < -650:
            self.kill()

class Turret(pygame.sprite.Sprite):
    def __init__(self):
        super(Turret, self).__init__()
        self.surf = pygame.image.load('met.png').convert()
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        self.rect = self.surf.get_rect(
            center=(400, 200)
        )
        self.angle = 0

    def check_in(self):
        r = 200
        if (player.rect.centerx - self.rect.centerx) ** 2 + (player.rect.centery - self.rect.centery) ** 2 <= r * r:
            self.shoot()
        
    def shoot(self):
        rads = math.atan2(player.rect.x - self.rect.x, player.rect.y - self.rect.y)
        degs = math.degrees(rads)

        missles.add(Missle())   

    def update(self):
        x_dir, y_dir = player.rect.x, player.rect.y
        rads = math.atan2(x_dir - self.rect.x, y_dir - self.rect.y)
        self.angle = math.degrees(rads)

        w, h       = self.surf.get_size()
        originPos = (w/2, h/2)
        box        = [pygame.math.Vector2(p) for p in [(0, 0), (w, 0), (w, -h), (0, -h)]]
        box_rotate = [p.rotate(self.angle) for p in box]
        min_box    = (min(box_rotate, key=lambda p: p[0])[0], min(box_rotate, key=lambda p: p[1])[1])
        max_box    = (max(box_rotate, key=lambda p: p[0])[0], max(box_rotate, key=lambda p: p[1])[1])


        pivot        = pygame.math.Vector2(originPos[0], -originPos[1])
        pivot_rotate = pivot.rotate(self.angle)
        pivot_move   = pivot_rotate - pivot

        origin = (round(self.rect.x - originPos[0] + min_box[0] - pivot_move[0]), round(self.rect.y - originPos[1] - max_box[1] + pivot_move[1]))

        rotated_image = pygame.transform.rotate(self.surf, self.angle)

        screen.blit(rotated_image, origin)

        self.check_in()

pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

player = Player()

hero = pygame.sprite.Group()
hero.add(player)

turret = Turret()

enemies = pygame.sprite.Group()
enemies.add(turret)

missles = pygame.sprite.Group()

clock = pygame.time.Clock()

running = True

while running:
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
        elif event.type == QUIT:
            running = False

        elif pygame.mouse.get_pressed()[0]:
            print(player.rect.centerx, player.rect.centery, turret.rect.centerx, turret.rect.centery)
    
    screen.fill((255, 255, 255))

    pressed_keys = pygame.key.get_pressed()

    player.update(pressed_keys)

    turret.update()

    missles.update()

    if pygame.sprite.groupcollide(hero, enemies, False, False):
        pass

    pygame.display.flip()

    clock.tick(30)