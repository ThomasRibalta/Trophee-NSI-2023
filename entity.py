import pygame


class Entity(pygame.sprite.Sprite):
    def __init__(self, name, x, y, xi, yi, long, L):
        super().__init__()
        self.image = pygame.image.load(f"sprite_sheet/{name}.png")
        self.image = self.get_image(xi, yi, long, L)
        self.rect = self.image.get_rect()
        self.position = [x, y]  # position du perso
        self.feet = pygame.Rect(0, 0, self.rect.width * 0.5, 12)  # pied du joueur

    def update(self):
        self.rect.topleft = self.position  # actualiser la position du joueur

    def get_image(self, xi, yi, long, L):
        image = pygame.Surface([xi, yi])  # défini une surface de 24px par 24px
        pygame.Surface.set_colorkey(image, (0, 0, 0))
        image.blit(self.image, (0, 0), (long, L, 96,
                                        96))  # vient coller sur la surface la zone découpé donc là ce sera le deuxième perso de la première ligne
        return image
