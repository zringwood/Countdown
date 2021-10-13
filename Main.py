import random
import re
import math
import sys
import threading
import time

#Dictionary needs to be read in once. The dictionary is a string array, not a string.
dictionary = []
for s in open("legalWords.txt") :
    dictionary.append(s.strip("\n"))
dictionary = sorted(dictionary)
#returns a string of uppercase letters with length equal to total,
#minimum numConsonants consonants and minimum numVowels vowels
#shuffled if shouldShuffle is true, else returns in vowel/consonant order
#weighted according to use in english    
def generateLetters(numVowels, numConsonants, total):
    #stack string has a number of letters that corresponds to weight in scrabble dictionary
    #vowels appear before consonants for ease of random selection
    weightedAlphabet = "AAAAAAAAAEEEEEEEEEEEEIIIIIIIIIOOOOOOOOUUUUBBCCDDDDFFGGGHHJKLLLLMMMMNNNNNNPPQRRRRRRSSSSTTTTTTVVWWXYYZ"
    letters = ""
    #add minimum number of vowels
    i = 0
    while i<numVowels :
        letters += weightedAlphabet[(int)(random.random()*weightedAlphabet.find("B"))] #B selected because it is the first consonant in alphabet
        i += 1
    #add minimum number of consonants
    i = 0
    while i<numConsonants :
        letters += weightedAlphabet[(int)(weightedAlphabet.find("B") + (random.random()*(len(weightedAlphabet) - weightedAlphabet.find("B"))))]
        i += 1
    #add remaining letters
    i = 0
    while i<(total - (numVowels + numConsonants)) :
        letters += weightedAlphabet[int(random.random()*len(weightedAlphabet))]
        i += 1
    
    return letters
#searches dictionary for the given word. Binary search. 
def searchDictionary(word) :
    a = 0
    b = len(dictionary) - 1
    while a <= b:
        m = (a+b) // 2
        if dictionary[m] < word :
            a = m + 1
        elif dictionary[m] > word :
            b = m - 1
        else :
            return m
    return -1
#returns true if all letters in word0 are contained in word1 the same number of times
def isAnagram(word0, word1) :
    temp = word1
    for c in word0 :
        if temp.find(c) == -1 :
            return False
        temp = temp.replace(c,"0",1)
    return True
#Checks to see if the given answer is valid.
#An answer is valid if all letters are present in the puzzle and the word is in the dictionary.
def checkLettersAnswer(puzzle, puzzleAnswer) :
    if len(puzzleAnswer) > len(puzzle) :
        return False
    if not isAnagram(puzzle, puzzleAnswer) :
            return False
    return searchDictionary(puzzleAnswer)
#Gets the highest scoring anagram from the dictionary.
def getHighestAnagram(string) :
    currentHighest = ""
    for word in dictionary :
        if len(word) > len(currentHighest) and isAnagram(word,string) :
            currentHighest = word
            if len(currentHighest) == len(string) :
                return currentHighest
    return currentHighest
#support for the timer, tells a thread to sleep for thirty seconds.
def timer_function():
    time.sleep(30)
#runs the letters game. Returns number of points won. This method prints to the console. 
def runLettersGame():
    puzzle = generateLetters(3,4,9)
    print(puzzle)
    #TODO: see if it's possible to display the timer counting down.
    timer = threading.Thread(target = timer_function)
    timer.start()
    puzzleAnswer = input("What is your word: ")
    #only returns true if the timer is still counting
    if timer.is_alive() :
        if len(puzzleAnswer) > len(puzzle) :
            print("Too many letters! No points.")
            return 0
        elif not isAnagram(puzzleAnswer.upper(), puzzle) :
            print("Not a valid anagram! No points.")
            return 0
        elif searchDictionary(puzzleAnswer.upper()) == -1 :
            print("Sorry, that word is not in the dictionary.")
            return 0
        else :
            print("Well done! You scored {} points!".format(len(puzzleAnswer)))
            return len(puzzleAnswer)
        highest = getHighestAnagram(puzzle)
        if len(highest) == len(puzzleAnswer) :
            print("Amazing! You got the best possible answer!")
            return len(puzzleAnswer)
        else :
            print("You also could have had {} for {} points.".format(highest,len(highest)))
            return len(puzzleAnswer)
    else :
        highest = getHighestAnagram(puzzle)
        print("Bad luck! Out of time. But you could have had {} for {} points.".format(highest,len(highest)))
        return 0
#function that runs the core program
def main():
    print("Welcome to Countdown!")
    score = 0
    while(True) :
        score += runLettersGame()
        print("Your score is now {}".format(score))
#keep this as the last call
main()
