#!/usr/bin/env python
# coding: utf-8

# In[1]:

#import stuff
import math
import pygame
from pygame.locals import *

#values of the board
ROWS = 6 #should be impossible to win if rows = 5
COLS = 7
board = [[0]*COLS for i in range(ROWS)]

#points                           4 in a row is a win
score_dict = {0:0,1:1,2:30,3:500,4:999999999999999}
winning_score = 999999999999999
threshhold = 900000000000000

#pygame colors
COLOR_RED = pygame.Color(255,0,0)
COLOR_GREEN = pygame.Color(0,255,0)
COLOR_BLUE = pygame.Color(0,0,255)
COLOR_WHITE = pygame.Color(255,255,255)
COLOR_BLACK = pygame.Color(0,0,0)
COLOR_GREY = pygame.Color(128,128,128)


# In[2]:


from IPython.display import clear_output
from pygame import font

class GameState():
    def __init__(self, state=None):
        self.board = [[0]*COLS for i in range(ROWS)]
        #change the board to a certain state
        if (state!=None):
            for i in range(ROWS):
                for j in range(COLS):
                    self.board[i][j] = state.board[i][j]
            self.player = state.player
        else:
            self.player = 1

    def printboard(self):
        #printing the board/tokens
        pygame.draw.rect(DISPLAYSURF,COLOR_WHITE,(0,100,900,700))
        pygame.display.set_caption("Connect 4")
        pygame.draw.rect(DISPLAYSURF,COLOR_BLACK,(100,100,700,600))
        for j in range(ROWS):
            for i in range(COLS):
                if self.board[j][i] == 0:
                    pygame.draw.circle(DISPLAYSURF,COLOR_WHITE,(150+100*i,150+100*j),25)
                elif self.board[j][i] == -1:
                    pygame.draw.circle(DISPLAYSURF,COLOR_RED,(150+100*i,150+100*j),25)
                else:
                    pygame.draw.circle(DISPLAYSURF,COLOR_BLUE,(150+100*i,150+100*j),25)

        #user input buttons
        for i in range(COLS):
            rect = Rect(110+100*i, 110+100*ROWS, 75, 50)
            pygame.draw.rect(DISPLAYSURF,COLOR_GREY,rect)
            textObj = arialFont.render(f"   {i}   ", True, COLOR_BLACK)
            textRect = textObj.get_rect()
            textRect.center = (140+100*i,130+100*ROWS)
            DISPLAYSURF.blit(textObj,textRect)
            
        #restart button
        rect = Rect(10,10,150,50)
        pygame.draw.rect(DISPLAYSURF,COLOR_GREY,rect)
        textObj = arialFont.render("Restart",True, COLOR_BLACK)
        textRect = textObj.get_rect()
        textRect.center = (75,30)
        DISPLAYSURF.blit(textObj,textRect)
        
        pygame.display.update()
    
    def insert(self,player,col):
        if col < 0 or col > (COLS-1):
            print(f'please enter a valid number (0-{COLS-1})')
            return False
        
        i = ROWS-1
        while i>=0:
            if self.board[i][col] == 0:
                self.board[i][col] = player
                return True

            else:
                i-=1

        #print('sorry, column is full')
        return False
    
    #check is there is a 4 in a row horizontally
    def checkRow(self):
        for i in range(ROWS):
            count = 0
            for j in range(COLS):
                if self.board[i][j]==self.player:
                    count += 1
                else:
                    count = 0
                if count >= 4:
                    return True
        return False

    #check is there is a 4 in a row vertically
    def checkCol(self):
        for i in range(COLS):
            count = 0
            for j in range(ROWS):
                if self.board[j][i]==self.player:
                    count += 1
                else:
                    count = 0
            if count >= 4:
                return True
        return False
    
    #check is there is a 4 in a row diagionally (top left to bottom right)
    def checkDia_TL_BR(self):
        hori = 0
        vert = 0
        count = 0
        for i in range(COLS):
            hori = i
            vert = 0
            count = 0
            while hori < COLS and vert < ROWS:
                if self.board[vert][hori] == self.player:
                    count +=1
                else:
                    count = 0

                hori += 1
                vert += 1
                #print(count)

                if count >= 4:
                    return True

        for i in range(ROWS):
            hori = 0
            vert = i
            count = 0
            while hori < COLS and vert < ROWS:
                if self.board[vert][hori] == self.player:
                    count +=1
                else:
                    count = 0

                hori += 1
                vert += 1
                #print(count)

                if count >= 4:
                    return True
        return False
    
    #check is there is a 4 in a row diagionally (top right to bottom left)
    def checkDia_TR_BL(self):
        hori = 0
        vert = 0
        count = 0
        for i in reversed(range(COLS)):
            hori = i
            vert = 0
            count = 0
            while hori >= 0 and vert < ROWS:
                if self.board[vert][hori] == self.player:
                    count +=1
                else:
                    count = 0

                hori -= 1
                vert += 1
                #print(count)

                if count >= 4:
                    return True

        for i in range(ROWS):
            hori = (COLS-1)
            vert = i
            count =0
            while hori >= 0 and vert < ROWS:
                if self.board[vert][hori] == self.player:
                    count +=1
                else:
                    count = 0

                hori -= 1
                vert += 1
                #print(count)

                if count >= 4:
                    return True
        return False
    
    #check if there is a winner
    def checkwinner(self):
        return (self.checkRow() or self.checkCol() or self.checkDia_TL_BR() or self.checkDia_TR_BL())
    
    #changes player value
    def switchplayer(self):
        self.player = self.player*(-1)
    
    #computes values of rows
    def computeRow(self):
        score = 0
        for i in range(ROWS):
            count = 0
            token = 1 #player 1
            zero_start = False
            for j in range(COLS):
                if count == 4:
                        return (winning_score * token)
                    
                if self.board[i][j] == token:
                    count +=1

                elif self.board[i][j] == 0:
                    if zero_start:
                        score += (score_dict[count] * token * 2)
                    else:
                        score += (score_dict[count] * token)
                        
                    count = 0
                    zero_start = True

                else:
                    if zero_start:
                        score += (score_dict[count] * token)
                    else:
                        score += (count * token)
                        
                    if count != 0:
                        zero_start = False
                    count = 1
                    token = token * -1
                    
                    
            if count == 4:
                        return (winning_score * token)
                
            if zero_start:
                score += (score_dict[count] * token)
            else:
                score += (count * token)
            

        return score

    #computes values of columns
    def computeColumn(self):
        score = 0
        for j in range(COLS):
            count = 0
            token = 1 #player 1 (O)
            zero_start = False
            for i in range(ROWS):
                if count == 4:
                        return (winning_score * token)
                    
                if self.board[i][j] == token:
                    count +=1

                elif self.board[i][j] == 0:
                    if zero_start:
                        score += (score_dict[count] * token * 2)
                    else:
                        score += (score_dict[count] * token)
                        
                    count = 0
                    zero_start = True

                else:
                    if zero_start:
                        score += (score_dict[count] * token)
                    else:
                        score += (count * token)
                        
                    if count != 0:
                        zero_start = False
                    count = 1
                    token = token * -1
                    
            if count == 4:
                        return (winning_score * token)
                
            if zero_start:
                score += (score_dict[count] * token)
            else:
                score += (count * token)
            

        return score

    #computes values of diagonals (top left to bottom right)
    def computeDia_TL_BR(self):
        score = 0
        for i in range(COLS):
            count = 0
            token = 1 #(O)
            zero_start = False
            hori = i
            vert = 1
            while hori < COLS and vert < ROWS:
                if count == 4:
                        return (winning_score * token)
                    
                if self.board[vert][hori] == token:
                    count += 1

                elif self.board[vert][hori] == 0:
                    if zero_start:
                        score += (score_dict[count] * token * 2)
                    else:
                        score += (score_dict[count] * token)
                        
                    count = 0
                    zero_start = True

                else:
                    if zero_start:
                        score += (score_dict[count] * token)
                    else:
                        score += (count * token)
                        
                    if count != 0:
                        zero_start = False
                    count = 1
                    token = token * -1
                
                hori += 1
                vert += 1
                    
            if count == 4:
                        return (winning_score * token)
                
            if zero_start:
                score += (score_dict[count] * token)
            else:
                score += (count * token)
            
            
        for i in range(ROWS):
            count = 0
            token = 1 #(O)
            zero_start = False
            hori = 0
            vert = i
            while hori < COLS and vert < ROWS:
                if count == 4:
                        return (winning_score * token)
                    
                if self.board[vert][hori] == token:
                    count += 1

                elif self.board[vert][hori] == 0:
                    if zero_start:
                        score += (score_dict[count] * token * 2)
                    else:
                        score += (score_dict[count] * token)
                        
                    count = 0
                    zero_start = True

                else:
                    if zero_start:
                        score += (score_dict[count] * token)
                    else:
                        score += (count * token)
                        
                    if count != 0:
                        zero_start = False
                    count = 1
                    token = token * -1
                
                hori += 1
                vert += 1
                    
            if count == 4:
                        return (winning_score * token)
                
            if zero_start:
                score += (score_dict[count] * token)
            else:
                score += (count * token)
                
        return score
    
    #computes values of diagonals (top right to bottom left)
    def computeDia_TR_BL(self):
        score = 0
        for i in reversed(range(COLS)):
            count = 0
            token = 1 #(O)
            zero_start = False
            hori = i
            vert = 1
            while hori >= 0 and vert < ROWS:
                if count == 4:
                        return (winning_score * token)
                    
                if self.board[vert][hori] == token:
                    count += 1

                elif self.board[vert][hori] == 0:
                    if zero_start:
                        score += (score_dict[count] * token * 2)
                    else:
                        score += (score_dict[count] * token)
                        
                    count = 0
                    zero_start = True

                else:
                    if zero_start:
                        score += (score_dict[count] * token)
                    else:
                        score += (count * token)
                        
                    if count != 0:
                        zero_start = False
                    count = 1
                    token = token * -1
                
                hori -= 1
                vert += 1
                    
            if count == 4:
                        return (winning_score * token)
                
            if zero_start:
                score += (score_dict[count] * token)
            else:
                score += (count * token)
            
            
        for i in range(ROWS):
            count = 0
            token = 1 #(O)
            zero_start = False
            hori = (COLS-1)
            vert = i
            while hori >= 0 and vert < ROWS:
                if count == 4:
                        return (winning_score * token)
                    
                if self.board[vert][hori] == token:
                    count += 1

                elif self.board[vert][hori] == 0:
                    if zero_start:
                        score += (score_dict[count] * token * 2)
                    else:
                        score += (score_dict[count] * token)
                        
                    count = 0
                    zero_start = True

                else:
                    if zero_start:
                        score += (score_dict[count] * token)
                    else:
                        score += (count * token)
                        
                    if count != 0:
                        zero_start = False
                    count = 1
                    token = token * -1
                
                hori -= 1
                vert += 1
                    
            if count == 4:
                        return (winning_score * token)
                
            if zero_start:
                score += (score_dict[count] * token)
            else:
                score += (count * token)
                
        return score
    
    #total score of the whole board
    def computeScore(self):
        return (self.computeRow() + self.computeColumn() + self.computeDia_TL_BR() + self.computeDia_TR_BL())
    
    #funtion used for game on the terminal, in pygame user is always blue
    def choice(self):
        choice = input("Which player goes first, X or O: ")
        while choice.upper() not in ['X','O']:
            choice = input('Please enter X or O: ')

        if choice.upper() == 'X':
            return -1
        else:
            return 1
    
    #check if there is a tie (if the board is full but no winner)
    def check_tie(self):
        for i in self.board:
            for j in i:
                if j == 0:
                    return False
        return True
    
    #check position of moousepress
    def buttonCheck(self,mousePos):
        #INPUT: x,y coordinate of mousepress (tuple)
        #output: 0,1,2,3,4,5,6,or -1
        x,y = mousePos
        ans = None
        #check for button press 0-6
        for i in range(COLS):
            left = 100+100*i
            right = left+75
            top = 110+100*ROWS
            bot = top + 50
            if x >= left and x <= right and y >= top and y<=bot:
                ans = i
        #check for restart button
        if x >= 10 and x<=160 and y >=10 and y<=60:
            ans = -999
        
        if ans == None:
            return -1
        else:
            return ans
        
    #text on screen
    def selectPos(self):
        #pygame.draw.rect(DISPLAYSURF,COLOR_WHITE,(0,0,900,100))
        textObj = arialFont.render("Select a Position", True, COLOR_BLACK)
        textRect = textObj.get_rect()
        textRect.center = (450,50)
        DISPLAYSURF.blit(textObj,textRect)
        pygame.display.update()
    
    #text on screen
    def fullColumn(self):
        #pygame.draw.rect(DISPLAYSURF,COLOR_WHITE,(0,0,900,100))
        textObj = arialFont.render(f"Please Press on A Valid Position", True, COLOR_BLACK)
        textRect = textObj.get_rect()
        textRect.center = (450,50)
        DISPLAYSURF.blit(textObj,textRect)
        pygame.display.update()
    
    #clear text (at the top) by making it white
    def clearText(self):
        pygame.draw.rect(DISPLAYSURF,COLOR_WHITE,(160,0,900,100))

    #moving text at the end of the game
    def movingTitle(self, text, color):
        x = 1100
        while x>=450:
            self.clearText()
            textObj = arialFont.render(f'{text}', True, color)
            textRect = textObj.get_rect()
            textRect.center = (x,50)
            DISPLAYSURF.blit(textObj,textRect)
            pygame.display.update()
            x -= 5
            #framerate
            clock.tick(120)

# In[3]:

#### 1 player vs robot (check 3 step ahead)
restart = True
quit = False
pygame.init()
clock = pygame.time.Clock()

#game loop
while restart and (not quit):
    # setup game
    restart = False
    game = GameState()
    game_over = False
    game_tie = False
    #print("BLUE goes first")
    #background is 900 x 800 pixels
    DISPLAYSURF = pygame.display.set_mode((900,800))
    #set the background to white
    DISPLAYSURF.fill(COLOR_WHITE)

    font.init()
    #text is arial, 40
    arialFont = pygame.font.SysFont("Arial", 40)

    while (not game_over) and (not game_tie) and (not quit) and (not restart):
#         game.printboard()
#         for event in pygame.event.get():
#             if event.type == QUIT:
#                 game_over = True
#                 quit = True
#             if event.type == pygame.MOUSEBUTTONUP:
#                 mousePos = event.pos
#                 print(mousePos)
#                 selection = game.buttonCheck(mousePos)

        game.printboard()

        #user's move
        if game.player == 1:
            #print('select a position')
            #displays 'select a position' on the board
            game.clearText()
            game.selectPos()

            selection = -1
            while (selection != -999) and (not quit) and ((selection < 0) or (not game.insert(game.player,selection))):
                if selection != -1:
                    game.clearText()
                    game.fullColumn()
                selection = -1
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONUP:
                        mousePos = event.pos
                        selection = game.buttonCheck(mousePos)
                    elif event.type == QUIT:
                        quit = True
            #check if placed token or restart
            if selection == -999:
                restart = True

        #bots move
        else:
            game.printboard()
            #all possible gamestates
            game_stateTop = []
            game_stateMid = []
            game_stateBot = []
            game_scoreTop = []
            game_scoreMid = []
            game_scoreBot = []
            for i in range(COLS):
                a = GameState(game)
                if (a.insert(game.player,i)):
                    game_stateTop.append(a)
                else:
                    game_stateTop.append(None)
            for i in range(len(game_stateTop)):
                for j in range(COLS):
                    a = GameState(game_stateTop[i])
                    a.switchplayer()
                    if (a.insert(a.player,j)):
                        game_stateMid.append(a)
                    else:
                        game_stateMid.append(None)
            for i in range(len(game_stateMid)):
                for j in range(COLS):
                    a = GameState(game_stateMid[i])
                    a.switchplayer()
                    if (a.insert(a.player,j)):
                        game_stateBot.append(a)
                    else:
                        game_stateBot.append(None)

            for i in range(len(game_stateBot)):
                if game_stateBot[i] != None:
                    game_scoreBot.append(game_stateBot[i].computeScore())
                else:
                    game_scoreBot.append(None)

            for i in range(len(game_stateMid)): #0-6,7-13,14-20,21-27
                if game_stateMid[i] == None:
                    game_scoreMid.append(None)
                elif game_stateMid[i].computeScore() > threshhold: #winning isn't infinity anymore so the value can still be changed
                    game_scoreMid.append(winning_score) #player wins
                else:
                    min_value = winning_score
                    allNone = True
                    for score in game_scoreBot[(COLS*i):(COLS*(i+1))]:
                        if (score != None):
                            allNone = False
                            if (score < min_value):
                                min_value = score
                    if allNone:
                        game_scoreMid.append(None)
                    else:
                        game_scoreMid.append(min_value)

            for i in range(len(game_stateTop)):
                if game_stateTop[i] == None:
                    game_scoreTop.append(None)
                elif game_stateTop[i].computeScore() == (winning_score*-1):
                    game_scoreTop.append(winning_score*-1000) #bot wins
                else:
                    max_value = winning_score*-1
                    allNone = True
                    for score in game_scoreMid[COLS*i:COLS*(i+1)]:
                        if (score != None):
                            allNone = False
                            if score > max_value:
                                max_value = score
                    if allNone:
                        game_scoreTop.append(None)
                    else:
                        game_scoreTop.append(max_value)
            #print(game_scoreTop)
            #print(game_scoreMid[35:42])
            #print(game_stateMid[41].computeScore())
            min_index = 0
            min_value = winning_score
            i=0
            for score in game_scoreTop: #find min value + that index
                if (score != None) and (score < min_value):
                    min_value = score
                    min_index = i
                i+=1

            game.insert(game.player,min_index)

        #add animation of token to drop to correct column: dropAnimation(token, col)

        #check for game over, game tie, and switch player
        game_over = game.checkwinner()
        game_tie = game.check_tie()
        game.switchplayer()

    game.printboard()
    
    #end game scenarios
    if (not quit) and (not restart):
        if game_tie:
            game.movingTitle('TIE GAME!', COLOR_BLACK)
        elif game.player == -1:
            game.movingTitle('Winner is BLUE', COLOR_BLUE)
        else:
            game.movingTitle('Winner is RED', COLOR_RED)
        while (not quit) and (not restart):
            for event in pygame.event.get():
                if event.type == QUIT:
                    quit = True
                if event.type == pygame.MOUSEBUTTONUP:
                    mousePos = event.pos
                    selection = game.buttonCheck(mousePos)
                    if selection == -999:
                        restart = True

#close window
pygame.quit()


# In[ ]:




