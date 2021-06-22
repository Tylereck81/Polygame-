#Othello8 GUI 
#Tyler Eck 
import pygame
from copy import copy, deepcopy
import time 
import os

pygame.init()

#Screen Dimensions and Offsets 
screen_width=880
screen_height=580
squaresize = 60
y_offset = 50
x_offset = 200


#Files to Read 
#board_file="//home//ailab_server//fb_polygames//Polygames//Oth_board.txt"

board_file = "boards//Oth_board.txt"

#Player Pieces to Load 
player_piece=pygame.image.load(".//res//othello8_res//white.png") #BLACK piece
enemy_piece=pygame.image.load(".//res//othello8_res//black_piece.png") #WHITE piece 
white_moved = pygame.image.load(".//res//othello8_res//white1_moved.png")
legal_move_indicator = pygame.image.load(".//res//othello8_res//move_indicator.png") #red dot
undo = pygame.image.load(".//res//othello8_res//undo.png") #undo 
pass_button = pygame.image.load(".//res//othello8_res//pass.png")


#Transformations to Images used
white_moved = pygame.transform.scale(white_moved,(56,56))
player_piece = pygame.transform.scale(player_piece,(56,56))
enemy_piece = pygame.transform.scale(enemy_piece,(56,56))

#Colors to Use 
black = (0,0,0)
brown_index = (88,66,36) #darker color 
menu_area_color=(42,51,64)
green_square=(32,174,60)


#matrix to link moves to i,j position values 
position_letter_grid_8=[
['a8', 'b8', 'c8', 'd8', 'e8', 'f8', 'g8', 'h8'],
['a7', 'b7', 'c7', 'd7', 'e7', 'f7', 'g7', 'h7'],
['a6', 'b6', 'c6', 'd6', 'e6', 'f6', 'g6', 'h6'],
['a5', 'b5', 'c5', 'd5', 'e5', 'f5', 'g5', 'h5'],
['a4', 'b4', 'c4', 'd4', 'e4', 'f4', 'g4', 'h4'],
['a3', 'b3', 'c3', 'd3', 'e3', 'f3', 'g3', 'h3'],
['a2', 'b2', 'c2', 'd2', 'e2', 'f2', 'g2', 'h2'],
['a1', 'b1', 'c1', 'd1', 'e1', 'f1', 'g1', 'h1']
]

new_layout = [
['S', 'S', 'S', 'S', 'S', 'S', 'S', 'S'],
['S', 'S', 'S', 'S', 'S', 'S', 'S', 'S'],
['S', 'S', 'S', 'S', 'S', 'S', 'S', 'S'],
['S', 'S', 'S', 'S', 'S', 'S', 'S', 'S'],
['S', 'S', 'S', 'S', 'S', 'S', 'S', 'S'],
['S', 'S', 'S', 'S', 'S', 'S', 'S', 'S'],
['S', 'S', 'S', 'S', 'S', 'S', 'S', 'S'],
['S', 'S', 'S', 'S', 'S', 'S', 'S', 'S'],
]



#used to draw text to screen
def draw_text(text, size, color, x,y): 
    font = pygame.font.SysFont(pygame.font.get_default_font(),size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect() 
    text_rect.center = (x,y)
    screen.blit(text_surface,text_rect)

def drawboard(): 
    screen.fill(menu_area_color)
    n = 8
    l = 'A'
    #draws the backboard with indexes 
    for x  in range(1,9): 
        for y in range(1,9): 
            x1 = (squaresize * (x - 1))+x_offset-30
            y1 = (squaresize * (y - 1))+y_offset-30
            pygame.draw.rect(screen, brown_index, [x1,y1,squaresize+60, squaresize+60])
    
    for x in range(1,9): 
        for y in range(1,9):
            x1 = (squaresize * (x - 1))+x_offset-30
            y1 = (squaresize * (y - 1))+y_offset-30
            if y==1:
                draw_text(str(l),50,black,x1+60,y1+15)
                l = chr(ord(l)+1)
            if x==1:
                draw_text(str(n),55,black,x1+15,y1+60)
                n -=1

    for x in range(1, 9):
        for y in range(1, 9):
            if x!=8 and y!=8:
                pygame.draw.rect(screen, black, [(squaresize * (x - 1))+x_offset, (squaresize * (y - 1))+y_offset,
                                                                squaresize, squaresize])
                
                pygame.draw.rect(screen, green_square, [((squaresize * (x - 1))+3)+x_offset, ((squaresize * (y - 1))+3)+y_offset,
                                                                squaresize-3, squaresize-3])
            else: 
                pygame.draw.rect(screen, black, [(squaresize * (x - 1))+x_offset, (squaresize * (y - 1))+y_offset,
                                                                squaresize+3, squaresize+3])
                
                pygame.draw.rect(screen, green_square, [((squaresize * (x - 1))+3)+x_offset, ((squaresize * (y - 1))+3)+y_offset,
                                                                squaresize-3, squaresize-3])


# reads in a boardfile as a file and returns a 2 dimensional array of the board 
def read_file(boardfile):

    #gets first line number to check what board we are reading 
    with open(boardfile, 'r') as l:
        firstline = l.readline()

    if firstline == "2\n": #Othello 
        numlist=123456789
        l=[]
        l2=[]
        r1=0 #holds row count 
        c1=0 #holds col count 
        cflag = 0 
        c=0 #holds temp col count 
        with open(boardfile, 'r') as f:
            board_layout=f.read()
            FILE_SIZE = len(board_layout)
            for j in range(FILE_SIZE):
                if(board_layout[j]!='\n' and board_layout[j]=='|' and board_layout[j+1]==' ' and board_layout[j+2]==' '):
                    l2.append("S") 
                    c+=1
                elif(board_layout[j]!='\n' and board_layout[j]=='|' and board_layout[j+1]=='B' and board_layout[j+2]==' '):
                    l2.append("B") 
                    c+=1
                elif(board_layout[j]!='\n' and board_layout[j]=='|' and board_layout[j+1]=='W' and board_layout[j+2]==' '):
                    l2.append("W") 
                    c+=1
                elif(board_layout[j]!='\n' and board_layout[j]=='|' and board_layout[j+1]=='?' and board_layout[j+2]==' '):
                    l2.append("?") 
                    c+=1
                elif(board_layout[j]=='\n'): #when the end of line is reached we increment the row and append list l2 into main list l
                    if c!=0:
                        l.append(l2)
                        l2=[]
                        r1+=1
                        if cflag == 0:  #holds column count one time before resetting back to 0 
                            cflag = 1 
                            c1 = c
                            c = 0
                        else:
                            c = 0
        return l,r1,c1
    else: 
        return  0,0,0 

#acually draws image onto the board 
def drawPieces(layout_file):
    global position_list
    position_list=[]
    global Player_Piece_Count
    global Enemy_Piece_Count 
    
    #player and enemy player count
    PP = 0
    EP = 0 
    for i in range(8):
        for j in range(8):
            if layout_file[j][i]=='B':
                screen.blit(enemy_piece,(i*squaresize+3+x_offset,j*squaresize+3+y_offset))
                #position_list.append((i*squaresize+3+x_offset, j*squaresize+3+y_offset))
                EP+=1
            if layout_file[j][i]=='W':
                screen.blit(player_piece,(i*squaresize+3+x_offset,j*squaresize+3+y_offset))
                #position_list.append((i*squaresize+3+x_offset, j*squaresize+3+y_offset))
                PP+=1
            if layout_file[j][i]=='?':
                screen.blit(white_moved,(i*squaresize+3+x_offset,j*squaresize+3+y_offset))
                #position_list.append((i*squaresize+3+x_offset, j*squaresize+3+y_offset))
    
    Player_Piece_Count = PP 
    Enemy_Piece_Count = EP
    #Output the Number of Pieces
    #Option 1
    draw_text("Player Pieces",35,black,screen_width-85,screen_height/2 - 100)
    screen.blit(player_piece, (screen_width-160,screen_height/2 - 90))
    draw_text(str(PP),70,black,screen_width-70,screen_height/2 - 60)

    draw_text("Enemy Pieces",35,black,83,screen_height/2 - 100)
    screen.blit(enemy_piece, (20,screen_height/2 - 90))
    draw_text(str(EP),70,black,110,screen_height/2 - 60)

    #Undo button 
    screen.blit(undo,(screen_width-40, 10))
    position_list.append(((screen_width-40, 10)))

    #Pass Button 
    #screen.blit(pass_button,(screen_width-66, screen_height-66))
    position_list.append(((screen_width-66, screen_height-66)))


def get_moves(layout,r,c): 
    moves=[]
    for i in range(r): 
        for j in range(c): 
            if layout[i][j]=="?":
                moves.append(position_letter_grid_8[i][j])
    return moves 

def determine_position(position_x, position_y):
    x=''
    y=''
    n1 = 0 
    n2 = 1
    l = 'a'
    flag = 1
    while(flag == 1): #checks x coordinate 
        if position_x >= n1*squaresize+x_offset and position_x<=n2*squaresize+x_offset: 
            x = l; 
            flag = 0
        else: 
            n1+=1
            n2+=1
            l = chr(ord(l)+1)
        if (n2>8): 
            break

    n1 = 0 
    n2 = 1
    l = 8
    flag = 1
    while(flag == 1): #checks y coordinate 
        if position_y >= n1*squaresize+y_offset and position_y<=n2*squaresize+y_offset: 
            y = l; 
            flag = 0
        else: 
            n1+=1
            n2+=1
            l -=1
        if (n2>8): 
            break
    if x =="" or y =="": 
        x = ""
        y = ""     
    
    return x+str(y)

#check winner 
def check_game():
    if Player_Piece_Count == 0: #computer wins 
        return -1
    elif Enemy_Piece_Count == 0: #human wins
        return 1
    else: 
        if Player_Piece_Count+Enemy_Piece_Count == 64: #if the counts equal to total board size then game is done 
            if Player_Piece_Count > Enemy_Piece_Count: #whoever has most pieces on board wins 
                return 1 
            else: 
                return -1
        else: 
            return 0 


#used to update the board we made by making a move (temporary board until program reads the new board)
def update_board(layout, move):
    l = deepcopy(layout)
    r = 10 
    c = 10 

    for i in range(8): 
        for j in range(8): 
            if position_letter_grid_8[i][j] == move: 
                l[i][j] = "W"
                break
    return l


def run(): 
    global screen
    screen=pygame.display.set_mode((screen_width,screen_height))
    running = True 
    while(running):
        layout,r,c = read_file(board_file)
        while(not layout and not r and not c): 
            layout,r,c = read_file(board_file)
        old_layout= deepcopy(layout) #keeps an initial copy for comparison later

        drawboard()
        drawPieces(layout) 
        moves = get_moves(layout,r,c)
        if check_game() == 1: #Human won 
            draw_text("HUMAN WON", 130,black, screen_width/2, screen_height/2)
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    os.remove("output.txt")
                    running=False
        elif check_game() == -1: #Computer won 
            draw_text("COMPUTER WON", 130,black, screen_width/2, screen_height/2)
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    os.remove("output.txt")
                    running=False
        else: #if no winner found we continue the game
            if not moves: 
                #Pass Button
                screen.blit(pass_button,(screen_width-66, screen_height-66))

                for event in pygame.event.get():
                    if event.type==pygame.MOUSEBUTTONDOWN: 
                        x,y=pygame.mouse.get_pos()
                        position=determine_position(x,y)
                        print(position)
                        #check if they pressed the undo button
                        selection_coordinates = (0,0)
                        for px,py in position_list:
                            if (x>=px and x<=px+32) and (y>=py and y<=py+32):
                                selection_coordinates=(px,py)
                                break
                        if selection_coordinates ==(screen_width-40, 10):  #they pressed the undo button 
                            output_file=open("output.txt", "w")
                            output_file.write("u")
                            output_file.close()
                            os.remove("output.txt")
                            break 

                        #checked if they pressed the undo button 
                        selection_coordinates = (0,0)
                        for px,py in position_list:
                            if (x>=px and x<=px+64) and (y>=py and y<=py+64):
                                selection_coordinates=(px,py)
                                break
                        
                        if selection_coordinates == (screen_width-66, screen_height-66): #they pressed pass button 
                            output_file=open("output.txt", "w")
                            output_file.write("pass")
                            output_file.close()
                            os.remove("output.txt")

            else: 
                for event in pygame.event.get():
                    if event.type==pygame.QUIT:
                        output_file=open("output.txt", "w")
                        output_file.write("exit")
                        output_file.close()
                        os.remove("output.txt")
                        running=False
                    if event.type==pygame.MOUSEBUTTONDOWN: 
                        x,y=pygame.mouse.get_pos()
                        position=determine_position(x,y)
                        print(position)
                        #check if they pressed the undo button
                        selection_coordinates = (0,0)
                        for px,py in position_list:
                            if (x>=px and x<=px+32) and (y>=py and y<=py+32):
                                selection_coordinates=(px,py)
                                break
                        if selection_coordinates ==(screen_width-40, 10):  #they pressed the undo button 
                            output_file=open("output.txt", "w")
                            output_file.write("u")
                            output_file.close()
                            os.remove("output.txt")
                            break 
                        if position:
                            for move in moves: 
                                if move == position: 
                                    #Writes the move to file first 
                                    print(move)
                                    output_file=open("output.txt", "w")
                                    output_file.write(move)
                                    output_file.close()

                                    
                                    new_layout = update_board(layout, move) 
                                    #updates the board with new move made by us 
                                    layout,r,c = read_file(board_file)
                                    while True: 
                                        drawboard() 
                                        drawPieces(new_layout)
                                        pygame.display.update()
                                        layout,r,c = read_file(board_file)
                                        if layout!= old_layout:  #when the board gets updated with the move computer makes, it will break out 
                                            break

                                    break 
        pygame.display.update()