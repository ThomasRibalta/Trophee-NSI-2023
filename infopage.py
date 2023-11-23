import pygame


class InfoPage:
    def __init__(self, screen):
        pygame.font.init()  # Initialisation de font
        self.statut = False
        self.text_x = 320
        self.text_y = 200
        self.line_break = 50
        self.screen = screen
        self.font = pygame.font.Font("discussion_assets/text_font.TTF", 18)  # Definir la font et la taille du texte
        self.text = ['A = jeter dechets poubelles', 'Z = attaquer', 'Espace = Faire avancer le dialogue',
                     'R = planter les arbres', 'E = recuperer le depollueur', 'F = ramasser les loots des mobs',
                     'Fleche directionelle = se deplacer', 'S = Activer depollueur dans usine', 'echap = ouvrir/fermer menu']

    def display_info_page(self):
        self.screen.fill('black')
        if self.statut:
            self.text_y = 20
            for i in range(0, len(self.text)):
                text = self.font.render(self.text[i], False, (250, 250, 250))  # font mise sur le texte
                self.text_y += self.line_break
                self.screen.blit(text, (self.screen.get_size()[0]/2 - (500-self.text_x), self.text_y))

    def closing(self):
        self.screen.fill('black')
        self.statut = False