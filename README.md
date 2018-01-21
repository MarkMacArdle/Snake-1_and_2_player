# Snake - 1 and 2 player
Classic snake with an additional 2 player mode. Made with in Python 3 with pygame. Created to practice using classes.

# How to Play
Standard rules of eat the fruit for points and to grow, if you hit the wall or yourself you'll die.

- In 1 player mode use arrow keys to start.
- In 2 player mode the player 2's snake starts on the left of screen uses WASD keys for directions, player 1 starts on the right and uses the arrow keys.
- The snakes will always start moving up.


# Highscore database functionality
Snake_with_db.py works with a PostgreSQL database to hold high scores. Prompts the winner to input their first and last name at end of a game then displays a board of the top 10 for either the one or two player game as relevant.

This does mean that running snake_with_db.py on a computer without PostgreSQL installed will give errors. If this is the case snake.py can be used. It contains the same game functionality just without the database.
