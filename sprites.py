import pygame as pg
from pygame.locals import RLEACCEL
from random import uniform, choice, randint
from settings import *
import pytweening as tween
import math
vec = pg.math.Vector2

class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self._layer = PLAYER_LAYER
        self.health = PLAYER_HEALTH
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.original_image = pg.Surface((TILESIZE, TILESIZE)).convert()
        self.original_image.set_colorkey((255, 255, 255), RLEACCEL)
        self.original_image.fill(DARKGREEN)
        self.image = self.original_image
        self.rect = self.image.get_rect(center=(x,y))
        self.hit_rect = PLAYER_HIT_RECT
        self.hit_rect.center = self.rect.center
        self.vel = vec(0, 0)
        self.pos = vec(x, y)
        self.rot = 0
        self.last_shot = 0


    def get_keys(self):
        self.rot_speed = 0
        self.vel = vec(0, 0)
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.vel.x = -PLAYER_SPEED
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.vel.x = PLAYER_SPEED
        if keys[pg.K_UP] or keys[pg.K_w]:
            self.vel.y = -PLAYER_SPEED
        if keys[pg.K_DOWN] or keys[pg.K_s]:
            self.vel.y = PLAYER_SPEED
        if self.vel.x != 0 and self.vel.y != 0:
            self.vel *= 0.7071

    def update(self):

        direction = self.game.mouse_pos - self.pos
        radius, angle = direction.as_polar()
        self.image = pg.transform.rotate(self.original_image, -angle)
        self.rot = -angle
        self.rect = self.image.get_rect(center=self.rect.center)

        self.get_keys()
        self.pos += self.vel * self.game.dt
        self.hit_rect.centerx = self.pos.x
        self.hit_rect.centery = self.pos.y
        self.rect.center = self.hit_rect.center


class Gun(pg.sprite.Sprite):
    def __init__(self, game, pos):
        self._layer = ITEM_LAYER
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.original_image = pg.Surface((40, 20)).convert()
        self.original_image.set_colorkey((255, 255, 255), RLEACCEL)
        self.original_image.fill(BLACK)
        self.image = self.original_image
        self.pos = vec(pos)
        self.rect = self.image.get_rect(center=pos)
        self.rot = 0

    def update(self):
        self.rot = self.game.player.rot
        self.image = pg.transform.rotate(self.original_image, self.rot)
        self.rect = self.image.get_rect(center=self.game.player.pos + vec(20, 40).rotate(-self.rot))


class Wall(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
