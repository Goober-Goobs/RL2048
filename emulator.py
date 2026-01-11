import random
import numpy as np

#set random value + positions for 
class Emulator:
    def __init__(self):
        self.arr = np.zeros((4,4))
        self.score = 0

    #generate a new number in the grid
    def newNum(self):
        randValue = (random.randint(0,1)+1)*2
        availablePos = self.available()
        position = random.randint(0,len(availablePos)-1)
        self.arr[availablePos[position][0]][availablePos[position][1]] = randValue
        return

    #return list with all available positions in array
    def available(self):
        availablePos = []
        for i in range(4):
            for j in range(4):
                if(self.arr[i][j] == 0):
                    availablePos.append([i,j])
        if(availablePos != []):
            return availablePos
        
        return -1

    #merge two tiles, priority = 0 means x1/y1 gets values, priority = 1 means x2/y2 gets values
    def merge(self,x1, y1, x2, y2, priority):
        total = 0
        if(self.arr[x1,y1] == self.arr[x2,y2]):
            total = self.arr[x1,y1]+self.arr[x2,y2]
            if(priority == 0):
                self.arr[x1,y1] = total
                self.arr[x2,y2] = 0
            else:
                self.arr[x2,y2] = total
                self.arr[x1,y1] = 0
        
        return total

    #swap x1/y1, x2/y2
    def swap(self,x1, y1, x2, y2):
        holder = self.arr[x2,y2]
        self.arr[x2,y2] = self.arr[x1,y1]
        self.arr[x1,y1] = holder

    #returns array with -1,0,1 (invalid moves, left/right, down/up) as valid possible moves
    def validMerge(self):
        valid = []
        
        #left/right
        rlFound = False
        for i in range(4):
            for j in range(3):
                if(((self.arr[i,j] == self.arr[i,j+1]) and not (0 in valid)) or (self.arr[i,j] == 0 or self.arr[i,j+1] == 0) ): 
                    valid.append(0)
                    rlFound = True
                    break
            if(rlFound):
                break
        
        #down/up
        duFound = False
        for i in range(3):
            for j in range(4):
                if((self.arr[i][j] == self.arr[i+1][j] and not(1 in valid)) or (self.arr[i,j] == 0 or self.arr[i+1,j] == 0)):
                    valid.append(1)
                    duFound = True
                    break
            if(duFound):
                break

        if(len(valid) == 0):
            valid.append(-1)
        return valid

    #does a move, returns score earned from that move, n is action
    def move(self,n): #n = 0 right, n = 1 down, n = 2, left, n = 3 up
        #if right
        score = 0
        
        valids = self.validMerge()
        if((0 not in valids and (n == 0 or n == 2)) or (1 not in valids and (n==1 or n==3))):
            print("invalid input, ignored.")
            return 0
        
        
        merged = np.full((4, 4), True, dtype=bool)
        if(n == 0):    
            for i in range(4):
                for j in range(2,-1,-1):
                    #if there is a value, move it all the right
                    jPos = j
                    if(self.arr[i][j] != 0  and self.arr[i][j+1] == 0):
                        #move element to the right until another value/border is reached
                        move = True
                        while(move):
                            self.swap(i,jPos,i,jPos+1)
                            jPos+=1
                            if(jPos == 3 or self.arr[i,jPos+1] != 0):
                                move = False
                    
                    #if j <= 2, and [i][j] == [i][j+1], merge (add the two, make [i][j+1] equal to total, [i][j] = 0)
                    if(self.arr[i][jPos] != 0 and jPos < 3 and merged[i,jPos+1]):
                        oldscore = score
                        score+=self.merge(i,jPos,i,jPos+1,1)
                        if(oldscore != score):
                            merged[i,jPos+1] = False
        
        
        #if down
        if(n == 1):
            for i in range(4):
                for j in range(2,-1,-1):
                    #if there is a value AND zero below, move all the way down
                    jPos = j
                    if(self.arr[j,i] != 0  and self.arr[j+1,i] == 0):
                        #move element to the right until another value/border is reached
                        move = True
                        while(move):
                            self.swap(jPos,i,jPos+1,i)
                            jPos+=1
                            if(jPos == 3 or self.arr[jPos+1,i] != 0):
                                move = False
                    
                    #if j <= 2, and [j][i] == [j+1][i], merge (add the two, make [j+1][i] equal to total, [j][i] = 0)
                    if(self.arr[jPos][i] != 0 and jPos < 3 and merged[jPos+1,i]):
                        oldscore = score
                        score+=self.merge(jPos,i,jPos+1,i,1)
                        if(oldscore != score):
                            merged[jPos+1,i] = False
        
        
        #if left 
        if(n == 2):
            for i in range(4):
                for j in range(1,4):
                    #if there is a value AND zero to left, move all the way to left
                    jPos = j
                    
                    if(self.arr[i,j] != 0 and self.arr[i,j-1] == 0):
                        #move element to left until another value/border is reached
                        move = True
                        while(move):
                            self.swap(i, jPos, i, jPos-1)
                            jPos -= 1
                            if(jPos == 0 or self.arr[i, jPos-1] != 0):
                                move = False
                    #if jPos > 0 [i][j] == [i][j-1], merge (add the two, make [i, j-1] equal to total, [i][j] = 0)
                    if(self.arr[i,jPos] != 0 and jPos > 0 and merged[i,jPos-1]):
                        oldscore = score
                        score+=self.merge(i,jPos-1, i, jPos, 0)
                        if(oldscore != score):
                            merged[i,jPos-1] = False


        #if up
        if(n == 3):
            for i in range(4):
                for j in range(1,4):
                    #if there is a value AND zero above, move all the way up
                    jPos = j
                    if(self.arr[j,i] != 0 and self.arr[j-1,i] == 0):
                        #move element to the right until another value is reacher
                        move = True
                        while(move):
                            self.swap(jPos, i, jPos-1, i)
                            jPos -= 1
                            if(jPos == 0 or self.arr[jPos-1,i] != 0):
                                move = False
                    #if jPos > 0 and [j][i] == [j-1][i], merge (add the two, make [j-1,i] = total, [j][i] = 0)
                    if(self.arr[jPos, i] != 0 and jPos > 0 and merged[jPos-1,i]):
                        oldscore = score
                        score+= self.merge(jPos-1,i,jPos,i,0)
                        if(oldscore != score):
                            merged[jPos-1,i] = False                    

        self.newNum()
        return score

    #start the game
    def startGame(self):

        self.score = 0
        self.arr = np.zeros((4,4)) 
        self.newNum()
        self.newNum()

    #returns if the game is over
    def isGameOver(self):
        return (self.available() == -1 and -1 in self.validMerge())

    #resets self back to np.zeros(4,4), scores back to 0
    def reset(self):
        self.arr = np.zeros(4,4)
        self.scores = 0




#actual user interation lmfao
arr = Emulator()
arr.startGame()

while(arr.available() != -1 and not(-1 in arr.validMerge())):
    print(f"score: {arr.score}\n",arr.arr)
    moveInput = int(input("which direction? (0: right, 1: down, 2: left, 3: up): "))
    arr.score+=arr.move(moveInput)
print(f"Final Score: {arr.score}")


