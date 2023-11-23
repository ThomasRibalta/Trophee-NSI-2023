import pygame

import pygame

import sound_manager


class Boss(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        pygame.init()
        self.sprite_sheet = pygame.image.load("sprite_sheet/Boss.png")  # charge l'image du perso
        self.image = self.get_image(0, 0)  # découpe un carré de l'image en x 24 et y 0
        self.rect = self.image.get_rect()  # capte la zone autour du sprite
        self.position = [x, y]  # position du perso
        self.clock = 0  # pour changer la vitesse à laquelle les animations défilent
        self.speed_attack = 200
        self.images = self.get_images_list(0, 0)
        self.animation = 1  # pour les sprites qui ont 3 frames
        self.mouvement = 0
        self.speed = 5  # vitesse du monstre
        self.feet = pygame.Rect(0, 0, self.rect.width * 0.5, 12)  # pied du joueur
        self.un = 1

    def switch_move(self):
        if self.speed > 0:
            if self.mouvement == 0:
                self.mouvement = 1
                self.position[0] -= 10
            else:
                self.position[0] += 10
                self.mouvement = 0
        else:
            if self.mouvement == 0:
                self.mouvement = 1
                self.position[0] += 10
            else:
                self.position[0] -= 10
                self.mouvement = 0

    def switch_speed(self):
        if self.speed < 0:
            self.speed = 5
            self.un = 1
            self.position[1] += 10
        else:
            self.speed = - 5
            self.un = -1
            self.position[1] -= 10

    def move(self):
        if self.mouvement == 0:
            self.right()
        else:
            self.left()

    def left(self):  # fait monter le perso et change se position
        self.walk_animation()
        self.position[1] += self.un
        self.position[0] -= self.speed

    def right(self):  # fait monter le perso et change se position
        self.walk_animation()
        self.position[1] += self.un
        self.position[0] += self.speed

    def walk_animation(self):  # animation de marche
        self.clock += abs(self.speed) * 8
        if self.clock >= 180:
            self.image = self.images[self.animation]
            self.animation += 1
            if self.animation == 3:
                self.animation = 0

    def update(self):
        self.rect.topleft = self.position  # actualiser la position du joueur
        self.feet.midbottom = self.rect.midbottom  # postionner le bas des pied par rapport au bas du rectangle

    def get_images_list(self, x, y):
        images = []
        for _ in range(0, 3):
            image = self.get_image(x, y)
            images.append(image)
            x = x + 48
        return images

    def get_image(self, x, y):
        image = pygame.Surface([48, 48])  # défini une surface de 24px par 24px
        pygame.Surface.set_colorkey(image, (0, 0, 0))
        image.blit(self.sprite_sheet, (0, 0), (x, y, 48,
                                               48))  # vient coller sur la surface la zone découpé donc là ce sera le deuxième perso de la première ligne
        return image
