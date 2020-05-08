import pygame 
import random
import math
import sys

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

FPS = 60  

screen = pygame.display.set_mode((800, 600)) 

pygame.display.set_caption('Derek in space')

movespeed = 4

class Player(pygame.sprite.Sprite):    
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.image.load('hero.png').convert()
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        self.rect = self.surf.get_rect(center=(400,550))
        self.lives = 10
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

    def shoot(self):
        mouse_x_pos, mouse_y_pos = pygame.mouse.get_pos()
        rads = math.atan2(mouse_x_pos - self.rect.x, mouse_y_pos - self.rect.y)
        degs = math.degrees(rads)

        missles.add(Missle())

class Missle(pygame.sprite.Sprite):
    def __init__(self):
        super(Missle, self).__init__()
        self.surf = pygame.image.load('Sprite-missle.png').convert()
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        self.rect = self.surf.get_rect()
        self.rect.x = player.rect.x
        self.rect.y = player.rect.y
        self.speed = 12
        self.angle = player.angle

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

class Meteor(pygame.sprite.Sprite):
    def __init__(self):    
        super(Meteor, self).__init__()
        self.surf = pygame.image.load('met.png').convert()
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        self.rect = self.surf.get_rect()
        self.speed = 2
        self.angle = 0
        self.rect.x = random.randint(20, 780)
        self.rect.y = random.randint(20, 100)

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

        dirvect = pygame.math.Vector2(player.rect.x - self.rect.x,
                                      player.rect.y - self.rect.y)
        dirvect.normalize()

        dirvect.scale_to_length(self.speed)
        self.rect.move_ip(dirvect)

        screen.blit(rotated_image, origin)

class Interface:    
    def update(self):
        hp_bar = player.lives * 10        
        self.rect = pygame.draw.rect(screen, (255, 0, 0), (20, 580, hp_bar, 10))

class GameController:   
    @staticmethod
    def render():
        for objects in all_sprites:
            screen.blit(objects.surf, objects.rect)


pygame.init()

ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, 500)

fire_rate = pygame.USEREVENT + 2
pygame.time.set_timer(fire_rate, 20)

interface = Interface()

enemies = pygame.sprite.Group()
missles = pygame.sprite.Group()

player = Player()

hero = pygame.sprite.Group()
hero.add(player)

all_sprites = pygame.sprite.Group()
all_sprites.add(missles)

pygame.key.set_repeat(1, 1)
clock = pygame.time.Clock() 

done = True

while done:
    screen.fill((255, 255, 255))
    interface.update()

    for event in pygame.event.get(): 
        if event.type == pygame.QUIT: 
            pygame.quit() 
            sys.exit()


        elif event.type == fire_rate:
            if pygame.mouse.get_pressed()[0]:
                player.shoot()

        elif event.type == ADDENEMY:
            new_enemy = Meteor()
            enemies.add(new_enemy)
            #all_sprites.add(new_enemy)

    pressed_keys = pygame.key.get_pressed()

    player.update(pressed_keys)

    enemies.update()
    missles.update()

    pygame.sprite.groupcollide(missles, enemies, True, True)
    
    if pygame.sprite.groupcollide(hero, enemies, False, True):
        player.lives -= 1
        if player.lives == 0:
            done = False

    pygame.display.flip()
    clock.tick(FPS)