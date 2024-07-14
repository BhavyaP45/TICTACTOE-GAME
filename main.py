import pygame as pg
import time 
import os

# Define colours and line thickness
green =(0, 255, 0)
red = (255, 0, 0)
line_width = 6

clicked = False
player = 1
position = []
markers = [[0]*3]*3
print(markers)

#***Define Functions***
#A function that generates a grid based on the start and end coordinates, number of squares
def create_grid(screen, x_squares, y_squares, colour = (0, 0, 0), x = (50, 350), y = (100, 400)):
  x_width = (x[1] - x[0])/ x_squares
  x_list = []
  for i in range(x_squares + 1):
    x_coord = x[0] + i * x_width
    x_list.append(x_coord)
    pg.draw.line(screen, colour, (x_coord, y[0]), (x_coord, y[1]), line_width)

  y_width = (y[1] -y[0])/ y_squares
  y_list = []
  for i in range(y_squares + 1):
    y_coord = y[0] + i * y_width
    pg.draw.line(screen, colour, (x[0], y_coord), (x[1], y_coord), line_width)
    y_list.append(y_coord)

  return x_list, y_list


def draw_markers():
  x_pos = 0

  for x in markers:
      y_pos = 0
      for y in x:
          if y == 1:
              pg.draw.line(screen, green, (x_pos * 200 + 30, y_pos * 200 + 30), (x_pos * 200 + 170, y_pos * 200 + 170), line_width)
              pg.draw.line(screen, green, (x_pos * 200 + 30, y_pos * 200 + 170), (x_pos * 200 + 170, y_pos * 200 + 30), line_width)
          if y == -1:
              pg.draw.circle(screen, red, (x_pos * 200 + 100, y_pos * 200 + 100), 80, line_width)
          y_pos += 1
      x_pos += 1

def main_screen():
  global x_list, y_list, clicked, position, markers, player
  opening_image = pg.image.load(os.path.join("Images", "mario.png"))
  bg = (150, 255, 255)
  screen.fill(bg)
 
  x = (50, 350)
  y = (100, 400)
  x_list, y_list = create_grid(screen, 3, 3, x = x, y = y)
  
  for event in pg.event.get():
      if event.type == pg.QUIT:
        running = False
  
      if event.type == pg.MOUSEBUTTONDOWN and clicked == False:
            clicked = True
      if event.type == pg.MOUSEBUTTONUP and clicked == True:
        clicked = False
        position = pg.mouse.get_pos()
        cell_x = position[0]
        cell_y = position[1]
      
        if markers[cell_x // 200][cell_y // 200] == 0:
            markers[cell_x // 200][cell_y // 200] = player
            player *= -1

  pg.display.update()
  time.sleep(1)




#Initialize Pygame window
pg.init()

#Set the display
screen = pg.display.set_mode((600,600))
pg.display.set_caption("Tic-Tac-Toe Game Window")
x_list = []
y_list = []



running = True
while running:
    main_screen()
    draw_markers()





#External Resources
"""
https://www.naukri.com/code360/library/pygame---blit-function#:~:text=The%20Pygame%20blit()%20method%20is%20one%20of%20the%20methods,in%20the%20pygame%20surface%20module.

"""