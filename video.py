import pygame
from moviepy.editor import *


class Video:
    def __init__(self, video):
        self.videos = {
            'intro': "intro.mp4",
            'evolution_1': "evolution_1.mp4"
        }
        self.clip = VideoFileClip(f'sprite_sheet/{video}.mp4')
        self.surface = pygame.Surface(self.clip.size).convert()
        self.start = pygame.time.get_ticks()
        self.clip = self.clip.set_start((pygame.time.get_ticks()/1000))

    def play_video(self, screen):
        frame = self.clip.get_frame(pygame.time.get_ticks() / 1000 - self.start/1000)
        frame_surface = pygame.surfarray.make_surface(frame.swapaxes(0, 1))
        resized_surface = pygame.transform.scale(frame_surface, (screen.get_size()[0], screen.get_size()[1]))
        self.surface.blit(resized_surface, (0, 0))
        screen.blit(self.surface, (0, 0))
