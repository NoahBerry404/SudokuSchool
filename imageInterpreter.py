from Classes import *
import numpy as np
import cv2
import pytesseract as pt

fileName = input("Enter a local Sudoku image file name: ")
puzzleImg = cv2.imread(fileName, cv2.IMREAD_GRAYSCALE)
if puzzleImg is None:
    raise Exception("Image read failed")
xBounds = [-1, -1]
yBounds = [-1, -1]
boundsInput = input("Enter the position of one of the puzzle's corners in \"x y\" format: ")
xBounds[0], yBounds[0] = [int(bound) for bound in boundsInput.split()]
boundsInput = input("Enter the position of the opposite corner in \"x y\" format: ")
xBounds[1], yBounds[1] = [int(bound) for bound in boundsInput.split()]
left = min(xBounds)
right = max(xBounds)
bottom = min(yBounds)
top = max(yBounds)
cellWidth = (right - left) / 9
cellHeight = (top - bottom) / 9
for row in range(9):
    for col in range(9):
        cellRowBounds = [round(row*cellHeight), round((row+1)*cellHeight)]
        cellColBounds = [round(col*cellWidth), round((col+1)*cellWidth)]
        currentCellImg = puzzleImg[cellRowBounds[0]:cellRowBounds[1], cellColBounds[0]:cellColBounds[1]]
        readString = pt.image_to_string(currentCellImg)