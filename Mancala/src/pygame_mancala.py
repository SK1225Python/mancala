import pygame
from pygame.locals import *
import sys
import random
import time
import copy
import threading

class Place:
    def __init__(self, myplace, mystore, couterplace, couterstore, eachStone, counterEachStone):
        self._myplace = myplace 
        self._mystore = mystore
        self._couterplace = couterplace
        self._couterstore = couterstore
        self._eachStone = eachStone
        self._counterEachStone = counterEachStone
        self._place = [0] * (myplace+mystore+couterplace+couterstore)
        self.initPlace(myplace, mystore, couterplace, couterstore, eachStone, counterEachStone)
    
    def sumHole(self):
        return self._myplace+self._mystore+self._couterplace+self._couterstore
    
    def getPlayerIniNum(self):
        return 0
    
    def getPlayerEndNum(self):
        return self._myplace 
    
    def getCounterIniNum(self):
        return self._myplace + self._mystore
    
    def getCounterEndNum(self):
        return self._myplace + self._mystore + self._couterplace - 1

    def initPlace(self, myplace, mystore, couterplace, couterstore, eachStone, counterEachStone):
        self._place = [0] * (myplace+mystore+couterplace+couterstore)
        for i in range(myplace):
            self._place[i] = eachStone
        
        for i in range(couterplace):
            num = i + myplace + mystore
            self._place[num] = counterEachStone
            
    def getEachPlace(self, num):
        return self._place[num]
    
    def setEachPlace(self, num, value):
        self._place[num] = value
        
    def addEachPlace(self, num, value):
        self._place[num] = self._place[num] + value
        
    def checkWinner(self, output):
        ret = False
        
        tempStart = self.getCounterIniNum()
        tempEnd = self.getCounterEndNum() + 1
        
        if sum(self._place[0:self._myplace])==0 :
            if output : print("You Win!")
            ret = True
        elif sum(self._place[tempStart:tempEnd])==0 :
            if output : print("You lose!")
            ret = True
            
        return ret
    
    def checkWhichWinner(self):
        tempStart = self.getCounterIniNum()
        tempEnd = self.getCounterEndNum() + 1
        if sum(self._place[0:self._myplace])==0 :
            return 0
        elif sum(self._place[tempStart:tempEnd])==0 :
            return 1
    
    # 評価関数
    def calcValue(self):
        tempStart = self.getCounterIniNum()
        tempEnd = self.getCounterEndNum() + 1   
        value = sum(self._place[0:self._myplace]) - sum(self._place[tempStart:tempEnd])
        return value
    
    def display(self):
        print("  {}**{}**{}  ".format(self._place[6],self._place[5],self._place[4]))
        print("{}*********{}".format(self.getEachPlace(7),self.getEachPlace(3)))
        print("  {}**{}**{}  ".format(self.getEachPlace(0),self.getEachPlace(1),self.getEachPlace(2)))

def calcCPU(place):
    number = random.randint(place.getCounterIniNum(), place.getCounterEndNum())
    while place.getEachPlace(number) == 0:
        number = random.randint(place.getCounterIniNum(), place.getCounterEndNum())
        
    return number

def debugMessage(str):
    debugMessage = True
    if debugMessage == True:
        print(str)

def calcCpuMinMax(place, turn, depth, initFlag):
    
    temp_place = copy.deepcopy(place)
    state = temp_place.checkWinner(False)
    value = 0
    nextAction = -1
    temp_depth = depth
    
    #debugMessage("状態:{},　深さ:{}".format(state,temp_depth))
    if state or depth == 0:
        value = temp_place.calcValue()
        #debugMessage("状態:{},　深さ:{}, 最深部評価値:{}".format(state, temp_depth, value))
        return value
    
    # player or counterの手の分だけループ
    #debugMessage("turn:{}".format(turn))
    if turn == 1:
        best = 10000
        for i in range(0, temp_place.getPlayerEndNum()):
            temp_place = copy.deepcopy(place)
            if temp_place.getEachPlace(i) == 0:
                continue
            sowing(temp_place, i)
            #temp_place.display()
            value = calcCpuMinMax(temp_place, turn*(-1), temp_depth-1, False)
            if best > value:
                #debugMessage("途中評価値:{}".format(value))
                best = value
    elif turn == -1:
        best = -10000
        for i in range(temp_place.getCounterIniNum(), temp_place.getCounterEndNum()+1):
            temp_place = copy.deepcopy(place)
            #debugMessage("i:{}".format(i))
            if temp_place.getEachPlace(i) == 0:
                continue
            sowing(temp_place, i)
            #temp_place.display()
            value = calcCpuMinMax(temp_place, turn*(-1), temp_depth-1, False)
            if best < value:
                #debugMessage("CPUの評価値:{},CPUの次の手:{}".format(value,i))
                best = value
                nextAction = i
    else:
        print("error")
                 
    if not initFlag:
        #debugMessage("評価値:{}".format(best))
        return best
    else:
        debugMessage("次の手:{}".format(i))
        return nextAction

def calcCpuAlphaBeta(place, turn, depth, alpha, beta, initFlag):
    
    temp_place = copy.deepcopy(place)
    state = temp_place.checkWinner(False)
    value = 0
    nextAction = -1
    temp_depth = depth
    
    #debugMessage("状態:{},　深さ:{}".format(state,temp_depth))
    if state or depth == 0:
        value = temp_place.calcValue()
        #debugMessage("状態:{},　深さ:{}, 最深部評価値:{}".format(state, temp_depth, value))
        return value
    
    # player or counterの手の分だけループ
    #debugMessage("turn:{}".format(turn))
    if turn == 1:
        value = 10000
        for i in range(0, temp_place.getPlayerEndNum()):
            temp_place = copy.deepcopy(place)
            if temp_place.getEachPlace(i) == 0:
                continue
            sowing(temp_place, i)
            #temp_place.display()
            beta = min(beta, calcCpuAlphaBeta(temp_place, turn*(-1), temp_depth-1, alpha, beta, False))
            if value > beta:
                value = beta
                if alpha > beta:
                    #debugMessage("alphaカット")
                    return value     
    elif turn == -1:
        value = -10000
        for i in range(temp_place.getCounterIniNum(), temp_place.getCounterEndNum()+1):
            temp_place = copy.deepcopy(place)
            #debugMessage("i:{}".format(i))
            if temp_place.getEachPlace(i) == 0:
                continue
            sowing(temp_place, i)
            #temp_place.display()
            alpha = max(alpha, calcCpuAlphaBeta(temp_place, turn*(-1), temp_depth-1, alpha, beta, False))
            if alpha > value:
                value = alpha
                nextAction = i
                if alpha > beta :
                    #debugMessage("betaカット")
                    return value
    else:
        print("error")
              
    if not initFlag:
        #debugMessage("評価値:{}".format(value))
        return value
    else:
        debugMessage("次の手:{}".format(i))
        return nextAction
    
def sowing(place, number):
    temp = place.getEachPlace(number)
    place.setEachPlace(number, 0)
    while temp >= 1:
        num = (number+temp)%place.sumHole()
        place.addEachPlace(num, 1)
        temp = temp - 1
        
class Counter(threading.Thread):

    def __init__(self, thread_name):
        self.thread_name = str(thread_name)
        threading.Thread.__init__(self)

    def __str__(self):
        return self.thread_name

    def run(self):
        print('Timer: %s started.' % self)
        sleep_seconds = random.randint(5, 10)
        time.sleep(sleep_seconds)
        print('Timer: %s ended.' % self)
                
def main():
    VIEW_WIDTH = 600
    VIEW_HEIGT = 400
    STORE_WIDTH = 100
    MAX_NUMBER_SEEDS = 5 #各穴に横に並べられる最大数
    TABLE_X = 10
    TABLE_Y = 10
    
    COLOR_HOLES = (255,255,255)
    COLOR_SEEDS = (255,217,0)
    COLOR_TABLE = (0,51,0)

    myPlace = 4
    myStore = 1
    counterPlace = 4
    counterStore = 1
    myEachStone = 3
    counterEachStone = 3
    seedWidth = 10
    seedHeight = 10
    seedDeltaX = 10
    seedDeltaY = 10

    storeWidth = STORE_WIDTH
    myStorePosition = VIEW_WIDTH - STORE_WIDTH - TABLE_X
    couterStorePosition = TABLE_X
    myPlaceWidth = (VIEW_WIDTH-2*TABLE_X-2*STORE_WIDTH)/myPlace
    couterPlaceWidth =(VIEW_WIDTH-2*TABLE_X-2*STORE_WIDTH)/counterPlace
    myHoleStartPosition = TABLE_X + storeWidth
    couterHoleStartPosition = TABLE_X + storeWidth
    
    placeHeight =(VIEW_HEIGT-2*TABLE_Y)/3
    
    place = Place(myPlace, myStore, counterPlace, counterStore, myEachStone, counterEachStone)
    place.display()
    
    endFlag = False
    counterTurn = random.randint(0, 1) #先攻後攻を決める
    count = 10
    
    pygame.init() # Pygameの初期化
    screen = pygame.display.set_mode((VIEW_WIDTH, VIEW_HEIGT))
    pygame.display.set_caption("Mancala v0.9") # タイトルバーに表示する文字
    font = pygame.font.Font(None, 55) 

    while (1):
        screen.fill(COLOR_TABLE)      

        # draw stores
        pygame.draw.rect(screen,COLOR_HOLES,
                         Rect(myStorePosition,TABLE_Y+placeHeight,storeWidth,placeHeight),5) 
        pygame.draw.rect(screen,COLOR_HOLES,
                         Rect(couterStorePosition,TABLE_Y+placeHeight,storeWidth,placeHeight),5) 
        
        # draw holes
        for i in range(0, myPlace):
            pygame.draw.rect(screen,COLOR_HOLES,
                             Rect(myHoleStartPosition+(myPlaceWidth*i),TABLE_Y+placeHeight*2,myPlaceWidth,placeHeight),5) 

        for i in range(0, counterPlace):
            pygame.draw.rect(screen,COLOR_HOLES,
                             Rect(couterHoleStartPosition+(couterPlaceWidth*i),TABLE_Y,couterPlaceWidth,placeHeight),5) 
        
        # draw seeds(player)
        for i in range(0, myPlace):
            seedx = couterStorePosition+storeWidth+(myPlaceWidth*i)+seedDeltaX
            seedy = TABLE_Y+placeHeight*2 + seedDeltaY
            for j in range(place.getEachPlace(i)):
                pygame.draw.ellipse(screen,COLOR_SEEDS,
                                    Rect(seedx+(j%MAX_NUMBER_SEEDS)*seedWidth, 
                                         seedy+(j//MAX_NUMBER_SEEDS+1)*seedWidth,
                                         seedWidth,seedHeight)) 
            
        for j in range(place.getEachPlace(myPlace)):
            pygame.draw.ellipse(screen,COLOR_SEEDS,
                                Rect(myStorePosition+(j%MAX_NUMBER_SEEDS)*seedWidth+seedDeltaX,
                                     TABLE_Y+placeHeight+(j//MAX_NUMBER_SEEDS+1)*seedWidth,
                                     seedWidth,seedHeight)) 
        
        # draw seeds(counter) 
        for i in range(myPlace+myStore, myPlace+myStore+counterPlace):
            seedx = myStorePosition-(i-myPlace)*couterPlaceWidth+seedDeltaX
            seedy = TABLE_Y + seedDeltaY
            for j in range(place.getEachPlace(i)):
                pygame.draw.ellipse(screen,COLOR_SEEDS,
                                    Rect( seedx + (j%MAX_NUMBER_SEEDS)*seedWidth, 
                                          seedy+(j//MAX_NUMBER_SEEDS+1)*seedWidth ,
                                          seedWidth,seedHeight)) 
                
        for j in range(place.getEachPlace(myPlace+myStore+counterPlace)):
            pygame.draw.ellipse(screen,COLOR_SEEDS,
                                Rect((j%MAX_NUMBER_SEEDS)*seedWidth+seedDeltaX,
                                     TABLE_Y+placeHeight+(j//MAX_NUMBER_SEEDS+1)*seedWidth,
                                     seedWidth,seedHeight)) 
        
        if not endFlag:
            if counterTurn == 0:
                text = font.render("ENEMY's TURN:"+str(count), True, (0,255,217))   # 描画する文字列の設定
            else:
                text = font.render("YOUR TURN", True, (255,221,153))   # 描画する文字列の設定  
        else:
            if place.checkWhichWinner()==0:
                text = font.render("YOU WIN!!", True, (255,170,153)) 
            else:
                text = font.render("YOU LOSE!!", True, (153,153,255)) 
        
        screen.blit(text, [150, 175])
        pygame.display.update() 
                
        if not endFlag:
            if count <= 0:
                if counterTurn == 0: #CPUが先行の場合
                    #calcCpuMinMax(place, turn, depth, initFlag)
                    #counterpartInput = calcCpuMinMax(place, -1, 6, True) #calcCPU(place)
                    counterpartInput = calcCpuAlphaBeta(place, -1, 6,-10000, 10000, True) #calcCPU(place)
                    print('CPUの選択は {} です'.format(counterpartInput))
                    sowing(place, counterpartInput)
                    place.display()
                    endFlag = place.checkWinner(True)
                    counterTurn = 1
            else:
                count = count -1
    
        # イベント処理
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONDOWN and event.button == 1:
                if not endFlag:
                    playerInput = -1
    
                    if counterTurn == 1:
                        x, y = event.pos
                        if y > placeHeight*2:
                            for i in range(0, myPlace):
                                if (x > storeWidth + myPlaceWidth * i and x < storeWidth + myPlaceWidth * (i+1)) :
                                    if place.getEachPlace(i)>0 :
                                        playerInput = i
                                        break
                                else:
                                    playerInput = -1
                
                        if playerInput != -1:
                            print('あなたの選択は {} です'.format(playerInput))
                            sowing(place, int(playerInput))
                            place.display()
                            endFlag = place.checkWinner(True)
                        
                            if not endFlag:
                                counterTurn = 0
                                count = 10
                    
            if event.type == QUIT:
                pygame.quit()       
                sys.exit()
                
            if event.type == KEYDOWN:       # キーを押したとき
                if event.key == K_ESCAPE:   # Escキーが押されたとき
                    pygame.quit()
                    sys.exit()

if __name__ == "__main__":
    main()