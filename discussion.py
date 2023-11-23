import pygame
import sound_manager


class Dialogue:
    def __init__(self, message,screen):
        pygame.font.init()  # Initialisation de font
        pygame.init()
        self.X_position = 40  # coordonnées du texte en X
        self.Y_postion = 490  # coordonnées du texte en X
        self.box = pygame.image.load("discussion_assets/Zone_de_texte.png")  # Charger l'asset de la bulle de dialogue
        self.robot = pygame.image.load("sprite_sheet/robot_king_1.png")
        self.image = self.get_image(0,0)
        self.box = pygame.transform.scale(self.box, (screen.get_size()[0], 600))  # Changer la taille de la bulle de dialogue
        self.texts = message  #
        # Stocker les dialogues
        self.text_split = []
        self.number_split = 0
        self.sound = sound_manager.Sound()
        self.text_index = 0  # compter le nombre de texte pour les faires défiler
        self.letter_index = 0  # Compter les lettres pour les afficher une par une
        self.font = pygame.font.Font("discussion_assets/text_font.TTF", 18)  # Definir la font et la taille du texte
        self.reading = False  # mode lecture
        self.reading_fast = False  # mode lecture rapide

    def execute(
            self):  # Fonction qui va executer le dialogue , mettre en mode lecture rapide , ou changer le texte , ect
        if self.reading and 0 <= self.letter_index >= len(self.texts[self.text_index]):
            self.reading_fast = False
            self.next_text()
            self.text_split = []
            self.number_split = 0
            self.split_text()

        elif self.reading and 0 < self.letter_index < len(self.texts[self.text_index]):
            self.reading_fast = True

        else:
            self.reading = True
            self.split_text()
            self.text_index = 0

    def get_image(self, x, y):
        pygame.Surface.set_colorkey(self.robot, (0, 0, 0))
        image = self.robot.subsurface(x, y, 32, 32)
        image = pygame.transform.scale(image, (96, 96))
        return image

    def split_text(self):  # Fonction qui split le texte pour le faire rentrer dans la bulle
        compteur = -1
        if self.reading:
            for i in range(len(self.texts[self.text_index]) + 1):
                compteur += 1
                if compteur == 86:
                    self.text_split.append(self.texts[self.text_index][i - 86:i])
                    compteur = 0
                if i == len(self.texts[self.text_index]):
                    if compteur < 86:
                        self.text_split.append(self.texts[self.text_index][i - compteur:i])

    def display_box(self, screen):  # Fonction qui va afficher le texte dans le bulle
        self.box = pygame.transform.scale(self.box, (screen.get_size()[0], 600))
        clock = pygame.time.Clock()
        h_ligne = 0
        if self.reading and self.reading_fast == False:
            if self.letter_index <= len(self.text_split[self.number_split]):
                self.sound.discussion_sound()
            else:
                self.sound.stop_sound(True)
            self.letter_index += 1  # compteur de lettre pour les afficher une par une
            if self.letter_index >= len(self.text_split[
                                            self.number_split]):  # faire en sorte que le compteur de dépasse pas le nombre max de lettre dans le dialogue
                if self.number_split < len(self.text_split) - 1:  # changer de partie du texte spliter
                    self.number_split += 1
                    self.letter_index = 0
                else:
                    self.letter_index = self.letter_index
            screen.blit(self.box, (0, screen.get_size()[1] - 600))  # Application de la bulle sur l'ecran
            if self.number_split >= 1:
                for i in range(self.number_split):  # afficher ligne par ligne le texte spliter
                    text = self.font.render(self.text_split[i], False, (0, 0, 0))  # font mise sur le texte
                    screen.blit(text, (self.X_position, screen.get_size()[1] - 110 + h_ligne))
                    h_ligne += 25  # Saut de ligne

            text = self.font.render(self.text_split[self.number_split][0:self.letter_index], False,
                                    (0, 0, 0))  # font mise sur le texte
            screen.blit(text, (80, screen.get_size()[1] - 110 + h_ligne))  # application du texte sur l'ecran
            screen.blit(self.image, (screen.get_size()[0] - (1000 - 868), screen.get_size()[1] - (600 - 138)))

        clock.tick(60)  # Vitesse d'appariton du texte

        if self.reading and self.reading_fast:  # mode lecture rapide
            self.letter_index = len(
                self.texts[self.text_index])  # compteur au max pour lecture du dialogue en entier d'un coup
            screen.blit(self.box, (0, screen.get_size()[1] - 600))  # Application de la bulle sur l'ecran
            for i in range(len(self.text_split)):
                text = self.font.render(self.text_split[i], False, (0, 0, 0))  # font mise sur le texte
                screen.blit(text, (80, screen.get_size()[1] - 110 + h_ligne))  # application du texte sur l'ecran
                h_ligne += 25
                screen.blit(self.image, (screen.get_size()[0] - (1000 - 868), screen.get_size()[1] - (600 - 138)))
                self.sound.stop_sound(True)

    def next_text(self):  # Fonction qui permet de passer au texte suivant
        self.text_index += 1
        self.letter_index = 0

        if self.text_index >= len(self.texts):  # fermeture de la bulle si il n'y a plus de texte
            self.text_index = 0
            self.reading = False
