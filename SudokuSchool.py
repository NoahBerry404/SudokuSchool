from Solver import *
from TestPuzzles import testPuzzle1, testPuzzle2, testPuzzle3, testPuzzle4, testPuzzle5, testPuzzle6, testPuzzle7

def processPuzzle(unsolvedPuzzle: Puzzle):
    puzzle = unsolvedPuzzle.copyPuzzle()
    file = open("SudokuSchoolOutput.txt", 'w')
    file.write("Starting Values:\n" + puzzle.printPuzzle())
    file.write("Starting Candidates:\n" + puzzle.printPuzzleCandidates(True))
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
        yWingInfo = checkYWing(puzzle, False)
        newInfo += yWingInfo
        if newInfo != []:
            outputString += newInfo[0].printInfo()
            newInfo[0].processInfo()
            outputString += puzzle.printPuzzle()
            outputString += puzzle.printPuzzleCandidates(True)
            outputString += "\n"
            file.write(outputString)
    if puzzle.isSolved:
        file.write("Puzzle is Solved, Valid Solution = " + str(puzzle.validateSolution(unsolvedPuzzle)) + ".")
    else:
        file.write("Puzzle is not solved, solving remaining using brute force.\n")
        cellList = []
        for row in puzzle.rows:
            for cell in row.members:
                if cell.value == 0:
                    cellList.append(cell)
        forceSolvedPuzzle = forceSolve(puzzle, puzzle, sorted(cellList, key=lambda x: x.numCandidates))
        try:
            file.write(forceSolvedPuzzle.printPuzzle())
            if forceSolvedPuzzle.validateSolution(unsolvedPuzzle):
                file.write("Puzzle is Solved.\n")
            else:
                file.write("FORCE SOLVE FAILED.\n")
        except:
            file.write("FORCE SOLVE FAILED.\n")
    file.close()

puzzleNum = input("Enter Test Puzzle Number: ")
match puzzleNum:
    case "1":
        selectedPuzzle = testPuzzle1
    case "2":
        selectedPuzzle = testPuzzle2
    case "3":
        selectedPuzzle = testPuzzle3
    case "4":
        selectedPuzzle = testPuzzle4
    case "5":
        selectedPuzzle = testPuzzle5
    case "6":
        selectedPuzzle = testPuzzle6
    case "7":
        selectedPuzzle = testPuzzle7
    case _:
        selectedPuzzle = None
        raise Exception("Invalid Test Puzzle Number")
processPuzzle(selectedPuzzle)
print("Check SudokuSchoolOutput.txt for Results")