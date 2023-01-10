#Author: Dhananjay Puranik, Tuffle 2023

#Loading Modules
import pygame as pg
from sys import exit

#Initializing Pygame
pg.init()

#Creating Window
width=600
height=600
win=pg.display.set_mode((width,height))

#Loading Images and setting the rects
board_img=pg.image.load("assets/board.png").convert_alpha()

font=pg.font.Font("assets/arial.ttf",24)
label_info=font.render("Player 1 chance",True,(255,255,255))
label_info_rect=label_info.get_rect(center=(300,30))

cross_img=pg.image.load("assets/cross.png").convert_alpha()
circle_img=pg.image.load("assets/circle.png").convert_alpha()

button_img=pg.image.load("assets/button.png").convert_alpha()
button_img_rect=button_img.get_rect(center=(300,550))

#setting global variables for game
block_size=120
is_player1_chance=True
someone_won=False
pos=(0,0)
chance_count=0
result=None
pieces=[]
matrix=[
    ['-','-','-'],
    ['-','-','-'],
    ['-','-','-']
]
clock=pg.time.Clock()

#function to check if the clicked position is a valid position
def checkClickedPosition(pos):
    if (pos[0]>120 and pos[0]<240) and (pos[1]>120 and pos[1]<240):
        return (1,1)
    elif (pos[0]>240 and pos[0]<360) and (pos[1]>120 and pos[1]<240):
        return (1,2)
    elif (pos[0]>360 and pos[0]<480) and (pos[1]>120 and pos[1]<240):
        return (1,3)
    elif (pos[0]>120 and pos[0]<240) and (pos[1]>240 and pos[1]<360):
        return (2,1)
    elif (pos[0]>240 and pos[0]<360) and (pos[1]>240 and pos[1]<360):
        return (2,2)
    elif (pos[0]>360 and pos[0]<480) and (pos[1]>240 and pos[1]<360):
        return (2,3)
    elif (pos[0]>120 and pos[0]<240) and (pos[1]>360 and pos[1]<480):
        return (3,1) 
    elif (pos[0]>240 and pos[0]<360) and (pos[1]>360 and pos[1]<480):
        return (3,2) 
    elif (pos[0]>360 and pos[0]<480) and (pos[1]>360 and pos[1]<480):
        return (3,3) 
    return None

#function to check if someone wins
def checkCompletion(matrix):
    for i in range(0,3):
        if matrix[i][0]==matrix[i][1]==matrix[i][2]:
            if matrix[i][0]=="x":
                winner="Player 1 is winner"
            elif matrix[i][0]=="o":
                winner="Player 2 is winner"
            if matrix[i][0]!="-":
                return winner,(120,120*(i+1)+60),(480,120*(i+1)+60) 
    
    for i in range(0,3):
        if matrix[0][i]==matrix[1][i]==matrix[2][i]:
            if matrix[0][i]=="x":
                winner="Player 1 is winner"
            elif matrix[0][i]=="o":
                winner="Player 2 is winner"
            if matrix[0][i]!="-":
                return winner,(120*(i+1)+60,120),(120*(i+1)+60,480)
    
    if matrix[0][0]==matrix[1][1]==matrix[2][2]:
        if matrix[0][0]=="x":
            winner="Player 1 is winner"
        elif matrix[0][0]=="o":
            winner="Player 2 is winner"
        if matrix[0][0]!="-":
            return winner,(120,120),(480,480)
    
    if matrix[0][2]==matrix[1][1]==matrix[2][0]:
        if matrix[1][2]=="x":
            winner="Player 1 is winner"
        elif matrix[1][2]=="o":
            winner="Player 2 is winner"
        if matrix[0][2]!="-":
            return winner,(480,120),(120,480)
    
    return "No one is winner",(0,0)

#function to restart the game 
def restart():
    global is_player1_chance,someone_won,pos,chance_count,result,pieces,matrix,label_info
    is_player1_chance=True
    someone_won=False
    pos=(0,0)
    chance_count=0
    result=None
    pieces=[]
    matrix=[
        ['-','-','-'],
        ['-','-','-'],
        ['-','-','-']
    ]
    label_info=font.render("Player 1 chance",True,(255,255,255))

#game loop
while True:
    #event handling
    for event in pg.event.get():
        if event.type==pg.QUIT:
            pg.quit()
            exit()
        if event.type==pg.MOUSEBUTTONUP:
            pos=pg.mouse.get_pos()
        if event.type==pg.MOUSEBUTTONDOWN:
            if button_img_rect.collidepoint(pg.mouse.get_pos()):
                restart()

    #check clicked position validation
    result=checkClickedPosition(pos)

    #logic to place cross and circle
    if result!=None:
        if matrix[result[0]-1][result[1]-1]=="-":
            if is_player1_chance:
                pieces.append([cross_img,block_size*result[1]+20,block_size*result[0]+20])
                is_player1_chance=False
                matrix[result[0]-1][result[1]-1]="x"
                label_info=font.render("Player 2 chance",True,(255,255,255))
            else:
                pieces.append([circle_img,block_size*result[1]+20,block_size*result[0]+20])
                is_player1_chance=True
                matrix[result[0]-1][result[1]-1]="o"
                label_info=font.render("Player 1 chance",True,(255,255,255))
            chance_count+=1

            temp=checkCompletion(matrix)
            if temp[1]!=(0,0):
                label_info=font.render(temp[0],True,(255,255,255))
                someone_won=True

    #reset pos
    pos=(0,0)  

    #draw everything on screen
    win.fill((18,18,18))
    win.blit(board_img,(120,120))
    win.blit(label_info,label_info_rect)

    for piece in pieces:
        win.blit(piece[0],(piece[1],piece[2]))

    if someone_won==True or chance_count==9:
        if someone_won:
            pg.draw.line(win,(255,255,255),temp[1],temp[2])
        else:
            label_info=font.render(temp[0],True,(255,255,255))

        win.blit(button_img,button_img_rect)

    pg.display.update()
    clock.tick(60)


