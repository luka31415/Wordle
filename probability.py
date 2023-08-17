with open("data/word_lists/word_list_complete.txt") as file:
    wordList = []
    for line in file:
        wordList.append(line.strip())

numOfWords = len(wordList)

letters = [0] * 26
alphabet = list("abcdefghijklmnopqrstuvwxyz")

for word in wordList:
    for index, letter in enumerate(alphabet):
        if letter in word:
            letters[index] += 1

for index, letter in enumerate(alphabet):
    print(f"{letter}: {letters[index]}")

for index, letter in enumerate(letters):
    letters[index] /= numOfWords

print(letters)