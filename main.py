import pygame as pg
import pygame_menu
import pygame_gui
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


def start_game():
  main_screen()

def main_screen():
  e = True
  while e:
    screen.fill((0,0,255))
    create_grid(screen, 3, 3)

    pg.display.update()
    time.sleep(1)


pg.init()

pg.font.init()
font = pg.font.Font(None, 4)

screen = pg.display.set_mode((400,500))
manager = pygame_gui.UIManager((400,500))
pg.display.set_caption("Tic-Tac-Toe Game Window")

clock = pg.time.Clock()
space_theme = pygame_menu.themes.THEME_DARK.copy()

colour_list = ['red', 'orange', 'yellow', 'green', 'blue', 'purple', 'pink']

def set_colour1(value, colour):
  print(colour)
  player1_colour = colour_list[colour-1]

def set_colour2(value, colour):
  print(colour)
  player2_colour = colour_list[colour-1]

def set_name1(name):
  player1_username = name

def set_name2(name):
  player2_username = name

def avatar_menu():
  menu._open(avatars)

menu = pygame_menu.Menu('Space Tac Toe', 400, 500,
                       theme=space_theme)

menu.add.button('Avatars', avatar_menu)
menu.add.button('Play', main_screen)

menu.add.button('Quit', pygame_menu.events.EXIT)

avatars = pygame_menu.Menu('Select an Avatar', 400, 500,
                       theme=pygame_menu.themes.THEME_BLUE)
avatars.add.text_input('Player 1: ', default='John Doe', onchange=set_name1)
avatars.add.selector('Colour: ', [('Red', 1), ('Orange', 2), ('Yellow', 3), ('Green', 4), ('Blue', 5), ('Purple', 6), ('Pink', 7)], onchange=set_colour1)

avatars.add.text_input('Player 2: ', default='Jane Smith')
avatars.add.selector('Colour: ', [('Red', 1), ('Orange', 2), ('Yellow', 3), ('Green', 4), ('Blue', 5), ('Purple', 6), ('Pink', 7)], onchange=set_colour2)


running = True
while running:
    time_delta = clock.tick(60)/1000
    events = pg.event.get()
    for event in events:
      if event.type == pg.QUIT:
          pg.quit()
          quit()
    if menu.is_enabled():
      menu.update(events)
      menu.draw(screen)
    pg.display.update()




#External Resources
"""
https://www.naukri.com/code360/library/pygame---blit-function#:~:text=The%20Pygame%20blit()%20method%20is%20one%20of%20the%20methods,in%20the%20pygame%20surface%20module.

"""