import re

rawWords = open("rawWords.txt", "r")
legalWords = open("legalWords.txt", "w")

dictionary = []
for line in rawWords:
    if len(line) < 11 and re.findall("[^a-z]", line) == ["\n"] :
        dictionary.append(line)
dictionary = sorted(dictionary)

for s in dictionary :
    legalWords.write(s.upper())
