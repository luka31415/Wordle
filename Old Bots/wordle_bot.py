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

def GoodGuess(word, commonLetters):
    for letter in commonLetters:
        if not letter in word:
            return False
    return True

def GoodWord(word, remainingLetters, numOfGoodLetters):
    counter = 0
    if remainingLetters == []:
        return 0
    for i in range(numOfGoodLetters):
        try:
            if remainingLetters[i-1] in word:
                counter += 1
        except:
            pass
    return counter

def ProcessAnswer(word, clue, yellowLetters, yellowPositions, blackLetters, greenLetters, greenPositions, doubleYellowLetters):
    possibleGuesses = []
    newYellowLetters = []
    newGreenLetters = []

    for i, letter in enumerate(clue):
        if letter == "G":
            greenLetters.append(word[i])
            greenPositions.append(i)
            newGreenLetters.append(word[i])
        elif letter == "Y":
            yellowLetters.append(word[i])
            yellowPositions.append(i)
            if word[i] in newYellowLetters:
                doubleYellowLetters.append(word[i])
            newYellowLetters.append(word[i])
        else:
            blackLetters.append(word[i])

    for letter in blackLetters:
        if letter in greenLetters:
            blackLetters.remove(letter)
        elif letter in yellowLetters:
            blackLetters.remove(letter)

    for letter in yellowLetters:
        if not letter in doubleYellowLetters:
            if letter in greenLetters:
                del yellowPositions[yellowLetters.index(letter)]
                yellowLetters.remove(letter)

    for word in wordList:
        if Green(word, greenLetters, greenPositions) and Yellow(word, yellowLetters, yellowPositions) and Black(word, blackLetters):
            possibleGuesses.append(word)

    if possibleGuesses == []:
        for word in wordListComplete:
            if Green(word, greenLetters, greenPositions) and Yellow(word, yellowLetters, yellowPositions) and Black(word, blackLetters):
                possibleGuesses.append(word)

    remainingLetters = []
    remainingWords = []

    if len(possibleGuesses) > 2:
        for word in possibleGuesses:
            for letter in word:
                remainingLetters.append(letter)

        remainingLetters = list(dict.fromkeys(remainingLetters))

        specialLetters = []

        for i in range(1, len(remainingLetters)):
            if remainingLetters[i-1] in greenLetters or remainingLetters[i-1] in newYellowLetters:
                specialLetters.append(remainingLetters[i-1])
        
        for letter in specialLetters:
            remainingLetters.remove(letter)

        numOfGoodLetters = 3
        
        while remainingWords == []:
            numOfGoodLetters += 2

            for word in possibleGuesses:
                remainingWords.append([GoodWord(word, remainingLetters, numOfGoodLetters), word])

            remainingWords.sort()
            remainingWords.reverse()

    if len(possibleGuesses) > 1:
        if not remainingWords == []:
            print("Number of remaining words:", len(remainingWords))
            choice = remainingWords[0][1]
            print(choice)
        else:
            print("Number of possible words:", len(possibleGuesses))
            choice = possibleGuesses[0]
            print(choice)
    else:
        choice = possibleGuesses[0]
        print(choice)

    return choice

def Play(guess, numOfGuesses, yellowLetters, yellowPositions, blackLetters, greenLetters, greenPositions, doubleYellowLetters):
    clue = input("The clue is: ").upper()

    if not clue == "GGGGG":
        numOfGuesses += 1
        return ProcessAnswer(guess, clue, yellowLetters, yellowPositions, blackLetters, greenLetters, greenPositions, doubleYellowLetters)
    else:
        print("You won!")
        return "STOPP"

def Main():
    guess = "arose"
    print("Initial guess:", guess)

    numOfGuesses = 0

    greenLetters = []
    greenPositions = []
    blackLetters = []
    yellowLetters = []
    yellowPositions = []
    doubleYellowLetters = []

    while numOfGuesses < 6:
        guess = Play(guess, numOfGuesses, yellowLetters, yellowPositions, blackLetters, greenLetters, greenPositions, doubleYellowLetters)
        if guess == "STOPP":
            break

if __name__ == "__main__":
    Main()