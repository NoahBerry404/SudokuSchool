from Solver import *
from TestPuzzles import testPuzzle1, testPuzzle2, testPuzzle3, testPuzzle4

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
        file.write("Puzzle is not solved.")
    file.close()

processPuzzle(testPuzzle1)