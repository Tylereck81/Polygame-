#Breakthrough GUI 
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
#board_file="//home//ailab_server//fb_polygames//Polygames//BT_board.txt"
#moves_file="//home//ailab_server//fb_polygames//Polygames//moves_list.txt"

board_file = "boards//BT_board.txt"
moves_file = "moves//breakthrough_moves.txt"

#Player Pieces to Load 
player_piece=pygame.image.load(".//res//breakthrough_res//black_piece1.png") #BLACK piece
enemy_piece=pygame.image.load(".//res//breakthrough_res//white_piece1.png") #WHITE piece 
black_moved = pygame.image.load(".//res//breakthrough_res//black_moved.png") #black moved piece 
white_moved = pygame.image.load(".//res//breakthrough_res//white_moved.png") #white moved piece
legal_move_indicator = pygame.image.load(".//res//breakthrough_res//move_indicator.png") #red dot
selection=pygame.image.load(".//res//breakthrough_res//selection.png") #red border 
undo = pygame.image.load(".//res//breakthrough_res//undo.png") #undo 
arrow = pygame.image.load(".//res//breakthrough_res//arrow.png") #arrow


#Transformations to Images used
white_moved = pygame.transform.scale(white_moved,(56,56))
black_moved = pygame.transform.scale(black_moved,(56,56))
player_piece = pygame.transform.scale(player_piece,(56,56))
enemy_piece = pygame.transform.scale(enemy_piece,(56,56))
W_arrow_left = pygame.transform.rotate(arrow,135)
W_arrow_middle = pygame.transform.rotate(arrow,90)
W_arrow_right = pygame.transform.rotate(arrow,45)

B_arrow_left = pygame.transform.rotate(arrow,-135)
B_arrow_middle = pygame.transform.rotate(arrow,-90)
B_arrow_right = pygame.transform.rotate(arrow,-45)


#Colors to Use 
black = (0,0,0)
white =(255,255,255)
black_square=(193,154,107)
white_square=(242, 222, 199)
brown_index =  (155,130,96) #normal 
menu_area_color=(42,51,64)


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

prev_board = [
['@', '@', '@', '@', '@', '@', '@', '@'],
['@', '@', '@', '@', '@', '@', '@', '@'],
['+', '+', '+', '+', '+', '+', '+', '+'],
['+', '+', '+', '+', '+', '+', '+', '+'],
['+', '+', '+', '+', '+', '+', '+', '+'],
['+', '+', '+', '+', '+', '+', '+', '+'],
['O', 'O', 'O', 'O', 'O', 'O', 'O', 'O'],
['O', 'O', 'O', 'O', 'O', 'O', 'O', 'O']
]

#used to draw text to screen
def draw_text(text, size, color, x,y): 
    font = pygame.font.SysFont(pygame.font.get_default_font(),size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect() 
    text_rect.center = (x,y)
    screen.blit(text_surface,text_rect)

#draws the board 
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

    #draws the main board 
    flag = 0
    for x in range(1, 9):
        if x%2 == 1: 
            flag = 0
        else: 
            flag = 1
        for y in range(1, 9):
            if x!=8 and y!=8:
                if flag == 0:
                    pygame.draw.rect(screen, black, [(squaresize * (x - 1))+x_offset, (squaresize * (y - 1))+y_offset,
                                                                    squaresize, squaresize])
                    pygame.draw.rect(screen, white_square, [squaresize * (x - 1)+3+x_offset, squaresize * (y - 1)+3+y_offset,
                                                                squaresize-3, squaresize-3])
                    flag = 1
                else: 
                    pygame.draw.rect(screen, black, [(squaresize * (x - 1))+x_offset, (squaresize * (y - 1))+y_offset,
                                                                    squaresize, squaresize])
                    pygame.draw.rect(screen, black_square, [squaresize * (x - 1)+3+x_offset, squaresize * (y - 1)+3+y_offset,
                                                                squaresize-3, squaresize-3])
                    flag = 0
            else: 
                if flag == 0:
                    pygame.draw.rect(screen, black, [(squaresize * (x - 1))+x_offset, (squaresize * (y - 1))+y_offset,
                                                                    squaresize+3, squaresize+3])
                    pygame.draw.rect(screen, white_square, [squaresize * (x - 1)+3+x_offset, squaresize * (y - 1)+3+y_offset,
                                                                squaresize-3, squaresize-3])
                    flag = 1
                else: 
                    pygame.draw.rect(screen, black, [(squaresize * (x - 1))+x_offset, (squaresize * (y - 1))+y_offset,
                                                                    squaresize+3, squaresize+3])
                    pygame.draw.rect(screen, black_square, [squaresize * (x - 1)+3+x_offset, squaresize * (y - 1)+3+y_offset,
                                                                squaresize-3, squaresize-3])
                    flag = 0


# reads in a boardfile as a file and returns a 2 dimensional array of the board 
def read_file(boardfile):

    #gets first line number to check what board we are reading 
    with open(boardfile, 'r') as l:
        firstline = l.readline()
  
    if firstline == "3\n": #Breakthrough 
        numlist=123456789
        alist = "qwertyuipasdfghjklzxcvnmb" #without "O" for breakthrough
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
                if(board_layout[j]!=' ' and board_layout[j]!='\n' and board_layout[j] not in str(numlist) and board_layout[j] not in str(alist) and board_layout[j] not in str(alist).upper()):
                    l2.append(board_layout[j]) 
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


#acually draws image onto the board 
def drawPieces(layout_file):
    global position_list
    position_list=[]
    global position_list_enemy
    position_list_enemy=[]
    
    #player and enemy player count
    PP = 0
    EP = 0 
    for i in range(8):
        for j in range(8):
            if layout_file[j][i]=='@':
                screen.blit(player_piece,(i*squaresize+3+x_offset,j*squaresize+3+y_offset))
                position_list.append((i*squaresize+3+x_offset, j*squaresize+3+y_offset))
                PP+=1
            if layout_file[j][i]=='O':
                screen.blit(enemy_piece,(i*squaresize+3+x_offset,j*squaresize+3+y_offset))
                position_list_enemy.append((i*squaresize+3+x_offset, j*squaresize+3+y_offset))
                EP+=1
    #Option 1
    draw_text("Player Pieces",35,black,screen_width-85,screen_height/2 - 100)
    screen.blit(player_piece, (screen_width-160,screen_height/2 - 90))
    draw_text(str(PP),70,black,screen_width-70,screen_height/2 - 60)

    draw_text("Enemy Pieces",35,black,83,screen_height/2 - 100)
    screen.blit(enemy_piece, (20,screen_height/2 - 90))
    draw_text(str(EP),70,black,110,screen_height/2 - 60)


    screen.blit(undo,(screen_width-40, 10))
    position_list.append(((screen_width-40, 10)))

    #Option 2
    # draw_text("Player Pieces",35,black,screen_width-85,screen_height/2 - 100)
    # screen.blit(player_piece, (screen_width-110,screen_height/2 - 90))
    # draw_text(str(PP),50,white,screen_width-83,screen_height/2 - 60)

    # draw_text("Enemy Pieces",35,black,83,screen_height/2 - 100)
    # screen.blit(enemy_piece, (50,screen_height/2 - 90))
    # draw_text(str(PP),50,black,77,screen_height/2 - 60)


#Reads the move_file and extracts the moves 
def get_moves(): 
    moves=[]
    with open (moves_file, 'r') as m:
        moves=m.read().split()
    return moves

#checks to see if the x and y values of the click has a enemy piece or player piece 
def isPiecePresent(player,x,y):
    if player == 1: 
        selection_coordinates = (0,0)
        for px,py in position_list:
            if (x>=px and x<=px+squaresize) and (y>=py and y<=py+squaresize):
                selection_coordinates=(px,py)
                break
        return selection_coordinates
    else: 
        selection_coordinates = (0,0)
        for px,py in position_list_enemy:
            if (x>=px and x<px+squaresize) and (y>=py and y<py+squaresize):
                selection_coordinates=(px,py)
                break
        return selection_coordinates



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

#moves list translated physically into dots on board to indicate where the specified piece can move 
def print_moves(letter_co, m_list):
    legal_moves=[] 
    for moves in m_list:
        if letter_co==moves[0:2]:
            legal_moves.append(moves[2:])
    
    #prints out those legal_moves onto board 
    for legal_move in legal_moves:
        x=-1
        y=-1
        for i in range(8):
            for j in range(8):
                if legal_move == position_letter_grid_8[i][j]:
                    x=i
                    y=j
        if x!=-1 and y!=-1:
            p = isPiecePresent(0,y*squaresize+x_offset+3,x*squaresize+y_offset+3)
            if p!=(0,0): #means eating occurs so we output a red dot
                screen.blit(legal_move_indicator,p)
            else:  
            #Option 1: 
                screen.blit(black_moved, (y*squaresize+x_offset+3,x*squaresize+y_offset+3))
            #Option 2: 
            #screen.blit(legal_move_indicator, (y*squaresize+x_offset,x*squaresize+y_offset))

    return legal_moves 

#check winner 
def check_game():
    layout,r,c = read_file(board_file)
    i_FLAG = 0 
    j_FLAG = 0 
    for i in range(r): 
        for j in range(c): 
            if i == 0: #checks if computer got to our side 
                if layout[i][j] == "O":
                    j_FLAG = -1
                    i_FLAG = 1
                    break 
            
            elif i == 7: #checks if computer got to our side 
                if layout[i][j] == "@":
                    j_FLAG = 1
                    i_FLAG = 1
                    break 
        if i_FLAG == 1:
            break
    return j_FLAG 


#checks the difference between prev and now board to determine last move the other player made 
def check_difference(board1, board2): 
    move =""
    c = 0 
    iflag = 0
    for i in range(8): 
        for j in range(8): 
            if board1[i][j]!=board2[i][j]: 
                move+=position_letter_grid_8[i][j]
                c+=1
                if c == 2:  ##difference is only supposed to be 2 
                    iflag = 1
                    break 
        if iflag == 1: 
            break 
    return move 

#used to update the board we made by making a move (temporary board until program reads the new board)
def update_board(layout, move):
    S = move[0:2] #source 
    D = move[2:4] #destination
    l = deepcopy(layout)
    for i in range(8): 
        for j in range(8): 
            if position_letter_grid_8[i][j] == S: 
                l[i][j] = "+"
            elif position_letter_grid_8[i][j] == D: 
                l[i][j] = "@"
    return l

def draw_prev_move(prev_move): 
    S = prev_move[0:2] #source 
    D = prev_move[2:4] #destination
    x_o = 0 
    y_o = 0

    x = -1 
    y = -1
    x1 = -1 
    y1 = -1
    if ord(str(S[0])) == ord(str(D[0])): 
        arrow = W_arrow_middle
        y_o = 30
    elif ord(str(S[0])) < ord(str(D[0])): 
        x_o = 20
        y_o = 20
        arrow = W_arrow_left
    else: 
        x_o = -50
        y_o = 20
        arrow = W_arrow_right
    
    for i in range(8): 
        for j in range(8): 
            if position_letter_grid_8[i][j] == S: 
                x = i 
                y = j 
            if position_letter_grid_8[i][j] == D:
                x1 = i 
                y1 = j

    if x1!=-1 and y1!=-1:
        screen.blit(white_moved, (y1*squaresize+x_offset+3,x1*squaresize+y_offset+3))
    if x!=-1 and y!=-1:
        screen.blit(arrow, (y*squaresize+x_offset+x_o,x*squaresize+y_offset+y_o))


def run():
    global screen
    screen=pygame.display.set_mode((screen_width,screen_height))
    running = True 
    selected = False
    selected_Piece = ""
    move_made = False 
    time_sleep = False
    undo_flag = False
    #used to prevent crash with file reading if user doesnt press board first 
    first_press_flag = False
    while(running):
        drawboard()
        layout,r,c = read_file(board_file)
        old_layout = deepcopy(layout)
        global prev_board
        prev_move = check_difference(layout,prev_board) #gets the pervious move 
        drawPieces(layout) 
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
            if undo_flag == False: 
                draw_prev_move(prev_move) 
            moves = get_moves() 
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    output_file=open("output.txt", "w")
                    output_file.write("exit")
                    output_file.close()
                    os.remove("output.txt")
                    running=False
                if event.type==pygame.MOUSEBUTTONDOWN: 
                    x,y=pygame.mouse.get_pos()
                    selection_xy = isPiecePresent(1,x,y)
                    position=determine_position(x,y)
                    #check if press was undo button
                    if selection_xy == (screen_width-40, 10): 
                        output_file=open("output.txt", "w")
                        output_file.write("u")
                        undo_flag = True
                        output_file.close()
                        os.remove("output.txt")
                        break 
                    if selection_xy != (0,0): #its a piece 
                        selected_Piece = position
                        selected = True 
                        first_press_flag = True
                    else: 
                        #if not piece then we check to see if space selected is a legal move 
                        if first_press_flag == True: 
                            for p in legal_moves: 
                                if p == position: 
                                    undo_flag = False
                                    move = selected_Piece+position #concatinate piece with new position
                                    print(move)
                                    output_file=open("output.txt", "w")
                                    output_file.write(move)
                                    output_file.close()

                                    new_layout = update_board(layout, move) 
                                    prev_board = deepcopy(new_layout) #board after our player moves 

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
                            selected = False 

            if selected == True: 
                screen.blit(selection, selection_xy)  
                legal_moves = print_moves(position, moves)
    
        pygame.display.update()