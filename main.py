import pygame

import infopage
import level
import video
from map_manager import MapsManagement
from player import Player
from homepage import HomePage
from sound_manager import Sound


class Main:

    def __init__(self):
        self.is_playing = False
        self.long = 1000
        self.larg = 600
        self.screen = pygame.display.set_mode((self.long, self.larg), pygame.RESIZABLE)  # Dimension de l'écran
        pygame.display.set_caption("Objectif dépolution")  # titre de l'écran
        pygame.init()

        self.player = Player(30, 40, 2)  # faire spawn le joueur
        self.Map = MapsManagement(self.screen, self.player)

        self.homepage = HomePage(self.screen)  # charger la class de la page d'acceuil

        self.sound = Sound()  # Ajouter du son

        self.theme = "principal"  # savoir quel son mettre

        self.Level = level.Level(self.screen)  # suivre l'histoire grace au lvl

        self.Video = video.Video("intro")  # charger vidéo d'intro

        self.info_page = infopage.InfoPage(self.screen)  # Page d'information

        self.clock = 0  # calcule le temps pour mettre en idle pose

    def press_input(self):  # fonction qui va se charger de capter les pressions de touche
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_UP]:
            self.player.move_up()
            self.clock = 0
        elif pressed[pygame.K_DOWN]:
            self.player.move_down()
            self.clock = 0
        elif pressed[pygame.K_LEFT]:
            self.player.move_left()
            self.clock = 0
        elif pressed[pygame.K_RIGHT]:
            self.player.move_right()
            self.clock = 0
        elif pressed[pygame.K_z]:
            self.player.fighting_stance()
            self.clock = 0
        self.clock += 5
        if self.clock == 20:
            self.player.idle_pose()
        return

    def get_switch(self):
        if self.theme != self.Map.theme:
            self.theme = self.Map.theme
            self.sound.stop_sound()

    def save(self, lvl):
        if lvl < 2:
            lvl = 2
        if lvl > 6:
            lvl = 6
        with open("Sauvegarde.txt", 'w') as f:
            f.write(str(lvl))

    def get_last(self):
        try:
            with open("Sauvegarde.txt", 'r') as f:
                last = float(f.readline())
            self.Map.restaure(int(last))
            return int(last)
        except:
            return 2

    def run(self):
        clock = pygame.time.Clock()

        running = True
        while running:
            if self.Level.level == 0:
                self.Video.play_video(self.screen)
                self.sound.back_sound("menu")
                if pygame.time.get_ticks() >= self.Video.clip.end * 1000:
                    self.Level.level += 1
                    self.screen.fill((0, 0, 0))
            if self.Level.level == 1:
                self.sound.back_sound("menu")
                if self.info_page.statut:
                    self.Map.update(self.Level.level)
                    self.info_page.display_info_page()
                else:
                    self.homepage.display_homepage(self.screen, pygame.mouse.get_pos())
            if 7 >= self.Level.level > 1 or 4 > self.Level.level >= 5 and self.info_page.statut == False:
                self.get_switch()
                self.Map.update(self.Level.level)
                self.player.save_location()
                self.sound.back_sound(self.theme)
                if not self.Level.is_reading():
                    self.press_input()
                self.Map.mobs_move()
                self.Map.draw()
                self.player.life_barre(self.screen)
                self.Level.quete_blit(self.screen)
                self.Map.blit_manager()
                self.Level.dialogue.display_box(self.screen)
            if 2 <= self.Level.level < 3:
                self.Level.level2(self.player)
            if 3 <= self.Level.level < 4:
                self.Level.level3(self.player)
            if 4 <= self.Level.level < 5:
                if round(self.Level.level) == 4:
                    self.sound.stop_sound()
                self.Level.level4(self.player, self.screen)
            if 5 <= self.Level.level < 6:
                self.Level.level5(self.player)
            if 6 <= self.Level.level < 7:
                self.Map.theme = "boss"
                if round(self.Level.level, 1) == 6:
                    self.sound.stop_sound()
                    self.Level.level += 0.1
                self.Level.level6(self.player, self.Map.get_map())
            if self.Level.level >= 7:
                if self.Level.level == 7:
                    self.sound.stop_sound()
                    self.save(self.Level.level)
                    self.player.reset()
                self.Level.level7(self.player, self.screen)
            if self.info_page.statut:
                self.info_page.display_info_page()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.save(self.Level.level)
                    running = False
                elif event.type == pygame.VIDEORESIZE:
                    self.long, self.larg = event.size
                    self.screen = pygame.display.set_mode((self.long, self.larg), pygame.RESIZABLE)
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE and self.info_page.statut:
                        self.info_page.closing()
                    elif event.key == pygame.K_ESCAPE and self.info_page.statut == False:
                        self.info_page.statut = True
                    if event.key == pygame.K_SPACE:
                        if self.Level.is_reading():
                            self.Level.execute()
                        if self.Map.discussion.reading:
                            self.Map.discussion.execute()
                elif event.type == pygame.MOUSEBUTTONDOWN and self.Level.level == 1:
                    if self.homepage.new_party.collidepoint(event.pos):
                        self.Level.level = self.get_last()
                        self.sound.stop_sound()
                    if self.homepage.game_progress.collidepoint(event.pos):
                        self.Level.level += 1
                        self.Map = MapsManagement(self.screen, self.player)
                        self.sound.stop_sound()
                    if self.homepage.information.collidepoint(event.pos):
                        self.info_page.statut = True
            pygame.display.flip()
            clock.tick(60)  # Nombre de fps
