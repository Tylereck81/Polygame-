import pygame
import time 
import os
from copy import copy, deepcopy

pygame.init()

#Screen Dimensions and Offsets 
screen_width=880
screen_height=550
squaresize = 90
x_offset = 215
y_offset = 50

#Files to Read 
#board_file="//home//ailab_server//fb_polygames//Polygames//MS_board.txt"
#moves_file="//home//ailab_server//fb_polygames//Polygames//moves_list.txt"

board_file= "boards//MS_board.txt"
moves_file ="moves//minishogi_moves.txt"

#Player Pieces to Load 
R = pygame.image.load(".//res//minishogi_res//R.png")
K = pygame.image.load(".//res//minishogi_res//K.png")
B = pygame.image.load(".//res//minishogi_res//B.png")
P = pygame.image.load(".//res//minishogi_res//P.png")
G = pygame.image.load(".//res//minishogi_res//G.png")
S = pygame.image.load(".//res//minishogi_res//S.png")
P_Pro = pygame.image.load(".//res//minishogi_res//+P.png")
S_Pro = pygame.image.load(".//res//minishogi_res//+S.png")
B_Pro = pygame.image.load(".//res//minishogi_res//+B.png")
R_Pro = pygame.image.load(".//res//minishogi_res//+R.png")
legal_move_indicator = pygame.image.load(".//res//minishogi_res//move_indicator.png") #WHITE piece 
selection=pygame.image.load(".//res//minishogi_res//selection.png") #red border 

#Transformations to Images used
Enemy_R = pygame.transform.rotate(R,180)
Enemy_K = pygame.transform.rotate(K,180)
Enemy_B = pygame.transform.rotate(B,180)
Enemy_P = pygame.transform.rotate(P,180)
Enemy_G = pygame.transform.rotate(G,180)
Enemy_S = pygame.transform.rotate(S,180)
Enemy_P_Pro = pygame.transform.rotate(P_Pro,180)
Enemy_S_Pro = pygame.transform.rotate(S_Pro,180)
Enemy_B_Pro = pygame.transform.rotate(B_Pro,180)
Enemy_R_Pro = pygame.transform.rotate(R_Pro,180)

#Colors to use 
brown_square= (185,136,38)
brown_index = (156,108,10) #orangy 
black = (0,0,0)
white =(255,255,255)
menu_area_color=(42,51,64)

#matrix to link moves to i,j position values 
position_letter_grid_5=[
['a1', 'b1', 'c1', 'd1', 'e1'],
['a2', 'b2', 'c2', 'd2', 'e2'],
['a3', 'b3', 'c3', 'd3', 'e3'],
['a4', 'b4', 'c4', 'd4', 'e4'],
['a5', 'b5', 'c5', 'd5', 'e5']
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
    n = 1
    l = 'A'
    #draws the backboard with indexes 
    for x  in range(1,6): 
        for y in range(1,6): 
            x1 = (squaresize * (x - 1))+x_offset-30
            y1 = (squaresize * (y - 1))+y_offset-30
            pygame.draw.rect(screen, brown_index, [x1,y1,squaresize+60, squaresize+60])
            if y==1:
                draw_text(str(l),50,black,x1+75,y1+17)
                l = chr(ord(l)+1)
            if x==1:
                draw_text(str(n),55,black,x1+15,y1+75)
                n +=1
    
    #Left Board
    for x in range (6): 
        pygame.draw.rect(screen,black,[0,(squaresize*x)+5,squaresize,squaresize])
        pygame.draw.rect(screen,brown_square,[0,(squaresize*x)+3+5,squaresize-3,squaresize-3])

    #Right Board  
    for x in range (6): 
        pygame.draw.rect(screen,black,[790,(squaresize*x)+5,squaresize,squaresize])
        pygame.draw.rect(screen,brown_square,[793,(squaresize*x)+3+5,squaresize-3,squaresize-3])

    #draws the actual board 
    for x in range(1, 6):
        for y in range(1, 6):
            if x!=5 and y!=5:
                pygame.draw.rect(screen, black, [(squaresize * (x - 1))+x_offset, (squaresize * (y - 1))+y_offset,
                                                                squaresize, squaresize])
                
                pygame.draw.rect(screen, brown_square, [((squaresize * (x - 1))+3)+x_offset, ((squaresize * (y - 1))+3)+y_offset,
                                                                squaresize-3, squaresize-3])
            else: 
                pygame.draw.rect(screen, black, [(squaresize * (x - 1))+x_offset, (squaresize * (y - 1))+y_offset,
                                                                squaresize+3, squaresize+3])
                
                pygame.draw.rect(screen, brown_square, [(squaresize * (x - 1))+3+x_offset, (squaresize * (y - 1))+3+y_offset,
                                                                squaresize-3, squaresize-3])

# reads in a boardfile as a file and returns a 2 dimensional array of the board 
def read_file(boardfile):

    #gets first line number to check what board we are reading 
    with open(boardfile, 'r') as l:
        firstline = l.readline()
    
    if firstline == "1\n": #MiniShogi 
        numlist=123456789
        l=[]
        l2=[]
        r1=0 #holds row count 
        c1=0 #holds col count 
        cflag = 0 
        c=0 #holds temp col count 
        with open(boardfile, 'r') as f:
            board_layout=f.read()
            for j in range(19, 121): #starting and ending values start at 3rd row and end at 7th row  
                if(board_layout[j]!='\n' and board_layout[j] not in str(numlist) and j%17 !=4 and board_layout[j]!="|"):
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
        
        #after getting board we get the list of pieces on left and right board 
        f = open(boardfile,'r') 
        lines = f.readlines() 
        t=[] 
        t.append(lines[7])
        t.append(lines[8])
        global left, right 
        left = [] 
        right = [] 

        for j in range(len(t[0])): 
            if(t[0][j] == "("): 
                left.append(t[0][j+1])
        
        for j in range(len(t[1])): 
            if(t[1][j] == "("): 
                right.append(t[1][j+1])
        
        l= l[::-1]
        return l,r1,c1
    else: 
        return 0,0,0


#acually draws image onto the board 
def drawPieces(layout_file):
    global position_list
    position_list=[]
    player_list=[] 
    
    #player and enemy player count
    PP = 0
    EP = 0 
    for j in range(5):
        for i in range(10):
            #i/2 because when writing to file, its 5*10 so need to translate 10 indexes to 5 
            if layout_file[j][i]==' ' and  i+1<=9: 
                if layout_file[j][i+1] == 'K' :
                    screen.blit(Enemy_K,((i/2)*squaresize+x_offset,j*squaresize+y_offset))
                    #position_list.append(((i/2)*squaresize+x_offset, j*squaresize+y_offset))
                if layout_file[j][i+1] == 'G' :
                    screen.blit(Enemy_G,((i/2)*squaresize+x_offset,j*squaresize+y_offset))
                    #position_list.append(((i/2)*squaresize+x_offset, j*squaresize+y_offset))
                if layout_file[j][i+1] == 'S' :
                    screen.blit(Enemy_S,((i/2)*squaresize+x_offset,j*squaresize+y_offset))
                    #position_list.append(((i/2)*squaresize+x_offset, j*squaresize+y_offset))
                if layout_file[j][i+1] == 'R' :
                    screen.blit(Enemy_R,((i/2)*squaresize+x_offset,j*squaresize+y_offset))
                    # position_list.append(((i/2)*squaresize+x_offset, j*squaresize+y_offset))
                if layout_file[j][i+1] == 'P' :
                    screen.blit(Enemy_P,((i/2)*squaresize+x_offset,j*squaresize+y_offset))
                    #position_list.append(((i/2)*squaresize+x_offset, j*squaresize+y_offset))
                if layout_file[j][i+1] == 'B' :
                    screen.blit(Enemy_B,((i/2)*squaresize+x_offset,j*squaresize+y_offset))
                    #position_list.append(((i/2)*squaresize+x_offset, j*squaresize+y_offset))


                #append our pieces to a list to keep track of where each piece is
                if layout_file[j][i+1] == 'k' :
                    screen.blit(K,((i/2)*squaresize+x_offset,j*squaresize+y_offset))
                    player_list.append('K') 
                    player_list.append(((i/2)*squaresize+x_offset, j*squaresize+y_offset))
                    position_list.append(player_list)
                    player_list = [] 
                if layout_file[j][i+1] == 'g' :
                    screen.blit(G,((i/2)*squaresize+x_offset,j*squaresize+y_offset))
                    player_list.append('G') 
                    player_list.append(((i/2)*squaresize+x_offset, j*squaresize+y_offset))
                    position_list.append(player_list)
                    player_list = [] 
                if layout_file[j][i+1] == 's' :
                    screen.blit(S,((i/2)*squaresize+x_offset,j*squaresize+y_offset))
                    player_list.append('S') 
                    player_list.append(((i/2)*squaresize+x_offset, j*squaresize+y_offset))
                    position_list.append(player_list)
                    player_list = [] 
                if layout_file[j][i+1] == 'r' :
                    screen.blit(R,((i/2)*squaresize+x_offset,j*squaresize+y_offset))
                    player_list.append('R') 
                    player_list.append(((i/2)*squaresize+x_offset, j*squaresize+y_offset))
                    position_list.append(player_list)
                    player_list = [] 
                if layout_file[j][i+1] == 'p' :
                    screen.blit(P,((i/2)*squaresize+x_offset,j*squaresize+y_offset))
                    player_list.append('P') 
                    player_list.append(((i/2)*squaresize+x_offset, j*squaresize+y_offset))
                    position_list.append(player_list)
                    player_list = [] 
                if layout_file[j][i+1] == 'b' :
                    screen.blit(B,((i/2)*squaresize+x_offset,j*squaresize+y_offset))
                    player_list.append('B') 
                    player_list.append(((i/2)*squaresize+x_offset, j*squaresize+y_offset))
                    position_list.append(player_list)
                    player_list = [] 
            
            #Promoted Pieces
            elif layout_file[j][i]=="+" and i+1<=9: 
                #Enemy Pro Pieces
                if layout_file[j][i+1] == 'S' :
                    screen.blit(Enemy_S_Pro,((i/2)*squaresize+x_offset,j*squaresize+y_offset))
                if layout_file[j][i+1] == 'R' :
                    screen.blit(Enemy_R_Pro,((i/2)*squaresize+x_offset,j*squaresize+y_offset))
                if layout_file[j][i+1] == 'P' :
                    screen.blit(Enemy_P_Pro,((i/2)*squaresize+x_offset,j*squaresize+y_offset))
                if layout_file[j][i+1] == 'B' :
                    screen.blit(Enemy_B_Pro,((i/2)*squaresize+x_offset,j*squaresize+y_offset))
                
                #Our Pro Pieces 
                if layout_file[j][i+1] == 's' :
                    screen.blit(S_Pro,((i/2)*squaresize+x_offset,j*squaresize+y_offset))
                    player_list.append('+S') 
                    player_list.append(((i/2)*squaresize+x_offset, j*squaresize+y_offset))
                    position_list.append(player_list)
                    player_list = []

                if layout_file[j][i+1] == 'r' :
                    screen.blit(R_Pro,((i/2)*squaresize+x_offset,j*squaresize+y_offset))
                    player_list.append('+R') 
                    player_list.append(((i/2)*squaresize+x_offset, j*squaresize+y_offset))
                    position_list.append(player_list)
                    player_list = []
                    
                if layout_file[j][i+1] == 'p' :
                    screen.blit(P_Pro,((i/2)*squaresize+x_offset,j*squaresize+y_offset))
                    player_list.append('+P') 
                    player_list.append(((i/2)*squaresize+x_offset, j*squaresize+y_offset))
                    position_list.append(player_list)
                    player_list = []

                if layout_file[j][i+1] == 'b' :
                    screen.blit(B_Pro,((i/2)*squaresize+x_offset,j*squaresize+y_offset))
                    player_list.append('+B') 
                    player_list.append(((i/2)*squaresize+x_offset, j*squaresize+y_offset))
                    position_list.append(player_list)
                    player_list = []
    
    #after drawing board we draw the posession board 
    #left board 
    n = 0 
    for l in left: 
        if l =='K':
            screen.blit(Enemy_K,(0,(squaresize*n)+3+5))
            n+=1
        elif l == 'G':
            screen.blit(Enemy_G,(0,(squaresize*n)+3+5))
            n+=1
        elif l == 'R': 
            screen.blit(Enemy_R,(0,(squaresize*n)+3+5))
            n+=1
        elif l == 'B': 
            screen.blit(Enemy_B,(0,(squaresize*n)+3+5))
            n+=1
        elif l == 'P': 
            screen.blit(Enemy_P,(0,(squaresize*n)+3+5))
            n+=1
        elif l == 'S': 
            screen.blit(Enemy_S,(0,(squaresize*n)+3+5))
            n+=1
        
        
    #right board 
    n = 0 
    for r in right: 
        if r =='k':
            screen.blit(K,(793,(squaresize*n)+3+5))
            player_list.append('K1') 
            player_list.append((793,(squaresize*n)+3+5))
            position_list.append(player_list) 
            player_list = []
            n+=1
        elif r == 'g':
            player_list.append('G1') 
            player_list.append((793,(squaresize*n)+3+5))
            position_list.append(player_list) 
            player_list = []
            screen.blit(G,(793,(squaresize*n)+3+5))
            n+=1
        elif r == 'r': 
            player_list.append('R1') 
            player_list.append((793,(squaresize*n)+3+5))
            position_list.append(player_list) 
            player_list = []
            screen.blit(R,(793,(squaresize*n)+3+5))
            n+=1
        elif r == 'b': 
            player_list.append('B1') 
            player_list.append((793,(squaresize*n)+3+5))
            position_list.append(player_list) 
            player_list = []
            screen.blit(B,(793,(squaresize*n)+3+5))
            n+=1
        elif r == 'p': 
            player_list.append('P1') 
            player_list.append((793,(squaresize*n)+3+5))
            position_list.append(player_list) 
            player_list = []
            screen.blit(P,(793,(squaresize*n)+3+5))
            n+=1
        elif r == 's': 
            player_list.append('S1') 
            player_list.append((793,(squaresize*n)+3+5))
            position_list.append(player_list) 
            player_list = []
            screen.blit(S,(793,(squaresize*n)+3+5))
            n+=1
        

def get_moves(): 
    moves=[]
    with open (moves_file, 'r') as m:
        moves=m.read().split()

    return moves

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


#moves list translated physically into dots on board to indicate where the specified piece can move 
def print_moves(letter_co, m_list):
    legal_moves=[] 

    off_board = False 
    #check if its on board or off board piece 
    if len(letter_co) == 2 and letter_co[0]!="+":
        off_board = True 
        letter_co = letter_co[0]
    
    if len(letter_co) == 1: 
        for moves in m_list:
            if letter_co == moves[0]: 
                legal_moves.append(moves[1:])
            if letter_co == "P":
                if "K" not in moves and "P" not in moves and "R" not in moves and "G" not in moves and "S" not in moves and "B" not in moves:
                    legal_moves.append(moves)
    else: 
        for moves in m_list: 
            if letter_co in moves: 
                legal_moves.append(moves[2:])
        

    # 1 - move normal (e3)  
    # 2 - eat (xa4) 
    # 3 - moving piece to board (@a2) 

    #HAVE NOT DONE YET 
    # 4 - moving to promotion (b5+)
    # 5 - eating piece and promoting (xb5+)

    if not(off_board): #onboard piece so we put moves with case 1 and 2 
        for move in legal_moves:
            x = -1
            y = -1
            if len(move) == 2: #just a regular move (#1)
                for i in range(5): 
                    for j in range(5): 
                        if move == position_letter_grid_5[i][j]: #e3
                            x = i 
                            y = j 
                if x!=-1 and y!=-1:
                    screen.blit(legal_move_indicator, (y*squaresize+x_offset,x*squaresize+y_offset))
            elif move[0] == 'x': #piece that is eating (#2)
                for i in range(5): 
                    for j in range(5): 
                        if move[1:]== position_letter_grid_5[i][j]: #xa4 to a4 
                            x = i 
                            y = j 
                if x!=-1 and y!= -1: 
                    screen.blit(legal_move_indicator, (y*squaresize+x_offset,x*squaresize+y_offset))
                else: # means its case #5 
                    for i in range(5): 
                        for j in range(5): 
                            if move[1:3]== position_letter_grid_5[i][j]: #xb5+ to b5
                                x = i 
                                y = j 
                    if x!=-1 and y!=-1:
                        screen.blit(legal_move_indicator, (y*squaresize+x_offset,x*squaresize+y_offset))
            elif move[2]=="+":#case #4 regular promotion
                for i in range(5): 
                        for j in range(5): 
                            if move[:2]== position_letter_grid_5[i][j]: #b5+ to b5
                                x = i 
                                y = j 
                if x!=-1 and y!=-1:
                    screen.blit(legal_move_indicator, (y*squaresize+x_offset,x*squaresize+y_offset))

    else: #offboard piece so case #3
        for move in legal_moves:
            x = -1
            y = -1
            if move[0]=='@':
                for i in range(5): 
                    for j in range(5): 
                        if move[1:] == position_letter_grid_5[i][j]: 
                            x = i 
                            y = j 
                if x!=-1 and y!=-1:
                    screen.blit(legal_move_indicator, (y*squaresize+x_offset,x*squaresize+y_offset))
    
    return legal_moves

#pops up the piece if selected 
def selected_piece_print(p,position): 
    x,y = position 
    new_position = (x,y-10)
    if p == "K" or p == "K1":
        screen.blit(K,new_position)
    elif p == "R" or p == "R1": 
        screen.blit(R,new_position)
    elif p == "B" or p == "B1": 
        screen.blit(B,new_position)
    elif p == "S" or p == "S1": 
        screen.blit(S,new_position)
    elif p =="P" or p == "P1": 
        screen.blit(P,new_position)
    elif p == "G" or p == "G1":
        screen.blit(G,new_position)
    #promoted pieces 
    elif p =="+R":
        screen.blit(R_Pro,new_position)
    elif p =="+B":
        screen.blit(B_Pro,new_position)
    elif p =="+S":
        screen.blit(S_Pro,new_position)
    elif p =="+P":
        screen.blit(P_Pro,new_position)


def update_board(layout,move): 
    l = deepcopy(layout) 
    piece = move[0].lower()
    if piece == "+": 
        piece += move[1].lower()
    print(piece)

    if len(piece) == 2: #for promoted pieces we check both areas 
        for j in range(5):
            for i in range(10):
                if l[j][i]== piece[0] and l[j][i+1]==piece[1]: 
                    l[j][i] = " "
                    l[j][i+1] = " "
        flag = 0 
        for j in range(5):
            for i in range(10):
                if position_letter_grid_5[j][int(i/2)] in move: 
                    if flag == 0:
                        l[j][i] = piece[0]
                        l[j][i+1] = piece[1]
                        flag = 1
    else: 
        for j in range(5):
            for i in range(10):
                if l[j][i]== piece: 
                    l[j][i] = " "

        flag = 0 
        for j in range(5):
            for i in range(10):
                if position_letter_grid_5[j][int(i/2)] in move: 
                    if flag == 0:
                        l[j][i+1] = piece
                        flag = 1
    return l 


def run(): 
    global screen
    screen=pygame.display.set_mode((screen_width,screen_height))
    running = True 
    selected = False
    selected_Piece = ""
    move_made = False 
    while running: 
        layout,r,c = read_file(board_file)
        while(not layout and not r and not c): 
            layout,r,c = read_file(board_file)

        old_layout= deepcopy(layout) #keeps an initial copy for comparison later

        drawboard()
        drawPieces(layout)
        moves = get_moves() 
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                running=False
            if event.type==pygame.MOUSEBUTTONDOWN: 
                x,y=pygame.mouse.get_pos()
                selection_xy, piece = isPiecePresent(x,y)
                position = determine_position(x,y)
                if selection_xy != (0,0): #its a piece 
                    selected_Piece = piece
                    selected = True 
                else: 
                    # 1.) the piece position is clicked on board
                    # 2.) random position on board is clicked 
                    # 3.) random position off the board is clicked 

                    if position: #3
                        if selected: #2
                            if (len(selected_Piece) == 2 and selected_Piece[1] == "1"): #for moving off board pieces (P1)
                                selected_Piece = selected_Piece[0]
                                
                                for p in moves: 
                                    if position in p and "@" in p:
                                        move  =  p
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
                                        for i in range(5): 
                                            for j in range(10): 
                                                print(new_layout[i][j],end="")
                                            print("")
                                        
                                        break
                            else:
                                #special case p does not have the letter in the move  so we just check for the position 
                                if selected_Piece == "P": 
                                    for p in moves: 
                                        if position in p and "K" not in p and "R" not in p and "S" not in p and "B" not in p and "G" not in p and "P" not in p:
                                            move  = p
                                            print(move)
                                            print(position)
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
                                            for i in range(5): 
                                                for j in range(10): 
                                                    print(new_layout[i][j],end="")
                                                print("")
                                            break 
                                else:
                                    for p in moves: 
                                        if position in p and selected_Piece in p:
                                            move  = p
                                            print(move)
                                            print(position)
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
                                            for i in range(5): 
                                                for j in range(10): 
                                                    print(new_layout[i][j],end="")
                                                print("")
                                            break 
                                            
                    selected_Piece =""
                    selected = False 

        if selected == True: 
            #pops up the selected piece 
            selected_piece_print(piece, selection_xy)
            legal_moves = print_moves(piece, moves)

        pygame.display.update()
