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
def checkOverlap(puzzle: Puzzle, solveFlag: bool) -> list[OverlapInfo]:
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
                overlapFound = True
                for cell in candidateCells[1:]:
                    if cell.getSameGroupType(infoGroup) != infoGroup:
                        overlapFound = False
                        break
                if overlapFound:
                    infoDict = {}
                    for cell in infoGroup.members:
                        if cell not in candidateCells and cell.candidates[val-1] == True:
                            infoDict[cell] = [val]
                    if infoDict:
                        information.append(OverlapInfo([candidateGroup] + candidateCells, infoDict))
    if information and solveFlag:
        information[0].processInfo()
    return information
 
# Checks the provided puzzle's candidates for each group. If two different values are only
# viable for the same two cells in a group, those cells cannot have any other value as a candidate.
# Will update puzzle with new found information if solveFlag is True
def checkHiddenPair(puzzle: Puzzle, solveFlag: bool) -> list[HiddenPairInfo]:
    information = []
    for group in puzzle.cols + puzzle.rows + puzzle.secs:
        pairs = [{}] * 9
        for val in range(1, 10):
            candidateCells = group.getCandidateCells(val)
            # If value is only a candidate in two cells of a group
            if len(candidateCells) == 2:
                # If a candidate has already been found for
                group1 = candidateCells[0].getSameGroupType(group).groupNum
                group2 = candidateCells[1].getSameGroupType(group).groupNum
                prevValue = pairs[group1].get(group2)
                if prevValue is not None:
                    infoDict = {}
                    nakedPair = [False] * 9
                    nakedPair[val-1] = True
                    nakedPair[prevValue-1] = True
                    for cell in candidateCells:
                        invalidCandidates = []
                        for i in range(9):
                            if cell.candidates[i] != nakedPair[i]:
                                invalidCandidates.append(i+1)
                        # If invalid candidates found
                        if invalidCandidates:
                            infoDict[cell] = invalidCandidates
                    # If new information found
                    if infoDict:
                        information.append(HiddenPairInfo(group.members, infoDict))
                else:
                    pairs[group1][group2] = val
                    pairs[group2][group1] = val
    if information and solveFlag:
        information[0].processInfo()
    return information