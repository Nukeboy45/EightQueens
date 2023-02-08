# Eight Queens Problem solved by Hill Climbing with Random Restarts Algorithm
# Written by Nathan Weisskopf
# ITCS 3153 - Introduction to Artificial Intelligence
# 2023

import random


# Queen object. Only stores row and column positions
class Queen(object):
    def __init__(self, row, column):
        self.row = row
        self.column = column
        # print("Created a queen with row,", row)

    # Utility function. Overrides how the object is outputted as a String
    def __str__(self):
        return "col: ", self.column, " row: ", self.row


# Board Object
class Board:

    # Constructor for Board, can take an empty list (used for new declaration) or an already established list
    def __init__(self, size, queens, *args):
        # Defaults
        self.__size = size
        self.__queenText = "♕"
        self.__emptyText = "-"

        # If a custom queen representation is passed, overwrite default values
        if len(args) > 0:
            self.__queenText = args[0]
            self.__emptyText = args[1]

        # If no queen list is passed, initialize new board
        if not queens:
            self.__queens = []
            for i in range(size):
                self.__queens.append(Queen(random.randint(0, size - 1), i))
        # If a custom queen is passed, overwrite
        else:
            self.__queens = []
            for i in range(size):
                self.__queens.append(Queen(queens[i].row, queens[i].column))

    # Utility function for printing a board object (essentially a toString method for Java users)
    def printBoard(self):
        i = 0
        while i < self.__size:
            rowString = ""
            x = 0
            while x < self.__size:
                if (self.__queens[x]).row == i:
                    rowString += self.__queenText + " "
                else:
                    rowString += self.__emptyText + " "
                x += 1
            i += 1
            print(rowString)

    # Calculates the cost of the current board setup (queens list)
    def calculateCost(self):
        cost = 0

        for queen in self.__queens:

            # horizontal left
            r = queen.row
            c = queen.column - 1
            while c >= 0:
                if self.__queens[c].row == r:
                    cost += 1
                c -= 1

            # horizontal right
            r = queen.row
            c = queen.column + 1
            while c < self.__size:
                if self.__queens[c].row == r:
                    cost += 1
                c += 1

            # Calculate diagonal - right up
            r = queen.row - 1
            c = queen.column + 1
            while c < self.__size and r >= 0:
                if self.__queens[c].row == r:
                    cost += 1
                r -= 1
                c += 1

            # Calculate diagonal - left up
            r = queen.row - 1
            c = queen.column - 1
            while c >= 0 and r >= 0:
                if self.__queens[c].row == r:
                    cost += 1
                r -= 1
                c -= 1

            # Calculate diagonal - right down
            r = queen.row + 1
            c = queen.column + 1
            while c < self.__size and r < self.__size:
                if self.__queens[c].row == r:
                    cost += 1
                r += 1
                c += 1

            # Calculate diagonal - left down
            r = queen.row + 1
            c = queen.column - 1
            while c >= 0 and r < self.__size:
                if self.__queens[c].row == r:
                    cost += 1
                r += 1
                c -= 1

        return cost

    # Takes another board object as argument, compares self and argument board and compares the two. Returns true if
    # boards are the same, false if they are not.

    # REDUNDANT FUNCTION - NEEDED TO TEST DUPLICATEBOARD FUNCTION, BUT DOES NOT SERVE A USE IN PROGRAM
    def compareBoards(self, b):
        neighbor = Board(b.__size, b.__queens)
        similar = 0
        for i in range(self.__size):
            if self.__queens[i].row == neighbor.__queens[i].row:
                similar += 1

        print(self.__size)
        print(similar)
        if similar == self.__size:
            return True

        return False

    # Take an external board as an argument, copy's the argument board's values to the current board.
    def duplicateBoard(self, b):
        for i in range(self.__size):
            self.__queens[i].row = b.__queens[i].row
            self.__queens[i].column = b.__queens[i].column

    # Finds the best neighboring board of the current board object and then sets the boards
    def getOptimalNeighbor(self):
        optBoard = Board(self.__size, [])
        optBoard.duplicateBoard(self)

        neighborBoard = Board(self.__size, [])
        neighborBoard.duplicateBoard(self)

        currCost = self.calculateCost()
        lowerCostNeighbors = 0

        for c in range(self.__size):
            for r in range(self.__size):

                if self.__queens[c].row != r:
                    neighborBoard.__queens[c].row = r
                    tempCost = neighborBoard.calculateCost()

                    if tempCost < currCost:
                        # print("Better neighbor found with, ", tempCost, " cost!" + "\n")
                        # neighborBoard.printBoard()
                        lowerCostNeighbors += 1
                        currCost = tempCost
                        optBoard.duplicateBoard(neighborBoard)

            neighborBoard.duplicateBoard(self)

        self.duplicateBoard(optBoard)
        print(lowerCostNeighbors, " neighbors found with lower h cost. Lowest h cost is new board state: ")
        self.printBoard()
        print("Current h = ", currCost)
        print("")

    # Method to access size variable from outside Board Object
    def getSize(self):
        return self.__size


# Hill climbing Algorithm to solve eight-queens problem
def hillClimb(b, qT, eT):
    tempBoard = Board(b.getSize(), [], qT, eT)
    tempBoard.duplicateBoard(b)

    restarts = 0
    neighborsFound = 0

    while True:
        tempCost = tempBoard.calculateCost()

        if tempCost == 0:
            break

        tempBoard.getOptimalNeighbor()
        if tempCost == tempBoard.calculateCost():
            print("local minimum found, restarting")
            tempBoard.printBoard()
            print("")
            tempBoard = Board(8, [], qT, eT)
            restarts += 1

        neighborsFound += 1

    print("\nGoal state found with ", neighborsFound, " neighbors found with lower h cost and ", restarts, " restarts")
    tempBoard.printBoard()


# Test & Driver Code
# Initial board declaration


# newBoard.printBoard()
# print(newBoard.calculateCost())

# Testing compare function
# newBoard.compareBoards(newBoard)

# Testing duplicateBoard function
# testboard = Board(8, [])
# testboard.duplicateBoard(newBoard)
# testboard.compareBoards(newBoard)

# Testing optimalNeighbor Function
# newBoard.getOptimalNeighbor()
# newBoard.printBoard()

queenText = "♕"
emptyText = "-"
while True:
    usrInput = input("\nRun an Eight-Queens problem simulation? (Y/N/Options): ")
    newBoard = Board(8, [])
    match usrInput:
        case "Y":
            hillClimb(newBoard, queenText, emptyText)
        case "N":
            exit()
        case "Options":
            while True:
                usrInput = input("To update queen or empty space text, type (Q/E) respectively, " +
                                 "or type Default to reset to original representation. Type F when finished: ")
                match usrInput:
                    case "Q":
                        usrInput = input("How do you want queens to be represented? Type a single character: ")
                        queenText = usrInput
                    case "E":
                        usrInput = input("How do you want empty spaces to be represented? Type a single character: ")
                        emptyText = usrInput
                    case "F":
                        break
                    case "Default":
                        queenText = "♕"
                        emptyText = "-"
                        print("Reset to default values!")
                    case _:
                        print("You didn't do something quite right...")
        case _:
            print("You didn't do something quite right...")
