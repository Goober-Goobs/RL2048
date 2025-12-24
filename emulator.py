import random
import numpy as np

#set random value + positions for 
def newNum():
    randValue = (random.randint(0,1)+1)*2
    availablePos = available()
    position = random.randint(0,len(availablePos)-1)
    arr[availablePos[position][0]][availablePos[position][1]] = randValue
    return

#return list with all available positions in array
def available():
    availablePos = []
    for i in range(4):
        for j in range(4):
            if(arr[i][j] == 0):
                availablePos.append([i,j])
    if(availablePos != []):
        return availablePos
    
    return -1

def merge(x1, y1, x2, y2, priority):
    total = 0
    if(arr[x1,y1] == arr[x2,y2]):
        total = arr[x1,y1]+arr[x2,y2]
        if(priority == 0):
            arr[x1,y1] = total
            arr[x2,y2] = 0
        else:
            arr[x2,y2] = total
            arr[x1,y1] = 0
    
    return total

def swap(x1, y1, x2, y2):
    holder = arr[x2,y2]
    arr[x2,y2] = arr[x1,y1]
    arr[x1,y1] = holder

#does a move
def move(n): #n = 0 right, n = 1 down, n = 2, left, n = 3 up
    #if right
    score = 0
    if(n == 0):
        for i in range(4):
            for j in range(2,-1,-1):
                #if there is a value, move it all the right
                jPos = j
                if(arr[i][j] != 0  and arr[i][j+1] == 0):
                    #move element to the right until another value/border is reached
                    move = True
                    while(move):
                        swap(i,jPos,i,jPos+1)
                        jPos+=1
                        if(jPos == 3 or arr[i,jPos+1] != 0):
                            move = False
                
                #if j <= 2, and [i][j] == [i][j+1], merge (add the two, make [i][j+1] equal to total, [i][j] = 0)
                if(arr[i][jPos] != 0 and jPos < 3):
                    score+=merge(i,jPos,i,jPos+1,1)
    
    #if down
    if(n == 1):
        for i in range(4):
            for j in range(2,-1,-1):
                #if there is a value AND zero below, move all the way down
                jPos = j
                if(arr[j,i] != 0  and arr[j+1,i] == 0):
                    #move element to the right until another value/border is reached
                    move = True
                    while(move):
                        swap(jPos,i,jPos+1,i)
                        jPos+=1
                        if(jPos == 3 or arr[jPos+1,i] != 0):
                            move = False
                
                #if j <= 2, and [j][i] == [j+1][i], merge (add the two, make [j+1][i] equal to total, [j][i] = 0)
                if(arr[jPos][i] != 0 and jPos < 3):
                    score+=merge(jPos,i,jPos+1,i,1)
    
    #if left 
    if(n == 2):
        for i in range(4):
            for j in range(1,4):
                #if there is a value AND zero to left, move all the way to left
                jPos = j
                
                if(arr[i,j] != 0 and arr[i,j-1] == 0):
                    #move element to left until another value/border is reached
                    move = True
                    while(move):
                        swap(i, jPos, i, jPos-1)
                        jPos -= 1
                        if(jPos == 0 or arr[i, jPos-1] != 0):
                            move = False
                #if jPos > 0 [i][j] == [i][j-1], merge (add the two, make [i, j-1] equal to total, [i][j] = 0)
                if(arr[i,jPos] != 0 and jPos > 0):
                    score+=merge(i,jPos-1, i, jPos, 0)

    #if up
    if(n == 3):
        for i in range(4):
            for j in range(1,4):
                #if there is a value AND zero abovee, move all the way up
                jPos = j
                if(arr[j,i] != 0 and arr[j-1,i] == 0):
                    #move element to the right until another value is reacher
                    move = True
                    while(move):
                        swap(jPos, i, jPos-1, i)
                        jPos -= 1
                        if(jPos == 0 or arr[jPos-1,i] != 0):
                            move = False
                #if jPos > 0 and [j][i] == [j-1][i], merge (add the two, make [j-1,i] = total, [j][i] = 0)
                if(arr[jPos, i] != 0 and jPos > 0):
                    score+= merge(jPos-1,i,jPos,i,0)

    newNum()
    return score
        
score = 0
arr = np.zeros((4,4)) 
newNum()
newNum()

while(available() != -1):
    print(f"score: {score}\n",arr)
    moveInput = int(input("which direction? (0: right, 1: down, 2: left, 3: up): "))
    score+=move(moveInput)

print(f"Final Score: {score}")


import random
import numpy as np

#set random value + positions for 
def newNum():
    randValue = (random.randint(0,1)+1)*2
    availablePos = available()
    position = random.randint(0,len(availablePos)-1)
    arr[availablePos[position][0]][availablePos[position][1]] = randValue
    return

#return list with all available positions in array
def available():
    availablePos = []
    for i in range(4):
        for j in range(4):
            if(arr[i][j] == 0):
                availablePos.append([i,j])
    if(availablePos != []):
        return availablePos
    
    return -1

def merge(x1, y1, x2, y2, priority):
    total = 0
    if(arr[x1,y1] == arr[x2,y2]):
        total = arr[x1,y1]+arr[x2,y2]
        if(priority == 0):
            arr[x1,y1] = total
            arr[x2,y2] = 0
        else:
            arr[x2,y2] = total
            arr[x1,y1] = 0
    
    return total

def swap(x1, y1, x2, y2):
    holder = arr[x2,y2]
    arr[x2,y2] = arr[x1,y1]
    arr[x1,y1] = holder

#does a move
def move(n): #n = 0 right, n = 1 down, n = 2, left, n = 3 up
    #if right
    score = 0
    if(n == 0):
        for i in range(4):
            for j in range(2,-1,-1):
                #if there is a value, move it all the right
                jPos = j
                if(arr[i][j] != 0  and arr[i][j+1] == 0):
                    #move element to the right until another value/border is reached
                    move = True
                    while(move):
                        swap(i,jPos,i,jPos+1)
                        jPos+=1
                        if(jPos == 3 or arr[i,jPos+1] != 0):
                            move = False
                
                #if j <= 2, and [i][j] == [i][j+1], merge (add the two, make [i][j+1] equal to total, [i][j] = 0)
                if(arr[i][jPos] != 0 and jPos < 3):
                    score+=merge(i,jPos,i,jPos+1,1)
    
    #if down
    if(n == 1):
        for i in range(4):
            for j in range(2,-1,-1):
                #if there is a value AND zero below, move all the way down
                jPos = j
                if(arr[j,i] != 0  and arr[j+1,i] == 0):
                    #move element to the right until another value/border is reached
                    move = True
                    while(move):
                        swap(jPos,i,jPos+1,i)
                        jPos+=1
                        if(jPos == 3 or arr[jPos+1,i] != 0):
                            move = False
                
                #if j <= 2, and [j][i] == [j+1][i], merge (add the two, make [j+1][i] equal to total, [j][i] = 0)
                if(arr[jPos][i] != 0 and jPos < 3):
                    score+=merge(jPos,i,jPos+1,i,1)
    
    #if left 
    if(n == 2):
        for i in range(4):
            for j in range(1,4):
                #if there is a value AND zero to left, move all the way to left
                jPos = j
                
                if(arr[i,j] != 0 and arr[i,j-1] == 0):
                    #move element to left until another value/border is reached
                    move = True
                    while(move):
                        swap(i, jPos, i, jPos-1)
                        jPos -= 1
                        if(jPos == 0 or arr[i, jPos-1] != 0):
                            move = False
                #if jPos > 0 [i][j] == [i][j-1], merge (add the two, make [i, j-1] equal to total, [i][j] = 0)
                if(arr[i,jPos] != 0 and jPos > 0):
                    score+=merge(i,jPos-1, i, jPos, 0)

    #if up
    if(n == 3):
        for i in range(4):
            for j in range(1,4):
                #if there is a value AND zero abovee, move all the way up
                jPos = j
                if(arr[j,i] != 0 and arr[j-1,i] == 0):
                    #move element to the right until another value is reacher
                    move = True
                    while(move):
                        swap(jPos, i, jPos-1, i)
                        jPos -= 1
                        if(jPos == 0 or arr[jPos-1,i] != 0):
                            move = False
                #if jPos > 0 and [j][i] == [j-1][i], merge (add the two, make [j-1,i] = total, [j][i] = 0)
                if(arr[jPos, i] != 0 and jPos > 0):
                    score+= merge(jPos-1,i,jPos,i,0)

    newNum()
    return score
        
score = 0
arr = np.zeros((4,4)) 
newNum()
newNum()

while(available() != -1):
    print(f"score: {score}\n",arr)
    moveInput = int(input("which direction? (0: right, 1: down, 2: left, 3: up): "))
    score+=move(moveInput)

print(f"Final Score: {score}")


