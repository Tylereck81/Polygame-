import pygame
import time 
import os
import random
from copy import copy, deepcopy

pygame.init()

#Screen Dimensions and Offsets 
screen_width=880
screen_height=550
squaresize = 90
x_offset = 215
y_offset = 50


#Files to Read 
# board_file="//home//ailab_server//fb_polygames//Polygames//E_board.txt"
# moves_file="//home//ailab_server//fb_polygames//Polygames//moves_list.txt"

board_file="boards//E_board.txt"
moves_file="moves//einstein_moves.txt"

legal_move_indicator = pygame.image.load(".//res//einstein_res//move_indicator.png") #red dot
undo = pygame.image.load(".//res//einstein_res//undo.png") #undo 

#Colors to use 
black_square=( 145, 151, 161 )
white_square=( 197, 208, 226 )
brown_index = ( 83, 93, 109 ) #orangy 
black = (0,0,0)
white =(255,255,255)
menu_area_color=( 160, 167, 178 )

#matrix to link moves to i,j position values 
position_letter_grid_5=[
['a1', 'b1', 'c1', 'd1', 'e1'],
['a2', 'b2', 'c2', 'd2', 'e2'],
['a3', 'b3', 'c3', 'd3', 'e3'],
['a4', 'b4', 'c4', 'd4', 'e4'],
['a5', 'b5', 'c5', 'd5', 'e5']
]

#Player Pieces to Load 
x1=pygame.image.load(".//res//einstein_res//red_1.png")
x2=pygame.image.load(".//res//einstein_res//red_2.png")
x3=pygame.image.load(".//res//einstein_res//red_3.png")
x4=pygame.image.load(".//res//einstein_res//red_4.png")
x5=pygame.image.load(".//res//einstein_res//red_5.png")
x6=pygame.image.load(".//res//einstein_res//red_6.png")

o1=pygame.image.load(".//res//einstein_res//blue_1.png")
o2=pygame.image.load(".//res//einstein_res//blue_2.png")
o3=pygame.image.load(".//res//einstein_res//blue_3.png")
o4=pygame.image.load(".//res//einstein_res//blue_4.png")
o5=pygame.image.load(".//res//einstein_res//blue_5.png")
o6=pygame.image.load(".//res//einstein_res//blue_6.png")


#used to draw text to screen
def draw_text(text, size, color, x,y): 
    font = pygame.font.SysFont(pygame.font.get_default_font(),size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect() 
    text_rect.center = (x,y)
    screen.blit(text_surface,text_rect)

def drawboard(): 
    global position_list
    position_list=[]
    player_list=[] 
    screen.fill(menu_area_color)
    n = 1
    l = 'A'
    #draws the backboard with indexes 
    for x  in range(1,6): 
        for y in range(1,6): 
            X = (squaresize * (x - 1))+x_offset-30
            y1 = (squaresize * (y - 1))+y_offset-30
            pygame.draw.rect(screen, brown_index, [X,y1,squaresize+60, squaresize+60])
            if y==1:
                draw_text(str(l),50,black,X+75,y1+17)
                l = chr(ord(l)+1)
            if x==1:
                draw_text(str(n),55,black,X+15,y1+75)
                n +=1

    #draws the actual board 
    flag = 0
    for x in range(1, 6):
        if x%2 == 1: 
            flag = 0
        else: 
            flag = 1
        for y in range(1, 6):
            if x!=5 and y!=5:
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
    
    if firstline == "4\n": #MiniShogi 
        numlist=1234560
        l=[]
        l2=[]
        r1=0 #holds row count 
        c1=0 #holds col count 
        cflag = 0 
        c=0 #holds temp col count 
        with open(boardfile, 'r') as f:
            board_layout=f.read()
            for j in range(19, 104): #starting and ending values start at 3rd row and end at 7th row  
                if j-1>=0: 
                    if(board_layout[j]!='\n' and ((board_layout[j] == " " and j%17 !=3) or (board_layout[j] == 'x' or board_layout[j] == 'o') or (board_layout[j] in str(numlist) and (board_layout[j-1] == 'x' or board_layout[j-1] == 'o'))) and board_layout[j]!="|"):
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
    else: 
        return 0,0,0

def drawPieces(layout_file,TX): 
    global position_list
    position_list=[]
    player_list=[] 

    pieces=['x1','x2','x3','x4','x5','x6','o1','o2','o3','o4','o5','o6']

    on_board_before=[] #array to check available moves in the beginning on the board 

    #starts adding pieces to board for moves when the board is already set up 
    for j in range(5): 
        for i in range(10): 
            if layout_file[j][i]=="x" and i+1<=9: 
                if layout_file[j][i+1] == "1": 
                    screen.blit(x1,((i/2)*squaresize+x_offset+5,j*squaresize+y_offset+5))
                    player_list.append('x1')
                    on_board_before.append('x1')
                    player_list.append(((i/2)*squaresize+x_offset+5,j*squaresize+y_offset+5))
                    position_list.append(player_list)
                    player_list = []
                if layout_file[j][i+1] == "2": 
                    screen.blit(x2,((i/2)*squaresize+x_offset+5,j*squaresize+y_offset+5))
                    player_list.append('x2')
                    on_board_before.append('x2')
                    player_list.append(((i/2)*squaresize+x_offset+5,j*squaresize+y_offset+5))
                    position_list.append(player_list)
                    player_list = []
                if layout_file[j][i+1] == "3": 
                    screen.blit(x3,((i/2)*squaresize+x_offset+5,j*squaresize+y_offset+5))
                    player_list.append('x3')
                    on_board_before.append('x3')
                    player_list.append(((i/2)*squaresize+x_offset+5,j*squaresize+y_offset+5))
                    position_list.append(player_list)
                    player_list = []
                if layout_file[j][i+1] == "4": 
                    screen.blit(x4,((i/2)*squaresize+x_offset+5,j*squaresize+y_offset+5))
                    player_list.append('x4')
                    on_board_before.append('x4')
                    player_list.append(((i/2)*squaresize+x_offset+5,j*squaresize+y_offset+5))
                    position_list.append(player_list)
                    player_list = []
                if layout_file[j][i+1] == "5": 
                    screen.blit(x5,((i/2)*squaresize+x_offset+5,j*squaresize+y_offset+5))
                    player_list.append('x5')
                    on_board_before.append('x5')
                    player_list.append(((i/2)*squaresize+x_offset+5,j*squaresize+y_offset+5))
                    position_list.append(player_list)
                    player_list = []
                if layout_file[j][i+1] == "6": 
                    screen.blit(x6,((i/2)*squaresize+x_offset+5,j*squaresize+y_offset+5))
                    player_list.append('x6')
                    on_board_before.append('x6')
                    player_list.append(((i/2)*squaresize+x_offset+5,j*squaresize+y_offset+5))
                    position_list.append(player_list)
                    player_list = []

            elif layout_file[j][i]=="o" and i+1<=9: 
                if layout_file[j][i+1] == "1": 
                    screen.blit(o1,((i/2)*squaresize+x_offset+5,j*squaresize+y_offset+5))
                    on_board_before.append('o1')
                    if TX > 6: #TX ensures that we cant click on pieces on board to move when we are setting up board in beginning 
                        player_list.append('o1')
                        player_list.append(((i/2)*squaresize+x_offset+5,j*squaresize+y_offset+5))
                        position_list.append(player_list)
                        player_list = []
                if layout_file[j][i+1] == "2": 
                    screen.blit(o2,((i/2)*squaresize+x_offset+5,j*squaresize+y_offset+5))
                    on_board_before.append('o2')
                    if TX > 6: 
                        player_list.append('o2')
                        player_list.append(((i/2)*squaresize+x_offset+5,j*squaresize+y_offset+5))
                        position_list.append(player_list)
                        player_list = []
                if layout_file[j][i+1] == "3": 
                    screen.blit(o3,((i/2)*squaresize+x_offset+5,j*squaresize+y_offset+5))
                    on_board_before.append('o3')
                    if TX > 6:
                        player_list.append('o3')
                        player_list.append(((i/2)*squaresize+x_offset+5,j*squaresize+y_offset+5))
                        position_list.append(player_list)
                        player_list = []
                if layout_file[j][i+1] == "4": 
                    screen.blit(o4,((i/2)*squaresize+x_offset+5,j*squaresize+y_offset+5))
                    on_board_before.append('o4')
                    if TX > 6:
                        player_list.append('o4')
                        player_list.append(((i/2)*squaresize+x_offset+5,j*squaresize+y_offset+5))
                        position_list.append(player_list)
                        player_list = []
                if layout_file[j][i+1] == "5": 
                    screen.blit(o5,((i/2)*squaresize+x_offset+5,j*squaresize+y_offset+5))
                    on_board_before.append('o5')
                    if TX > 6:
                        player_list.append('o5')
                        player_list.append(((i/2)*squaresize+x_offset+5,j*squaresize+y_offset+5))
                        position_list.append(player_list)
                        player_list = []
                if layout_file[j][i+1] == "6": 
                    screen.blit(o6,((i/2)*squaresize+x_offset+5,j*squaresize+y_offset+5))
                    on_board_before.append('o6')
                    if TX > 6:  
                        player_list.append('o6')
                        player_list.append(((i/2)*squaresize+x_offset+5,j*squaresize+y_offset+5))
                        position_list.append(player_list)
                        player_list = []

    if TX < 7: #after board has been set up, there is no need to do this part 
        #after placing pieces on board then we have to check if the piece is not on the board 
        for i in range(len(pieces)): 
            flag = 1
            for j in range(len(on_board_before)): 
                if pieces[i] == on_board_before[j]: #if piece is in list then it is on board
                    flag =  0
                    break 
            if flag: 
                if pieces[i] == 'x1':
                    screen.blit(x1,(10,155))
                    # player_list.append('x1')
                    # player_list.append((10,155))
                    # position_list.append(player_list)
                    # player_list = []
                elif pieces[i] == 'x2':
                    screen.blit(x2,(10,235))
                    # player_list.append('x2')
                    # player_list.append((10,235))
                    # position_list.append(player_list)
                    # player_list = []
                elif pieces[i] == 'x3':
                    screen.blit(x3,(10,315))
                    # player_list.append('x3')
                    # player_list.append((10,315))
                    # position_list.append(player_list)
                    # player_list = []
                elif pieces[i] == 'x4':
                    screen.blit(x4,(95,155))
                    # player_list.append('x4')
                    # player_list.append((95,155))
                    # position_list.append(player_list)
                    # player_list = []
                elif pieces[i] == 'x5':
                    screen.blit(x5,(95,235))
                    # player_list.append('x5')
                    # player_list.append((95,235))
                    # position_list.append(player_list)
                    # player_list = []
                elif pieces[i] == 'x6':
                    screen.blit(x6,(95,315))
                    # player_list.append('x6')
                    # player_list.append((95,315))
                    # position_list.append(player_list)
                    # player_list = []
                
                elif pieces[i] == 'o1':
                    screen.blit(o1,(screen_width-175,155))
                    player_list.append('o0')
                    player_list.append((screen_width-175,155))
                    position_list.append(player_list)
                    player_list = []
                elif pieces[i] == 'o2':
                    screen.blit(o2,(screen_width-175,235))
                    player_list.append('o1')
                    player_list.append((screen_width-175,235))
                    position_list.append(player_list)
                    player_list = []
                elif pieces[i] == 'o3':
                    screen.blit(o3,(screen_width-175,315))
                    player_list.append('o2')
                    player_list.append((screen_width-175,315))
                    position_list.append(player_list)
                    player_list = []
                elif pieces[i] == 'o4':
                    screen.blit(o4,(screen_width-90,155))
                    player_list.append('o3')
                    player_list.append((screen_width-90,155))
                    position_list.append(player_list)
                    player_list = []
                elif pieces[i] == 'o5':
                    screen.blit(o5,(screen_width-90,235))
                    player_list.append('o4')
                    player_list.append((screen_width-90,235))
                    position_list.append(player_list)
                    player_list = []
                elif pieces[i] == 'o6':
                    screen.blit(o6,(screen_width-90,315))
                    player_list.append('o5')
                    player_list.append((screen_width-90,315))
                    position_list.append(player_list)
                    player_list = []

    #Undo Button drawn 
    screen.blit(undo,(screen_width-40, 10))
    player_list.append('undo')
    player_list.append((screen_width-40, 10))
    position_list.append(player_list)
    player_list = [] 


def get_moves(): 
    moves=[]
    with open (moves_file, 'r') as m: 
        moves=m.read().split()

    print(moves)
    # l = [] 
    # l[:] = piece
    # l[1]=chr(ord(l[1])+1) 
    actions = [] 
    official_moves = [] 
    for i in range(0,len(moves),4): 
        action = moves[i]
        piece = moves[i+1]
        move = moves[i+3]

        actions.append(piece) 
        actions.append(action)
        actions.append(move)

        official_moves.append(actions)
        actions = []

    return official_moves

def isPiecePresent(x,y):
    selection_coordinates = (0,0)
    position = "T"
    for i in range(len(position_list)):
        px,py = position_list[i][1]
        if (x>=px and x<=px+squaresize) and (y>=py and y<=py+squaresize):
            selection_coordinates=(px,py)
            position = position_list[i][0]
            break         
    return selection_coordinates,position


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
        if (n2>5): 
            break

    n1 = 0 
    n2 = 1
    l = 1
    flag = 1
    while(flag == 1): #checks y coordinate 
        if position_y >= n1*squaresize+y_offset and position_y<=n2*squaresize+y_offset: 
            y = l; 
            flag = 0
        else: 
            n1+=1
            n2+=1
            l +=1
        if (n2>5): 
            break
    
    if x =="" or y =="": 
        x = ""
        y = ""     
      
    return x+str(y)

#pops up the piece if selected 
def selected_piece_print(p,position,TX): 
    x,y = position 
    new_position = (x,y-4)
    # if p == "x1": 
    #     screen.blit(x1,new_position)
    # if p == "x2": 
    #     screen.blit(x2,new_position)
    # if p == "x3": 
    #     screen.blit(x3,new_position)
    # if p == "x4": 
    #     screen.blit(x4,new_position)
    # if p == "x5": 
    #     screen.blit(x5,new_position)
    # if p == "x6": 
    #     screen.blit(x6,new_position)
    if TX<=6:
        if p == "o0": 
            screen.blit(o1,new_position)
        if p == "o1": 
            screen.blit(o2,new_position)
        if p == "o2": 
            screen.blit(o3,new_position)
        if p == "o3": 
            screen.blit(o4,new_position)
        if p == "o4": 
            screen.blit(o5,new_position)
        if p == "o5": 
            screen.blit(o6,new_position)
    else: 
        if p == "o1": 
            screen.blit(o1,new_position)
        if p == "o2": 
            screen.blit(o2,new_position)
        if p == "o3": 
            screen.blit(o3,new_position)
        if p == "o4": 
            screen.blit(o4,new_position)
        if p == "o5": 
            screen.blit(o5,new_position)
        if p == "o6": 
            screen.blit(o6,new_position)


def print_moves(piece,moves): 
    legal_moves=[] 
    for i in range(len(moves)): 
        if piece == moves[i][0]:
            legal_moves.append(moves[i][2].lower()) 
    
    for legal_move in legal_moves: 
        x = -1
        y = -1
        for i in range(5): 
            for j in range(5): 
                if legal_move == position_letter_grid_5[i][j]: 
                    x = i
                    y = j 
        if x!=-1 and y!=-1: 
            screen.blit(legal_move_indicator,(y*squaresize+x_offset,x*squaresize+y_offset))

def update_board(layout, piece, move,TX): 
    layout_file = deepcopy(layout) 

    if TX<=6:
        #first we erase the piece from the board 
        for j in range(5): 
            for i in range(10):
                if layout_file[j][i]==piece[0] and i+1<=9: 
                    if layout_file[j][i+1] == chr(ord(piece[1])+1): 
                        layout_file[j][i] =" "
                        layout_file[j][i+1] = " " 

        #then we add piece to new part of the board 
        for i in range(5): 
            for j in range(5): 
                if position_letter_grid_5[i][j] == move.lower(): 
                    layout_file[i][j*2] = piece[0] 
                    layout_file[i][(j*2)+1] = chr(ord(piece[1])+1)

    else:
        #first we erase the piece from the board 
        for j in range(5): 
            for i in range(10):
                if layout_file[j][i]==piece[0] and i+1<=9: 
                    if layout_file[j][i+1] == piece[1]: 
                        layout_file[j][i] =" "
                        layout_file[j][i+1] = " " 

        #then we add piece to new part of the board 
        for i in range(5): 
            for j in range(5): 
                if position_letter_grid_5[i][j] == move.lower(): 
                    layout_file[i][j*2] = piece[0] 
                    layout_file[i][(j*2)+1] = piece[1]
        
        for i in range (5): 
            for j in range(10): 
                print(layout_file[i][j],end="")
            print("\n",end="")


    return layout_file


def run(): 
    global screen
    screen=pygame.display.set_mode((screen_width,screen_height))

    global TX 
    TX = 0
    layout,r,c = read_file(board_file)
    old_layout = deepcopy(layout)
    drawboard() #draws initial board
    drawPieces(layout,TX)
    pygame.display.update() 

    running = True 
    selected = False
    selected_Piece = ""
    move_made = False 
    random_flag = True
    undo_flag = False 

    while running: 


        if random_flag: 
            n =  random.randint(1,6)
            output_file=open("output.txt", "w")
            output_file.write(str(n))
            output_file.close()
            os.remove("output.txt")
            time.sleep(1) 

            print("in here 1")

            n =  random.randint(1,6)
            output_file=open("output.txt", "w")
            output_file.write(str(n))
            output_file.close()
            os.remove("output.txt")

            time.sleep(1)
            random_flag = False 
            TX+=1


        layout,r,c = read_file(board_file)
        while(not layout and not r and not c): 
            layout,r,c = read_file(board_file)
        moves = get_moves()
        old_layout= deepcopy(layout) #keeps an initial copy for comparison later

        drawboard()
        drawPieces(layout,TX) 
        # for i in range (r): 
        #     for j in range(c): 
        #         print(layout[i][j],end="")
        #     print("\n",end="")


        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                output_file=open("output.txt", "w")
                output_file.write("exit")
                output_file.close()
                os.remove("output.txt")
                running=False
            if event.type==pygame.MOUSEBUTTONDOWN: 
                x,y=pygame.mouse.get_pos()
                selection_xy, piece = isPiecePresent(x,y)
                position = determine_position(x,y)
                #check if press was undo button
                if selection_xy == (screen_width-40, 10): 
                    output_file=open("output.txt", "w")
                    output_file.write("u")
                    undo_flag = True
                    output_file.close()
                    os.remove("output.txt")
                    TX-=1 
                    break 
                if not selected:  #nothing is selected yet so we pop up piece 
                    if selection_xy != (0,0): 
                        selected_Piece = piece
                        selected = True 
                else: 
                    #something is already selected so we check if the press is an avaialable move
                    for i in range(len(moves)):
                        if selected_Piece == moves[i][0]: # checks to see if selected piece has that available move 
                            if position.upper() == moves[i][2]:
                                output_file=open("output.txt", "w")
                                print(moves[i][1])
                                output_file.write(moves[i][1])
                                output_file.close()
                                os.remove("output.txt")
                                random_flag = True 

                                new_layout = update_board(layout, selected_Piece, moves[i][2],TX) 
                                # for i in range (r): 
                                #     for j in range(c): 
                                #         print(new_layout[i][j],end="")
                                #     print("\n",end="")
                                #updates the board with new move made by us 
                                layout,r,c = read_file(board_file)
                                while True: 
                                    drawboard() 
                                    drawPieces(new_layout,TX)
                                    pygame.display.update()
                                    if random_flag: 
                                        time.sleep(1)
                                        n =  random.randint(1,6)
                                        output_file=open("output.txt", "w")
                                        output_file.write(str(n))
                                        output_file.close()
                                        os.remove("output.txt")

                                        time.sleep(1) 
                                        print(n)

                                        print("in here 2")

                                        n =  random.randint(1,6)
                                        print(n)
                                        output_file=open("output.txt", "w")
                                        output_file.write(str(n))
                                        output_file.close()
                                        os.remove("output.txt")

                                        random_flag = False 
                                        TX+=1
                                        time.sleep(1) 

                                    layout,r,c = read_file(board_file)
                                    if layout!= old_layout:  #when the board gets updated with the move computer makes, it will break out 
                                        break
                                    
                                break 

                                
                    selected = False


        if selected:
            #pops up the selected piece 
            selected_piece_print(piece, selection_xy,TX)
            print_moves(piece,moves)

        pygame.display.update()
