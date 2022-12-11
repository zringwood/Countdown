import random
#Returns a randomized copy of the given list. 
def shuffle(array):
    randomized = array.copy()
    for i in range(len(randomized)-1):
        index = i + (int)(random.random()*(len(randomized)-i))
        sav = randomized[i]
        randomized[i] = randomized[index]
        randomized[index] = sav
        
    return randomized

def rungame():
    print("Let's play Countdown!")
    numbigones = (int)(input("How many big ones? "))
    #You can't have two of the same big numbers, so an array with all four possibilities is randomized and then a subset is selected. 
    numbers = shuffle([25,50,75,100])
    numbers.extend([0,0])
    for i in range(6-numbigones):
        numbers[i+numbigones] = (int)(random.random()*9)+1
    print("Your numbers are {}".format(numbers))
    #Target is a three-digit integer.
    target = 100 + (int)(random.random()*900)
    print("The target is {}. You have 60 seconds!".format(target))
    equation = postfix(nput("What is your answer?: "))

def getprecedence(operator):
    if operator == "+" or operator == "-" :
        return 2
    if operator == "*" or operator == "/" :
        return 4
    return 0
#Converts to postfix using the shunting yard algorithm
def postfix(string):
    equation = ""
    stack = []
    for c in string:
        if c.isdigit():
            equation += c
        elif getprecedence(c) > 0:
            #We always add a space if it's anything other than a single digit because we aren't reading tokens.
            equation += " "
            #Push the operator to the stack if it is a greater precedence than the one already present 
            if len(stack) > 0 :
                if getprecedence(stack[0]) < getprecedence(c) :
                    stack.insert(0,c)
                else:
                    equation += stack.pop(0) + " "
                    stack.insert(0,c)
            else:
                stack.insert(0,c)
        elif c == "(":
            stack.insert(0,c)
        elif c == ")" :
            while stack[0] != "(" :
                equation += " " + stack.pop(0)+" "
            #discard the extra parentheses
            stack.pop(0)
    #Add everything remaining in the stack
    while len(stack) > 0:
        
        equation += " "+stack.pop(0)
    return equation

#Takes a postfix equation and solves it. 
def solvepostfix(string):
    tokens = string.split(" ")
    stack = []
    while len(stack) != 1:
        for t in tokens:
            if t.isdigit():
                stack.insert(0,(int)(t))
            if not t.isdigit():
                if t == "+":
                    stack.insert(0,stack.pop(0)+stack.pop(0))
                elif t == "-":
                    stack.insert(0,stack.pop(1)-stack.pop(0))
                elif t == "*":
                    stack.insert(0,stack.pop(0)*stack.pop(0))
                elif t == "/":
                    stack.insert(0,(int)(stack.pop(0)/stack.pop(0)))
    return stack[0];
    

def rungame():
    print("Let's play Countdown!")
    numbigones = (int)(input("How many big ones? "))
    #You can't have two of the same big numbers, so an array with all four possibilities is randomized and then a subset is selected. 
    numbers = shuffle([25,50,75,100])
    numbers.extend([0,0])
    for i in range(6-numbigones):
        numbers[i+numbigones] = (int)(random.random()*9)+1
    print("Your numbers are {}".format(numbers))
    #Target is a three-digit integer.
    target = 100 + (int)(random.random()*900)
    print("The target is {}. You have 60 seconds!".format(target))
    answer = solvepostfix(postfix(input("What is your answer?: ")))
    if answer == target:
        print("You win!")
    else:
        print("That was {} away, very close.".format(answer-target))
    
rungame()

