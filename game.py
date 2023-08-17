import random

def FindLetterPositions(word, letter):
    positions = []
    pos = word.find(letter)
    while pos != -1:
        positions.append(pos)
        pos = word.find(letter, pos + 1)
    return positions

def GenerateClue(solution, guess):
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

def Main():
    while True:
        solution = random.choice(wordList)
        wonGame = False

        for numOfGuesses in range(1, 7):
            guess = ""
            while not guess in wordListComplete:
                guess = input(f"\nWhat is your {numOfGuesses}. guess? ").lower()
                if not guess in wordListComplete:
                    print("The guess is not valid. Please try again:")
            clue = GenerateClue(solution, guess)
            print(f"The clue is {clue}")
            if clue == "GGGGG":
                print(f"Congratulations! You won the game in {numOfGuesses} guesses!")
                wonGame = True
                break
            numOfGuesses += 1

        if not wonGame:
            print(f"\nYou have run out of guesses! The solution was {solution}.")
        print("\n\n------------------------------------")
    
if __name__ == "__main__":
    Main()