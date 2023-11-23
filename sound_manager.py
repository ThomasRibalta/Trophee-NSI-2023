import pygame


class Sound:
    def __init__(self):
        pygame.init()
        self.sound = {
            "footsteps": "sound/Normal_footsteps.mp3",
            "cavefootsteps": "sound/Cave_footsteps.mp3",
            "discussion": "sound/bruit_affichage_texte.mp3",
            "menu": "sound/menu2.mp3",
            "principal": "sound/principal.mp3",
            "robot": "sound/robot.mp3",
            "cave": "sound/cave.mp3",
            "fight": "sound/coup.mp3",
            "evolution": "sound/evolution.mp3",
            "trash": "sound/trash.mp3",
            "boss": "sound/boss.mp3",
            "activate": "sound/activate.mp3",
            "degat": "sound/degat.mp3",
            "arbre": "sound/arbre.mp3",
            "point": "sound/point.mp3"
        }
        self.theme = pygame.mixer.Sound(self.sound["menu"])  # Definir le son principal de chaque page
        self.footsteps_sound = pygame.mixer.Sound(self.sound["footsteps"])  # Definir bruit de pas du perso
        self.discussion = pygame.mixer.Sound(self.sound["discussion"])  # Definir le bruit d'écriture de texte
        self.theme.set_volume(0.05)
        self.last = -self.theme.get_length()  # Pour faire en sorte qu'on puisse le faire en boucle sans spam

    def back_sound(self, scene):  # Gere implantation du son principal en fonction de la zone
        temps_act = pygame.time.get_ticks() / 1000
        if temps_act - self.last >= self.theme.get_length():
            self.theme = pygame.mixer.Sound(self.sound[scene])
            self.theme.set_volume(0.04)
            self.theme.play()
            self.last = temps_act

    def walk_sound(self, map_sound=str):  # Bruit de pas aussi en fonction de la zone
        self.footsteps_sound = pygame.mixer.Sound(self.sound[f"{map_sound}footsteps"])
        self.footsteps_sound.set_volume(0.03)
        self.footsteps_sound.play()

    def spawn_robot(self):
        spawn = pygame.mixer.Sound(self.sound[f"robot"])
        spawn.set_volume(0.1)
        spawn.play()

    def trash(self):
        temps_act = pygame.time.get_ticks() / 1000
        if temps_act - self.last >= self.theme.get_length():
            trash = pygame.mixer.Sound(self.sound[f"trash"])
            trash.set_volume(0.1)
            trash.play()

    def arbre(self):
        arbre = pygame.mixer.Sound(self.sound[f"arbre"])
        arbre.set_volume(0.1)
        arbre.play()
    def fight(self):
        temps_act = pygame.time.get_ticks() / 1000
        if temps_act - self.last >= self.theme.get_length():
            fight = pygame.mixer.Sound(self.sound[f"fight"])
            fight.set_volume(0.1)
            fight.play()

    def degat(self):
        degat = pygame.mixer.Sound(self.sound[f"degat"])
        degat.set_volume(0.1)
        degat.play()

    def discussion_sound(self):  # Joue sans spam le bruit d'écriture
        temps_act = pygame.time.get_ticks() / 1000
        if temps_act - self.last >= self.discussion.get_length():
            self.discussion = pygame.mixer.Sound(self.sound[f"discussion"])
            self.discussion.set_volume(0.2)
            self.discussion.play()
            self.last = temps_act
            self.last = temps_act

    def stop_sound(self, discussion=False):  # Arrête les sons mais fonction à revoir
        if discussion:
            self.discussion.stop()
        else:
            pygame.mixer.stop()
        self.last = -100000000000000000

    def activate(self):
        spawn = pygame.mixer.Sound(self.sound[f"activate"])
        spawn.set_volume(0.1)
        spawn.play()

    def point(self):
        point = pygame.mixer.Sound(self.sound[f"point"])
        point.set_volume(0.1)
        point.play()
