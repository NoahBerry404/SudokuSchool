from Solver import *
from TestPuzzles import testPuzzle, testPuzzle2

def processPuzzle(unsolvedPuzzle: Puzzle):
    puzzle = unsolvedPuzzle.copyPuzzle()
    outputString = ""
    outputString += "Starting Values:\n" + puzzle.printPuzzle() + "\n"
    newInfoFound = True
    while newInfoFound:
        newInfo = []
        newInfoFound = False
        basicInfo = checkBasic(puzzle, False)
        newInfo += basicInfo
        soloInfo = checkSoloCandidate(puzzle, False)
        newInfo += soloInfo
        soleOccInfo = checkSoleOccurrence(puzzle, False)
        newInfo += soleOccInfo
        overlapInfo = checkOverlap(puzzle, False)
        newInfo += overlapInfo
        hidPairInfo = checkHiddenPair(puzzle, False)
        newInfo += hidPairInfo
        if newInfo:
            outputString += newInfo[0].printInfo()
            newInfo[0].processInfo()
            newInfoFound = True
            outputString += puzzle.printPuzzle()
            outputString += puzzle.printPuzzleCandidates(False)
            outputString += "\n"
    if puzzle.isSolved:
        outputString += "Puzzle is Solved, Valid Solution = " + str(puzzle.validateSolution(unsolvedPuzzle)) + "."
    else:
        outputString += "Puzzle is not solved."
    with open("SudokuSchoolOutput.txt", 'w') as file:
        file.write(outputString)

processPuzzle(testPuzzle)