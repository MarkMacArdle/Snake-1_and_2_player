#To check what 79 chars wide looks like as per PEP8
#234567890123456789012345678901234567890123456789012345678901234567890123456789
#        1         2         3         4         5         6         7        7
#        0         0         0         0         0         0         0        9

#Known Issues and TODOs
#1 - if a fruit appears in the body of a snake another is generated straight
#    away but the yellow square stays there until the snake moves on
#2 - when players are one block long at the start they can pass through each
#    other if they don't land on the same square
#3 - The way I create the rectangles for the start and end screens could
#    do with refactoring. There's some repitition between update_score(),
#    create_text() and game_over(). And I pass a lot of the same info when
#    calling create_text() so it could be made a lot cleaner.


import pygame
from random import randint
from math import floor

import inputbox
import db_funcs

class Snake1(object):
    def __init__(self, snake_col, player_name, x_adjust=0, y_adjust=0):
        self.length = 1
        self.dir = 1 #dirs are 1, 2, 3, 4 clockwise from top
        self.new_dir = 1 #used for checking change of dir against current
        self.score = 0
        self.player_name = player_name
        self.pos_head = [(x_adjust + buff_side_unit + floor(board_sqs_across/2)) * sq_size,
                         (y_adjust + buff_top_unit + floor(board_sqs_tall/2)) * sq_size]
        self.pos_body = []
        self.pos_body.append([self.pos_head[0], self.pos_head[1]])
        self.snake_col = snake_col
        draw_block(self.pos_body[0], self.snake_col) #draw first square
        pygame.display.update()


    def check_dir_change(self):
        #check if dir changed but don't allow turning back on yourself
        #in it's own func as snake2 will use different keys to snake1
        for event in event_list:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.new_dir = 1
                elif event.key == pygame.K_RIGHT:
                    self.new_dir = 2
                elif event.key == pygame.K_DOWN:
                    self.new_dir = 3
                elif event.key == pygame.K_LEFT:
                    self.new_dir = 4


    def move_head(self):
        self.check_dir_change()
        if self.new_dir == 1 and self.dir != 3:
            self.dir = 1
        elif self.new_dir == 2 and self.dir != 4:
            self.dir = 2
        elif self.new_dir == 3 and self.dir != 1:
            self.dir = 3
        elif self.new_dir == 4 and self.dir != 2:
            self.dir = 4

        #create new head position
        #not done at same time as checking keypresses above as no keys might have been pressed.
        if self.dir == 1:
            self.pos_head[1] -= sq_size
        elif self.dir == 2:
            self.pos_head[0] += sq_size
        elif self.dir == 3:
            self.pos_head[1] += sq_size
        elif self.dir == 4:
            self.pos_head[0] -= sq_size

        #check if move in dir will cause crash
        if ((self.pos_head in self.pos_body)
                or (self.pos_head[0] < buff_side)
                or (self.pos_head[0] > (buff_side + board_w - sq_size))
                or (self.pos_head[1] < buff_top)
                or (self.pos_head[1] > (buff_top + board_h - sq_size))
               ):
            global crashed
            global crashed_snake
            crashed = True
            crashed_snake = self
            game_over_screen(self.player_name + ' loses. You crashed!')
            return

        #if no crash add new head to body and draw it
        self.pos_body.append([self.pos_head[0], self.pos_head[1]])
        draw_block(self.pos_head, self.snake_col)


    def move_tail(self):
        #cover over tail square in background color then get rid of it from the body.
        draw_block(self.pos_body[0], board_col)
        self.pos_body.pop(0)


class Snake2(Snake1):
    def __init__(self, snake_col, x_adjust=-1, y_adjust=0):
        Snake1.__init__(self, snake_col, x_adjust, y_adjust)

    def check_dir_change(self):
        #check if dir changed but don't allow turning back on yourself
        #need to overwrite Snake1 func as looking at wasd keys instead of arrows.
        for event in event_list:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    self.new_dir = 1
                elif event.key == pygame.K_d:
                    self.new_dir = 2
                elif event.key == pygame.K_s:
                    self.new_dir = 3
                elif event.key == pygame.K_a:
                    self.new_dir = 4


class Fruit(object):
    def __init__(self):
        self.color = yellow
        self.pos = []

    def create(self):
        #draw a square in a random position within the board
        self.pos = [randint(buff_side_unit, board_sqs_across)*sq_size,
                    randint(buff_top_unit, board_sqs_tall)*sq_size]
        draw_block(self.pos, self.color)

def draw_block(rect_xy, col):
    pygame.draw.rect(disp_window, col,
                     [rect_xy[0], rect_xy[1], sq_size, sq_size]) #last two args are rect width and height


def wait():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                return


def update_score(score, players):
    score_font = pygame.font.SysFont(None, 30)
    title = 'Score:{:4d}'.format(score) #have space for at least 4 characters in the score (it still display more if needed)
    if players == 1:
        title = 'P1 ' + title
    else:
        title = 'P2 ' + title
    score_text = score_font.render(title, True, scores_col, bg_col)
    score_rect = score_text.get_rect()

    if players == 1:
        score_rect.right = buff_side + board_w
    else:
        score_rect.left = buff_side
    score_rect.centery = buff_top / 2
    disp_window.blit(score_text, score_rect)


def create_text(text, centerx, centery):
    text_font= pygame.font.SysFont(None, 30) #could put in a font name instead of none if wanted to
                                              #font size of 30 is about height of a 20 pixel block.
    text_ren = text_font.render(text, True, scores_col, bg_col)
    text_rect = text_ren.get_rect()
    text_rect.centerx = centerx
    text_rect.centery = centery
    disp_window.blit(text_ren, text_rect)
    return text_rect #need to return the rect so it can be used later to check for where the mouse is clicking.


def blank_screen():
    #set up basic screen
    disp_window.fill(bg_col)
    pygame.draw.rect(disp_window, board_col, [buff_side, buff_top, board_w, board_h])
    pygame.display.update()


def game_over_screen(end_cause_text):
    create_text('Game Over!', (disp_w/2), (disp_h/2)-100)
    end_cause_rect = create_text(end_cause_text, (disp_w/2), (disp_h/2))
    pygame.display.update()


def highscores_screen(players_count):
    blank_screen()
    top100_scores = db_funcs.get_scores(db_current_table)
    x=150 #offset for start of scores

    #highscores chart title
    chart_title = str(players_count) + ' Player Highscores'
    create_text(chart_title, (disp_w/2), (disp_h/2) - (x+35))

    for i in range(min(10, len(top100_scores))): #the min() is to stop error when less than 10 scores in database
        #format string to have 8 characters followed by a space for f_ and l_name, then the score
        y = str(i+1) + '. ' + '{:<9}'.format(str(top100_scores[i][0])[:8]) + '{:<9}'.format(str(top100_scores[i][1])[:8]) + str(top100_scores[i][2])
        create_text(y, (disp_w/2), (disp_h/2) - x)
        x -= 22

    pygame.display.update()

def ending_options():
    global main_menu_rect
    global exit_rect
    main_menu_rect = create_text('Main Menu', (disp_w/2), (disp_h/2)+140)
    exit_rect = create_text('Exit', (disp_w/2), (disp_h/2)+170)
    pygame.display.update()


def homescreen():
    blank_screen()
    create_text('Welcome to Darragh Snake', disp_w/2, disp_h/2)
    #p1 and p2_rect global as checked later to see if player wants 1 or 2 player game
    global p1_rect
    global p2_rect
    p1_rect = create_text('One Player', (disp_w/2)-100, (disp_h/2)+100)
    p2_rect = create_text('Two Player', (disp_w/2)+100, (disp_h/2)+100)
    pygame.display.update()



###########
# Set up basics
###########
pygame.init() #you just have to do this with pygame as you essentially create an instance of it
clock = pygame.time.Clock() #will be used for frames per second setting
snake1_name = 'P1'
snake2_name = 'P2'

#python has no predefined colors
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
yellow = (255, 255, 0)
bg_col = blue #bg for background
board_col = black
scores_col = white

disp_w = 500
disp_h = 500
disp_window = pygame.display.set_mode((disp_w,  disp_h)) #function only accepts one argument so height and width passed as a tuple
pygame.display.set_caption('darragh snake') #window name

#set up board and block sizes
sq_size = 20 #size of the square blocks
buff_top_unit = 2
buff_bottom_unit = 1
buff_side_unit = 1
buff_top = buff_top_unit * sq_size #there'll be a two block space above the board for the scores
buff_bottom = buff_bottom_unit * sq_size
buff_side = buff_side_unit * sq_size
board_w = disp_w - 2*buff_side
board_h = disp_h - (buff_top + buff_bottom)
board_sqs_across = board_w / sq_size
board_sqs_tall = board_h / sq_size



###########
# Main loop
###########
play_again = True
while play_again:
    #set up home screen
    homescreen()

    #check if one player or two player button clicked
    loop_again = True
    while loop_again:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.MOUSEBUTTONUP and loop_again:
                pos = pygame.mouse.get_pos()
                if p1_rect.collidepoint(pos):
                    players = 1
                    db_current_table = 'one_p_scores'
                    loop_again = False
                if p2_rect.collidepoint(pos):
                    players = 2
                    db_current_table = 'two_p_scores'
                    loop_again = False
            if event.type == pygame.QUIT:
                pygame.quit()

    db_funcs.setup_DB(db_current_table)
    winner = None #used to ask name of player who's score should be added to db
    crashed_snake = None

    #cover over start screen
    pygame.draw.rect(disp_window, board_col, [buff_side, buff_top, board_w, board_h])

    if players == 1:
        snake1 = Snake1(red, snake1_name) #will start at default position of center
        update_score(0, 1)
        winner = snake1
    else:
        snake1 = Snake1(red, snake1_name, 2) #change p1's position a bit to the right of center
        update_score(0, 1)
        snake2 = Snake2(green, snake2_name, -2) #start P2 a bit to the left of center
        update_score(0, 2)

    fruit = Fruit()
    pygame.display.update()

    #############
    # Game playing loop
    #############
    wait() #wait for button press to start
    fruit.create()
    crashed = False #will break out of game loop if crashed
    while not crashed:

        event_list = [] #when events.get() is looped through the values are deleted after reading so need to make a copy.
        for event in pygame.event.get(): #pygame creates a list of all events that have happened every frame
            if event.type == pygame.QUIT: #react to user X-ing the window.
                crashed = True
            event_list.append(event)

        snake1.move_head()
        if fruit.pos in snake1.pos_body:
            snake1.score += 10
            update_score(snake1.score, 1)
            fruit.create()
        elif not crashed:
            snake1.move_tail() #delete block from tail unless a fruit was eaten or crashed

        if players == 2:
            snake2.move_head()
            if fruit.pos in snake2.pos_body:
                snake2.score += 10
                update_score(snake2.score, 2)
                fruit.create()
            elif not crashed:
                snake2.move_tail()

            #check if the snakes have crashed into each other
            if any(i in snake1.pos_body for i in snake2.pos_body): #generator expression to check if any elements match
                crashed = True
                #if there has been a collision between snakes check who crashed into who or if both crashed into each other
                #A player crashing into a wall on their own is handled seperately in that snake's class
                if snake1.pos_head == snake2.pos_head:
                    game_over_screen('You hit each other at the same time')
                elif snake1.pos_head in snake2.pos_body:
                    winner = snake2
                    game_over_screen(f'{snake1_name} loses. You crashed into {snake2_name}!')
                elif snake2.pos_head in snake1.pos_body:
                    winner = snake1
                    game_over_screen(f'{snake2_name} loses. You crashed into {snake1_name}!')

            #assign winner if one of snakes crashed on it's own
            if crashed_snake == snake1:
                winner = snake2
            elif crashed_snake == snake2:
                winner = snake1

        pygame.display.update()
        clock.tick(10) #argument is frames per second speed wanted

    if winner: #winner will be None and consquently false if it was a draw
        f_name = inputbox.ask(disp_window, f'{winner.player_name} first name')
        l_name = inputbox.ask(disp_window, 'and last name')
        db_funcs.add_score(db_current_table, f_name, l_name, winner.score)
        highscores_screen(players)
        ending_options()
    else:
        #for if it was a draw in the two player game
        ending_options()

    #check if they want to play again
    play_again = False
    loop_again = True
    while loop_again:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONUP and loop_again:
                pos = pygame.mouse.get_pos()
                if main_menu_rect.collidepoint(pos):
                    play_again = True
                    loop_again = False
                if exit_rect.collidepoint(pos):
                    loop_again = False


pygame.quit() #you have to quit pygame like the corresponding part to the .init function at the start
