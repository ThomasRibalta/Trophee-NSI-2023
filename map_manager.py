from dataclasses import dataclass

import pygame
import pyscroll
import pytmx

import Boss
import discussion
import entity
import sound_manager
from mobs import Mobs


@dataclass
class Portal:
    from_world: str
    origin_point: str
    target_world: str
    teleport_point: str


@dataclass
class Map:
    name: str  # stocker le nom de la map
    group: pyscroll.PyscrollGroup  # stocker le group à draw
    mobs: list[pygame.sprite.Sprite]  # stocker les mobs
    tmx_data: pytmx.TiledMap
    walls: list[pygame.Rect]
    trash: list[list[pygame]]
    arbre: list[pygame.Rect]
    dep: list[pygame.Rect]
    portails: list[Portal]


class MapsManagement:

    def __init__(self, screen, player):
        self.font = pygame.font.Font("discussion_assets/text_font.TTF", 18)  # Definir la font et la taille du texte
        self.sound = sound_manager.Sound()
        self.screen = screen  # récupere l'écran pour draw
        self.maps = {}  # stocker les maps avec leurs nom en clé et information en valeur
        self.player = player  # récupere le joueurs pour centrer le draw plus bas sur lui et l'add à chaque groupe
        self.boss = Boss.Boss(500000, 0)
        self.boss.update()
        self.discussion = discussion.Dialogue([], screen)
        self.default_map = "main_map"  # map sur laquelle on se trouve
        self.theme = "principal"  # Pour gerer le son de fond selon la map
        self.score = 0  # score du jeux
        self.touche = ""
        self.point = {
            "pickup_item": 100,
            "clear_inventory": 50,
            "lay_tree": 150,
            "lay_machine": 100
        }
        self.register_map("main_map", [],
                          [Portal('main_map', 'entre_grotte1', 'map_grotte1',
                                  'spawn_grotte1'),
                           Portal('main_map', 'entre_grotte2', 'map_grotte2',
                                  'spawn_grotte2'),
                           Portal('main_map', 'entre_grotte3', 'map_grotte3',
                                  'spawn_grotte3'),
                           Portal('main_map', 'entre_usine', 'bossmap',
                                  'spawn')], 3)
        self.register_map("map_grotte1",
                          [Mobs(319, 609, 0), Mobs(247, 439, 0), Mobs(335, 337, 0), Mobs(489, 113, 0),
                           Mobs(525, 231, 0),
                           Mobs(447, 463, 0), Mobs(523, 329, 0), Mobs(627, 419, 0), Mobs(715, 309, 0),
                           Mobs(667, 203, 0)],
                          [Portal('map_grotte1', 'sortie_grotte1', 'main_map', 'pnt_sortie_grotte1')], 4)
        self.register_map("map_grotte2",
                          [Mobs(158, 159, 1), Mobs(386, 157, 1), Mobs(616, 313, 1), Mobs(392, 319, 1),
                           Mobs(160, 399, 1),
                           Mobs(388, 477, 1), Mobs(614, 483, 1), Mobs(164, 559, 1), Mobs(472, 567, 1),
                           Mobs(500, 683, 1)],
                          [Portal('map_grotte2', 'sortie_grotte2', 'main_map', 'pnt_sortie_grotte2')], 4)
        self.register_map("map_grotte3",
                          [Mobs(138, 501, 2), Mobs(352, 671, 2), Mobs(554, 709, 2), Mobs(656, 579, 2),
                           Mobs(674, 407, 2),
                           Mobs(612, 195, 2), Mobs(384, 117, 2), Mobs(166, 277, 2), Mobs(436, 535, 2),
                           Mobs(416, 389, 2)],
                          [Portal('map_grotte3', 'sortie_grotte3', 'main_map', 'pnt_sortie_grotte3')], 4)
        self.register_map("bossmap",
                          [],
                          [Portal('bossmap', 'sortie_usine', 'main_map', 'sortie_usine')], 4)
        self.teleport("spawn")

    def register_map(self, map_name, mobs=[], portails=[], layer_zoom=0):
        tmx_data = pytmx.util_pygame.load_pygame(f'maps/{map_name}.tmx')  # charger la map tiled
        map_date = pyscroll.data.TiledMapData(tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(map_date, self.screen.get_size())
        map_layer.zoom = layer_zoom  # zoom sur le joueur

        group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=100)  # dessiner le groupe de calques
        group.add(self.player)  # ajout du joueur au group pour le dessiner ig

        for mob in mobs:
            group.add(mob)  # ajoute chaques mob au group
        walls = []
        trash = [[], [], []]
        arbres, dep = [], []
        for obj in tmx_data.objects:
            if obj.name is not None:
                if obj.name == 'collision':
                    walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))
                if obj.name == 'poubelle_verte':
                    trash[0].append((pygame.Rect(obj.x, obj.y, obj.width, obj.height)))
                if obj.name == 'poubelle_jaune':
                    trash[1].append((pygame.Rect(obj.x, obj.y, obj.width, obj.height)))
                if obj.name == 'poubelle_noir':
                    trash[2].append((pygame.Rect(obj.x, obj.y, obj.width, obj.height)))
                if obj.name[0:9] == 'ZONEarbre':
                    arbres.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))
                if obj.name == "dep":
                    dep.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))

        self.maps[map_name] = Map(map_name, group, mobs, tmx_data, walls, trash, arbres, dep,
                                  portails)  # enregistre la map

    def teleport(self, name):
        point = self.get_object(name)
        self.player.position[0] = point.x
        self.player.position[1] = point.y

    def get_map(self):
        return self.maps[self.default_map]  # renvoie les info stocké de la map actuelle

    def get_object(self, name):
        return self.get_map().tmx_data.get_object_by_name(name)

    def mobs_move(self):
        for mob in self.get_map().mobs:
            mob.target_find(self.player)  # permet de foncer sur la cible qui est player

    def get_group(self):
        return self.get_map().group  # récupère le group de la map

    def get_trash(self):
        return self.get_map().trash

    def update(self, lvl):
        if self.get_map().name == "bossmap" and len(self.player.inventory) == 3:
            self.get_group().remove(self.boss)
        self.get_group().update()  # update du group
        self.boss.move()
        self.collision(lvl)
        if self.player.vie == 0:
            self.theme = "principal"
            self.default_map = "main_map"
            self.teleport("spawn")
        for mob in self.get_map().mobs:
            mob.save_location()

    def restaure(self, last):
        if last >= 3:
            maps = ["map_grotte1", "map_grotte2", "map_grotte3"]
            for map in maps:
                for mob in self.maps[map].mobs:
                    self.maps[map].group.remove(mob)
                self.maps[map].mobs.clear()
            for e in range(0, 11):
                if e in [10, 9, 6]:
                    enti = entity.Entity("arbre", self.get_map().arbre[e].x - 50, self.get_map().arbre[e].y - 87, 96,
                                         192, 48, 280)
                elif e in [5, 3, 1, 8, 7]:
                    enti = entity.Entity("arbre", self.get_map().arbre[e].x - 61, self.get_map().arbre[e].y - 96, 96,
                                         192, 192, 128)
                else:
                    enti = entity.Entity("arbre", self.get_map().arbre[e].x - 40, self.get_map().arbre[e].y - 91, 96,
                                         192, 80, 128)
                self.get_group().add(enti)
        if last >= 6:
            for e in range(0, 3):
                self.get_group().add(
                    entity.Entity("decors_2", self.get_map().dep[e].x, self.get_map().dep[e].y - 10, 32, 32, 0, 96))

    def draw(self):
        self.get_group().center(self.player.rect.center)  # centre la caméra du jeu sur le joueur (son rect)
        self.get_group().draw(self.screen)  # dessine le group sur l'écran

    def blit_manager(self):
        text = str(self.score)
        text = self.font.render(text, False, (0, 0, 0))  # font mise sur le texte
        self.screen.blit(text, (self.screen.get_size()[0]/2 - (500-490), 10))
        self.touche = self.font.render(self.touche, False, (0, 0, 0))  # font mise sur le texte
        self.screen.blit(self.touche, (self.screen.get_size()[0]/2 - (500-480), self.screen.get_size()[1] - 35))
        self.discussion.display_box(self.screen)

    def collision(self, lvl):
        self.touche = ""
        pressed = pygame.key.get_pressed()
        if self.player.feet.collidelist(self.get_map().walls) > -1:  # Get collision mur
            self.player.move_back()  # Personnage retour en arriere
        for portal in self.get_map().portails:  # Recuperer portail par portail
            if portal.from_world == self.default_map:  # Si portail d'ou on viens est la map
                point = self.get_object(portal.origin_point)  # Récupère les points du rectangle du portail
                rect = pygame.Rect(point.x, point.y, point.width, point.height)  # Fais un rectangle de collision
                if self.player.feet.colliderect(rect):  # Si joueurs collision portail
                    self.default_map = portal.target_world  # Changer de monde
                    self.teleport(portal.teleport_point)  # Tp au point de spawn du monde
                    if portal.target_world == "bossmap" and round(lvl, 1) >= 6:  # Si étape du boss
                        self.theme = "boss"  # Musique de fond égale musique du boss
                        self.boss = Boss.Boss(self.get_object("spawn_boss").x - 5, self.get_object("spawn_boss").y - 5)  # Faire spawn le boss des boss
                        self.get_group().add(self.boss)  # Ajouter le boss au group déssiné
                    if portal.target_world == "main_map" and round(lvl, 1) >= 6 and portal.from_world == "bossmap":
                        self.get_group().remove(self.boss)
                    elif portal.target_world != "main_map":  # Si map visé n'est pas main_map
                        self.theme = "cave"  # Musique de fond egale à cave
                        self.player.theme = "cave"  # De même pour bruit de pas
                    else: # et sinon
                        self.theme = "principal"  # Mettre musique principal
                        self.player.theme = ""  # De même pour bruit de pas
        if self.player.feet.collidelist(self.get_map().arbre) > -1:  # Si joueur collision arbre
            self.touche = "Planter [R]"  # Texte affiché en bas de l'écran pour dire la touche
            if pressed[pygame.K_r]:  # Si R est appuyé
                index = self.player.feet.collidelist(self.get_map().arbre)  # Récuperer le position de l'arbre dans la liste
                if f"Graine{index}" in self.player.inventory:  # Si je joueur à la graine de l'arbre en question
                    if index in [10, 9, 6]:  # Si c'est arbre 10,9, ou 6
                        enti = entity.Entity("arbre", self.get_map().arbre[index].x - 50,
                                             self.get_map().arbre[index].y - 87, 96, 192, 48, 280) # Apparition de l'arbre
                    elif index in [5, 3, 1, 8, 7]:  # Si c'est arbre 5,3,1,8 ou 7
                        enti = entity.Entity("arbre", self.get_map().arbre[index].x - 61,
                                             self.get_map().arbre[index].y - 96, 96, 192, 192, 128) # Apparition de l'arbre
                    else:  # Si ce n'est pas un des autres arbres
                        enti = entity.Entity("arbre", self.get_map().arbre[index].x - 40,
                                             self.get_map().arbre[index].y - 91, 96, 192, 80, 128) # Apparition de l'arbre
                    self.score += self.point["lay_tree"]  # Ajouts des points pour arbre
                    self.sound.arbre()  # Son du placement d'arbre
                    self.sound.point()  # Son d'ajout de points
                    self.player.inventory.remove(f"Graine{index}")  # Suppr la graine de l'arbre en question
                    self.get_group().add(enti)  # Ajouter l'arbre sur la map
        if self.player.feet.collidelist(self.get_trash()[2]) > -1:
            self.touche = "Jeter [A] b"  # Texte affiché en bas de l'écran pour dire la touche
            if pressed[pygame.K_a]:  # Si A est appuyé
                self.sound.trash()  # Bruit de poubelle
                self.player.clear_inventory('black')  # vider les déchets
        if self.player.feet.collidelist(self.get_trash()[1]) > -1:
            self.touche = "Jeter [A] y"  # Texte affiché en bas de l'écran pour dire la touche
            if pressed[pygame.K_a]:  # Si A est appuyé
                self.sound.trash()  # Bruit de poubelle
                self.player.clear_inventory('yellow')  # vider les déchets
        if self.player.feet.collidelist(self.get_trash()[0]) > -1:
            self.touche = "Jeter [A] g"  # Texte affiché en bas de l'écran pour dire la touche
            if pressed[pygame.K_a]:  # Si A est appuyé
                self.sound.trash()  # Bruit de poubelle
                self.player.clear_inventory('green')  # vider les déchets
        if self.player.check:  # point si on vide les dechets
            self.score += self.point["clear_inventory"]  # Ajouts des points
            self.sound.point()  # Son des points
            self.player.check = False  # Remise sur pause
        if self.player.feet.colliderect(pygame.Rect(self.get_object("récup").x, self.get_object("récup").y, self.get_object("récup").width, self.get_object("récup").height)):
            self.touche = "Prendre [E]"  # Texte affiché en bas de l'écran pour dire la touche
            if pressed[pygame.K_e]:  # Si E est appuyé
                if lvl > 5:  # Si c'est le moment dans la partie
                    self.get_object("récup").x, self.get_object("récup").y = 50000, 50000  # Faire en sorte que le perso puisse plus récup la machine + d'une fois
                    self.player.inventory.append("dépollueur")  # Ajout de la machine à l'inventaire
                else:
                    self.discussion = discussion.Dialogue(
                        ["Attendez, il reste d'autre monstre a eliminer avant de prendre cela. Revenez plus tard !"], self.screen)
                    self.sound.spawn_robot()
                    self.discussion.execute()
        if self.player.feet.collidelist(self.get_map().dep) > -1 and self.get_map().name != "bossmap":  # Si c'est le mob moment est qu'on est collision avec un dep
            self.touche = "Poser [E]"  # Texte affiché en bas de l'écran pour dire la touche
            if pressed[pygame.K_e]:  # Si E est appuyé
                if "dépollueur" in self.player.inventory:  # Si dépollueur dans inventaire
                    index = self.player.feet.collidelist(self.get_map().dep)  # Récuperer l'index du dep
                    self.get_group().add(entity.Entity("decors_2", self.get_map().dep[index].x, self.get_map().dep[index].y - 10, 32, 32,0, 96))  # Ajouter au grp
                    self.score += self.point["lay_machine"]  # Ajouts des points
                    self.sound.point()  # Bruit de point
                    self.get_map().dep[index].x, self.get_map().dep[index].y = 300000, 30000  # Faire en sorte qu'il puisse pas en placer deux ou plus
                    self.player.inventory.remove("dépollueur")  # Remove depollueur
        for mob in self.get_map().mobs:  # Récup mob par mob
            if mob.rect.collidelist(self.get_map().walls) > -1:  # Get collision mur
                mob.move_back()  # Mob retour en arriere
            if self.player.feet.colliderect(mob):   # collison mob joueur
                self.touche = "Attaquer [Z]"  # Texte affiché en bas de l'écran pour dire la touche
                if pressed[pygame.K_z]:  # Z appuyez
                    self.player.ko += 1  # Pour le message de prévention ramassage
                    mob.monster_damage()  # dégat monstre
            if mob.rect.colliderect(self.player.rect) and mob.life > 0:  # collison mob joueur
                self.player.vie -= mob.attaque()  # dégat  du monstre
            if mob.life == 0:  # Si c'est un dechet
                if self.player.feet.colliderect(mob): # collision items joueur
                    self.touche = "Ramasser [F]"  # Texte affiché en bas de l'écran pour dire la touche
                    if pressed[pygame.K_f]:  # F appuyez
                        self.score += self.point['pickup_item']  # Ajouts des points
                        self.sound.point()  # son des points
                        self.player.add_inventory(mob.type)  # AJouts du dechet à l'inv
                        self.get_map().mobs.remove(mob)  # Suppression du mob
                        self.get_group().remove(mob)  # Suppression du mob
        if self.get_map().name == "bossmap":     # Si maps est bossmap
            if self.boss.feet.collidelist([pygame.Rect(self.get_object("Mur_boss").x, self.get_object("Mur_boss").y,
                                                       self.get_object("Mur_boss").width,
                                                       self.get_object("Mur_boss").height),
                                           pygame.Rect(self.get_object("Mur_boss0").x, self.get_object("Mur_boss0").y,
                                                       self.get_object("Mur_boss0").width,
                                                       self.get_object("Mur_boss0").height)]) > -1:  # Collision du boss
                self.boss.switch_move()
            elif self.boss.feet.collidelist([pygame.Rect(self.get_object("Mur_boss1").x, self.get_object("Mur_boss1").y,
                                                         self.get_object("Mur_boss1").width,
                                                         self.get_object("Mur_boss1").height),
                                             pygame.Rect(self.get_object("Mur_boss2").x, self.get_object("Mur_boss2").y,
                                                         self.get_object("Mur_boss2").width,
                                                         self.get_object("Mur_boss2").height)]) > -1:  # Collision du boss
                self.boss.switch_speed()
                self.boss.switch_move()
        if self.player.feet.colliderect(self.boss.rect):  # Quand le joueur est touché par le boss
            self.get_group().remove(self.boss)  # Suppression du boss
            self.default_map = "main_map"  # main_map
            self.teleport("sortie_usine")  # Tp au spawn de la map
        if self.player.feet.collidelist(self.get_map().dep) > -1 and self.get_map().name == "bossmap":
            self.touche = "Activer [S]"
            if pressed[pygame.K_s]:  # S appuyez
                self.sound.activate()  # son chargement
                index = self.player.feet.collidelist(self.get_map().dep)  # Index du dep
                self.player.inventory.append("clé pour la suite qui sais peut-être une partie deux :)")  # ajout fun inventaire
                self.get_map().dep[index].x, self.get_map().dep[index].y = 300000, 30000  # Faire en sorte qu'on puise pas deux fois le même