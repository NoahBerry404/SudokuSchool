class Cell:
    # Initiate a new cell. Cells will be unsolved and have all candidates possible by default
    def __init__(self, column: object, row: object, section: object):
        # Unsolved cells have a value of 0
        self.value = 0
        # candidates is a list with size 9, with each element representing the candidacy of numbers 1-9
        self.candidates = [True] * 9
        self.numCandidates = 9
        # Column that the cell belongs to
        self.col = column
        # Row that the cell belongs to
        self.row = row
        # Section that the cell belongs to
        self.sec = section
    # Set a cell to be solved at the given value
    def setCell(self, value: int):
        if self.value != 0:
            raise Exception("Tried to set value of a solved cell")
        self.value = value
        self.candidates = [False] * 9
        self.numCandidates = 0
        for group in [self.col, self.row, self.sec]:
            if group.numSolved == 9:
                raise Exception("Group is already solved")
            group.numSolved += 1
            if group.numSolved == 9:
                puzzle = group.puzzle
                if puzzle.solvedGroups == 27:
                    raise Exception("Puzzle is already solved")
                puzzle.solvedGroups += 1
    # Remove a candidate from a cell
    def removeCandidate(self, candidate: int, strict = False):
        if self.candidates[candidate-1] == True:
            if self.numCandidates == 1:
                raise Exception("Tried to remove last candidate.")
            self.candidates[candidate-1] = False
            self.numCandidates -= 1
        elif strict:
            raise Exception("Tried to remove nonexistent candidate.")
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
    def __init__(self, puzzle: object, groupNum: int):
        # Puzzle that the group belongs to
        self.puzzle = puzzle
        # List of 9 Ordered cells in the group, ordered top to bottom for a column, ordered left to right for a row, and ordered like reading a book for a section
        self.members = []
        # The number of cells in the group that are solved
        self.numSolved = 0
        # The index of the group in puzzle
        self.groupNum = groupNum
    # Returns all cells in the group that have the provided val as a candidate
    def getCandidateCells(self, val: int):
        cellList = []
        for cell in self.members:
            if cell.candidates[val-1] == True:
                cellList.append(cell)
        return cellList
    # Print the values of the cells in the group (Implemented by subclass)
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
    # Initialize a new puzzle and set up with columns, rows, and sections containing default cells
    def __init__(self):
        self.rows = []
        self.cols = []
        self.secs = []
        # solvedGroups is used to check if the puzzle is complete
        self.solvedGroups = 0
        for i in range(9):
            self.rows.append(Row(self, i))
            self.cols.append(Column(self, i))
            self.secs.append(Section(self, i))
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
    # Get a puzzle's cell by column and row and set it to the given value
    def setCellValue(self, val: int, col: int, row: int):
        targetCell = self.getCell(col, row)
        targetCell.setCell(val)
    # Print the puzzle's solved cells
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
        print("\n\n")
    # Print the puzzle's cell candidates (Solved cells show their value as all of their candidates)
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
        print("\n\n")
 
class Info:
    # Create a new Info object, the superclass for the sudoku info subclasses
    def __init__(self, sources: list[object], results: dict[Cell, int]):
        self.sources = sources
        self.results = results
    # Update the cells in results to reflect the new information
    def processInfo(self):
        raise NotImplementedError("Subclasses must implement this method")
 
class BasicInfo(Info):
    def processInfo(self):
        for cell in self.results:
            cell.removeCandidate(self.results[cell])
 
class SoloCandidateInfo(Info):
    def processInfo(self):
        # There will always be only one entry in this dictionary
        cell = list(self.results.keys())[0]
        value = self.results[cell]
        cell.setCell(value)
 
class SoleOccurrenceInfo(Info):
    def processInfo(self):
        # There will always be only one entry in this dictionary
        cell = list(self.results.keys())[0]
        value = self.results[cell]
        cell.setCell(value)
