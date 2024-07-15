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

#Default colours for the players
player1_colour = red
player2_colour = green
line_width = 6

# Define global variables
clicked = False
player = 1
position = []
markers = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
click_counter = 0
game_over = False
winner = 0

# Create play again button
again_rect = Rect(SCREEN_WIDTH // 2 - 80, SCREEN_HEIGHT // 2, 160, 50)

# Define font
font = pg.font.SysFont(None, 40)

#***Define Functions***

#A function that generates a grid based on the start and end coordinates, number of squares
# Inputs: Screen, number of squares in the x and y directions, colour, start and end coordinates in the x and y directions
# Outputs: list of x_coordinates, list of y_coordinates, width and height of boxes
def create_grid(screen, x_squares, y_squares, colour = (0, 0, 0), x = (50, 350), y = (100, 400)):
  #Calculate width of each box
  x_width = (x[1] - x[0])/ x_squares
  #Initialize x list
  x_list = []
  #Add the coordinates for the vertical lines to the x list, and draw the line on the screen
  for i in range(x_squares + 1):
    x_coord = x[0] + i * x_width
    x_list.append(x_coord)
    pg.draw.line(screen, colour, (x_coord, y[0]), (x_coord, y[1]), line_width)

  #Do the same process for the y-values
  y_width = (y[1] -y[0])/ y_squares
  y_list = []
  for i in range(y_squares + 1):
    y_coord = y[0] + i * y_width
    pg.draw.line(screen, colour, (x[0], y_coord), (x[1], y_coord), line_width)
    y_list.append(y_coord)

  return x_list, y_list, x_width, y_width

#A function that reads the markers list and draws corresponding markers (X or O)
#Inputs: Side lengths of each box
def draw_markers(box_side_length):
  global markers, x_list, y_list, line_width

  #Create a counter that will be used to translate the markers accordingly
  x_pos = 0
  #A scale value that will leave some margin between the box and the marker
  scale = 2 * line_width

  #Loop through the various rows and columns in the 2d Array
  for x in markers:
      y_pos = 0
      for y in x:
          #1 is used in the marker list to indicate an X
          if y == 1:
              #Create start and end coordinates for both diagonal lines in an x
              start_coord1 = (x_pos * box_side_length + 50 + scale, y_pos * box_side_length + 100 + scale)
              end_coord1 = (x_pos * box_side_length + box_side_length + 50 - scale , y_pos * box_side_length + box_side_length + 100 - scale)
              start_coord2 = (x_pos * box_side_length + 50 + scale, y_pos * box_side_length + box_side_length + 100 - scale)
              end_coord2 = (x_pos * box_side_length + box_side_length + 50 - scale , y_pos * box_side_length + 100 + scale)
              #Draw the lines on the screen
              pg.draw.line(screen, player1_colour, start_coord1, end_coord1, line_width)
              pg.draw.line(screen, player1_colour, start_coord2, end_coord2, line_width)
          #-1 is used in the marker list to indicate an O
          if y == -1:
              #Draw circle on board
              pg.draw.circle(screen, player2_colour, (x_pos * box_side_length + box_side_length//2 + 50, y_pos * box_side_length + box_side_length//2 + 100), box_side_length//2 - scale, line_width)
      #Increment both counters  
          y_pos += 1
      x_pos += 1

#A function that loops through the main screen in the program 
def main_screen():
  #Access all the global variables
  global x_list, y_list, clicked, position, markers, player, running, click_counter, game_over, winner, event, again_rect

  #Initialize boolean that will continue running until the program is quit
  running = True
  while running:
    #Background for the screen
    bg = (150, 255, 255)
    screen.fill(bg)

    #Initialize start and end coordinates for the grid
    x = (50, 350)
    y = (100, 400)

    x_list, y_list, x_width, y_width = create_grid(screen, 3, 3, x = x, y = y)

    #Draw the markers based on the list 
    draw_markers(x_width)

    #Iterate through all the events in Pygame
    for event in pg.event.get():
      #Quit loop if x is clicked
      if event.type == pg.QUIT:
          running = False
          continue
      
      #Check if the game is still continuing
      if game_over == False:
        #Check if user clicked mousebutton down and up
        if event.type == pg.MOUSEBUTTONDOWN and clicked == False:
              clicked = True
        if event.type == pg.MOUSEBUTTONUP and clicked == True:
          clicked = False
          #Get the mouse position and store it in two variables
          position = pg.mouse.get_pos()
          cell_x = position[0]
          cell_y = position[1]
          
          #Call get_row_column function
          col, row = get_row_column(cell_x, cell_y)

          #If the pointer was clicked outside of the grid, continue to next iteration
          if col == None or row == None:
            continue
          
          #0 indicates an unmarked square. If the user clicks on one, add their respective marker
          if markers[col][row] == 0:
              markers[col][row] = player
              player *= -1
              click_counter += 1
              #Call function check_winner
              check_winner()
    
    #If the game is finished, display the winner
    if game_over == True:
          display_winner(winner)
          # check to see if user plays again
          if event.type == pg.MOUSEBUTTONDOWN and clicked == False:
              clicked = True
          if event.type == pg.MOUSEBUTTONUP and clicked == True:
              clicked = False
              position = pg.mouse.get_pos()
              if again_rect.collidepoint(position):
                  # rest variables
                  position = []
                  player = 1
                  winner = 0
                  game_over = False
                  click_counter = 0
                  markers = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]

    #Update the display
    pg.display.update()

#Get the row and column in the grid based on user coordinates
#Inputs: x and y coordinates
#Outputs: Row and column numbers (0 indexing)
def get_row_column(x, y):
  global x_list, y_list
  #Initialize row and column as none
  col, row = None, None

  #Iterate through the x_list, setting lower and upper bounds for the coordinates
  for i in range(0, len(x_list) - 1):
    if x_list[i] <= x <= x_list[i + 1]:
      col = i

  #Iterate through the y_list, setting lower and upper bounds for the coordinates
  for i in range(0, len(y_list) - 1):
    if y_list[i] <= y <= y_list[i + 1]:
      row = i

  return col, row

def check_winner():
    global winner, game_over, click_counter

    y_pos = 0
    for x in markers:
        # check columns
        if sum(x) == 3:
            winner = 1
            game_over = True

        if sum(x) == -3:
            winner = 2
            game_over = True

        # check rows
        if markers[0][y_pos] + markers[1][y_pos] + markers[2][y_pos] == 3:
            winner = 1
            game_over = True

        if markers[0][y_pos] + markers[1][y_pos] + markers[2][y_pos] == -3:
            winner = 2
            game_over = True
        
        y_pos += 1

    # check cross
    if markers[0][0] + markers[1][1] + markers[2][2] == 3 or markers[2][0] + markers[1][1] + markers[0][2] == 3:
        winner = 1
        game_over = True
    elif markers[0][0] + markers[1][1] + markers[2][2] == -3 or markers[2][0] + markers[1][1] + markers[0][2] == -3:
        winner = 2
        game_over = True
    
    # check tie
    if click_counter == 9 and winner == 0:
        game_over = True
        

def display_winner(winner):
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

    again = "Play Again?"
    again_img = font.render(again, True, blue)
    pg.draw.rect(screen, green, again_rect)
    screen.blit(again_img, (SCREEN_WIDTH // 2 - 80, SCREEN_HEIGHT // 2 + 10))


screen = pg.display.set_mode((400,500))
manager = pygame_gui.UIManager((400,500))
pg.display.set_caption("Space Tac Toe Game")
x_list = []
y_list = []
    
clock = pg.time.Clock()

# Initializing the theme of the menu
space_theme = pygame_menu.themes.THEME_DARK.copy()

# Possible colours to choose from 
colour_list = ['red', 'orange', 'yellow', 'green', 'blue', 'purple', 'pink']

# Set colours based on menu input
def set_colour1(value, colour):
  global player1_colour
  player1_colour = colour_list[colour-1]

def set_colour2(value, colour):
  global player2_colour
  player2_colour = colour_list[colour-1]

# Set usernames based on menu input
def set_name1(name):
  player1_username = name

def set_name2(name):
  player2_username = name

# Opening the "Avatar Selection" tab from the menu
def avatar_menu():
  menu._open(avatars)

# Creating the main menu
menu = pygame_menu.Menu('Space Tac Toe', 400, 500,
                       theme=space_theme)

# Menu buttons
menu.add.button('Avatars', avatar_menu)
menu.add.button('Play', main_screen)
menu.add.button('Quit', pygame_menu.events.EXIT)

# Creating the "Avatar Selection" menu and its inputs
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
    # Causes game to quit when necessary
    for event in events:
      if event.type == pg.QUIT:
          pg.quit()
          quit()
    # Menu appears if it is enabled
    if menu.is_enabled():
      menu.update(events)
      menu.draw(screen)
    pg.display.update()


#External Resources
"""
https://www.naukri.com/code360/library/pygame---blit-function#:~:text=The%20Pygame%20blit()%20method%20is%20one%20of%20the%20methods,in%20the%20pygame%20surface%20module.
https://www.youtube.com/watch?v=KBpfB1qQx8w 

"""