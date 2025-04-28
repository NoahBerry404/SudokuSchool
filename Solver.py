from Classes import *

# Sets a puzzle cell's value and updates the affected cell's candidates
def insertCellValue(puzzle, val, col, row):
    targetCell = puzzle.getCell(col, row)
    targetCell.setCell(val)
    for cell in targetCell.col.members:
        if cell != targetCell:
            cell.removeCandidate(val)
    for cell in targetCell.row.members:
        if cell != targetCell:
            cell.removeCandidate(val)
    for cell in targetCell.sec.members:
        if cell != targetCell:
            cell.removeCandidate(val)

# Testing Code (Using 4/27/25 NYT Daily Hard Crossword)
testPuzzle = Puzzle()
insertCellValue(testPuzzle, 4, 1, 0)
insertCellValue(testPuzzle, 2, 1, 1)
insertCellValue(testPuzzle, 4, 3, 1)
insertCellValue(testPuzzle, 3, 5, 1)
insertCellValue(testPuzzle, 6, 7, 1)
insertCellValue(testPuzzle, 8, 0, 2)
insertCellValue(testPuzzle, 7, 4, 2)
insertCellValue(testPuzzle, 4, 6, 2)
insertCellValue(testPuzzle, 1, 8, 2)
insertCellValue(testPuzzle, 3, 0, 3)
insertCellValue(testPuzzle, 9, 1, 4)
insertCellValue(testPuzzle, 8, 3, 4)
insertCellValue(testPuzzle, 6, 5, 4)
insertCellValue(testPuzzle, 6, 0, 5)
insertCellValue(testPuzzle, 1, 2, 5)
insertCellValue(testPuzzle, 2, 7, 5)
insertCellValue(testPuzzle, 4, 8, 5)
insertCellValue(testPuzzle, 8, 1, 6)
insertCellValue(testPuzzle, 9, 2, 6)
insertCellValue(testPuzzle, 7, 6, 7)
insertCellValue(testPuzzle, 9, 8, 7)
insertCellValue(testPuzzle, 8, 4, 8)
insertCellValue(testPuzzle, 6, 8, 8)
testPuzzle.printPuzzle()
testPuzzle.printPuzzleCandidates()
