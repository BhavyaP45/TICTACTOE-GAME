# Import libraries
import pygame as pg
import pygame_menu
import pygame_gui
from pygame.locals import *
import pygame_menu
import time 
import os
import json
from datetime import datetime, timezone

#Initialize Pygame window
pg.init()

# Screen dimensions
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600

# counter 
trigger_counter = 0

# set up usernames
player1_username = 'Player 1'
player2_username = 'Player 2'
winner_username = ''
loser_username = ''
raw_player1_colour = 'red'
raw_player2_colour = 'red'

# utility function to read json files
def read_json_file(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

# utility function to add on entries json files
def append_entry(file_path, new_entry):
    # Read the existing data
    data = read_json_file(file_path)
    # Append the new entry
    data.append(new_entry)
    # Write the updated data back to the JSON file
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

def get_winner_username():
    global player1_username, player2_username, winner, winner_username
    if winner == 1:
        winner_username = player1_username
    elif winner == 2:
        winner_username = player2_username
    else:
        winner_username = 'Tie Game'

    return winner_username

def update_gamelog():
    global player1_username, player2_username, winner, winner_username, loser_username
    # New entry to append
    new_entry = {
        "timestamp": datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),
        "winner": player1_username if winner == 1 else player2_username, 
    }

    # Path to the JSON file
    file_path = 'gamelog.json'

    # Append the new entry
    append_entry(file_path, new_entry)

# Define colours and line thickness
green =(0, 0, 0)
red = (255, 0, 0)
white = (255, 255, 255)
blue = (0, 0, 255)
orange =(252, 152, 3)
yellow = (252, 227, 3)
purple = (152, 3, 252)
pink = (252, 3, 240)
line_width = 6

#Default colours for the players
player1_colour = red
player2_colour = red

# Define global variables
clicked = False
player = 1
position = []
markers = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
click_counter = 0
game_over = False
winner = 0
score1_counter = 0
score2_counter = 0



# Define font
font = pg.font.SysFont(None, 40)

#***Define Functions***

#A function that generates a grid based on the start and end coordinates, number of squares
# Inputs: Screen, number of squares in the x and y directions, colour, start and end coordinates in the x and y directions
# Outputs: list of x_coordinates, list of y_coordinates, width and height of boxes
def create_grid(screen, x_squares, y_squares, colour = (255, 255, 255), x = (50, 350), y = (100, 400)):
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
  global markers, x_list, y_list, line_width, player1_colour, player2_colour

  # Display Win counter for each player
  score_counter()

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
              start_coord1 = (x_pos * box_side_length + 50 + scale, y_pos * box_side_length + 150+ scale)
              end_coord1 = (x_pos * box_side_length + box_side_length + 50 - scale , y_pos * box_side_length + box_side_length + 150- scale)
              start_coord2 = (x_pos * box_side_length + 50 + scale, y_pos * box_side_length + box_side_length + 150- scale)
              end_coord2 = (x_pos * box_side_length + box_side_length + 50 - scale , y_pos * box_side_length + 150+ scale)
              #Draw the lines on the screen
              pg.draw.line(screen, player1_colour, start_coord1, end_coord1, line_width)
              pg.draw.line(screen, player1_colour, start_coord2, end_coord2, line_width)
          #-1 is used in the marker list to indicate an O
          if y == -1:
              #Draw circle on board
              pg.draw.circle(screen, player2_colour, (x_pos * box_side_length + box_side_length//2 + 50, y_pos * box_side_length + box_side_length//2 + 150), box_side_length//2 - scale, line_width)
      #Increment both counters  
          y_pos += 1
      x_pos += 1

# Possible colours to choose from 
colour_list = ['red', 'orange', 'yellow', 'green', 'blue', 'purple', 'pink']
redav = pg.image.load('Images/RedAvatar.png')
orangeav = pg.image.load('Images/OrangeAvatar.png')
yellowav = pg.image.load('Images/YellowAvatar.png')
greenav = pg.image.load('Images/GreenAvatar.png')
blueav = pg.image.load('Images/BlueAvatar.png')
purpleav = pg.image.load('Images/PurpleAvatar.png')
pinkav = pg.image.load('Images/PinkAvatar.png')

avatar_list = [redav, orangeav, yellowav, greenav, blueav, purpleav, pinkav]

for avatar in avatar_list:
  avatar = pg.transform.scale(avatar, (200, 200))

avatar1 = avatar_list[0]       
avatar2 = avatar_list[0]

# Set colours and avatars based on menu input
def set_colour1(value, colour):
    global player1_colour, avatar1, raw_player1_colour
    player1_colour = colour_list[colour-1]
    avatar1 = avatar_list[colour-1]
    raw_player1_colour = colour_list[colour-1]

def set_colour2(value, colour):
    global player2_colour, avatar2, raw_player2_colour
    player2_colour = colour_list[colour-1]
    avatar2 = avatar_list[colour-1]
    raw_player2_colour = colour_list[colour-1]

#A function that loops through the main screen in the program 
def main_screen():
  #Access all the global variables
  global x_list, y_list, clicked, position, markers, player, running, click_counter, game_over, winner, event, again_rect
  global score1_counter, score2_counter, avatar1, avatar2

  #Initialize boolean that will continue running until the program is quit
  running = True
  while running:
    #Background for the screen
    bg = pg.image.load("Images/bg.png")
    screen.blit(bg, (0, 0))

    #Initialize start and end coordinates for the grid
    x = (50, 350)
    y = (150, 450)

    x_list, y_list, x_width, y_width = create_grid(screen, 3, 3, x = x, y = y)

    # image = pygame.image.load('your_image.png')
    new_size = (75, 75)
    avatar1 = pg.transform.scale(avatar1, new_size)
    avatar2 = pg.transform.scale(avatar2, new_size)
    # screen.blit(scaled_image, (50, 50))

    screen.blit(avatar1, (90, 60))
    screen.blit(avatar2, (230, 60))

    
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
              
              # Update win counter
              if winner == 1:
                score1_counter += 1
      
              elif winner == 2:
                score2_counter += 1
                
    
    
    #If the game is finished, display the winner
    if game_over == True:
          global trigger_counter
          if trigger_counter == 0:
            update_gamelog()
            fetchGameLog()
            trigger_counter += 1

          display_winner(winner)
          


    #Update the display
    pg.display.update()

#Get the row and column in the grid based on user coordinates
#Inputs: x and y coordinates
#Outputs: Row and column numbers (0 indexing)
def gameReset():
  global x_list, y_list, clicked, position, markers, player, running, click_counter, game_over, winner, event, trigger_counter
  trigger_counter = 0
  position = []
  player = 1
  winner = 0
  game_over = False
  click_counter = 0
  markers = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]

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

def fetchGameLog():
  with open('gamelog.json', 'r') as file:
    game_log_data = json.load(file)
    for entry in game_log_data:
      timestampData = entry['timestamp']
      winner = entry['winner']
      game_log.add.label(f"Winner: {winner} - {timestampData}", font_size=10)

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
  global end_menu, SCREEN_HEIGHT
  
  winner_username = get_winner_username()

  if winner == 1:
      winner_username = player1_username
      win_text = "" + str(player1_username) + " wins!"

  elif winner == 2:
      winner_username = player2_username
      win_text = "" + str(winner_username) + " wins!"
      
  else:
      win_text = "Tie Game!"
  
    
  # update_leaderboard()
  win_img = font.render(win_text, True, blue)
  
  # pygame_menu.events.RESET

  # menu._open(end_menu)
  gameReset()
  end_menu = pygame_menu.Menu('GAME OVER', 400, SCREEN_HEIGHT,
                theme=space_theme)
  end_menu.add.label(win_text, font_size=24)
  end_menu.add.button('Change Avatars', avatar_endmenu)
  end_menu.add.button('Game Log', game_log_endmenu)
  end_menu.add.button('Play Again!', main_screen)
  end_menu.add.button('Quit', pygame_menu.events.EXIT)
  end_menu.mainloop(screen)

# Displays # of wins for each player
def score_counter():
  p1_img = fontM.render(player1_username, True, white)
  p2_img = fontM.render(player2_username, True, white)
  screen.blit(p1_img, (30, 40))
  screen.blit(p2_img, (230, 40))

  score1 = "Wins: " + str(score1_counter)
  score1_img = font.render(score1, True, white)

  screen.blit(score1_img, (40, 90))

  score2 = "Wins: " + str(score2_counter)
  score2_img = font.render(score2, True, white)

  screen.blit(score2_img, (300, 90))

  currentTurn = (str(player1_username) + "'s turn " if player == 1 else str(player2_username) + "'s turn ")
  currentTurn_img = fontXL.render(currentTurn, True, white)

  screen.blit(currentTurn_img, (65, 500))



pg.font.init()
font = pg.font.Font(None, 24)
fontM = pg.font.Font(None, 40)
fontXL = pg.font.Font(None, 50)

screen = pg.display.set_mode((400, SCREEN_HEIGHT))
manager = pygame_gui.UIManager((400, SCREEN_HEIGHT))
pg.display.set_caption("Space Tac Toe")
x_list = []
y_list = []
    
clock = pg.time.Clock()

# Initializing the theme of the menu
space_theme = pygame_menu.themes.THEME_DARK.copy()

# Set usernames based on menu input
def set_name1(name):
  global player1_username
  player1_username = name[:10]

def set_name2(name):
  global player2_username
  player2_username = name[:10]

# Opening the "Avatar Selection" tab from the menu
def avatar_menu():
  menu._open(avatars)

# Creating the game_log_menu
def game_log_endmenu():
  global end_menu
  end_menu._open(game_log)

def avatar_endmenu():
  global end_menu
  end_menu._open(avatars)

game_log = pygame_menu.Menu('GAME LOG', 400, SCREEN_HEIGHT,
            theme=space_theme)
game_log.add.label("Past Games:", font_size=24)
# Create a scrollable area
if game_over == True:
   fetchGameLog()

# Add some dummy data to the scrollable area
# for i in range(1, 21):
#     scroll_area.add.label(f"Game {i}: Player X won", font_size=20)



menu = pygame_menu.Menu('Space Tac Toe', 400, SCREEN_HEIGHT,
                       theme=space_theme)

# Menu buttons

menu.add.button('Avatars', avatar_menu)
menu.add.button('Play', main_screen)
menu.add.button('Quit', pygame_menu.events.EXIT)
menu.add.image("Images/earth.png", scale = (0.5, 0.5))
# Creating the "Avatar Selection" menu and its inputs
avatars = pygame_menu.Menu('Select an Avatar', 400, SCREEN_HEIGHT, theme=pygame_menu.themes.THEME_DARK)
avatars.add.text_input('Player 1: ', default='John Doe', onchange=set_name1)
avatars.add.selector('Colour: ', [('Red', 1), ('Orange', 2), ('Yellow', 3), ('Green', 4), ('Blue', 5), ('Purple', 6), ('Pink', 7)], onchange=set_colour1)
avatars.add.text_input('Player 2: ', default='Jane Smith', onchange=set_name2)
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