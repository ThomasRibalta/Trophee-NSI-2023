import pygame

import sound_manager


class Mobs(pygame.sprite.Sprite):
    def __init__(self, x, y, type):
        super().__init__()
        self.speed_find = 0
        self.type = type
        self.sprite_sheet = pygame.image.load("sprite_sheet/Monstres_1.png")  # charge l'image du monstre
        self.image = self.get_image(0, 0 + (24 * type))  # découpe un carré de l'image en x 24 et y 0
        self.rect = self.image.get_rect()  # capte la zone autour du sprite
        self.position = [x, y]  # position du perso
        self.clock = 0  # pour changer la vitesse à laquelle les animations défilent 1= jaune 2= verre 3= viollet
        self.attaque_clock = 0
        self.images = {  # sprites des mobs
            "down": self.get_images_list(48, 0 + (24 * type), 2),
            "up": self.get_images_list(96, 0 + (24 * type), 2),
            "left": self.get_images_list(0, 0 + (24 * type), 2),
            "right": self.get_images_list(0, 0 + (24 * type), 2),
            "Dechet": self.get_image(144, 0 + (24 * type))
        }
        self.animation_duo = 0  # pour les sprites qui ont 2 frames
        self.mob_type = type  # pour savoir quel type de mob c'est
        self.feet = pygame.Rect(0, 0, self.rect.width * 0.5, 12)
        self.speed = 1  # vitesse du mob
        self.life = 100
        self.old_position = self.position.copy()

    def get_images_list(self, x, y, i):
        images = []
        for _ in range(0, i):
            image = self.get_image(x, y)
            images.append(image)
            x = x + 24
        return images

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

    def walk_animation(self, direction):  # animation de marche
        self.clock += self.speed * 8
        if self.clock >= 72:
            if direction == "right":
                self.image = self.images[direction][self.animation_duo]
                self.image = pygame.transform.flip(self.image, True, False)
            else:
                self.image = self.images[direction][self.animation_duo]
            self.animation_duo += 1
            if self.animation_duo == 2:
                self.animation_duo = 0
            self.clock = 0

    def update(self):
        self.rect.topleft = self.position  # actualiser la position du joueur

    def get_image(self, x, y):
        image = pygame.Surface([24, 24])  # défini une surface de 24px par 24px
        pygame.Surface.set_colorkey(image, (0, 0, 0))
        image.blit(self.sprite_sheet, (0, 0), (x, y, 24,
                                               24))  # vient coller sur la surface la zone découpé donc là ce sera le deuxième perso de la première ligne
        return image

    def monster_damage(self):  # dégat mob
        self.life = 0

    def save_location(self):  # Enregister l'ancienne position du mob
        self.old_position = self.position.copy()

    def attaque(self):
        if self.attaque_clock == 50:
            self.attaque_clock = 0
            sound_manager.Sound().degat()
            return 1
        self.attaque_clock += 1
        return 0

    def move_back(self):
        self.position = self.old_position
        self.rect.topleft = self.position  # actualiser la position du joueur
        self.feet.midbottom = self.rect.midbottom  # postionner le bas des pied par rapport au bas du rectangle

    def target_find(self, player):  # Fonction qui va faire en sorte que le monstre soit toujours attiré par sa cible
        target_position = player.position  # Cible est donc le personnage
        if self.life > 0:
            if abs(self.position[1] - target_position[1]) <= 64 and abs(self.position[0] - target_position[0]) <= 64:
                if self.speed_find == 20:  # pour eviter que les monstres soient trop rapide
                    if int(self.position[1]) > int(target_position[1]):
                        self.move_up()
                    elif int(self.position[1]) < int(target_position[1]):
                        self.move_down()
                    if int(self.position[0]) > int(target_position[0]):
                        self.move_left()
                    elif int(self.position[0]) < int(target_position[0]):
                        self.move_right()
                    self.speed_find = 0
                self.speed_find += 5
        else:
            self.image = self.images["Dechet"]