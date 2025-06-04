class Cell:
    # Initiate a new cell. Cells will be unsolved and have all candidates possible by default
    def __init__(self, column: 'Group', row: 'Group', section: 'Group'):
        # Unsolved cells have a value of 0
        self.value = 0
        # candidates is a list the tracks which values are potential candidates for the cell
        # Each element represents the value of its index plus one (eg. index of 0 represents a value of 1)
        self.candidates = [True] * 9
        self.numCandidates = 9
        # Column that the cell belongs to
        self.col = column
        # Row that the cell belongs to
        self.row = row
        # Section that the cell belongs to
        self.sec = section
    # Set a cell to be solved at the given value
    def setValue(self, value: int):
        if self.value != 0:
            raise Exception("Tried to set value of a solved cell")
        if self.candidates[value-1] == False:
            raise Exception("Value must be an eligible candidate")
        self.value = value
        self.candidates = [False] * 9
        self.numCandidates = 0
        for group in [self.col, self.row, self.sec]:
            if group.values[value-1] == True:
                raise Exception("Group already contains new value")
            group.values[value-1] = True
            if group.numSolved == 9:
                raise Exception("Group is already solved")
            group.numSolved += 1
            if group.numSolved == 9:
                puzzle = group.puzzle
                if puzzle.solvedGroups == 27:
                    raise Exception("Puzzle is already solved")
                puzzle.solvedGroups += 1
                if puzzle.solvedGroups == 27:
                    puzzle.isSolved = True
    # Set a cell's candidates field
    def setCandidates(self, valueList: list[int]):
        if valueList == []:
            raise Exception("At least 1 candidate must be provided")
        if len(valueList) != len(set(valueList)):
            raise Exception("All candidates must be unique")
        if self.value != 0:
            raise Exception("Cannot set the candidates of a solved Cell")
        newCandidates = [False] * 9
        for value in valueList:
            newCandidates[value-1] = True
        self.candidates = newCandidates
        self.numCandidates = len(valueList)
    # Remove a candidate from a cell
    def removeCandidate(self, candidate: int, strict = False):
        if self.candidates[candidate-1] == True:
            if self.numCandidates == 1:
                raise Exception("Tried to remove last candidate.")
            self.candidates[candidate-1] = False
            self.numCandidates -= 1
        elif strict:
            raise Exception("Tried to remove nonexistent candidate.")
    # Returns a Cell's candidates as a list of their values
    def getCandidates(self) -> list[int]:
        candList = []
        for i in range(len(self.candidates)):
            if self.candidates[i] == True:
                candList.append(i+1)
        return candList
    # Returns a cell's parent group of the same type as targetGroup
    def getSameGroupType(self, targetGroup: 'Group') -> 'Group':
        match targetGroup.type:
            case "col":
                return self.col
            case "row":
                return self.row
            case "sec":
                return self.sec
            case _:
                raise Exception("Invalid Group Type")
    # Returns a string representing a cell's value
    def printCell(self) -> str:
        cellString = ""
        if self.value == 0:
            cellString += "_"
        else:
            cellString += str(self.value)
        cellString += " "
        return cellString
    # Returns a string representing a line of a cell's candidates
    def printCandidateLine(self, line: int, printSolved: bool) -> str:
        candidateString = ""
        for i in range(3):
                if self.value != 0:
                    if printSolved:
                        if line == 1 and i == 1:
                            candidateString += str(self.value) + " "
                        else:
                            candidateString += "* "
                    else:
                        candidateString += "_ "
                elif self.candidates[line*3+i] == False:
                    candidateString += "_ "
                else:
                    candidateString += str(line*3+i+1) + " "
        return candidateString
    # Print all of a Cell's Candidates
    def printCandidates(self, printSolved: bool):
        candidateString = ""
        for i in range(3):
            candidateString += self.printCandidateLine(i, printSolved) + "\n"
        return candidateString
    # Returns a string with the location of the cell in the puzzle in "(col, row)" format
    def printLocation(self) -> str:
        return "(" + str(self.col.groupNum) + ", " + str(self.row.groupNum) + ")"

class Group:
    # Initiate a new group, the super class for Column, Row, and Section
    def __init__(self, puzzle: 'Puzzle', groupNum: int, type: str):
        # Puzzle that the group belongs to
        self.puzzle = puzzle
        # List of 9 Ordered cells in the group, ordered top to bottom for a column, ordered left to right for a row, and ordered like reading a book for a section
        self.members = []
        # values is a list the tracks which values are solved in the group
        # Each element represents the value of its index plus one (eg. index of 0 represents a value of 1)
        self.values = [False] * 9
        # The number of cells in the group that are solved
        self.numSolved = 0
        # The order of the group in puzzle
        self.groupNum = groupNum
        if type not in ["col", "row", "sec"]:
            raise Exception("Invalid Group Type")
        self.type = type
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
    def printGroup(self) -> str:
        colString = ""
        for cell in self.members:
            groupString += cell.printCell() + "\n"
        return colString
    def printType(self) -> str:
        return "column"

class Row(Group):
    def printGroup(self) -> str:
        rowString = ""
        for cell in self.members:
            rowString += cell.printCell()
        rowString += "\n"
        return rowString
    def printType(self) -> str:
        return "row"

class Section(Group):
    def printGroup(self) -> str:
        secString = ""
        for cell in self.members:
            secString += cell.printCell()
            if cell.col.groupNum > 1 and cell.col.groupNum % 3 == 1:
                secString += "\n"
        return secString
    def printType(self) -> str:
        return "section"

class Puzzle:
    # Initialize a new puzzle and set up with columns, rows, and sections containing default cells
    def __init__(self):
        self.rows = []
        self.cols = []
        self.secs = []
        # solvedGroups is used to check if the puzzle is complete
        self.solvedGroups = 0
        self.isSolved = False
        for i in range(9):
            self.rows.append(Row(self, i+1, "row"))
            self.cols.append(Column(self, i+1, "col"))
            self.secs.append(Section(self, i+1, "sec"))
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
    # Retrieve a cell by its column and row
    def getCell(self, col: int, row: int) -> Cell:
        return self.rows[row-1].members[col-1]
    # Get a puzzle's cell by column and row and set it to the given value
    def setCellValue(self, val: int, col: int, row: int):
        targetCell = self.getCell(col, row)
        targetCell.setValue(val)
    def setCellCandidates(self, valueList: list[int], col: int, row: int):
        targetCell = self.getCell(col, row)
        targetCell.setCandidates(valueList)
    # Makes a copy of a puzzles original values and candidates
    def copyPuzzle(self) -> 'Puzzle':
        newPuzzle = Puzzle()
        for i in range(9):
            row = self.rows[i]
            newRow = newPuzzle.rows[i]
            for j in range(9):
                cell = row.members[j]
                newCell = newRow.members[j]
                if cell.value != 0:
                    newCell.setValue(cell.value)
                newCell.candidates = cell.candidates.copy()
        return newPuzzle
    # Checks that a puzzle is a solution of original
    def validateSolution(self, original: 'Puzzle'):
        if self.isSolved == False:
            raise Exception("Puzzle is not solved")
        for group in self.cols + self.rows + self.secs:
            valueCheck = [False] * 9
            for cell in group.members:
                if cell.value == 0:
                    return False
                valueCheck[cell.value-1] = True
            if valueCheck != [True] * 9:
                return False
        for i in range(9):
            solvedRow = self.rows[i]
            unsolvedRow = original.rows[i]
            for j in range(9):
                solvedCell = solvedRow.members[j]
                unsolvedCell = unsolvedRow.members[j]
                if unsolvedCell.value != 0 and solvedCell.value != unsolvedCell.value:
                    print(original.printPuzzle())
                    return False
        return True
    # Print the puzzle's solved cells and returns it as a string
    def printPuzzle(self) -> str:
        puzzleString = ""
        for i in range(81):
            currentCol = i % 9 + 1
            currentRow = i // 9 + 1
            currentCell = self.getCell(currentCol, currentRow)
            puzzleString += currentCell.printCell()
            if currentCol == 9:
                puzzleString += "\n"
            if currentCol % 3 == 0 and currentCol != 9:
                puzzleString += "| "
            elif currentRow % 3 == 0 and currentCol == 9 and currentRow != 9:
                puzzleString += "----------------------\n"
        puzzleString += "\n\n"
        return puzzleString
    # Print the puzzle's cell candidates (Solved cells show their value as all of their candidates)
    def printPuzzleCandidates(self, printSolved: bool = False):
        candidateString = ""
        for i in range(27):
            for j in range(9):
                currentCell = self.getCell(j + 1, i // 3 + 1)
                candidateString += currentCell.printCandidateLine(i%3, printSolved)
                if j % 3 == 2 and j != 8:
                    candidateString += "| "
            candidateString += "\n"
            if i % 9 == 8 and i != 26:
                candidateString += "----------------------------------------------------------\n"
        candidateString += "\n\n"
        return candidateString

class Info:
    # Create a new Info object, the superclass for the sudoku info subclasses
    def __init__(self, sources: list[object], results: dict[Cell, list[int]]):
        self.sources = sources
        self.results = results
    # Update the cells in results to reflect the new information
    def processInfo(self):
        raise NotImplementedError("Subclasses must implement this method")
    # Print the details of the learned info
    def printInfo(self):
        raise NotImplementedError("Subclasses must implement this method")

class BasicInfo(Info):
    def processInfo(self):
        for cell in self.results:
            cell.removeCandidate(self.results[cell][0])
    def printInfo(self) -> str:
        infoString = ""
        cell = self.sources[0]
        infoString += "BASIC: The cell at " + cell.printLocation() + " (column, row) is solved for a value of " + str(cell.value) + ".\n"
        length = len(self.results)
        infoString += "This means that the cell"
        if length > 1:
            infoString += "s"
        infoString += " at "
        i = 0
        for ineligibleCell in self.results:
            if i != 0:
                if length > 2:
                    infoString += ","
                if i == length-1:
                    infoString += " and "
                else:
                    infoString += " "
            infoString += ineligibleCell.printLocation()
            i += 1
        infoString += " cannot have " + str(cell.value) + " as a candidate.\n"
        return infoString

class SoloCandidateInfo(Info):
    def processInfo(self):
        # There will always be only one entry in this dictionary
        cell = list(self.results.keys())[0]
        value = self.results[cell][0]
        cell.setValue(value)
    def printInfo(self) -> str:
        infoString = ""
        cell = list(self.results.keys())[0]
        val = self.results[cell][0]
        infoString += "SOLO CANDIDATE: The cell at " + cell.printLocation() + " (column, row) has " + str(val) + " as its only Candidate.\n"
        infoString += "This means that " + str(val) + " is the cell's solution.\n"
        return infoString

class SoleOccurrenceInfo(Info):
    def processInfo(self):
        # There will always be only one entry in this dictionary
        cell = list(self.results.keys())[0]
        value = self.results[cell][0]
        cell.setValue(value)
    def printInfo(self) -> str:
        infoString = ""
        cell = list(self.results.keys())[0]
        val = self.results[cell][0]
        infoString += "SOLE OCCURRENCE: The cell at " + cell.printLocation() + " (column, row) is the only cell in "
        if(all(currentCell.col == self.sources[0].col for currentCell in self.sources[1:])):
            infoString += "column " + str(self.sources[0].col.groupNum)
        elif(all(currentCell.row == self.sources[0].row for currentCell in self.sources[1:])):
            infoString += "row " + str(self.sources[0].row.groupNum)
        else:
            infoString += "section " + str(self.sources[0].sec.groupNum)
        infoString += " with " + str(val) + " as an eligible candidate.\n"
        infoString += "This means that " + str(val) + " is the cell's solution.\n"
        return infoString

class PointingPairInfo(Info):
    def processInfo(self):
        for cell in self.results:
            cell.removeCandidate(self.results[cell][0])
    def printInfo(self) -> str:
        infoString = ""
        infoString += "POINTING PAIR: The cells at "
        numSrcCells = len(self.sources) - 1
        for i in range(numSrcCells):
            if i != 0:
                if numSrcCells > 2:
                    infoString += ","
                if i == numSrcCells-1:
                    infoString += " and "
                else:
                    infoString += " "
            infoString += self.sources[i+1].printLocation()
        infoString += " (column, row) are the only cells in "
        srcGroup = self.sources[0]
        infoString += srcGroup.printType()
        candidate = self.results[list(self.results.keys())[0]][0]
        infoString += " " + str(srcGroup.groupNum) + " with " + str(candidate) + " as a candidate.\n"
        infoString += "Since these cells are in the same "
        if srcGroup.type == "sec":
            if self.sources[1].col == self.sources[2].col:
                infoType = "column"
            else:
                infoType = "row"
        else:
            infoType = "section"
        infoString += infoType + ", the candidate " + str(candidate) + " is removed from the cell"
        numResults = len(self.results)
        if numResults > 1:
            infoString += "s"
        infoString += " at "
        i = 0
        for key in self.results:
            if i != 0:
                if numResults > 2:
                    infoString += ","
                if i == numResults-1:
                    infoString += " and "
                else:
                    infoString += " "
            infoString += key.printLocation()
            i += 1
        infoString += ".\n"
        return infoString

class HiddenPairInfo(Info):
    def processInfo(self):
        for cell in self.results:
            for candidate in self.results[cell]:
                cell.removeCandidate(candidate)
    def printInfo(self) -> str:
        sourceGroup = self.sources[0]
        sourceCells = self.sources[1:]
        comboSize = len(sourceCells)
        infoString = "HIDDEN PAIR: " + sourceGroup.printType() + " " + str(sourceGroup.groupNum)
        infoString += " contains " + str(comboSize) + " cells exclusively sharing the same " + str(comboSize)
        infoString += " candidates.\nThis group consists of the cells at "
        i = 0
        for cell in sourceCells:
            if i != 0:
                if comboSize > 2:
                    infoString += ","
                if i == comboSize-1:
                    infoString += " and "
                else:
                    infoString += " "
            infoString += cell.printLocation()
            i += 1
        infoString += " (column, row).\nThis means that "
        i = 0
        numResults = len(self.results)
        for infoCell in self.results:
            if i != 0:
                infoString += ","
                if i == numResults-1:
                    infoString += " and "
                else:
                    infoString += " "
            infoString += "the cell at " + infoCell.printLocation() + " cannot have "
            candidates = self.results[infoCell]
            numCandidates = len(candidates)
            for j in range(numCandidates):
                currentCandidate = candidates[j]
                if j != 0:
                    if numCandidates > 2:
                        infoString += ","
                    if j == numCandidates-1:
                        infoString += " and "
                    else:
                        infoString += " "
                infoString += str(currentCandidate)
            infoString += " as a candidate"
            i += 1
        infoString += ".\n"
        return infoString

class FishInfo(Info):
    def processInfo(self):
        for cell in self.results:
            cell.removeCandidate(self.results[cell][0])
    def printInfo(self) -> str:
        return "FISH INFO: WIP\n"