import pygame


class HomePage:
    def __init__(self, screen):
        self.clock = 0
        self.skin = pygame.image.load("sprite_sheet/normalp.png")
        self.button = pygame.image.load("sprite_sheet/bouton.png")
        self.title = pygame.image.load("sprite_sheet/titre.png")
        self.nous = pygame.image.load("sprite_sheet/nous.png")
        self.skin_images = {
            0: self.get_images_list(0, 0, 3, 0, "Skin"),
            1: self.get_images_list(0, 72, 2, 0, "Skin"),
            2: self.get_images_list(72, 0, 3, 0, "Skin"),
            3: self.get_images_list(0, 72, 2, 3, "Skin")
        }
        self.button_images = {
            0: self.get_images_list(0, 39, 2, 0, "Button"),
            1: self.get_images_list(0, 71, 2, 0, "Button"),
            2: self.get_images_list(0, 103, 2, 0, "Button"),
            3: self.get_images_list(0, 0, 2, 0, "Button")
        }
        self.position_skin = 0
        self.index = 0
        self.screen = screen
        self.new_party = self.screen.blit(self.button_images[0][0], (343, 190))  # fait pour les deux
        self.game_progress = self.screen.blit(self.button_images[1][0], (355, 290))  # fait pour les deux
        self.information = self.screen.blit(self.button_images[2][0], (430, 390))  # fait pour les deux

    def display_homepage(self, screen, position):  # Gere l'affichage des images dans le menu
        screen.blit(self.title, (screen.get_size()[0]/2 - 200, 70))
        screen.blit(self.nous, (40, 130))
        self.get_collide(position, screen)
        self.skin_move(screen)

    def get_collide(self, position, screen):  # Fonction qui check quand on survole un bouton avec notre sourit
        if self.new_party.collidepoint(position):
            self.new_party = screen.blit(self.button_images[0][1], (screen.get_size()[0]/2 - (500 -343), 190))
        else:
            self.new_party = screen.blit(self.button_images[0][0], (screen.get_size()[0]/2 - (500 -343), 190))
        if self.game_progress.collidepoint(position):
            self.game_progress = screen.blit(self.button_images[1][1], (screen.get_size()[0]/2 - (500 -355), 290))
        else:
            self.game_progress = screen.blit(self.button_images[1][0], (screen.get_size()[0]/2 - (500 -355), 290))
        if self.information.collidepoint(position):
            self.information = screen.blit(self.button_images[2][1], (screen.get_size()[0]/2 - (500 -430), 390))
        else:
            self.information = screen.blit(self.button_images[2][0], (screen.get_size()[0]/2 - (500 -430), 390))

    def get_images_list(self, x, y, i, direction=0, image_name=""):  #Fait une liste des images coupé recup
        images = []
        if image_name == "Skin":
            for _ in range(0, i):
                image = self.get_image(x, y, direction)
                images.append(image)
                x = x + 24
            if i == 2:
                images.append(images[0])
        else:
            for _ in range(0, i):
                image = self.get_image_button(x, y)
                images.append(image)
                x = x + 60
        return images

    def get_image_button(self, x, y):  # Récupere qu'une partie de l'image mais pour les boutton
        if y != 103:
            image = self.button.subsurface(x, y, 43, 16)
            image = pygame.transform.scale(image, (290, 55))
        else:
            image = self.button.subsurface(x, y, 29, 10)
            image = pygame.transform.scale(image, (120, 45))
        return image

    def get_image(self, x, y, direction=0):  # Recupere qu'une partie de l'image
        image = self.skin.subsurface(x, y, 24, 24)
        image = pygame.transform.scale(image, (110, 150))
        if direction == 0:
            image = pygame.transform.flip(image, True, False)
        return image

    def skin_move(self, screen):  # Permet de faire tourner les personnage en bas de l'écran
        self.clock += 8
        screen.blit(self.skin_images[self.position_skin][self.index], (screen.get_size()[0] - (1000 - 830), 420))
        if self.clock >= 100:
            self.index += 1
            if self.index == 3:
                self.position_skin += 1
                self.index = 0
            if self.position_skin == 4:
                self.position_skin = 0
            self.clock = 0
            delete = pygame.Surface((95, 150))
            delete.fill((0, 0, 0))
            screen.blit(delete, (screen.get_size()[0] - (1000 - 830), 420))
