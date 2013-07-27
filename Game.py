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
		# using the self.wins instance variable, put  some logic here 
		# to check if a player has won
		return False

	def counterMove(self, num):
		# for now, we are justing countering randomly
		# our strategic counters will eventually be
		# embedded in this method
		if (len(self.available) > 0):
			randomcell = self.available[0]
			self.makeMove(self.cmarker, randomcell)
		
		else:
			self.gameOver()

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

	def gameOver(self):
		self.drawBoard()
                sys.exit(0)

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
                                        print "\nComputer (" + winner + ") won!"
                                elif winner == self.omarker:
                                        print "\nyou + won!"

                                self.gameOver()

                        elif winner and winner.upper() == 'CATS':
                                print '\nCATS'
                                self.gameOver()

	def play(self):

                try:

                        self.firstMove = None

                        while True:

                                num = raw_input("Which cell would you like to select?")

                                if num.isdigit():

                                        num = int(num)
                                        if num in self.available:
                                                # check to see if this is the first move
                                                if self.turnCount == 0:
                                                        firstMove = num

                                                # opponent made a valid move
                                                self.makeMove(self.omarker, num)
                                                self.counterMove(num)
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
			
