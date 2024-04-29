import numpy as np
import random

#Difficult puzzle
p3 = """
    100000607
    000050020
    609007080
    402080000
    750000090
    000060204
    080500103
    060320000
    304000000
    """

#Easy puzzle
p2 = """
    079132085
    060590700
    508700210
    000800900
    706340000
    801200403
    087000300
    903000508
    250000190
    """

#Easy Puzzle
p = """
    005310720
    300642500
    124000063
    470500630
    090463080
    638009005
    009806102
    206090308
    013074050
    """

#Difficult Puzzle
p4 = """
    607001003
    000300890
    400500201
    010070500
    000000000
    004050030
    205009008
    041008000
    800600302
    """

puzzle = np.array([[int(i) for i in line] for line in p.split()])
puzzle2 = np.array([[int(i) for i in line] for line in p.split()])

def PrintFunction(puzzle):
    print(" -----------------------")
    for i in range(len(puzzle)):
        if i == 3 or i == 6:
            print("|-----------------------|")
        row = ""
        for j in range(len(puzzle[i])):
            if (j == 3) or (j == 6) or (j == 0):
                row += ("| ")
            if puzzle[i][j] == 0:
                row += " "
                if j == 8:
                    row += " |"
            else:
                row += str(puzzle[i][j])
                if j == 8:
                    row += " |"
            row += " "
        print(row)
    print(" -----------------------")

def CreateBlocks(puzzle):
    sub = np.array_split(puzzle, 3, axis=0)
    sub2 = []
    i = 0
    while i < 3:
        sub2 += np.hsplit(sub[i], 3)
        i+=1
    return sub2

def FillPuzzle(puzzle):
    for i in range(9):
        temp = []
        temp2 = ""
        check = [1,2,3,4,5,6,7,8,9]
        for j in range(3):
            for k in range(3):
                temp.append(puzzle[i][j][k])
        for n in range(len(temp)):
            for l in check:
                if l == temp[n]:
                    check.remove(l)
        for n in range(len(temp)):
            if temp[n] == 0:
                ran = random.choice(check)
                check.remove(ran)
                temp[n] = ran

        #creates a string for each row and then converts it to a np array.
        for num in range(9):
            temp2 = temp2 + str(temp[num])
        filledPuzzle = np.array([int(i) for i in temp2])

        #places the random numbers into the block of the puzzle.
        count = 0
        for row in range(len(puzzle[i])):
            for col in range(len(puzzle[i])):
                puzzle[i][row][col] = filledPuzzle[count]
                count+=1

    top = np.concatenate((puzzle[0], puzzle[1], puzzle[2]), axis=1)
    mid = np.concatenate((puzzle[3], puzzle[4], puzzle[5]), axis=1)
    bottom = np.concatenate((puzzle[6], puzzle[7], puzzle[8]), axis=1)
    whole = np.concatenate((top, mid, bottom), axis=0)

    return whole

def CheckPuzzle(puzzle):
    count = 0
    pos = 0
    for i in range(len(puzzle[pos])):
        for j in range(len(puzzle[pos])):
            b = j+1
            while b < 9:
                if puzzle[i][j] == puzzle[i][b]:
                    count+=1
                b+=1

    for i in range(len(puzzle[pos])):
        for j in range(len(puzzle[pos])):
            b = j+1
            while b < 9:
                if puzzle[j][i] == puzzle[b][i]:
                    count+=1
                b+=1
    return count

def Switch(puzzle, puzzle2, block):
    while True:
        box1 = random.choice(block)
        notpicked = [box for box in block if box != box1]
        box2 = random.choice(notpicked)

        if puzzle2[box1[0]][box1[1]] == 0:
            if puzzle2[box2[0]][box2[1]] == 0:
                break

    tmpPuzzle = np.copy(puzzle)
    tmp = tmpPuzzle[box1[0]][box1[1]]
    tmpPuzzle[box1[0]][box1[1]] = tmpPuzzle[box2[0]][box2[1]]
    tmpPuzzle[box2[0]][box2[1]] = tmp

    return tmpPuzzle

def ListofCoords():
    list = []

    for row in range(3):
        for col in range(3):
            block = []
            for i in range(3):
                for j in range(3):
                    x = col * 3 + j
                    y = row * 3 + i
                    block.append([x, y])
            list.append(block)
    return list

def SimulateAnnealing(puzzle):
    temp = 1.0
    cool = 0.9999
    blocks = CreateBlocks(puzzle)
    curr = FillPuzzle(blocks)

    best = np.copy(curr)
    currVal = CheckPuzzle(curr)
    bestVal = CheckPuzzle(curr)
    counter = 0

    for i in range(1000000):
        if (counter == 1500) or (temp < 0.0001):
            temp = temp + .5
            counter = 0
            print("reheating  ", temp)

        r =  random.choice(ListofCoords())
        newPuzzle = Switch(curr, puzzle2, r)
        checkVal = CheckPuzzle(newPuzzle)

        prob = np.exp((-(checkVal - currVal)) / temp)
        if checkVal < currVal or np.random.uniform(0,1,1) < prob:
            curr = np.copy(newPuzzle)
            currVal = checkVal
            counter=0
            if currVal < bestVal:
                bestVal = currVal
                best = np.copy(curr)
                if bestVal > 9:
                    print(" ", bestVal, "    ", f"{temp:.6f}")
                else:
                    print(" ", bestVal, "     ", f"{temp:.6f}")
                if currVal == 0:
                    break
        
        counter += 1
        temp = temp * cool

    return best

PrintFunction(puzzle)
print("", "Best  ", "Temperature")
final = SimulateAnnealing(puzzle)
print("\n    Final Score: ", CheckPuzzle(final))
PrintFunction(final)
