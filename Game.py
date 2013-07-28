import sys, traceback

class TicTacToe:

	def __init__(self, char='x'):

		# set the opponent's marker
                self.omarker = char

                # set the computer's marker
                if self.omarker != 'x':
                        self.cmarker = 'x'
                elif self.omarker != 'o':
                        self.cmarker = 'o'

                # set the board style
                self.board = """

 -----------
| %(1)s   %(2)s   %(3)s
+---+---+---
| %(4)s   %(5)s   %(6)s
+---+---+---
| %(7)s   %(8)s   %(9)s
 -----------

                """

                # set the default display of the board
                self.mode = 'default'

                # initialize the available cells, and their default owners
                self.available = [1, 2, 3, 4, 5, 6, 7, 8, 9]

                self.owners = {}

                for i in self.available:
                        self.owners[i] = None

                # this property allows us to keep track of the last move made
                self.lastMove = None

		# keep track of what turn we are on
                self.turnCount = 0

                # this is a list of all of the winning combinations, which will be
                # updated throughout the game
                self.wins = [
                                [1, 2, 3],
                                [4, 5, 6],
                                [7, 8, 9],
                                [1, 4, 7],
                                [2, 5, 8],
                                [3, 6, 9],
                                [1, 5, 9],
                                [3, 5, 7]
                        ]

	def checkWin(self):
		# this method works by checking each winning combination for a win
		for combination in self.wins:
                        cellowners = {}
                        for cell in combination:
                                if self.owners[cell] in cellowners:
                                        cellowners[self.owners[cell]] += 1
                                else:
                                        cellowners[self.owners[cell]] = 1

                        # check to see if any of the owners are winners
                        for owner, total in cellowners.iteritems():
                                if total == 3:
                                        return owner

                if len(self.available) == 0:
                        # no more available sqaure, so the game ended in a CATS draw
                        return 'CATS'

                # otherwise, no one has won yet
                return False

	def counterMove(self, num):
                # strategic counters
                if self.turnCount == 1 and num == 5:
                        self.makeMove(self.cmarker, 7)
                        return
                elif self.turnCount == 1 and (num == 1 or num == 3 or num == 7 or num == 9):
                        # the user selected a corner for their first move, so we need to select the center       
                        self.makeMove(self.cmarker, 5)
                        return
                elif self.turnCount == 3 and self.firstMove == 5 and self.lastMove == 3:
                        # special condition
                        self.makeMove(self.cmarker, 1)
                        return
                else:
                        # see if we have a winning move
                        for combination in self.wins:
                                if self.howManyOwnedBy(self.cmarker, combination) > 1 and self.howManyOwnedBy(self.omarker, combination) == 0:
                                        cell = self.firstAvailable(combination)
                                        if cell:
                                                self.makeMove(self.cmarker, cell)
                                                return


                # worst case scenario, we have no strategic move and we place our marker randomly
                self.simpleCounter(num)


	def drawBoard(self):

                # interpolate the board with the cell owners
                strowners = {}
                for i, j in self.owners.iteritems():

                        # if there is no owner, and we are in minimal mode, 
                        # show empty strings for these cells
                        if j is None and self.mode == 'minimal':
                                j = ' '

                        # if we are the default mode, show cell numbers for empty owners
                        elif j is None and self.mode == 'default':
                                j = str(i)

                        strowners[str(i)] = j

                # print the board, with the interpolated values, to the screen
                print self.board % strowners
		

	def firstAvailable(self, combination):
                # find the first available cell in a combination of cells
		for i in combination:
                        if i in self.available:
                                return i

                return False

	
	def gameOver(self):
                
		# show the game over message and exit
		self.drawBoard()
		message = """
~~~~~~~~~~~~~~~~~~~~~

Game Over!

Outcome:
"""
		message += self.outcome


		message += """
~~~~~~~~~~~~~~~~~~~~~
"""
		print message
                sys.exit(0)


	def howManyOwnedBy(self, char, combination):
                num = 0
                for i in combination:
                        if self.owners[i] == char:
                                num += 1

                return num

	def makeMove(self, char, num):
                # increment the turn count
                self.turnCount += 1
                # remove the cell from the available cells
                if num:
                        self.available.remove(num)
                        # update the owner of the cell
                        self.owners[num] = char
                        # save the last move
                        self.lastMove = num
                # check to see if this move led to a win
                winner = self.checkWin()

                if winner:
                        if winner and winner.upper() != 'CATS':
                                if winner == self.cmarker:
                                        self.outcome = "\nComputer (" + winner + ") won!"
                                elif winner == self.omarker:
                                        self.outcome = "\nyou won!"

                                self.gameOver()

                        elif winner and winner.upper() == 'CATS':
                                self.outcome = "\nCat's game"
                                self.gameOver()

	def minimalMode(self):
                self.mode = 'minimal'

	def play(self):

                try:

                        self.firstMove = None

                        while True:

                                num = raw_input("Which cell would you like to select? ")

                                if num.isdigit():

                                        num = int(num)
                                        if num in self.available:
                                                # check to see if this is the first move
                                                if self.turnCount == 0:
                                                        firstMove = num

                                                # opponent made a valid move
                                                self.makeMove(self.omarker, num)
                                                print '\nYou placed "' + self.omarker + '" on cell ' + str(num)
						self.counterMove(num)	
						print 'Computer placed "' + self.cmarker + '" on cell ' + str(self.lastMove)
                                                self.drawBoard()

                                        else:
                                                print str(num) + " is not available"
                                else:
                                        print str(num) + " isn't a number!"

                        checkWin()

                except KeyboardInterrupt:
                        # user exited the game
                        print "\n\nExiting the tic tac toe game\n"
                except Exception:
                        traceback.print_exc(file=sys.stdout)
                sys.exit(0)

	def simpleCounter(self, num):
                # remove the winning combinations that can no longer be played
                self.updateWins()

                # check each remaining winning combination that contains the opponent's last move
                for combination in self.wins:
                        if self.lastMove in combination:
                                if self.howManyOwnedBy(self.omarker, combination) > 1:
                                        self.makeMove(self.cmarker, self.firstAvailable(combination))
                                        return False

                # make a somewhat random move. it doesn't matter where, we can't lose at this point
                for combination in self.wins:
                        cell = self.firstAvailable(combination)
                        if cell:
                                self.makeMove(self.cmarker, cell)
                                return False
		
	def updateWins(self):
		# check each remaining winning combination to see if it's still possible to win with this set of cells
                for combination in self.wins:
                        computer = self.howManyOwnedBy(self.cmarker, combination)
                        opponent = self.howManyOwnedBy(self.omarker, combination)
		
			# check to see if a computer and opponent marker both exist in the combination.
                        if computer > 0 and opponent > 0:
                                # a block occurred
                                self.wins.remove(combination)	
