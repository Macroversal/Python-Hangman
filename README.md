# Hangman Game

A simple Hangman game implemented using Python and the Tkinter library for the graphical user interface.

## Description

Hangman is a classic word-guessing game where the player attempts to guess a hidden word by suggesting letters. For each incorrect guess, a part of a hangman figure is drawn. The player has a limited number of attempts to guess the word correctly.

This project implements the Hangman game using Python's Tkinter library for the GUI, and it allows the player to select different difficulty levels and play the game interactively.

## Features

- Multiple difficulty levels with varying word lengths and maximum attempts.
- Graphical representation of the hangman figure as incorrect guesses are made.
- Real-time updates of game progress, attempted letters, and remaining attempts.
- Option to give up and reveal the hidden word.
- Leaderboard showing the player's win and loss count.

## Known Issues
- Hangman automatically disappears upon losing.

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/hangman-game.git
   cd hangman-game

How to Play:
1. Choose a difficulty level from the drop-down menu.
2. The game will select a random word based on the chosen difficulty.
3. Click on the letter buttons to guess the letters.
4. If the guessed letter is incorrect, a part of the hangman figure is drawn.
5. Keep guessing until you either guess the word correctly or run out of attempts.
6. You can give up at any time to reveal the hidden word.

Credits
This project was created by Macroversal.
It uses the Python programming language and the Tkinter library for GUI.
The NLTK library is used for word selection.
The game concept is based on the classic Hangman word-guessing game.

License
This project is licensed under the MIT License - see the LICENSE file for details.
