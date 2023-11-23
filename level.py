import pygame

import discussion
import sound_manager
import video


class Level:
    def __init__(self, screen):
        self.screen = screen
        self.level = 0
        self.dialogue = discussion.Dialogue([], self.screen)
        self.sound = sound_manager.Sound()
        self.font = pygame.font.Font("discussion_assets/text_font.TTF", 12)  # Definir la font et la taille du texte
        self.image = pygame.image.load("sprite_sheet/quete.png")
        self.image = pygame.transform.scale(self.image, (220, 50))
        self.quete = ""
        self.Video = ""

    def level2(self, player):
        if round(self.level, 1) == 2:
            self.sound.spawn_robot()
            self.dialogue = discussion.Dialogue(["Bien le bonjour jeune depollueur !",
                                                 "Cela fait un petit moment qu'on ne l'on vous avez pas vu mais bon ce n'est pas grave.",
                                                 "Nous avons besoin de vous, voici donc un topo de la situation actuelle de notre monde."
                                                 "Tout d'abord toutes nos mines sont contaminees par des monstres avec cela les arbres sont tous dans un sale etat, "
                                                 "les machines a depolluer ont etes volees et de droles de bruits provienent de l'usine.",
                                                 "Si vous souhaitez guerrir cette planete je vous invite dans un premier temps a chasser les monstres des mines. Vous pourrez trouver les entrees en vous baladant dans les environs, Bonne chance a vous !"], self.screen)
            self.dialogue.execute()
            self.quete = "Trouver/Chasser les monstres \n des mines."
            self.level += 0.1
        if 2.1 <= round(self.level, 1) < 2.8:
            if player.vie == 0:
                self.sound.spawn_robot()
                self.dialogue = discussion.Dialogue(
                    ["On ne va pas se laisser tuer par des dechets, retournons au combat !"], self.screen)
                self.dialogue.execute()
                player.vie = 100
            if not self.dialogue.reading:
                if player.ko == 1 and round(self.level, 2) < 2.15:
                    self.sound.spawn_robot()
                    self.dialogue = discussion.Dialogue(["Et voila d'un monstre elimine. Appuyez une fois sur [F] pour ramasser le dechet."], self.screen)
                    self.dialogue.execute()
                    self.level = 2.15
                if round(self.level, 1) < 2.2 and player.ko > 0:
                    if not self.dialogue.reading:
                        self.dialogue = discussion.Dialogue(["Bien joue ! Tu viens de finir de nettoyer une mine entiere. Tu peux te rendre a la suivante :)"], self.screen)
                        self.level = 2.2
            if 2.2 <= round(self.level, 1) < 2.8:
                if player.kill == 10 and round(self.level, 1) == 2.2:
                    self.sound.spawn_robot()
                    self.dialogue.execute()
                    self.level += 0.1
                if player.kill == 20 and round(self.level, 1) == 2.3:
                    self.sound.spawn_robot()
                    self.dialogue.execute()
                    self.level += 0.1
                if player.kill == 30 and round(self.level, 1) == 2.4:
                    self.level += 0.4
            if round(self.level, 1) == 2.8:
                self.dialogue = discussion.Dialogue([
                    "Parfait, tu viens de finir de chasser tout les monstres. Je t'invite a me rejoindre au point de depart pour jeter les dechets a la poubelle."], self.screen)
                self.sound.spawn_robot()
                self.dialogue.execute()
                self.quete = "Jeter les dechets a la \n poubelle."
                self.level += 0.1
        if not self.dialogue.reading:
            if round(self.level, 1) == 2.9 and player.dechet == 30:
                self.dialogue = discussion.Dialogue([
                    "Nickel, vous venez de faire un geste vraiment ecologique.", "Grace a cela vous verrez bientot la planete dans un meilleur etat.", "Cependant je ne pense pas que cela va suffire, comme dit plus tot les arbres sont dans un sale etat.", "Pour palier a cela voici quelques graines, utilisez les sur les arbres coupes !"], self.screen)
                self.sound.spawn_robot()
                self.quete = "Aller planter les graines \n sur les troncs d'arbres."
                self.dialogue.execute()
                for e in range(0, 11):
                    player.inventory.append(f"Graine{e}")
                self.level += 0.1

    def level3(self, player):
        if len(player.inventory) == 0 and round(self.level, 1) == 3:
            self.dialogue = discussion.Dialogue(["Super, vous avez fini de reforester notre merveilleuse planete mais "
                                                 "le saviez-vous: ...", "Actuellement, la deforestation tropicale "
                                                                        "induit chaque annee l'emission de 6 "
                                                                        "gigatonnes de CO2, soit de l'ordre de 20% "
                                                                        "des emissions mondiales annuelles de CO2"], self.screen)
            self.sound.spawn_robot()
            self.dialogue.execute()
            self.level += 0.1
        if not self.is_reading() and round(self.level, 1) == 3.1:
            self.level = 4

    def level4(self, player, screen):
        if round(self.level, 1) == 4:
            self.Video = video.Video("intro")
            self.level += 0.1
        if round(self.level, 1) == 4.1:
            self.Video.play_video(screen)
            self.sound.back_sound("evolution")
            if pygame.time.get_ticks() >= self.Video.clip.end * 1000:
                self.level += 0.9
                player.switch_skin(1)
                screen.fill((0, 0, 0))

    def level5(self, player):
        if round(self.level, 1) == 5:
            self.dialogue = discussion.Dialogue(
                ["Bien joue, vous avez vu comment la terre est deja bien plus belle :).",
                 "Maintenant le probleme de la deforestation regle, il faudrait purifier l'air et l'eau a l'aide de machine. Retournez chercher les machines dans les mines."], self.screen)
            self.sound.spawn_robot()
            self.quete = "Aller chercher les machines \n dans les mines."
            self.dialogue.execute()
            self.level += 0.1
        if round(self.level, 1) == 5.1:
            if len(player.inventory) == 1:
                self.dialogue = discussion.Dialogue(
                        ["Et d'une machine en poche, foncez recuperer les deux autres !"], self.screen)
                self.sound.spawn_robot()
                self.dialogue.execute()
                self.level += 0.1
        if round(self.level, 1) == 5.2:
            if len(player.inventory) == 2:
                self.dialogue = discussion.Dialogue(
                            ["Parfait une de plus, il vous manque plus que la derniere."], self.screen)
                self.sound.spawn_robot()
                self.dialogue.execute()
                self.level += 0.1
        if round(self.level, 1) == 5.3:
            if len(player.inventory) == 3:
                self.dialogue = discussion.Dialogue(
                        ["Vous voila avec les trois machines qu'il nous fallait.", "Trouver les points de ces machines sur la carte et placez-les."], self.screen)
                self.sound.spawn_robot()
                self.dialogue.execute()
                self.quete = "Mettre les machine a \n leurs place."
                self.level += 0.1
        if round(self.level, 1) == 5.4:
            if len(player.inventory) == 0:
                self.dialogue = discussion.Dialogue(
                    ["C'est encore un travail de qualite que vous avez fournis la.", "Helas jeune depollueur il reste encore un gros probleme a regler mais je ne peux pas vous en dire plus que rendez-vous dans l'usine."], self.screen)
                self.sound.spawn_robot()
                self.quete = "Rendez-vous a l'usine."
                self.dialogue.execute()
                self.level = 6

    def level6(self, player, map):
        if round(self.level,1) == 6.1:
            if map.name == "bossmap":
                self.dialogue = discussion.Dialogue(
                    ["Argg je m'en doutais !",
                     "C'est le monstre poubelle, il doit provenir de toute la pollution qu'emet cette usine.","Pour le vaincre du devras passer derriere lui sans te faire toucher et activer les machines a depollueur [S]."], self.screen)
                self.sound.spawn_robot()
                self.quete = "Passer derriere le boss \n pour activer les machines."
                self.dialogue.execute()
                self.level = 6.2
        if len(player.inventory) == 3 and round(self.level, 1) == 6.2:
                self.dialogue = discussion.Dialogue(
                    ["Ha ha on l'a bien eu celui-ci :) !",
                     "Bon bah je crois que c'est la fin pour moi dans un monde sans pollution je n'ai pas besoin de rester.",
                     "Merci d'avoir suivie mes conseilles le long de cette aventure, adieu C0dy."], self.screen)
                self.sound.spawn_robot()
                self.quete = "Attendez la suite du jeu \n ou recommencez :)."
                self.dialogue.execute()
                self.level += 0.1
        if self.level > 6.2:
            if not self.is_reading():
                self.level = 7

    def execute(self):
        self.dialogue.execute()

    def is_reading(self):
        if self.dialogue.reading:
            return True
        return False

    def quete_blit(self, screen):
        quete = self.quete.split("\n")
        screen.blit(self.image, (screen.get_size()[0] - (1000-770), 20))
        i = 35
        for e in quete:
            quet = self.font.render(e, False, (0, 0, 0))
            screen.blit(quet, (screen.get_size()[0] - (1000-778), i))
            i += 10

    def level7(self, player, screen):
        if self.level == 7:
            self.Video = video.Video('intro')
            self.level = 7.1
        if self.level == 7.1:
            self.Video.play_video(screen)
            self.sound.back_sound("evolution")
            if pygame.time.get_ticks() >= self.Video.clip.end * 1000:
                self.sound.stop_sound()
                self.level = 1
                screen.fill((0, 0, 0))
