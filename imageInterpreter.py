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
blurredImages = []
for blurAmount in range(3, 12, 2):
    blurredImages.append(cv2.medianBlur(puzzleImg, blurAmount))
threshImages = []
for blurredImg in blurredImages:
    _, threshImg = cv2.threshold(blurredImg, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    threshImages.append(threshImg)
cellDimensions = puzzleDimension / 9
readPuzzle = Puzzle()
images = []
for image in threshImages:
    images.append(cv2.bitwise_not(image))
count = 1
for img in images:
    cv2.imwrite("Processed" + str(count) + ".png", img)
    count += 1
for row in range(9):
    for col in range(9):
        cellRowBounds = [round(row*cellDimensions), round((row+1)*cellDimensions)]
        cellColBounds = [round(col*cellDimensions), round((col+1)*cellDimensions)]
        currentCellImg = images[0][cellRowBounds[0]:cellRowBounds[1], cellColBounds[0]:cellColBounds[1]]
        cellHeight = cellRowBounds[1] - cellRowBounds[0]
        cellWidth = cellColBounds[1] - cellColBounds[0]
        innerCellImg = currentCellImg[cellHeight//4:cellHeight*3//4, cellWidth//4:cellWidth*3//4]
        # pixelCount = innerCellImg.size - cv2.countNonZero(innerCellImg)
        pixelCount = cv2.countNonZero(innerCellImg)
        if pixelCount > innerCellImg.size / 10:
            contours, hierarchy = cv2.findContours(currentCellImg, cv2.RETR_TREE , cv2.CHAIN_APPROX_SIMPLE)
            largestContour = max(contours, key=lambda ctr: ctr.size)
            x, y, w, h = cv2.boundingRect(largestContour)
            # roi = currentCellImg[y:y+h, x:x+w]
            # cv2.imwrite("roi.png", roi)
            # Contour Testing
            # cv2.drawContours(currentCellImg, contours, -1, (0,255,0), 3)
            # color = cv2.cvtColor(currentCellImg, cv2.COLOR_GRAY2BGR)
            # cv2.drawContours(color, [contours[1]], -1, (0, 255, 0), 3)
            # cv2.imwrite("contour.png", color)
            
            #extraSpace = puzzleDimension // 200
            extraSpace = 10
            readStrings = []
            count = 1
            for img in threshImages:
                currentCellImg = img[cellRowBounds[0]:cellRowBounds[1], cellColBounds[0]:cellColBounds[1]][y:y+h, x:x+w]
                paddedCellImg = None
                paddedCellImg = cv2.copyMakeBorder(currentCellImg, extraSpace, extraSpace, extraSpace, extraSpace, cv2.BORDER_CONSTANT | cv2.BORDER_ISOLATED, value=255)
                cv2.imwrite("currentCell.png", paddedCellImg)
                # input("Proceed?")
                readString = pt.image_to_string(paddedCellImg, config='-c tessedit_char_whitelist="123456789" --psm 10').strip()
                if len(readString) == 1:
                    print(readString)
                    readStrings.append(readString)
                count += 1
            string_counts = Counter(readStrings)
            if len(readStrings) > 0:
                bestString = string_counts.most_common(1)[0][0]
                readPuzzle.setCellValue(int(bestString), col+1, row+1)
print(readPuzzle.printPuzzle())