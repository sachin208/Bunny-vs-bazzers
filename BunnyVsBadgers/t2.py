import sys
import pygame
from pygame.locals import *
pygame.init()

size = width, height = 720, 480
speed = [2, 2]
black = (0,0,0)
blue = (0,0,255)
green = (0,255,0)
red = (255,0,0)

screen = pygame.display.set_mode(size)

pygame.display.set_caption("BETA::00.0.1")

clock = pygame.time.Clock()


def text_objects(text, font):
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()

def game_intro():

  screen.fill(blue)

  largeText = pygame.font.Font('freesansbold.ttf',115)
  TextSurf, TextRect = text_objects("BETA", largeText)
  TextRect.center = ((width/2),(height/2))
  screen.blit(TextSurf, TextRect)

  pygame.draw.rect(screen, green,(150,450,100,50))
  pygame.draw.rect(screen, red,(550,450,100,50))

  pygame.display.flip()
  pygame.display.update()
  clock.tick(15)

  intro = True

  while intro:
     for event in pygame.event.get():
         print(event)
         if event.type == pygame.QUIT:
             pygame.quit()
             quit()


game_intro()