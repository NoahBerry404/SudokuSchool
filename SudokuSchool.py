from Solver import *
from TestPuzzles import testPuzzle, testPuzzle2

def processPuzzle(puzzle: Puzzle):
    puzzle.printPuzzle()
    newInfoFound = True
    while newInfoFound:
        newInfoFound = False
        basicInfo = checkBasic(puzzle, True)
        if basicInfo:
            newInfoFound = True
            continue
        soloInfo = checkSoloCandidate(puzzle, True)
        if soloInfo:
            newInfoFound = True
            continue
        soleOccInfo = checkSoleOccurrence(puzzle, True)
        if soleOccInfo:
            newInfoFound = True
            continue
        overlapInfo = checkOverlap(puzzle, True)
        if overlapInfo:
            newInfoFound = True
            continue
    puzzle.printPuzzle()
    puzzle.printPuzzleCandidates(False)

processPuzzle(testPuzzle2)