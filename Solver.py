from Classes import *
from itertools import combinations

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
        # Hidden groups without two excluded candidates are redundant, can be solved by sole candidate.
        maxHiddenSize = 9 - group.numSolved - 2
        groupCandidateList = []
        for cell in group:
            # Don't include solved cells or solo candidate cells
            if cell.value == 0 and cell.numCandidates > 1:
                groupCandidateList.append(cell.candidates)
        combos = []
        for tupleLength in range(2, maxHiddenSize + 1):
            combos.append()
    if information and solveFlag:
        information[0].processInfo()
    return information