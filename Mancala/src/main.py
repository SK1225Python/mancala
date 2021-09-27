import random
import time
import copy

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

def playerTurn(place):
    turnFlag = True
    playerInput = -1
    
    while turnFlag:
        print("数字を0 - {}の範囲から１つ選んでください".format(place.getPlayerEndNum()-1))
        playerInput = input()
        
        if not playerInput.isdecimal() :
            print("数字を入れてください")
            continue
        
        intPlayerInput = int(playerInput)
        if intPlayerInput < 0 or intPlayerInput >= place.getPlayerEndNum():
            print("数字は0 - {}までが有効です".format(place.getPlayerEndNum()-1))
            continue
        
        if place.getEachPlace(intPlayerInput) == 0:
            print("石がありません。別の場所を選んでください")
            continue
        
        turnFlag = False
    
    return playerInput

def calcCPU(place):
    number = random.randint(place.getCounterIniNum(), place.getCounterEndNum())
    while place.getEachPlace(number) == 0:
        number = random.randint(place.getCounterIniNum(), place.getCounterEndNum())
        
    return number

def debugMessage(str):
    debugMessage = False
    if debugMessage == True:
        print(str)

def calcCpuMinMax(place, turn, depth, initFlag):
    
    temp_place = copy.deepcopy(place)
    debugMessage(temp_place)
    state = temp_place.checkWinner(False)
    value = 0
    nextAction = -1
    temp_depth = depth
    
    debugMessage("state:{}, depth:{}".format(state,temp_depth))
    if state or depth == 0:
        value = temp_place.calcValue()
        debugMessage("value:{}".format(value))
        return value
    
    # player or counterの手の分だけループ
    if turn == 1:
        best = 10000
        debugMessage("turn:{}".format(turn))
        for i in range(0, temp_place.getPlayerEndNum()):
            temp_place = copy.deepcopy(place)
            if temp_place.getEachPlace(i) == 0:
                continue
            sowing(temp_place, i)
            #temp_place.display()
            value = calcCpuMinMax(temp_place, turn*(-1), temp_depth-1, False)
            if best >= value:
                debugMessage("value:{}".format(value))
                best = value
    elif turn == -1:
        best = -10000
        debugMessage("turn:{}".format(turn))
        for i in range(temp_place.getCounterIniNum(), temp_place.getCounterEndNum()+1):
            temp_place = copy.deepcopy(place)
            debugMessage("i:{}".format(i))
            if temp_place.getEachPlace(i) == 0:
                continue
            sowing(temp_place, i)
            #temp_place.display()
            value = calcCpuMinMax(temp_place, turn*(-1), temp_depth-1, False)
            if best <= value:
                debugMessage("cpu_turn_value:{}".format(value))
                debugMessage("cpu_turn_nextAction:{}".format(i))
                best = value
                nextAction = i
    else:
        print("error")
                 
    if not initFlag:
        debugMessage("best:{}".format(best))
        return best
    else:
        return nextAction

def sowing(place, number):
    temp = place.getEachPlace(number)
    place.setEachPlace(number, 0)
    while temp >= 1:
        num = (number+temp)%place.sumHole()
        place.addEachPlace(num, 1)
        temp = temp - 1

def main():
    myPlace = 3
    myStore = 1
    couterPlace = 3
    couterStore = 1
    eachStone = 3
    
    place = Place(myPlace, myStore, couterPlace, couterStore, eachStone, eachStone)
    place.display()
    
    endFlag = False
    counterTurn = random.randint(0, 2)
    
    if counterTurn == 0: #CPUが先行の場合
        counterpartInput = calcCpuMinMax(place, -1, 10, True) #calcCPU(place)
        print('CPUの選択は {} です'.format(counterpartInput))
        sowing(place, counterpartInput)
        place.display()
        endFlag = place.checkWinner(True)
    
    while not endFlag:
        playerInput = playerTurn(place)
                    
        print('あなたの選択は {} です'.format(playerInput))
        sowing(place, int(playerInput))
        place.display()
        endFlag = place.checkWinner(True)
        
        if not endFlag:
            time.sleep(1)
            counterpartInput = calcCpuMinMax(place, -1, 10, True) #calcCPU(place)
            
            print('CPUの選択は {} です'.format(counterpartInput))
            sowing(place, counterpartInput)
            place.display()
            endFlag = place.checkWinner(True)
                
if __name__ == '__main__':
    main()