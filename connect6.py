#Connect 6 GUI 
#Tyler Eck 
import pygame
from copy import copy, deepcopy
import time 
import os

pygame.init()

#Screen Dimensions and Offsets 
screen_width=1160
screen_height=860
squaresize = 40
y_offset = 50
x_offset = 200


#Files to Read 
#board_file="//home//ailab_server//fb_polygames//Polygames//C6_board.txt"

board_file = "boards//C6_board.txt"

#Player Pieces to Load 
player_piece=pygame.image.load(".//res//othello8_res//white.png") #BLACK piece
enemy_piece=pygame.image.load(".//res//othello8_res//black_piece.png") #WHITE piece 

undo = pygame.image.load(".//res//othello8_res//undo.png") #undo 

#Transformations to Images used
player_piece = pygame.transform.scale(player_piece,(40,40))
enemy_piece = pygame.transform.scale(enemy_piece,(40,40))

#Colors to Use 
black = (0,0,0)
brown_index = (88,66,36) #darker color 
menu_area_color=(42,51,64)
brown_index =  (155,130,96) #normal 
menu_area_color=(42,51,64)
board_square =(255,230,150) #beige sqaures 

#matrix to link moves to i,j position values 
position_letter_grid_19=[
['a19', 'b19', 'c19', 'd19', 'e19', 'f19', 'g19', 'h19','i19','j19','k19','l19','m19','n19','o19','q19','r19','s19'],
['a18', 'b18', 'c18', 'd18', 'e18', 'f18', 'g18', 'h18','i18','j18','k18','l18','m18','n18','o18','q18','r18','s18'],
['a17', 'b17', 'c17', 'd17', 'e17', 'f17', 'g17', 'h17','i17','j17','k17','l17','m17','n17','o17','q17','r17','s17'],
['a16', 'b16', 'c16', 'd16', 'e16', 'f16', 'g16', 'h16','i16','j16','k16','l16','m16','n16','o16','q16','r16','s16'],
['a15', 'b15', 'c15', 'd15', 'e15', 'f15', 'g15', 'h15','i15','j15','k15','l15','m15','n15','o15','q15','r15','s15'],
['a14', 'b14', 'c14', 'd14', 'e14', 'f14', 'g14', 'h14','i14','j14','k14','l14','m14','n14','o14','q14','r14','s14'],
['a13', 'b13', 'c13', 'd13', 'e13', 'f13', 'g13', 'h13','i13','j13','k13','l13','m13','n13','o13','q13','r13','s13'],
['a12', 'b12', 'c12', 'd12', 'e12', 'f12', 'g12', 'h12','i12','j12','k12','l12','m12','n12','o12','q12','r12','s12'],
['a11', 'b11', 'c11', 'd11', 'e11', 'f11', 'g11', 'h11','i11','j11','k11','l11','m11','n11','o11','q11','r11','s11'],
['a10', 'b10', 'c10', 'd10', 'e10', 'f10', 'g10', 'h10','i10','j10','k10','l10','m10','n10','o10','q10','r10','s10'],
['a9', 'b9', 'c9', 'd9', 'e9', 'f9', 'g9', 'h9','i9','j9','k9','l9','m9','n9','o9','q9','r9','s9'],
['a8', 'b8', 'c8', 'd8', 'e8', 'f8', 'g8', 'h8','i8','j8','k8','l8','m8','n8','o8','q8','r8','s8'],
['a7', 'b7', 'c7', 'd7', 'e7', 'f7', 'g7', 'h7','i7','j7','k7','l7','m7','n7','o7','q7','r7','s7'],
['a6', 'b6', 'c6', 'd6', 'e6', 'f6', 'g6', 'h6','i6','j6','k6','l6','m6','n6','o6','q6','r6','s6'],
['a5', 'b5', 'c5', 'd5', 'e5', 'f5', 'g5', 'h5','i5','j5','k5','l5','m5','n5','o5','q5','r5','s5'],
['a4', 'b4', 'c4', 'd4', 'e4', 'f4', 'g4', 'h4','i4','j4','k4','l4','m4','n4','o4','q4','r4','s4'],
['a3', 'b3', 'c3', 'd3', 'e3', 'f3', 'g3', 'h3','i3','j3','k3','l3','m3','n3','o3','q3','r3','s3'],
['a2', 'b2', 'c2', 'd2', 'e2', 'f2', 'g2', 'h2','i2','j2','k2','l2','m2','n2','o2','q2','r2','s2'],
['a1', 'b1', 'c1', 'd1', 'e1', 'f1', 'g1', 'h1','i1','j1','k1','l1','m1','n1','o1','q1','r1','s1']
]


def drawboard(): 
    screen.fill(menu_area_color)
    # #draws the backboard with indexes 
    # for x  in range(1,20): 
    #     for y in range(1,20): 
    #         x1 = (squaresize * (x - 1))+x_offset-30
    #         y1 = (squaresize * (y - 1))+y_offset-30
    #         pygame.draw.rect(screen, brown_index, [x1,y1,squaresize+60, squaresize+60])
    
    # for x in range(1,20): 
    #     for y in range(1,20):
    #         x1 = (squaresize * (x - 1))+x_offset-30
    #         y1 = (squaresize * (y - 1))+y_offset-30
    #         if y==1:
    #             draw_text(str(l),50,black,x1+60,y1+15)
    #             l = chr(ord(l)+1)
    #         if x==1:
    #             draw_text(str(n),55,black,x1+15,y1+60)
    #             n -=1

    for x in range(1, 19):
            for y in range(1, 19):
                if x!=18 and y!=18:
                    pygame.draw.rect(screen, black, [(squaresize * (x - 1))+x_offset, (squaresize * (y - 1))+y_offset,
                                                                    squaresize, squaresize])
                    
                    pygame.draw.rect(screen, board_square, [((squaresize * (x - 1))+3)+x_offset, ((squaresize * (y - 1))+3)+y_offset,
                                                                    squaresize-3, squaresize-3])
                else: 
                    pygame.draw.rect(screen, black, [(squaresize * (x - 1))+x_offset, (squaresize * (y - 1))+y_offset,
                                                                    squaresize+3, squaresize+3])
                    
                    pygame.draw.rect(screen, board_square, [((squaresize * (x - 1))+3)+x_offset, ((squaresize * (y - 1))+3)+y_offset,
                                                                    squaresize-3, squaresize-3])

# reads in a boardfile as a file and returns a 2 dimensional array of the board 
def read_file(boardfile):
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
            if(board_layout[j]!='\n' and board_layout[j]==' ' and board_layout[j+1]=='.' and board_layout[j+2]==' '):
                l2.append(".") 
                c+=1
            elif(board_layout[j]!='\n' and board_layout[j]==' ' and board_layout[j+1]=='O' and board_layout[j+2]==' ' and c!=0):
                l2.append("O") 
                c+=1
            elif(board_layout[j]!='\n' and board_layout[j]==' ' and board_layout[j+1]=='X' and board_layout[j+2]==' '):
                l2.append("X") 
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
    
    for i in range(19):
        for j in range(19):
            if layout_file[j][i]=='O':
                screen.blit(enemy_piece,(i*squaresize+3+x_offset-20,j*squaresize+3+y_offset-20))
                #position_list.append((i*squaresize+3+x_offset, j*squaresize+3+y_offset))
            if layout_file[j][i]=='X':
                screen.blit(player_piece,(i*squaresize+3+x_offset-20,j*squaresize+3+y_offset-20))
                #position_list.append((i*squaresize+3+x_offset, j*squaresize+3+y_offset))


def determine_position(position_x, position_y):
    x=''
    y=''
    n1 = 0 
    n2 = 1
    l = 'a'
    flag = 1
    while(flag == 1): #checks x coordinate 
        if position_x >= n1*squaresize+x_offset-20 and position_x<=n2*squaresize+x_offset-20: 
            x = l; 
            flag = 0
        else: 
            n1+=1
            n2+=1
            l = chr(ord(l)+1)
        if (n2>19): 
            break

    n1 = 0 
    n2 = 1
    l = 19
    flag = 1
    while(flag == 1): #checks y coordinate 
        if position_y >= n1*squaresize+y_offset-20 and position_y<=n2*squaresize+y_offset-20: 
            y = l; 
            flag = 0
        else: 
            n1+=1
            n2+=1
            l -=1
        if (n2>19): 
            break
    if x =="" or y =="": 
        x = ""
        y = ""     
    
    return x+str(y)

#checks to see if the x and y values of the click has a enemy piece or player piece 
def isPiecePresent(x,y):
    selection_coordinates = (0,0)
    for px,py in position_list:
        if (x>=px and x<px+squaresize) and (y>=py and y<py+squaresize):
            selection_coordinates=(px,py)
            break
    return selection_coordinates
     


def run(): 
    global screen
    screen=pygame.display.set_mode((screen_width,screen_height))
    running = True 
    while(running):
        layout,r,c = read_file(board_file)
        while(not layout and not r and not c): 
            layout,r,c = read_file(board_file)
        old_layout= deepcopy(layout) #keeps an initial copy for comparison later

        # for i in range(r): 
        #     for j in range(c):
        #         print(layout[i][j],end="") 
        #     print("")
        # print("")
        drawboard()
        drawPieces(layout) 
       
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                output_file=open("output.txt", "w")
                output_file.write("exit")
                output_file.close()
                os.remove("output.txt")
                running=False
            if event.type == pygame.MOUSEBUTTONDOWN:
                x,y = pygame.mouse.get_pos() 
                position = determine_position(x,y)
                print(position)

        pygame.display.update()
