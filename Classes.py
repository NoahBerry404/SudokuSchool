class Cell:
    # Initiate a new cell. Cells will have be unsolved with all candidates possible by default
    def __init__(self, column: object, row: object, section: object):
        # Unsolved cells have a value of 0
        self.value = 0
        # candidates is a list with size 9, with each element representing the candidacy of numbers 1-9
        self.candidates = [True] * 9
        # numCan
        self.numCandidates = 9
        # Column that the cell belongs to
        self.col = column
        # Row that the cell belongs to
        self.row = row
        # Section that the cell belongs to
        self.sec = section
    # Set a cell to be solved at the given value
    def setCell(self, value: int):
        self.value = value
        self.candidates = [False] * 9
        self.candidates[value-1] = True
        self.numCandidates = 1
    # Remove a candidate from a cell
    def removeCandidate(self, candidate: int, strict = False):
        if self.candidates[candidate-1] == True:
            if self.numCandidates == 1:
                raise Exception("Tried to remove last candidate.")
            self.candidates[candidate-1] = False
            self.numCandidates -= 1
        elif strict:
            raise Exception("Tried to remove nonexistent candidate.")
    # Solve a cell
    def solveCell(self):
        if self.numCandidates == 1:
            count = 0
            for candidateBool in self.candidates:
                if candidateBool == True:
                    self.value = count + 1
                    break
                count += 1
            if self.value == 0:
                raise Exception("numCandidates is 1, but no candidates found")
        elif self.numCandidates > 1:
            raise Exception("Tried to solve a cell with multiple candidates.")
        else:
            raise Exception("Cell has less than 1 candidate.")
    # Print a Cell's Value
    def printCell(self):
        if self.value == 0:
            print("_", end=" ")
        else:
            print(self.value, end=" ")
    # Print one line of a Cell's Candidates
    def printCandidateLine(self, line: int):
        for i in range(3):
                if self.value != 0:
                    print(self.value, end=" ")
                elif self.candidates[line*3+i] == False:
                    print(" ", end=" ")
                else:
                    print(line*3+i+1, end=" ")
    # Print all of a Cell's Candidates
    def printCandidates(self):
        for i in range(3):
            self.printCandidateLine(i)
            print()

class Group:
    # Initiate a new group, the super class for Column, Row, and Section
    def __init__(self, groupNum: int):
        # List of 9 Ordered cells in the group, ordered top to bottom for a column, ordered left to right for a row, and ordered like reading a book for a section
        self.members = []
        self.groupNum = groupNum
    def printGroup(self):
        raise NotImplementedError("Subclasses must implement this method")

class Column(Group):
    def printGroup(self):
        for cell in self.members:
            cell.printCell()
            print()

class Row(Group):
    def printGroup(self):
        for cell in self.members:
            cell.printCell()
        print()

class Section(Group):
    def printGroup(self):
        for cell in self.members:
            cell.printCell()
            if cell.col.groupNum > 0 and cell.col.groupNum % 3 == 0:
                print()

class Puzzle:
    def __init__(self):
        self.rows = []
        self.cols = []
        self.secs = []
        for i in range(9):
            self.rows.append(Row(i))
            self.cols.append(Column(i))
            self.secs.append(Section(i))
        for i in range(81):
            currentColIndex = i % 9
            currentCol = self.cols[currentColIndex]
            currentRowIndex = i // 9
            currentRow = self.rows[currentRowIndex]
            currentSecIndex = (currentColIndex // 3) + (currentRowIndex // 3 * 3)
            currentSec = self.secs[currentSecIndex]
            newCell = Cell(currentCol, currentRow, currentSec)
            currentCol.members.append(newCell)
            currentRow.members.append(newCell)
            currentSec.members.append(newCell)
    # Retrieve a cell by its column and row indices
    def getCell(self, col: int, row: int) -> Cell:
        return self.rows[row].members[col]
    def printPuzzle(self):
        for i in range(81):
            currentCol = i % 9
            currentRow = i // 9
            currentCell = self.getCell(currentCol, currentRow)
            currentCell.printCell()
            if currentCol == 8:
                print()
            if currentCol % 3 == 2 and currentCol != 8:
                print("|", end=" ")
            elif currentRow % 3 == 2 and currentCol == 8 and currentRow != 8:
                print("----------------------")
    def printPuzzleCandidates(self):
        for i in range(27):
            for j in range(9):
                currentCell = self.getCell(j, i // 3)
                currentCell.printCandidateLine(i%3)
                if j % 3 == 2 and j != 8:
                    print("|", end=" ")
            print()
            if i % 9 == 8 and i != 26:
                print("----------------------------------------------------------")