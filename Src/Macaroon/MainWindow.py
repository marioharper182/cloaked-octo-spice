__author__ = 'Mario'

import pygame

windowSurface = pygame.display.set_mode((500,400), 0, 32)
pygame.display.set_caption('Macaroon')

Black = (0,0,0)
White = (255, 255, 255)
Red = (200, 0, 0)
Green = (0, 212, 0)
Blue = (0, 5, 250)

class Game(object):
    def main(self, screen):
        clock = pygame.time.Clock()
        windowSurface.fill(Black)
        pygame.draw.rect(screen, (Blue), (40,40, 155, 75), 0)


        while 1:
            clock.tick(30)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    return

            #screen.fill((0, 0, 0))
            #screen.blit(image, (320, 240))
            pygame.display.flip()

if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    Game().main(screen)