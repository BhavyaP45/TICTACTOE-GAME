import pygame as pg
import time 
import os

#***Define Functions***
#A function that generates a grid based on the start and end coordinates, number of squares
def create_grid(screen, x_squares, y_squares, colour = (0, 0, 0), x = (50, 350), y = (100, 400)):
  x_width = (x[1] - x[0])/ x_squares

  for i in range(x_squares + 1):
    x_coord = x[0] + i * x_width
    pg.draw.line(screen, colour, (x_coord, y[0]), (x_coord, y[1]))

  y_width = (y[1] -y[0])/ y_squares
  for i in range(y_squares + 1):
    y_coord = y[0] + i * y_width
    pg.draw.line(screen, colour, (x[0], y_coord), (x[1], y_coord))


def main_screen():
  opening_image = pg.image.load(os.path.join("Images", "mario.png"))
  create_grid(screen, 3, 3)

  pg.display.update()
  time.sleep(1)


#Initialize Pygame window
pg.init()

#Set the display
screen = pg.display.set_mode((400,500))
pg.display.set_caption("Tic-Tac-Toe Game Window")

running = True
while running:
    main_screen()
    event = pg.event.poll()
    if event.type == pg.QUIT:
        running=0
    screen.fill((0, 0, 255))
    pg.display.flip()




#External Resources
"""
https://www.naukri.com/code360/library/pygame---blit-function#:~:text=The%20Pygame%20blit()%20method%20is%20one%20of%20the%20methods,in%20the%20pygame%20surface%20module.

"""