import random
import os

with open(os.path.dirname(__file__) + "/../data/word_lists/word_list.txt", "r") as file:
    wordList = []
    for line in file:
        wordList.append(line.strip())

with open(os.path.dirname(__file__) + "/../data/word_lists/word_list_complete.txt", "r") as file:
    wordListComplete = []
    for line in file:
        wordListComplete.append(line.strip())

wordList.sort()
wordListComplete.sort()

def Green(word, letters, positions):
    for i in range(len(letters)):
        if not word[positions[i-1]] == letters[i-1]:
            return False
    return True

def Yellow(word, letters, positions):
    for i in range(len(letters)):
        if word[positions[i-1]] == letters[i-1]:
            return False
        elif not letters[i-1] in word:
            return False
    return True
            
def Black(word, letters):
    for letter in letters:
        if letter in word:
            return False
    return True

def ProcessAnswer(word, clue, yellowLetters, yellowPositions, blackLetters):
    possibleGuesses = []
    greenLetters = []
    greenPositions = []
    position = 0

    for letter in clue:
        if letter == "G":
            greenLetters.append(word[position])
            greenPositions.append(position)
        elif letter == "Y":
            yellowLetters.append(word[position])
            yellowPositions.append(position)
        else:
            blackLetters.append(word[position])
        position += 1

    for word in wordList:
        if Green(word, greenLetters, greenPositions) and Yellow(word, yellowLetters, yellowPositions) and Black(word, blackLetters):
            possibleGuesses.append(word)

    if possibleGuesses == []:
        for word in wordListComplete:
            if Green(word, greenLetters, greenPositions) and Yellow(word, yellowLetters, yellowPositions) and Black(word, blackLetters):
                possibleGuesses.append(word)

    print(possibleGuesses)
    choice = random.choice(possibleGuesses)
    print(choice)
    return choice

def Play(guess, guessedCorrectly, yellowLetters, yellowPositions, blackLetters):
    clue = input("Type in the clue: ")

    if not clue == "GGGGG":
        return ProcessAnswer(guess, clue, yellowLetters, yellowPositions, blackLetters), False
    else:
        print("You won!")
        return "", True

def Main():
    guess = "arose"
    print("Initial guess:", guess)

    guessedCorrectly = False
    numOfGuesses = 0

    yellowLetters = []
    yellowPositions = []
    blackLetters = []

    while not guessedCorrectly or numOfGuesses < 6:
        guess, guessedCorrectly = Play(guess, guessedCorrectly, yellowLetters, yellowPositions, blackLetters)

if __name__ == "__main__":
    Main()