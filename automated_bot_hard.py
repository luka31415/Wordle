import pyautogui
import time

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

def GetPixelColor(x, y, blackCol, greenCol, yellowCol): # Check which color a given pixel matches (black, yellow or green)
    if pyautogui.pixelMatchesColor(x, y, blackCol):
        return "B"
    if pyautogui.pixelMatchesColor(x, y, greenCol):
        return "G"
    if pyautogui.pixelMatchesColor(x, y, yellowCol):
        return "Y"
    return "N"

def Green(word, greenLetters, greenPositions): # Check if a word contains all the green letters in the right spots
    for index, letter in enumerate(greenLetters):
        if word[greenPositions[index]] != letter:
            return False
    return True

def Yellow(word, yellowLetters, yellowPositions): # Check if a word contains all the yellow letters in new spots
    for index, letter in enumerate(yellowLetters):
        if word[yellowPositions[index]] == letter:
            return False
        elif not letter in word:
            return False
    return True

def Black(word, blackLetters, greenLetters): # Check if a word contains none of the black letters
    for letter in blackLetters:
        if letter in word:
            if letter in greenLetters and word[word.index(letter)] == letter:
                pass
            else:
                return False
    return True

def FindLetterPositions(word, letter): # Find all the positions a given letter is in a given word
    positions = []
    pos = word.find(letter)
    while pos != -1:
        positions.append(pos)
        pos = word.find(letter, pos + 1)
    return positions

def Colors(solution, guess): # Return the clue the game would give on a guess for a given solution
    clue = ["B"] * len(solution)
    countedPos = []

    for index, (solutionLetter, guessLetter) in enumerate(zip(solution, guess)):
        if solutionLetter == guessLetter:
            clue[index] = "G"
            countedPos.append(index)

    for index, letter in enumerate(guess):
        if letter in solution and clue[index] != "G":
            positions = FindLetterPositions(solution, letter)
            for pos in positions:
                if pos not in countedPos:
                    clue[index] = "Y"
                    countedPos.append(pos)
                    break
    clueStr = ""
    for letter in clue:
        clueStr += letter
    return clueStr

def AddLetters(guess, clue): # Add all of the neccessary letters to the lists for the different colors
    greenLetters = []
    greenPositions = []
    yellowLetters = []
    yellowPositions = []
    blackLetters = []

    for index, letter in enumerate(clue):
        if letter == "G":
            greenLetters.append(guess[index])
            greenPositions.append(index)
        elif letter == "Y":
            yellowLetters.append(guess[index])
            yellowPositions.append(index)
        else:
            blackLetters.append(guess[index])
    blackLetters = list(dict.fromkeys(blackLetters))

    for letter in blackLetters.copy():
        if letter in greenLetters or letter in yellowLetters:
          blackLetters.remove(letter)

    return [greenLetters, greenPositions, yellowLetters, yellowPositions, blackLetters]

def GetPossibleSolutions(guessedWords, wordList, greenLetters, greenPositions, yellowLetters, yellowPositions, blackLetters):
    possibleSolutions = []
    for word in wordList: # Check for all of the possible solutions with the new information from the clue
        if Green(word, greenLetters, greenPositions) and Yellow(word, yellowLetters, yellowPositions) and Black(word, blackLetters, greenLetters) and not word in guessedWords:
            possibleSolutions.append(word)
    return possibleSolutions

def GetWordClues(possibleSolutions): # Go through all words and check how many different color-combinations can be formed with the possible solutions
    clues = []
    for word in possibleSolutions: 
        wordClues = []
        for solution in possibleSolutions:
            current_clue = Colors(solution, word)
            if not current_clue in wordClues:
                wordClues.append(current_clue)
        clues.append([len(wordClues), word, wordClues])
    clues.sort()
    clues.reverse()
    return clues

def GetClue(numOfGuesses, xList, yList, blackCol, greenCol, yellowCol):
    clue = ""
    for x in xList: # Check for the colors of the pixels to get the clue
        y = yList[numOfGuesses]
        clue += GetPixelColor(x, y, blackCol, greenCol, yellowCol)
    return clue

def EnterGuess(guess): # Enter a given word by pressing the buttons
    pyautogui.moveTo(1800, 500)
    for letter in guess:
        pyautogui.press(letter)
    pyautogui.press("enter")
    time.sleep(2)

def Restart(): # Restart the game after winning or losing
    time.sleep(3)
    pyautogui.click(266, 786)
    while not pyautogui.pixelMatchesColor(320, 190, (18, 18, 19)):
        time.sleep(0.1)
    return

def Play(guess, clue, guessedWords, wordList, greenLetters, greenPositions, yellowLetters, yellowPositions, blackLetters, possibleSolutions=[]): # Return the next guess
    # Add all the letters from the clue:
    newLists = AddLetters(guess, clue)
    greenLetters += newLists[0]
    greenPositions += newLists[1]
    yellowLetters += newLists[2]
    yellowPositions += newLists[3]
    blackLetters += newLists[4]

    if possibleSolutions == []:
        possibleSolutions = GetPossibleSolutions(guessedWords, wordList, greenLetters, greenPositions, yellowLetters, yellowPositions, blackLetters)
    print(f"Number of possible solutions: {len(possibleSolutions)}")

    if len(possibleSolutions) == 1: # Print the solution if there is only one left
        print(f"\nYou won! The solution is {possibleSolutions[0]}!\n\n------------------------------------")
        EnterGuess(possibleSolutions[0])
        return ["BREAK", []]
    elif len(possibleSolutions) == 2: # If there are two or less solutions left, just return one of them
        return [possibleSolutions[0], []]

    clues = GetWordClues(possibleSolutions)
    for element in clues:
        word = element[1]
        if not word in guessedWords:
            newGuess = word
            break
    return [newGuess, clues] # The word with the highest number of different clues will be the next guess


def Main():
    xList = [316, 408, 500, 592, 684]
    yList = [190, 284, 378, 472, 566, 660]
    blackCol = (58, 58, 60)
    greenCol = (83, 141, 78)
    yellowCol = (181, 159, 59)

    pyautogui.click(700, 500)

    while True: # Loop for multiple rounds of Wordle to test how well the bot performs
        # Reset all of the letters:
        greenLetters = []
        greenPositions = []
        yellowLetters = []
        yellowPositions = []
        blackLetters = []
        guessedWords = []

        numOfGuesses = 0

        guess = "trace"
        print(f"\nThe guess is {guess}")
        EnterGuess(guess)
        clue = GetClue(numOfGuesses, xList, yList, blackCol, greenCol, yellowCol)
        numOfGuesses += 1
        print(f"The clue is {clue}")

        if "N" in clue:
            print("Oops! Something went wrong with the guess!")
            return

        if clue == "GGGGG": # If all letters are green, you won
            print("You won!\n\n------------------------------------")
            Restart()
            pass

        processGuess = Play(guess, clue, guessedWords, wordList, greenLetters, greenPositions, yellowLetters, yellowPositions, blackLetters)
        guess = processGuess[0]

        while numOfGuesses < 6: # Game loop for 1 round of Wordle
            print(f"\nThe guess is {guess}") # Print the next guess
            EnterGuess(guess) # Enter the next guess

            clue = GetClue(numOfGuesses, xList, yList, blackCol, greenCol, yellowCol)
            
            numOfGuesses += 1
            print(f"The clue is {clue}")

            if "N" in clue:
                print("Oops! Something went wrong with the guess!")
                return

            if clue == "GGGGG": # If all letters are green, you won
                print("You won!\n\n------------------------------------")
                Restart()
                break

            possibleSolutions = []
            for colors in processGuess[1]:
                if colors[0] == clue:
                    possibleSolutions = colors[1]
                    break

            processGuess = Play(guess, clue, guessedWords, wordList, greenLetters, greenPositions, yellowLetters, yellowPositions, blackLetters, possibleSolutions) # Find out the next guess
            guess = processGuess[0]
            guessedWords.append(guess)
            if guess == "BREAK":
                Restart()
                break

if __name__ == "__main__":
    Main()