from Classes import *
 
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
                for groupMate in cell.col.members:
                    if groupMate.candidates[val-1] == True:
                        infoDict[groupMate] = val
                for groupMate in cell.row.members:
                    if groupMate.candidates[val-1] == True:
                        infoDict[groupMate] = val
                for groupMate in cell.sec.members:
                    if groupMate.candidates[val-1] == True:
                        infoDict[groupMate] = val
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
                information.append(SoloCandidateInfo([cell], {cell:val}))
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
                newInfo = SoleOccurrenceInfo(group.members, {cellList[0]:val})
                information.append(newInfo)
    if information and solveFlag:
        information[0].processInfo()
    return information

# Checks the provided puzzle for situations where all of a group's cells that have
# a certain value as a candidate share another group in common
# Will update puzzle with new found information if solveFlag is True
def checkOverlap(puzzle: Puzzle, solveFlag: bool) -> list[OverlapInfo]:
    information = []
    for val in range(1, 10):
        for column in puzzle.cols:
            colCandidateCells = column.getCandidateCells(val)
            if len(colCandidateCells) < 2:
                continue
            exampleCell = colCandidateCells[0]
            currentSec = exampleCell.sec
            if all(currentCell.sec == colCandidateCells[0].sec for currentCell in colCandidateCells[1:]):
                infoDict = {}
                for currentCell in currentSec.members:
                    if currentCell.col != exampleCell.col and currentCell.candidates[val-1] == True:
                        infoDict[currentCell] = val
                if infoDict:
                    information.append(OverlapInfo(colCandidateCells, infoDict))
        for row in puzzle.rows:
            rowCandidateCells = row.getCandidateCells(val)
            if len(rowCandidateCells) < 2:
                continue
            exampleCell = rowCandidateCells[0]
            currentSec = exampleCell.sec
            if all(currentCell.sec == rowCandidateCells[0].sec for currentCell in rowCandidateCells[1:]):
                infoDict = {}
                for currentCell in currentSec.members:
                    if currentCell.row != exampleCell.row and currentCell.candidates[val-1] == True:
                        infoDict[currentCell] = val
                if infoDict:
                    information.append(OverlapInfo(rowCandidateCells, infoDict))
        for section in puzzle.secs:
            secCandidateCells = section.getCandidateCells(val)
            if len(secCandidateCells) < 2:
                continue
            exampleCell = secCandidateCells[0]
            currentCol = exampleCell.col
            currentRow = exampleCell.row
            if all(cell.col == currentCol for cell in secCandidateCells[1:]):
                infoDict = {}
                for currentCell in currentCol.members:
                    if currentCell.sec != exampleCell.sec and currentCell.candidates[val-1] == True:
                        infoDict[currentCell] = val
                if infoDict:
                    information.append(OverlapInfo(secCandidateCells, infoDict))
            if all(cell.row == currentRow for cell in secCandidateCells[1:]):
                infoDict = {}
                for currentCell in currentRow.members:
                    if currentCell.sec != exampleCell.sec and currentCell.candidates[val-1] == True:
                        infoDict[currentCell] = val
                if infoDict:
                    information.append(OverlapInfo(secCandidateCells, infoDict))
    if information and solveFlag:
        information[0].processInfo()
    return information
