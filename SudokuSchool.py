from Solver import *
 
# Testing Code (Using 4/27/25 NYT Daily Hard Crossword)
testPuzzle = Puzzle()
testPuzzle.setCellValue(4, 1, 0)
testPuzzle.setCellValue(2, 1, 1)
testPuzzle.setCellValue(4, 3, 1)
testPuzzle.setCellValue(3, 5, 1)
testPuzzle.setCellValue(6, 7, 1)
testPuzzle.setCellValue(8, 0, 2)
testPuzzle.setCellValue(7, 4, 2)
testPuzzle.setCellValue(4, 6, 2)
testPuzzle.setCellValue(1, 8, 2)
testPuzzle.setCellValue(3, 0, 3)
testPuzzle.setCellValue(9, 1, 4)
testPuzzle.setCellValue(8, 3, 4)
testPuzzle.setCellValue(6, 5, 4)
testPuzzle.setCellValue(6, 0, 5)
testPuzzle.setCellValue(1, 2, 5)
testPuzzle.setCellValue(2, 7, 5)
testPuzzle.setCellValue(4, 8, 5)
testPuzzle.setCellValue(8, 1, 6)
testPuzzle.setCellValue(9, 2, 6)
testPuzzle.setCellValue(7, 6, 7)
testPuzzle.setCellValue(9, 8, 7)
testPuzzle.setCellValue(8, 4, 8)
testPuzzle.setCellValue(6, 8, 8)
 
newInfoFound = True
while newInfoFound:
    newInfoFound = False
    basicInfo = checkBasic(testPuzzle, True)
    if basicInfo:
        newInfoFound = True
        continue
    soloInfo = checkSoloCandidate(testPuzzle, True)
    if soloInfo:
        newInfoFound = True
        continue
    soleOccInfo = checkSoleOccurrence(testPuzzle, True)
    if soleOccInfo:
        newInfoFound = True
        continue
 
testPuzzle.printPuzzle()
testPuzzle.printPuzzleCandidates()