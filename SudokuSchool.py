from Solver import *
from TestPuzzles import testPuzzle1, testPuzzle2, testPuzzle3, testPuzzle4, testPuzzle5, testPuzzle6

def processPuzzle(unsolvedPuzzle: Puzzle):
    puzzle = unsolvedPuzzle.copyPuzzle()
    file = open("SudokuSchoolOutput.txt", 'w')
    file.write("Starting Values:\n" + puzzle.printPuzzle() + "\n")
    newInfo = [""]
    while newInfo != []:
        outputString = ""
        newInfo = []
        basicInfo = checkBasic(puzzle, False)
        newInfo += basicInfo
        soloInfo = checkSoloCandidate(puzzle, False)
        newInfo += soloInfo
        soleOccInfo = checkSoleOccurrence(puzzle, False)
        newInfo += soleOccInfo
        pointingPairInfo = checkPointingPair(puzzle, False)
        newInfo += pointingPairInfo
        hidPairInfo = checkHiddenPair(puzzle, False)
        newInfo += hidPairInfo
        fishInfo = checkFishes(puzzle, False)
        newInfo += fishInfo
        if newInfo != []:
            outputString += newInfo[0].printInfo()
            newInfo[0].processInfo()
            outputString += puzzle.printPuzzle()
            outputString += puzzle.printPuzzleCandidates(False)
            outputString += "\n"
            file.write(outputString)
    if puzzle.isSolved:
        file.write("Puzzle is Solved, Valid Solution = " + str(puzzle.validateSolution(unsolvedPuzzle)) + ".")
    else:
        file.write("Puzzle is not solved, solving remaining using brute force.\n")
        unsolvedCellDict = {}
        for i in range(9):
            unsolvedCellDict[i+1] = []
        for row in puzzle.rows:
            for cell in row.members:
                if cell.value == 0:
                    unsolvedCellDict[cell.numCandidates] += [(cell.col.groupNum, cell.row.groupNum)]
        forceSolvedPuzzle = forceSolve(puzzle, puzzle, unsolvedCellDict)
        try:
            file.write(forceSolvedPuzzle.printPuzzle())
        except:
            file.write("FORCE SOLVE FAILED")
    file.close()

processPuzzle(testPuzzle3)