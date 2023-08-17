with open("data/word_lists/word_list.txt", "r") as file:
    wordList = []
    for line in file:
        wordList.append(line.strip())

with open("data/word_lists/word_list_complete.txt", "r") as file:
    wordListComplete = []
    for line in file:
        wordListComplete.append(line.strip())

wordList.sort()
wordListComplete.sort()
allWords = wordList + wordListComplete

def Colors(guess, solution):
    solutionList = list(solution).copy()
    clue = ''
    for index, letter in enumerate(guess):
        if letter == solution[index]:
            clue += 'G'
        elif letter in solutionList:
            solutionList.remove(letter)
            clue += 'Y'
        else:
            clue += 'B'
    return clue

clues = []

for word in allWords:
    wordClues = []
    for solution in wordList:
        clue = Colors(word, solution)
        wordClues.append(clue)
    wordClues = list(dict.fromkeys(wordClues))
    clues.append([len(wordClues), word])

clues.sort()
clues.reverse()

print(clues[0:10])