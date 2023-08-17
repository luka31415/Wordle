# Wordle

## Files

### data/word_lists:

word_list.txt -> List of words that can be the answer

word_list_complete.txt -> List of all words including those that can be guessed but can't be the answer

### Main files:

game.py -> The game of Wordle to play in the terminal

probability.py -> Program to calculate how often each letter is found in the word list

bot.py -> Bot for the game Wordle that can guess the answer (best version)

automated_bot.py -> Bot from bot.py automated to press the buttons to play the game

bot_hard.py -> Bot for the game Wordle that plays in hard mode

automated_bot_hard.py -> Bot from bot_hard.py automated to press the buttons to play the game

starting_word.py -> Program that calculates the best starting word for bot.py (the top 3 words are trace, salet and crate)

### Old Bots:

random_bot.py -> Bot for the game Wordle that guesses a random possible word

wordle_bot.py / filler_bot.py / filler_bot_2.py / filler_bot_final.py / good_bot.py -> Previous versions of bots that can guess a filler word to increase their performance

automated_bot.py / automated_good_bot.py -> Automated versions from filler_bot_final.py and good_bot.py solving the game continuously (by pressing the buttons for you)

/!\ The automated versions of the bot are designed to work for the website wordleunlimited.org and NOT for the official Wordle website. To play there, the manual version must be used /!\


## Performance

The data was gathered using bot_tester.py which was slightly modified from the current state for the normal mode. This program goes through all possible solutions and plays every game with the bot, storing the information about how good the bot performed. This way the performance of a bot can be accurately measured in comparison to playing the game multiple times on a website like the official one or wordleunlimited.org that all use a random solution each time. On those websites some solutions come up multiple times and some don't at all. With my program, every possible solution is played exactly once, which gives the exact performance of the bot.

### Normal Mode

| Game Length | Absolute Frequency | Relative Frequency |
| :---------: | :----------------: | :----------------: |
|      1      |           1        |       0.0432%      |
|      2      |          51        |       2.2049%      |
|      3      |        1110        |      47.9896%      |
|      4      |        1032        |      44.6174%      |
|      5      |         115        |       4.9719%      |
|      6      |           4        |       0.1729%      |

Average: 3.528

This data was gathered using the bot from bot.py.

### Hard Mode

| Game Length | Absolute Frequency | Relative Frequency |
| :---------: | :----------------: | :----------------: |
|      1      |           1        |       0.0432%      | 
|      2      |         149        |       6.4419%      | 
|      3      |        1004        |      43.4068%      | 
|      4      |         880        |      38.0458%      | 
|      5      |         212        |       9.1656%      | 
|      6      |          67        |       2.8967%      | 

Average: 3.585

This data was gathered using the Bot from bot_hard.py in the hard mode of Wordle. The average number of guesses if pretty close to the one from normal mode, although a bit higher. The distribution of the guesses is way higher with more games taking 2, 5 or 6 guesses to be completed.