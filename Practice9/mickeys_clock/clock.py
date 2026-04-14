import pygame
import datetime

class MickeyClock:
    def __init__(self, image):
        self.hand = pygame.transform.scale(image, (150, 30))

    def draw(self, screen, center):
        now = datetime.datetime.now()

        minutes = now.minute
        seconds = now.second

        min_angle = -minutes * 6
        sec_angle = -seconds * 6

        min_hand = pygame.transform.rotate(self.hand, min_angle)
        sec_hand = pygame.transform.rotate(self.hand, sec_angle)

        screen.blit(min_hand, min_hand.get_rect(center=center))
        screen.blit(sec_hand, sec_hand.get_rect(center=center))