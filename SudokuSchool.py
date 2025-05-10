from Solver import *
from TestPuzzles import testPuzzle, testPuzzle2

def processPuzzle(puzzle: Puzzle):
    print("Starting Values:")
    puzzle.printPuzzle()
    print()
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
            newInfo[0].printInfo()
            newInfo[0].processInfo()
            newInfoFound = True
            puzzle.printPuzzle()
            puzzle.printPuzzleCandidates(True)
            print()

processPuzzle(testPuzzle2)