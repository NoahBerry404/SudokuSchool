from Classes import *
from itertools import combinations

# Recursive Function to Brute Force Solve a Sudoku
def forceSolve(originalPuzzle: Puzzle, puzzle: Puzzle, unsolvedCells: list[Cell]) -> Puzzle:
    if len(unsolvedCells) == 0:
        return puzzle
    cell = unsolvedCells[0]
    cellLocation = (cell.col.groupNum, cell.row.groupNum)
    cellCandidates = cell.getCandidates()
    for candidate in cellCandidates:
        try:
            newPuzzle = puzzle.copyPuzzle()
            newCell = newPuzzle.getCell(cellLocation[0], cellLocation[1])
            newCell.setValue(candidate)
            result = forceSolve(originalPuzzle, newPuzzle, unsolvedCells[1:])
            if result != None:
                return result
            else:
                if candidate == cellCandidates[-1]:
                    return None
        except:
            if candidate == cellCandidates[-1]:
                    return None
    
# Identifies basic sudoku candidate ineligibility (each group can only have one of each value)
# Will update puzzle with new found information if solveFlag is True
def checkBasic(puzzle: Puzzle, solveFlag: bool) -> list[BasicInfo]:
    information = []
    for row in puzzle.rows:
        for cell in row.members:
            if cell.value != 0:
                val = cell.value
                infoDict = {}
                # Check every cell in the relevant groups, add to infoDict if a candidate should be removed
                for groupMate in cell.col.members + cell.row.members + cell.sec.members:
                    if groupMate.candidates[val-1] == True:
                        infoDict[groupMate] = [val]
                # Add new Info object to information if new info was found
                if len(infoDict) > 0:
                    information.append(BasicInfo([cell], infoDict))
    if information and solveFlag:
        information[0].processInfo()
    return information
 
# Checks the provided puzzle for cells with one candidate remaining
# Will update puzzle with new found information if solveFlag is True
def checkSoloCandidate(puzzle: Puzzle, solveFlag: bool) -> list[SoloCandidateInfo]:
    information = []
    for row in puzzle.rows:
        for cell in row.members:
            if cell.numCandidates == 1:
                val = 0
                for i in range(len(cell.candidates)):
                    if cell.candidates[i] == True:
                        val = i+1
                        break
                if val == 0:
                    raise Exception("No Candidate Found")
                information.append(SoloCandidateInfo([cell], {cell:[val]}))
    if information and solveFlag:
        information[0].processInfo()
    return information
 
# Checks the provided puzzle for groups where a candidate is only possible in one cell
# Will update puzzle with new found information if solveFlag is True
def checkSoleOccurrence(puzzle: Puzzle, solveFlag: bool) -> list[SoleOccurrenceInfo]:
    information = []
    for group in puzzle.cols + puzzle.rows + puzzle.secs:
        for val in range(1, 10):
            cellList = group.getCandidateCells(val)
            if len(cellList) == 1:
                newInfo = SoleOccurrenceInfo(group.members, {cellList[0]:[val]})
                information.append(newInfo)
    if information and solveFlag:
        information[0].processInfo()
    return information

# Checks the provided puzzle for situations where all of a group's cells that have
# a certain value as a candidate share another group in common
# Will update puzzle with new found information if solveFlag is True
def checkPointingPair(puzzle: Puzzle, solveFlag: bool) -> list[PointingPairInfo]:
    information = []
    for val in range(1, 10):
        for candidateGroup in puzzle.cols + puzzle.rows + puzzle.secs:
            candidateCells = candidateGroup.getCandidateCells(val)
            numCandidates = len(candidateCells)
            if numCandidates < 2 or numCandidates > 3:
                continue
            exampleCell = candidateCells[0]
            if candidateGroup.type == "col" or candidateGroup.type == "row":
                infoGroups = [exampleCell.sec]
            else:
                infoGroups = [exampleCell.col, exampleCell.row]
            for infoGroup in infoGroups:
                pointingPairFound = True
                for cell in candidateCells[1:]:
                    if cell.getSameGroupType(infoGroup) != infoGroup:
                        pointingPairFound = False
                        break
                if pointingPairFound:
                    infoDict = {}
                    for cell in infoGroup.members:
                        if cell not in candidateCells and cell.candidates[val-1] == True:
                            infoDict[cell] = [val]
                    if infoDict:
                        information.append(PointingPairInfo([candidateGroup] + candidateCells, infoDict))
    if information and solveFlag:
        information[0].processInfo()
    return information
 
# Checks the provided puzzle's candidates for each group. If two different values are only
# viable for the same two cells in a group, those cells cannot have any other value as a candidate.
# Will update puzzle with new found information if solveFlag is True
def checkHiddenPair(puzzle: Puzzle, solveFlag: bool) -> list[HiddenPairInfo]:
    information = []
    for group in puzzle.cols + puzzle.rows + puzzle.secs:
        # Hidden pairs without two excluded candidates are redundant, can be solved by sole candidate.
        maxHiddenSize = 9 - group.numSolved - 2
        validCells = []
        for cell in group.members:
            # Don't include solved cells or solo candidate cells
            if cell.value == 0 and cell.numCandidates > 1:
                validCells.append(cell)
        potentialInfo = []
        for tupleLength in range(2, maxHiddenSize + 1):
            for combo in combinations(validCells, tupleLength):
                comboCandidates = [False] * 9
                cells = []
                for currentCell in combo:
                    cells.append(currentCell)
                    for i in range(9):
                        comboCandidates[i] = comboCandidates[i] or currentCell.candidates[i]
                if comboCandidates.count(True) == len(cells):
                    potentialInfo.append([cells, comboCandidates])
        for combo in potentialInfo:
            infoDict = {}
            for cell in group.members:
                if cell in combo[0]:
                    continue
                invalidValues = []
                for i in range(9):
                    if cell.candidates[i] == True and combo[1][i] == True:
                        invalidValues.append(i+1)
                if invalidValues:
                    infoDict[cell] = invalidValues
            if infoDict:
                information.append(HiddenPairInfo([group] + combo[0], infoDict))
    if information and solveFlag:
        information[0].processInfo()
    return information

# Checks for when n rows or n columns exclusively have 2 to n cells each with x as a candidate where the cells
# are all in the same n columns and rows. The name of the strategy is X Wing if n=2, Sword Fish if n=3, etc.
# Will update puzzle with new found information if solveFlag is True
def checkFishes(puzzle: Puzzle, solveFlag: bool) -> list[FishInfo]:
    information = []
    maxSize = 9 - 2
    fishDict = {}
    for size in range(2, maxSize + 1):
        # First blankCandByValue is for Columns, Second is for Rows
        fishDict[size] = [[list() for _ in range(9)], [list() for _ in range(9)]]
    for group in puzzle.cols + puzzle.rows:
        for i in range(9):
            candidateCells = group.getCandidateCells(i+1)
            numCells = len(candidateCells)
            if numCells > 1 and numCells <= maxSize:
                for j in range(numCells, maxSize+1):
                    fishDict[j][0 if group.type == "col" else 1][i].append(candidateCells)
    for key in range(2, maxSize + 1):
        for candByValue in fishDict[key]:
            if candByValue == fishDict[key][0]:
                groupType = "col"
            else:
                groupType = "row"
            for i in range(9):
                candCells = candByValue[i]
                numCandCells = len(candCells)
                for combo in combinations(candCells, key):
                    cols = set()
                    rows = set()
                    fishCells = []
                    for groupCandidateCells in combo:
                        for candidateCell in groupCandidateCells:
                            cols.add(candidateCell.col)
                            rows.add(candidateCell.row)
                            fishCells.append(candidateCell)
                    if cols == rows and len(cols) == key:
                        infoDict = {}
                        for group in rows if groupType == "col" else cols:
                            for member in group.members:
                                if member.candidates[i] == True and member not in fishCells:
                                    infoDict[member] = [i+1]
                        if infoDict:
                            information.append(FishInfo(combo, infoDict))
    if information and solveFlag:
        information[0].processInfo()
    return information