import pygame

import sound_manager


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, i):
        super().__init__()
        pygame.init()
        self.sprite_sheet = pygame.image.load("sprite_sheet/normalp.png")  # charge l'image du perso
        self.barre_vie = pygame.image.load("sprite_sheet/vie.png")
        self.barre_vie = pygame.transform.scale(self.barre_vie, (200, 90))
        self.view = 187
        self.image = self.get_image(0, 0+(24*i))  # découpe un carré de l'image en x 24 et y 0
        self.rect = self.image.get_rect()  # capte la zone autour du sprite
        self.position = [x, y]  # position du perso
        self.clock = 0  # pour changer la vitesse à laquelle les animations défilent
        self.speed_punch = 200
        self.images = {
            "down": self.get_images_list(0, 0+(24*i)),
            "up": self.get_images_list(72, 0+(24*i)),
            "left": self.get_images_list(0+(48*i), 72),
            "right": self.get_images_list(0+(48*i), 72),
            "punch_down": self.get_images_list(24+(48*i), 120),
            "punch_up": self.get_images_list(24+(48*i), 144),
            "punch_left": self.get_images_list(24+(48*i), 96),
            "punch_right": self.get_images_list(24+(48*i), 96),
            'fighting_stance_up': self.get_images_list(0+(48*i), 144),
            'fighting_stance_down': self.get_images_list(0+(48*i), 120),
            'fighting_stance_left': self.get_images_list(0+(48*i), 96),
            'fighting_stance_right': self.get_images_list(0+(48*i), 96)

        }
        self.animation = 1  # pour les sprites qui ont 3 frames
        self.animation_duo = 0  # pour les sprites qui ont 2 frames
        self.clock_punch = 0
        self.last_pose = "down"
        self.speed = 2  # vitesse du joueur
        self.sound = sound_manager.Sound()
        self.theme = ''
        self.feet = pygame.Rect(0, 0, self.rect.width * 0.5, 12)  # pied du joueur
        self.old_position = self.position.copy()  # copie de la position du joueur
        self.inventory = []
        self.check = False
        self.kill = 0
        self.ko = 0
        self.vie = 100
        self.dechet = 0

    def save_location(self):  # Enregister l'ancienne position du joueur
        self.old_position = self.position.copy()

    def get_images_list(self, x, y):
        images = []
        for _ in range(0, 3):
            image = self.get_image(x, y)
            images.append(image)
            x = x + 24
        return images

    def switch_skin(self, i):
        self.images = {
            "down": self.get_images_list(0, 0 + (24 * i)),
            "up": self.get_images_list(72, 0 + (24 * i)),
            "left": self.get_images_list(0 + (48 * i), 72),
            "right": self.get_images_list(0 + (48 * i), 72),
            "punch_down": self.get_images_list(24 + (48 * i), 120),
            "punch_up": self.get_images_list(24 + (48 * i), 144),
            "punch_left": self.get_images_list(24 + (48 * i), 96),
            "punch_right": self.get_images_list(24 + (48 * i), 96),
            'fighting_stance_up': self.get_images_list(0 + (48 * i), 144),
            'fighting_stance_down': self.get_images_list(0 + (48 * i), 120),
            'fighting_stance_left': self.get_images_list(0 + (48 * i), 96),
            'fighting_stance_right': self.get_images_list(0 + (48 * i), 96)

        }

    def life_barre(self, screen):
        screen.blit(self.barre_vie, (10, 20))
        self.view = 187 - round(187 * ((1 - self.vie * 0.01) * 100) / 100)
        pygame.draw.rect(screen, (150, 0, 0), (17.9, 29, self.view, 8))

    def move_up(self):  # fait monter le perso et change se position
        self.walk_animation("up")
        self.position[1] -= self.speed

    def move_down(self):  # fait monter le perso et change se position
        self.walk_animation("down")
        self.position[1] += self.speed

    def move_left(self):  # fait monter le perso et change se position
        self.walk_animation("left")
        self.position[0] -= self.speed

    def move_right(self):  # fait monter le perso et change se position
        self.walk_animation("right")
        self.position[0] += self.speed

    def fighting_stance(self):  # coup de poing
        if self.last_pose == 'left' or self.last_pose == 'fighting_stance_left':
            self.sound.fight()
            self.walk_animation("punch_left")
        elif self.last_pose == 'right' or self.last_pose == 'fighting_stance_right':
            self.sound.fight()
            self.walk_animation("punch_right")
        elif self.last_pose == 'up' or self.last_pose == 'fighting_stance_up':
            self.sound.fight()
            self.walk_animation("punch_up")
        elif self.last_pose == 'down' or self.last_pose == 'fighting_stance_down':
            self.sound.fight()
            self.walk_animation("punch_down")

    def walk_animation(self, direction):  # animation de marche
        self.clock += self.speed * 8
        if self.clock >= 100:
            self.sound.walk_sound(self.theme)
            if direction == "left" or direction == "right":
                if direction == "left":
                    self.image = self.images[direction][self.animation_duo]
                    self.image = pygame.transform.flip(self.image, True, False)
                else:
                    self.image = self.images[direction][self.animation_duo]
                self.animation_duo += 1
                if self.animation_duo == 2:
                    self.animation_duo = 0
            else:
                self.image = self.images[direction][self.animation]
                self.animation += 1
            if self.animation == 3:
                self.animation = 1
            self.clock = 0
        self.last_pose = direction

    def update(self):
        self.rect.topleft = self.position  # actualiser la position du joueur
        self.feet.midbottom = self.rect.midbottom  # postionner le bas des pied par rapport au bas du rectangle
        if self.last_pose == 'punch_left' or self.last_pose == 'punch_up' or self.last_pose == 'punch_down' or self.last_pose == 'punch_right':
            self.clock_punch += 10
            if self.clock_punch >= self.speed_punch:  # animation du coup de poing
                if self.last_pose == 'punch_left':
                    self.image = self.images['fighting_stance_left'][0]
                    self.last_pose = 'fighting_stance_left'
                elif self.last_pose == 'punch_right':
                    self.image = self.images['fighting_stance_right'][0]
                    self.last_pose = 'fighting_stance_right'
                elif self.last_pose == 'punch_up':
                    self.image = self.images['fighting_stance_up'][0]
                    self.last_pose = 'fighting_stance_up'
                elif self.last_pose == 'punch_down':
                    self.image = self.images['fighting_stance_down'][0]
                    self.last_pose = 'fighting_stance_down'

                self.idle_pose()
                self.clock_punch = 0

    def move_back(self):
        self.position = self.old_position
        self.rect.topleft = self.position  # actualiser la position du joueur
        self.feet.midbottom = self.rect.midbottom  # postionner le bas des pied par rapport au bas du rectangle

    def get_image(self, x, y):
        image = pygame.Surface([24, 24])  # défini une surface de 24px par 24px
        pygame.Surface.set_colorkey(image, (0, 0, 0))
        image.blit(self.sprite_sheet, (0, 0), (x, y, 24,
                                               24))  # vient coller sur la surface la zone découpé donc là ce sera le deuxième perso de la première ligne
        return image

    def idle_pose(self):
        if self.last_pose == "left":
            self.image = pygame.transform.flip(self.images[self.last_pose][0], True, False)
        else:
            self.image = self.images[self.last_pose][0]
        if self.last_pose == 'punch_left':
            self.image = pygame.transform.flip(self.images[self.last_pose][0], True, False)
        if self.last_pose == 'fighting_stance_left':
            self.image = pygame.transform.flip(self.images[self.last_pose][0], True, False)

    def reset(self):
        self.vie = 100
        self.dechet = 0
        self.ko = 0
        self.kill = 0
        self.inventory.clear()
        self.switch_skin(2)
            
    def add_inventory(self, type):  # ajoute de l'item dans l'inventaire
        if type == 0:
            self.inventory.append('plastique')
            self.kill += 1
        elif type == 1:
            self.inventory.append('verre')
            self.kill += 1
        elif type == 2:
            self.inventory.append('organique')
            self.kill += 1
            # faire un txt pour dire l'objet qui viens d'etre mis dans l'onventaire

    def clear_inventory(self, trash_can_type):  # clear l'inventaire des déchets correspondants à la poubelle choisit
        for trash in self.inventory:
            if trash_can_type == 'black':
                if trash == 'verre':
                    self.inventory.remove(trash)
                    self.check = True
                    self.dechet += 1
            if trash_can_type == 'yellow':
                if trash == 'plastique':
                    self.inventory.remove(trash)
                    self.check = True
                    self.dechet += 1
            if trash_can_type == "green":
                if trash == 'organique':
                    self.inventory.remove(trash)
                    self.check = True
                    self.dechet += 1