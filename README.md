# Focus Board Game

## Description

This is a two-player version of the game Focus (also known as Domination) written in Python. A link to the rules of the game can be found [here](https://boardgamegeek.com/boardgame/789/focus).

---

## How To Use

To play the game, create an instance of the FocusGame class by passing both players' names and piece colors as strings inside of tuples (for example, game = FocusGame(('Player1', 'R'), ('Player2', 'G'))). Pieces can then be moved around the board by calling the instance methods move_piece and reserved_move in line with the game rules. The board, a player's reserved and captured pieces, and the pieces at a specific location can also be printed through the use of instance methods.  

---

## Author

Stephen Ilardi
