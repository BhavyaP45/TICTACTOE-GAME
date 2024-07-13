import pygame as pg
import time 
import os

#***Define Functions***
def opening_game():
  opening_image = pg.image.load(os.path.join("TICTACTOE GAME", "Images", "mario.png"))
  screen.blit(opening_image, (100, 100))
  pg.display.update()
  time.sleep(1)


#Initialize Pygame window
pg.init()

#Set the display
screen = pg.display.set_mode((400,500))
pg.display.set_caption("Tic-Tac-Toe Game Window")

running = True
while running:
    opening_game()
    event = pg.event.poll()
    if event.type == pg.QUIT:
        running=0
    screen.fill((0, 0, 255))
    pg.display.flip()




#External Resources
"""
https://www.naukri.com/code360/library/pygame---blit-function#:~:text=The%20Pygame%20blit()%20method%20is%20one%20of%20the%20methods,in%20the%20pygame%20surface%20module.

"""