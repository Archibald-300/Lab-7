import pygame
from pygame.draw import *
from random import randint
pygame.init()

FPS = 70 #shows, how often our screen will reload and show changes 

#RGB-code for color, wich was in use
green = (0, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
white = (255, 255, 255)
grey = (192, 192, 192)
#list of colors for changing colors of objects
COLORS = [RED, BLUE, YELLOW, green, MAGENTA, CYAN]

length_screen = 1100
high_screen = 600
screen = pygame.display.set_mode((length_screen, high_screen))# the name of the main surface
font = pygame.font.Font('freesansbold.ttf', 32)# very useful font for creating some writings in the game
quit_button = pygame.font.Font('freesansbold.ttf', 32)# for quit button, which will appear after the game
save_button = pygame.font.Font('freesansbold.ttf', 32)#for save result button, which will appear after the game
restart_button = pygame.font.Font('freesansbold.ttf', 32)#for save result button, which will appear after the game
#open file, where all results will be saved

#lists of coordinates for centres for circles
x_circle = []
y_circle = []

#list of radiuses of cirles
radius = []

#Vx and Vy are the x_speed and y_speed of circles (how many pixels a change of dislocation for one round conlude)
Vx_circle = []
Vy_circle = []

#lists of coordinates for left high corners for circles
x_rectangle = []
y_rectangle = []

#Length_x_rectangle is a list with widths of rectangles and length_y_rectangle is a list with highs of rectangles 
Length_x_rectangle = []
length_y_rectangle = []

#Vx and Vy are the x_speed and y_speed of circles (how many pixels a change of dislocation for one round conlude)
Vx_rectangle = []
Vy_rectangle = []

#bool list for disappearing objects 
boom_circle = []
boom_rectangles = []

number_of_circles = 3
number_of_rectangles = 2

#filling lists of parametres for balls
for i in range(number_of_circles):
    x_circle.append(randint(100, length_screen - 100))
    y_circle.append(randint(100, high_screen - 100))
    Vx_circle.append(10)
    Vy_circle.append(randint(-10, 10))
    radius.append(randint(30, 40))
    boom_circle.append(0)

#filling lists of parametres for rectangles
for i in range(number_of_rectangles):
    x_rectangle.append(randint(100, length_screen - 100))
    y_rectangle.append(high_screen - 50)
    Length_x_rectangle.append(randint(30, 50))
    length_y_rectangle.append(randint(30, 50))
    Vx_rectangle.append(randint(10, 10))
    Vy_rectangle.append(11)
    boom_rectangles.append(0)
#function that look, if click in needed area
def click_in_polygon(x_click, y_click, x_length, y_length, x_border, y_border):
    if (x_click - x_border <= x_length) and (x_click - x_border >= 0) and (y_click - y_border <= y_length) and (y_click - y_border >= 0):
        return True
#function that make new rectengle in random place after click on the rectangle
def edit_rectangle(i):
    global x_rectangle, y_rectangle, length_y_rectangle, Length_x_rectangle, Vx_rectangle, Vy_rectangle, boom_rectangle
    x_rectangle[i] = randint(100, length_screen - 100)
    y_rectangle[i] = high_screen - 50
    Length_x_rectangle[i] = randint(30, 50)
    length_y_rectangle[i] = randint(30, 50)
    Vx_rectangle[i] = randint(10, 12)
    Vy_rectangle[i] = 11
    boom_rectangles[i] = 0
#function that make rectangle move in the chosen direction
def move_rectangle(i):
    global x_rectangle, y_rectangle, Vx_rectangle, Vy_rectangle
    x_rectangle[i] += Vx_rectangle[i]
    y_rectangle[i] += Vy_rectangle[i]

#edit new circle after boom
def edit_circle(i):
    global x_rectangle, y_rectangle, radius, boom_circle, Vx_circle, Vy_circle
    x_circle[i] = randint(100, length_screen - 100)
    y_circle[i] = randint(100, high_screen - 100)
    Vx_circle[i] = randint(10, 12)
    Vy_circle[i] = randint(-10, 10)
    radius[i] = randint(30, 40)
    boom_circle[i] = 0 
#function that make circle move in the chosen direction
def move_circle(i):
    global x_circle, y_circle, Vx_circle, Vy_circle
    x_circle[i] += Vx_circle[i]
    y_circle[i] += Vy_circle[i]
#function that looks if the [X] button were clicked in the main window
def quit_condition():
    global done, event
    if event.type == pygame.QUIT:
            done = False

#this function creates circles in points according to x, y, which was set before and change these x and y
def new_ball():
    global x_circle, y_circle, radius, Vx_circle, Vy_circle, number_of_circles
    color = COLORS[randint(0, 5)]#for changing colors
    
    for i in range(number_of_circles): 
        #make balls dissapear or let them continue moving
        if boom_circle[i] == 1:
            edit_circle(i)
        else:
            move_circle(i)
        #drawing of ball number i
        circle(screen, color, (x_circle[i], y_circle[i]), radius[i])       

        #conditions of change of the circles' direction becase of borders
        if (x_circle[i] >= length_screen - 2 * radius[i]) or (x_circle[i] <= radius[i] + 10):
            Vx_circle[i] = -Vx_circle[i]
        if (y_circle[i] >= high_screen - 2 * radius[i]) or (y_circle[i] <= radius[i] + 10):
            Vy_circle[i] = -Vy_circle[i]
#function tha generate random book position
def generate_book_position():
    global book_position, time
    #book_position[0] is x coordinate and book_position[1] is y coordinate
    book_position_x_before = book_position[0]
    book_position_y_before = book_position[1]
    #condition for how often will book its position
    if time % 5 == 0:
        while book_position[0] == book_position_x_before:
            book_position[0] = randint(50, length_screen - 50)
        while book_position[1] == book_position_y_before:        
            book_position[1] = randint(80, high_screen - 80)
#function that takes information from old scoreboard and search the place for new result
def read_scorefile():
    global number_score_list, result_list
    score_file = open('scoreboard.txt', 'r')
    result_list = score_file.readlines()
  
    number_score_list = []
    for i in result_list:
        number_symbol = 1
        count = ''
        #surching for the end of the name of some record
        while i[number_symbol - 1] + i[number_symbol] != ': ':
            number_symbol += 1
        #copy this score record in one var
        for j in range(number_symbol + 1, len(i), 1):
            count += i[j]#for bringing an old result in one var
        number_score_list.append( int(count))  
        
    score_file.close()

def add_score_on_scoreboard():
    global number_score_list, result_list, name
    score_file = open('scoreboard.txt', 'w')
    number_in_scoreboard = 0
    result_in_scoreborad = 0
    boolean = False
    for i in number_score_list:
        number_in_scoreboard += 1
        #serch if score more than next result
        if (score > i) and (boolean == False):
            result_in_scoreborad = number_in_scoreboard
            boolean = True
    #addition of the new result in the right place near/between others
    result_list.insert(result_in_scoreborad - 1, name+ ': ' + str(score)+ '\n')
    #add all results in file
    for i in result_list:
        score_file.write(i)
    score_file.close()

#x,y - coordinates of the center of button
def button(font, text, x, y, color):
    textrun = font.render(text, True, green, color)
    textRect = textrun.get_rect()
    textRect.center = (x, y)
    screen.blit(textrun, textRect)

book_position = [50, 80]
length_book = 100
high_book = 160

def init_new_book():
    global book_number, scale, scale_rect
    book_number += 1
    if book_number == 10:
        book_number = 0
    #make available picture of book with number book_number  
    book_surf = pygame.image.load(book_list[book_number])
    book_rect = book_surf.get_rect(bottomright=(263, 400))
    #make image smaller
    scale = pygame.transform.scale(book_surf, (length_book, high_book))
    scale_rect = scale.get_rect(center = book_position)

#this function creates circles in points according to x, y, which was set before and also change them
def new_rectangle():
    global x_rectangle, y_rectangle, Length_x_rectangle, length_y_rectangle, Vx_rectangle, Vy_rectangle, number_of_rectangles, time
    color = COLORS[randint(0, 5)]#for changing colors
    var = 0# some var, which'll help to change rectangles' direction randomly
    for i in range(number_of_rectangles):
        #make rectangles dissapear or let them continue moving
        if boom_rectangles[i] == 1:
            edit_rectangle(i)
        else:
            move_rectangle(i)
        #drawing rectangles 
        rect(screen, color, (x_rectangle[i], y_rectangle[i], Length_x_rectangle[i], length_y_rectangle[i]))
        var = randint(1, 100)#some var for finding random moment to change direction of our rectangle
        
        #conditions of random change of direction
        if ((abs(time - var)<= 10) or (time >= 100)) and (x_rectangle[i] < length_screen - 60 - Length_x_rectangle[i]) and (x_rectangle[i] > Length_x_rectangle[i] + 15):
            time = 0
            Vx_rectangle[i] = - Vx_rectangle[i]
        
        #conditions of change of the rectangles' direction becase of borders    
        if (x_rectangle[i] >= length_screen - 10 - Length_x_rectangle[i]) or (x_rectangle[i] <= Length_x_rectangle[i] + 9):
            Vx_rectangle[i] = -Vx_rectangle[i]
        if (y_rectangle[i] >= high_screen - 50 - length_y_rectangle[i]) or (y_rectangle[i] <= high_screen - length_y_rectangle[i] + 9 ):
            Vy_rectangle[i] = -Vy_rectangle[i]

time = 20
clock = pygame.time.Clock()
time += 1
finished = False
number_of_available_clicks = 30 

quit = 'Quit'
save_res = 'Save result'
#text = font.render('Score:0', True, green, BLUE) 
book_list = ['book0.jpg', 'book1.jpg', 'book2.jpg', 'book3.jpg', 'book4.jpg', 'book5.jpg', 'book6.jpg', 'book7.jpg', 'book8.jpg', 'book9.jpg']
book_number = -1
score = 0
#textRect = text.get_rect()  
text_score = 'Score:'
number_of_score = '0'
#first window of the game
screen.fill(white)
button(font, 'Please, write your nickname,', length_screen // 2, high_screen // 2 - 60, BLUE)
button(font, 'push Enter-button afterwards', length_screen // 2, high_screen // 2 - 15, BLUE)
#add book

init_new_book()
#drawing big black line on the screen for printing name there
rect(screen, BLACK, (0, high_screen // 2 + 5, length_screen, 50) )
#make green line in the black field
button(font, '', length_screen // 2 - 5, high_screen // 2 + 30, green)
pygame.display.update()
done = True
name = ''
#reading the nickname
while done:
    for event in pygame.event.get():
            quit_condition()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    done = False
                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                    rect(screen, BLACK, (0, high_screen // 2 + 5, length_screen, 50) )
                else:
                    name += event.unicode 
            #show what was printed in the moment
            button(quit_button, name, length_screen // 2, high_screen // 2 + 30, BLACK)                
            pygame.display.update()
done = True
#counting of score
while done:
    clock.tick(FPS)
    time += 1
    #drawing of available tries table
    button(quit_button, "Available tries:" + str(number_of_available_clicks), length_screen - 140, 16, BLUE)
    for event in pygame.event.get():
        quit_condition()
        if event.type == pygame.MOUSEBUTTONDOWN:
            #minus 1 click
            number_of_available_clicks -= 1
            
            #searching if cirlcle had been reached by user
            for i in range(number_of_circles):
                if (x_circle[i] - event.pos[0]) ** 2 + (y_circle[i] - event.pos[1]) ** 2 <= radius[i] ** 2:
                    boom_circle[i] = 1
                    score += 1
                    number_of_score = str(score)
            #searching if rectangle had been reached by user
            for i in range(number_of_rectangles):
                if click_in_polygon(event.pos[0], event.pos[1], Length_x_rectangle[i], length_y_rectangle[i], x_rectangle[i], y_rectangle[i]):
                    boom_rectangles[i] = 1
                    score += 3
                    number_of_score = str(score)
            #searching if book had been reached by user
            if click_in_polygon(event.pos[0], event.pos[1], length_book, high_book, book_position[0] - 50, book_position[1] - 80):
                init_new_book()  
                score += 10
                number_of_score = str(score)
    #drawing of score table
    #conditions are for stabil drawing without "hiding" the first letter in nowhere
    if score < 10:
        button(font, text_score + number_of_score, 60, 16, BLUE)
    elif score > 99:
        button(font, text_score + number_of_score, 77, 16, BLUE)
    else:
        button(font, text_score + number_of_score, 66, 16, BLUE)
    generate_book_position()
    scale_rect = scale.get_rect(center = book_position)
    screen.blit(scale, scale_rect)
    #drawing of balls and rectangles
    new_ball()
    new_rectangle()
    pygame.display.update()
    screen.fill(BLACK)
    if number_of_available_clicks == 0:
        done = False
screen.fill(white)

#Quit button
button(quit_button, quit, length_screen // 2 - 100, high_screen // 2 - 30, BLUE)
#Save result button
button(save_button, save_res, length_screen // 2 + 90, high_screen // 2 - 30, BLUE)
done = True

#waiting for user to push buttons
while done:
    clock.tick(FPS)
    pygame.display.update()
    for event in pygame.event.get():
        quit_condition()
        if event.type == pygame.MOUSEBUTTONDOWN:
            #Quit button
            if click_in_polygon(event.pos[0], event.pos[1], 60, 30, length_screen // 2 - 135, high_screen // 2 - 45):   
                done = False
            #Save result button
            if click_in_polygon(event.pos[0], event.pos[1], 180, 30, length_screen // 2 , high_screen // 2 - 45):   
                read_scorefile()
                add_score_on_scoreboard()    
                button(save_button, 'Successfuly saved', length_screen // 2 + 10, high_screen // 2 + 30, white)
                
pygame.quit() 