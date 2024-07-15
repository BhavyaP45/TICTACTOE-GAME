import pygame as pg
import pygame_menu
import pygame_gui
from pygame.locals import *
import pygame_menu
import time 
import os

#Initialize Pygame window
pg.init()

# Screen dimensions
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 500

# Define colours and line thickness
green =(0, 255, 0)
red = (255, 0, 0)
blue = (0, 0, 255)
orange =(252, 152, 3)
yellow = (252, 227, 3)
purple = (152, 3, 252)
pink = (252, 3, 240)
player1_colour = red
player2_colour = red
line_width = 6

# Define variables
clicked = False
player = 1
position = []
markers = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
click_counter = 0
game_over = False
winner = 0
score1_counter = 0
score2_counter = 0

# Create play again button
again_rect = Rect(SCREEN_WIDTH // 2 - 80, SCREEN_HEIGHT // 2, 160, 50)

# Define font
font = pg.font.SysFont(None, 40)

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
  
  return x_list, y_list, x_width, y_width

def draw_markers(box_side_length):
  global markers, x_list, y_list, line_width

  # Display Win counter for each player
  score_counter()

  x_pos = 0
  scale = 2 * line_width
  for x in markers:
      y_pos = 0
      for y in x:
          if y == 1:
              
              start_coord1 = (x_pos * box_side_length + 50 + scale, y_pos * box_side_length + 100 + scale)
              end_coord1 = (x_pos * box_side_length + box_side_length + 50 - scale , y_pos * box_side_length + box_side_length + 100 - scale)
              start_coord2 = (x_pos * box_side_length + 50 + scale, y_pos * box_side_length + box_side_length + 100 - scale)
              end_coord2 = (x_pos * box_side_length + box_side_length + 50 - scale , y_pos * box_side_length + 100 + scale)
              pg.draw.line(screen, player1_colour, start_coord1, end_coord1, line_width)
              pg.draw.line(screen, player1_colour, start_coord2, end_coord2, line_width)
          if y == -1:
              pg.draw.circle(screen, player2_colour, (x_pos * box_side_length + box_side_length//2 + 50, y_pos * box_side_length + box_side_length//2 + 100), box_side_length//2 - scale, line_width)
             
          y_pos += 1
      x_pos += 1

def main_screen():
  global x_list, y_list, clicked, position, markers, player, running, click_counter, game_over, winner, event, again_rect
  global score1_counter, score2_counter
  running = True
  while running:
    bg = (150, 255, 255)
    screen.fill(bg)
  
    x = (50, 350)
    y = (100, 400)
    x_list, y_list, x_width, y_width = create_grid(screen, 3, 3, x = x, y = y)

    draw_markers(x_width)

    for event in pg.event.get():
      if event.type == pg.QUIT:
          running = False
      if game_over == False:
        if event.type == pg.MOUSEBUTTONDOWN and clicked == False:
              clicked = True
        if event.type == pg.MOUSEBUTTONUP and clicked == True:
          clicked = False
          position = pg.mouse.get_pos()
          cell_x = position[0]
          cell_y = position[1]
          
          col, row = get_row_column(cell_x, cell_y)
          if col == None or row == None:
            continue

          if markers[col][row] == 0:
              markers[col][row] = player
              player *= -1
              click_counter += 1
              check_winner()
              
              # Update win counter
              if winner == 1:
                score1_counter += 1
      
              elif winner == 2:
                score2_counter += 1
                
    
    if game_over == True:
          display_winner(winner)
          
          # check to see if user plays again
          if event.type == pg.MOUSEBUTTONDOWN and clicked == False:
              clicked = True
          if event.type == pg.MOUSEBUTTONUP and clicked == True:
              clicked = False
              position = pg.mouse.get_pos()
              print(position)
              if again_rect.collidepoint(position):
                  # rest variables
                  position = []
                  player = 1
                  winner = 0
                  game_over = False
                  click_counter = 0
                  markers = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]

    pg.display.update()

def get_row_column(x, y):
  global x_list, y_list
  col, row = None, None

  for i in range(0, len(x_list) - 1):
    if x_list[i] <= x <= x_list[i + 1]:
      col = i

  for i in range(0, len(y_list) - 1):
    if y_list[i] <= y <= y_list[i + 1]:
      row = i

  return col, row

# Determine the winner (player 1 or player 2, or tie game)
def check_winner():
    global winner, game_over, click_counter

    y_pos = 0

    # Loop through each square (coordinate) in the grid
    for x in markers:
        
        # Check columns for 3 markers (X or O) in a row
        if sum(x) == 3:
            winner = 1
            game_over = True

        if sum(x) == -3:
            winner = 2
            game_over = True

        # Check rows for 3 markers in a row
        if markers[0][y_pos] + markers[1][y_pos] + markers[2][y_pos] == 3:
            winner = 1
            game_over = True

        if markers[0][y_pos] + markers[1][y_pos] + markers[2][y_pos] == -3:
            winner = 2
            game_over = True
        
        y_pos += 1

    # Check diagonals for 3 markers in a row
    if markers[0][0] + markers[1][1] + markers[2][2] == 3 or markers[2][0] + markers[1][1] + markers[0][2] == 3:
        winner = 1
        game_over = True
    elif markers[0][0] + markers[1][1] + markers[2][2] == -3 or markers[2][0] + markers[1][1] + markers[0][2] == -3:
        winner = 2
        game_over = True
    
    # Check for tie game
    if click_counter == 9 and winner == 0:
        game_over = True
      
        
# Displays the outcome of the game, and a button to play again
def display_winner(winner):
    
    # Display which player won, otherwise display "tie game"
    if winner > 0:
        win_text = "Player " + str(winner) + " wins!"
        win_img = font.render(win_text, True, blue)
        pg.draw.rect(screen, green, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 110, 200, 50))
        screen.blit(win_img, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 100))
    else:
        win_text = "Tie Game!"
        win_img = font.render(win_text, True, blue)
        pg.draw.rect(screen, green, (SCREEN_WIDTH // 2 - 70, SCREEN_HEIGHT // 2 - 110, 140, 50))
        screen.blit(win_img, (SCREEN_WIDTH // 2 - 70, SCREEN_HEIGHT // 2 - 100))

    # Play again button
    again = "Play Again?"
    again_img = font.render(again, True, blue)
    pg.draw.rect(screen, green, again_rect)
    screen.blit(again_img, (SCREEN_WIDTH // 2 - 80, SCREEN_HEIGHT // 2 + 10))
    

# Displays # of wins for each player
def score_counter():
  
  score1 = "Wins: " + str(score1_counter)
  score1_img = font.render(score1, True, blue)
  pg.draw.rect(screen, green, (40, 50, 55, 23))
  screen.blit(score1_img, (40, 50))

  score2 = "Wins: " + str(score2_counter)
  score2_img = font.render(score2, True, blue)
  pg.draw.rect(screen, green, (310, 50, 55, 23))
  screen.blit(score2_img, (310, 50))



pg.font.init()
font = pg.font.Font(None, 24)

screen = pg.display.set_mode((400,500))
manager = pygame_gui.UIManager((400,500))
pg.display.set_caption("Space Tac Toe Game")
x_list = []
y_list = []
    
clock = pg.time.Clock()
space_theme = pygame_menu.themes.THEME_DARK.copy()

colour_list = ['red', 'orange', 'yellow', 'green', 'blue', 'purple', 'pink']

def set_colour1(value, colour):
  global player1_colour
  player1_colour = colour_list[colour-1]

def set_colour2(value, colour):
  global player2_colour
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
https://www.youtube.com/watch?v=KBpfB1qQx8w 

"""