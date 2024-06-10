'''
notes:

using pygame to print screen and stuff
https://www.pygame.org/wiki/

tutorial: https://www.youtube.com/watch?v=FfWpgLFMI7w&t=1s




'''

import pygame
import time


pygame.init()

#create screen

screen = pygame.display.set_mode((800,600))



#Title and Icon
pygame.display.set_caption("Chess by Yorgo")



# Game Loop


#section of code that will quit pygame when the X button is pressed
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


