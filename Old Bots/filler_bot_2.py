import pyautogui
import time
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

def Color(x, y, blackCol, greenCol, yellowCol):
    if pyautogui.pixelMatchesColor(x, y, blackCol):
        return "b"
    if pyautogui.pixelMatchesColor(x, y, greenCol):
        return "g"
    if pyautogui.pixelMatchesColor(x, y, yellowCol):
        return "y"
    return "n"

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

def LetterCounter(word, letters):
    goodLetters = []
    for letter in word:
        if letter in letters:
            goodLetters.append(letter)
    goodLetters = list(dict.fromkeys(goodLetters))
    return len(goodLetters)

def FillerChoice(greenLetters, yellowLetters, possibleWords, wordList):
    letters = []
    words = []
    for word in possibleWords:
        for letter in word:
            letters.append(letter)
    letters = list(dict.fromkeys(letters))
    for letter in greenLetters:
        try:
            letters.remove(letter)
        except:
            pass
    for letter in yellowLetters:
        try:
            letters.remove(letter)
        except:
            pass
    for word in wordList:
        words.append(LetterCounter(word, letters))

    word = wordList[words.index(max(words))]
    return word

def ProcessAnswer(word, clue, yellowLetters, yellowPositions, blackLetters, greenLetters, greenPositions, doubleYellowLetters, guessedWords):
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

    for word in guessedWords:
        try:
            possibleGuesses.remove(word)
        except:
            pass

    remainingLetters = []
    remainingWords = []

    allWords = wordList + wordListComplete
    madeChoice = False

    if len(possibleGuesses) > 2:
        choice = FillerChoice(greenLetters, yellowLetters, possibleGuesses, allWords)
        madeChoice = True

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

    if not madeChoice:
        if len(possibleGuesses) > 1:
            if not remainingWords == []:
                print("Number of possible words:", len(possibleGuesses))
                choice = remainingWords[0][1].lower()
            else:
                print("Number of possible words:", len(possibleGuesses))
                choice = possibleGuesses[0].lower()
        else:
            print("Number of possible words:", len(possibleGuesses))
            try:
                choice = possibleGuesses[0]
            except IndexError:
                return "STOPP"
    else:
        print("Number of possible words:", len(possibleGuesses))
        print("Guessing a filler word:")

    print(choice)
    return choice

def Play(guess, numOfGuesses, guessedWords, yellowLetters, yellowPositions, blackLetters, greenLetters, greenPositions, doubleYellowLetters, xList, yList, blackCol, greenCol, yellowCol):
    clue = ""
    for x in xList:
        y = yList[numOfGuesses]
        clue += Color(x, y, blackCol, greenCol, yellowCol)

    clue = clue.upper()
    print(clue)

    if not clue == "GGGGG":
        if Color(xList[-1], yList[-1], blackCol, greenCol, yellowCol) != "n":
            print("You lost!")
            return "STOPP"
        return ProcessAnswer(guess, clue, yellowLetters, yellowPositions, blackLetters, greenLetters, greenPositions, doubleYellowLetters, guessedWords)
    else:
        print("You won!")
        return "STOPP"

def Main():
    xList = [316, 408, 500, 592, 684]
    yList = [190, 284, 378, 472, 566, 660]
    blackCol = (58, 58, 60)
    greenCol = (83, 141, 78)
    yellowCol = (181, 159, 59)

    pyautogui.click(700, 500)

    while True:
        guess = "arose"
        print("Initial guess:", guess)
        
        numOfGuesses = 0
        pyautogui.moveTo(1800, 500)
        for letter in list(guess):
            pyautogui.press(letter)
        pyautogui.press('enter')
        time.sleep(2)

        greenLetters = []
        greenPositions = []
        blackLetters = []
        yellowLetters = []
        yellowPositions = []
        doubleYellowLetters = []
        guessedWords = []

        while numOfGuesses < 6:
            guess = Play(guess, numOfGuesses, guessedWords, yellowLetters, yellowPositions, blackLetters, greenLetters, greenPositions, doubleYellowLetters, xList, yList, blackCol, greenCol, yellowCol)
            guessedWords.append(guess)
            numOfGuesses += 1
            if guess == "STOPP":
                time.sleep(3)
                pyautogui.click(266, 786)
                while not pyautogui.pixelMatchesColor(320, 190, (18, 18, 19)):
                    time.sleep(0.1)
                break

            for letter in list(guess.lower()):
                pyautogui.press(letter)
            pyautogui.press('enter')
            time.sleep(2)

if __name__ == "__main__":
    Main()