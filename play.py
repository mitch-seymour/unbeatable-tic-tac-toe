from Game import TicTacToe

welcome = """
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Welcome to tic tac toe. I hate to break it
to you, but you're going to lose. But lets
play anyways! To choose a cell, simply
specify the corresponding number...

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

"""

print welcome
game = TicTacToe('o');
game.drawBoard()
#game.minimalMode()
game.play()
