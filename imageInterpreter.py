from Classes import *
import cv2
import pytesseract as pt
from collections import Counter

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
puzzleImg = puzzleImg[left:right, bottom:top]
puzzleDimension = 1000
puzzleImg = cv2.resize(puzzleImg, (puzzleDimension, puzzleDimension))
# puzzleImg = cv2.medianBlur(puzzleImg, 5)
blurredImages = []
for blurAmount in range(3, 16, 2):
    # blurredImages.append(cv2.GaussianBlur(puzzleImg,(blurAmount,blurAmount),0))
    blurredImages.append(cv2.medianBlur(puzzleImg, blurAmount))
threshImages = []
for blurredImg in blurredImages:
    _, threshImg = cv2.threshold(blurredImg, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    threshImages.append(threshImg)
cellDimensions = puzzleDimension / 9
# borderThickness = puzzleDimension // 200
borderThickness = 0
readPuzzle = Puzzle()
# Preprocessing Debugging
images = threshImages
count = 1
for img in images:
    cv2.imwrite("Processed" + str(count) + ".png", img)
    count += 1
for row in range(9):
    for col in range(9):
        cellRowBounds = [round(row*cellDimensions) + borderThickness, round((row+1)*cellDimensions) - borderThickness]
        cellColBounds = [round(col*cellDimensions) + borderThickness, round((col+1)*cellDimensions) - borderThickness]
        currentCellImg = images[0][cellRowBounds[0]:cellRowBounds[1], cellColBounds[0]:cellColBounds[1]]
        cellHeight = cellRowBounds[1] - cellRowBounds[0]
        cellWidth = cellColBounds[1] - cellColBounds[0]
        innerCellImg = currentCellImg[cellHeight//4:cellHeight*3//4, cellWidth//4:cellWidth*3//4]
        pixelCount = innerCellImg.size - cv2.countNonZero(innerCellImg)
        if pixelCount > innerCellImg.size / 10:
            readStrings = []
            count = 1
            for img in images:
                currentCellImg = img[cellRowBounds[0]:cellRowBounds[1], cellColBounds[0]:cellColBounds[1]]
                readString = pt.image_to_string(currentCellImg, config='-c tessedit_char_whitelist="123456789" --psm 10').strip()
                if len(readString) == 1:
                    readStrings.append(readString)
                count += 1
            string_counts = Counter(readStrings)
            if len(readStrings) > 0:
                bestString = string_counts.most_common(1)[0][0]
                readPuzzle.setCellValue(int(bestString), col+1, row+1)
print(readPuzzle.printPuzzle())