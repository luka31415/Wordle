from ast import literal_eval as strToList

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

def GenerateClue(solution, guess): # Return the clue the game would give on a guess for a given solution
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

def GetWordClues(possibleSolutions, allWords): # Go through all words and check how many different color-combinations can be formed with the possible solutions
    clues = []
    for word in allWords: 
        wordClues = []
        for solution in possibleSolutions:
            currentClue = GenerateClue(solution, word)
            isInWordClues = False
            for wordClue in wordClues:
                if wordClue[0] == currentClue:
                    wordClue[1].append(solution)
                    isInWordClues = True
                    break
            if not isInWordClues:
                wordClues.append([currentClue, [solution]])
        clues.append([len(wordClues), word, wordClues])
    clues.sort()
    clues.reverse()
    return clues

def ProcessInitialGuess(guess, clue, greenLetters, greenPositions, yellowLetters, yellowPositions, blackLetters):
    newLists = AddLetters(guess, clue)
    greenLetters += newLists[0]
    greenPositions += newLists[1]
    yellowLetters += newLists[2]
    yellowPositions += newLists[3]
    blackLetters += newLists[4]

    with open("data/bot_help/guesses.txt") as file:
        clues = []
        for line in file:
            clues.append(strToList(line.strip()))
    newGuess = ""
    for line in clues:
        if line[0] == clue:
            newGuess = line[1]
    return newGuess

def Play(guess, clue, guessedWords, wordList, allWords, greenLetters, greenPositions, yellowLetters, yellowPositions, blackLetters, possibleSolutions=[]): # Return the next guess
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

    if len(possibleSolutions) == 1:
        print(f"\nYou won! The solution is {possibleSolutions[0]}!\n\n------------------------------------")
        return ["BREAK", []]
    elif len(possibleSolutions) == 2: # If there are two or less solutions left, just return one of them
        return [possibleSolutions[0], []]

    clues = GetWordClues(possibleSolutions, allWords)
    for element in clues:
        word = element[1]
        if not word in guessedWords:
            newGuess = word
            break
    return [newGuess, clues] # The word with the highest number of different clues will be the next guess

def Main():
    while True: # Loop for multiple rounds of Wordle to test how well the bot performs
        # Reset all of the letters:
        greenLetters = []
        greenPositions = []
        yellowLetters = []
        yellowPositions = []
        blackLetters = []
        guessedWords = []
        foundSolution = False

        guess = "trace"
        guessedWords.append(guess)
        print(f"\nThe guess is {guess}")
        clue = input("What is the clue? ").upper()
        print("")
        if clue == "GGGGG":
            print("You won!\n\n------------------------------------")
            foundSolution = True

        if not foundSolution:
            guess = ProcessInitialGuess(guess, clue, greenLetters, greenPositions, yellowLetters, yellowPositions, blackLetters)
            guessedWords.append(guess)
            print(f"The guess is {guess}")
            clue = input("What is the clue? ").upper()

            if clue == "GGGGG":
                print("You won!\n\n------------------------------------")
                foundSolution = True

            if not foundSolution:
                processGuess = Play(guess, clue, guessedWords, wordList, allWords, greenLetters, greenPositions, yellowLetters, yellowPositions, blackLetters)
                guess = processGuess[0]
                if guess != "BREAK":
                    while True: # Game loop for 1 round of Wordle
                        print(f"\nThe guess is {guess}") # Print the next guess
                        clue = input("What is the clue? ").upper() # Get the clue from the player
                        if clue == "GGGGG":
                            print("You won!\n\n------------------------------------")
                            foundSolution = True
                            break

                        if not foundSolution:
                            possibleSolutions = []
                            for colors in processGuess[1]:
                                if colors[0] == clue:
                                    possibleSolutions = colors[1]
                                    break
                            processGuess = Play(guess, clue, guessedWords, wordList, allWords, greenLetters, greenPositions, yellowLetters, yellowPositions, blackLetters, possibleSolutions) # Find out the next guess
                            guess = processGuess[0]
                            guessedWords.append(guess)
                            if guess == "BREAK":
                                break

if __name__ == "__main__":
    Main()