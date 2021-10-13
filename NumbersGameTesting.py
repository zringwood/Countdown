import random
import time

#Binary operations tree implementation
class Tree:
    def __init__(self,operator,left,right) :
        self.operator = operator
        self.left = left
        self.right = right
        
    def __str__(self) :
        return "({}{}{})".format(self.left,self.operator, self.right)
    def hasChild(self) :
        return type(self.left) == Tree or type(self.right) == Tree
    def getChildren(self) :
        return [self.left,self.right]
#returns an array of numbers for the letters game.
#This does not return the large number.
#The possible big ones are 25,50,75, and 100, and never duplicate. 
def generateNumbers(large,small) :
    numbers = []
    bigOnes = [25,50,75,100]
    i = 0
    while i < large :
        numbers.append(bigOnes.pop((int)(random.random()*len(bigOnes))))
        i += 1
        
    i = 0
    while i < small:
        numbers.append((int)(1 + random.random()*10))
        i+=1
        
    return numbers
#returns an array containing all factors of a number.
#this method does not call square root.
#this method does not return the original number or 1
def factors(number) :
    factors = []
    i = 0
    while i < number/2 :
        i += 1
        if number%i == 0 and factors.count(i) == 0:
            factors.append(i)
            factors.append(number//i)
    factors.remove(1)
    factors.remove(number)
    return factors
#returns false if the node is None or either subnodes are None
def checkNode(node) :
    return type(node) != int and not(node == None or node.left == None or node.right == None)

#the algorithm we've built can't handles cases where the only solution
#is an equation of the form a x b = c where neither a nor b are part
#of the given numbers. This is a rare case and can only be solved
#with an awkward algorithm, so we only want to check it if absolutely
#necessary. 
def buildTree(numbers, target) :
    tree = buildTree_(numbers,target)
    if (tree == None) :
         #factorization
        for j in factors (target) :
            nTree = Tree("*",buildTree_(numbers,j),target//j)
            leaves = getLeaves(nTree)
            leaves.remove(target//j)
            newNumbers = numbers.copy()
            for i in leaves :
                newNumbers.remove(i)
            nTree.right = buildTree_(newNumbers,target//j)
            if checkNode(nTree) :
               return nTree
    return tree

#solves the puzzle given an array of numbers and a target.
#tree-based recursion
def buildTree_(numbers, target) :
    if target in numbers:
        return target

    for i in numbers :
        newNumbers = numbers.copy()
        newNumbers.remove(i)
        #multiplication
        if target%i == 0 :
            nTree = Tree("*",i,buildTree_(newNumbers,target//i))
            if checkNode(nTree) :
                return nTree
        #addition
        if target-i > 0 :
            nTree = Tree("+",i,buildTree_(newNumbers,target-i))
            if checkNode(nTree) :
                return nTree
        #subtraction
        nTree = Tree("-",buildTree_(newNumbers,target+i),i)
        if checkNode(nTree) :
            return nTree
        #division
        nTree = Tree("/",buildTree_(newNumbers,target*i),i)
        if checkNode(nTree) :
            return nTree




    

#solves an operations tree
def solve(tree) :
    if(tree == None) :
        return 0
    if isinstance(tree,int) :
        return tree
    
    if tree.operator == "+" :
        return solve(tree.right) + solve(tree.left)
    if tree.operator == "-" :
        return solve(tree.left) - solve(tree.right)
    if tree.operator == "*" :
        return solve(tree.right) * solve(tree.left)
    if tree.operator == "/" :
        return solve(tree.left) // solve(tree.right)
    
def getLeaves(tree) :
    stack = []
    leaves = []
    current = tree
    stack.insert(0,current)
    while current != None and len(stack) > 0 :
        while type(current) == Tree :
            stack.insert(0,current)
            current = current.left
        if len(stack) > 0 :
            current = stack.pop(0)
            if type(current.left) == int and not current.left in leaves:
                leaves.append(current.left)
            if type(current.right) == int and not current.right in leaves: 
                leaves.append(current.right)
            current = current.right
    return leaves

#buildTree is working BUT
    #It's inefficient, especially in the worst case. 
def testProgram(numTests) :
    i = 0
    rightCount = 0
    large = 0
    while large < 5 :
        i = 0
        rightCount = 0
        while i < numTests :
            numbers = generateNumbers(large,6-large)
            target = (int)(100 + random.random()*900)
            solution = solve(buildTree(numbers,target))

            if solution == target :
                rightCount += 1
            i += 1
        
        print("Out of {} puzzles with {} large numbers, we got {} correct!".format(numTests,large,rightCount))
        large += 1
while True :
    timeStart = time.time()
    large = random.random()*4
    numbers = generateNumbers(large,6-large)
    target = (int)(100 + random.random()*900)
    print("{} {}".format(numbers, target))
    tree = buildTree(numbers,target)
    print("{} in {time:.2f} seconds".format(tree, time = (time.time()-timeStart)))

