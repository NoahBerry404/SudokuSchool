from Solver import *
from imageInterpreter import *
from TestPuzzles import testPuzzle1, testPuzzle2, testPuzzle3, testPuzzle4, testPuzzle5, testPuzzle6, testPuzzle7, testPuzzle8

def promptPuzzle() -> Puzzle:
    puzzleType = input("Would you like to use a CUSTOM or TEST puzzle: ").lower().strip()
    if puzzleType == "custom":
        return createCustomPuzzle()
    elif puzzleType == "test":
        return chooseTestPuzzle()
    else:
        print("Invalid Puzzle Type, please enter \'CUSTOM\' or \'TEST\'")
        return promptPuzzle()
    
def createCustomPuzzle() -> Puzzle:
    entryType = input("Would you like generate the puzzle using an IMAGE or MANUALLY: ").lower().strip()
    if entryType == "image":
        return createPuzzleWithImage()
    elif entryType == "manually" or entryType == "manual":
        return createPuzzleManually(Puzzle())
    else:
        print("Invalid Entry Type, please enter \'IMAGE\' or \'MANUALLY\'")
        return createCustomPuzzle()
    
def createPuzzleWithImage() -> Puzzle:
    fileName = input("Enter a local Sudoku image file name: ").strip()
    puzzleImg = cv2.imread(fileName, cv2.IMREAD_GRAYSCALE)
    if puzzleImg is None:
        if "." in fileName:
            print("Image could not be read, verify spelling and location of image")
        else:
            print("Image could not be read, make sure to include file type")
        return createPuzzleWithImage()
    xBounds = [-1, -1]
    yBounds = [-1, -1]
    boundsInput = input("Enter the position of one of the puzzle's corners in \"x y\" format: ")
    xBounds[0], yBounds[0] = [int(bound) for bound in boundsInput.split()]
    boundsInput = input("Enter the position of the opposite corner in \"x y\" format: ")
    xBounds[1], yBounds[1] = [int(bound) for bound in boundsInput.split()]
    readPuzzle = readPuzzleImage(puzzleImg, xBounds, yBounds)
    print(readPuzzle.printPuzzle())
    nextStep = None
    while nextStep not in ["continue", "edit", "retry"]:
        if nextStep is not None:
            print("Invalid Input, please enter \'CONTINUE\', \'EDIT\', or \'RETRY\'.")
        else:
            print("Please check the accuracy of the puzzle above.")
        nextStep = input("Would you like to CONTINUE with this puzzle, EDIT this puzzle, or RETRY reading the image: ").lower().strip()
    if nextStep == "continue":
        return readPuzzle
    elif nextStep == "edit":
        return createPuzzleManually(readPuzzle)
    else:
        return createPuzzleWithImage()

def createPuzzleManually(targetPuzzle: Puzzle) -> Puzzle:
    action = None
    while action != "continue":
        print(targetPuzzle.printPuzzle())
        print("Your current puzzle is shown above")
        print("Enter \'EDIT CELL# VALUE\' to update a value, \'CLEAR CELL#\' to remove a value, or \'CONTINUE\' when finished.")
        print("Note: The cell numbering starts at the top left with 1, and is ordered like the words in a book")
        action = input("Action: ").lower().strip()
        action_params = action.split()
        if action_params[0] not in ["edit", "clear", "continue"]:
            print("Invalid Action, make sure to follow the given format")
        elif action_params[0] == "edit":
            if len(action_params) == 3:
                targetPuzzle.setCellValue(int(action_params[2]), (int(action_params[1])-1)%9+1, (int(action_params[1])-1)//9+1, False)
            else:
                print("Invalid Edit, enter \'EDIT CELL_NUMBER VALUE\' eg. EDIT 23 8")
        elif action_params[0] == "clear":
            if len(action_params) == 2:
                targetPuzzle.getCell((int(action_params[1])-1)%9+1, (int(action_params[1])-1)//9+1).clearValue()
            else:
                print("Invalid Clear, enter \'CLEAR CELL_NUMBER\' eg. CLEAR 23")
        else:
            return targetPuzzle


def chooseTestPuzzle() -> Puzzle:
    puzzleNum = input("Enter Test Puzzle Number (1-8): ")
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
        case "8":
            selectedPuzzle = testPuzzle8
        case _:
            selectedPuzzle = None
            print("Invalid Puzzle Number, please enter a number from 1 to 8")
            return chooseTestPuzzle()
    return selectedPuzzle

def promptIncludeSteps() -> bool:
    stepsRequested = input("Would you like a step by step solution? (yes/no) ").lower().strip()
    if stepsRequested in ["y", "yes"]:
        return True
    elif stepsRequested in ["n", "no"]:
        return False
    else:
        print("ERROR: Please enter 'yes' or 'no'")
        return promptIncludeSteps()

def stepSolvePuzzle(unsolvedPuzzle: Puzzle):
    puzzle = unsolvedPuzzle.copyPuzzle()
    file = open("SudokuSchoolOutput.txt", 'w')
    file.write("Starting Values:\n" + puzzle.printPuzzle())
    file.write("\nStarting Candidates:\n" + puzzle.printPuzzleCandidates(True) + "\n")
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
            outputString += newInfo[0].printInfo() + "\n\n"
            newInfo[0].processInfo()
            outputString += puzzle.printPuzzleCandidates(True) + "\n"
            outputString += puzzle.printPuzzle()
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
        listHead = initializeLinkedList(unsolvedPuzzle)
        forceSolvedPuzzle = algorithmX(unsolvedPuzzle, listHead)
        try:
            file.write(forceSolvedPuzzle.printPuzzle())
            if forceSolvedPuzzle.validateSolution(unsolvedPuzzle):
                file.write("Puzzle is Solved.\n")
            else:
                file.write("Force Solve Failed.\n")
        except:
            file.write("FORCE SOLVE FAILED.\n")
    file.close()

def forceSolvePuzzle(unsolvedPuzzle: Puzzle):
    file = open("SudokuSchoolOutput.txt", 'w')
    startNode = initializeLinkedList(unsolvedPuzzle)
    forceSolvedPuzzle = algorithmX(unsolvedPuzzle, startNode)
    if forceSolvedPuzzle == None:
        file.write("FORCE SOLVE FAILED.\n")
    elif forceSolvedPuzzle.validateSolution(unsolvedPuzzle):
        file.write("Original Puzzle:\n" + unsolvedPuzzle.printPuzzle() + "\n")
        file.write("Solved Puzzle:\n"+ forceSolvedPuzzle.printPuzzle())
    else:
        file.write("FORCE SOLVE INCORRECT.\n")
        file.write(forceSolvedPuzzle.printPuzzle())
    file.close()

targetPuzzle = promptPuzzle()
includeSteps = promptIncludeSteps()
if includeSteps:
    stepSolvePuzzle(targetPuzzle)
else:
    forceSolvePuzzle(targetPuzzle)
print("Check SudokuSchoolOutput.txt for Results")