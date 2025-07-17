from Classes import *
import cv2
import pytesseract as pt

def readPuzzleImage(puzzleImg, xBounds: list[int, int], yBounds: list[int, int]) -> Puzzle:
    left = min(xBounds)
    right = max(xBounds)
    bottom = min(yBounds)
    top = max(yBounds)
    puzzleImg = puzzleImg[bottom:top, left:right]
    puzzleDimension = 500
    puzzleImg = cv2.resize(puzzleImg, (puzzleDimension, puzzleDimension))
    blurredImages = []
    for blurAmount in range(3, 10, 2):
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
    for img in threshImages:
        count += 1
    for row in range(9):
        for col in range(9):
            cellRowBounds = [round(row*cellDimensions), round((row+1)*cellDimensions)]
            cellColBounds = [round(col*cellDimensions), round((col+1)*cellDimensions)]
            currentCellImg = images[0][cellRowBounds[0]:cellRowBounds[1], cellColBounds[0]:cellColBounds[1]]
            cellHeight = cellRowBounds[1] - cellRowBounds[0]
            cellWidth = cellColBounds[1] - cellColBounds[0]
            innerCellImg = currentCellImg[cellHeight//4:cellHeight*3//4, cellWidth//4:cellWidth*3//4]
            pixelCount = cv2.countNonZero(innerCellImg)
            if pixelCount > innerCellImg.size / 10:
                contours, _ = cv2.findContours(currentCellImg, cv2.RETR_TREE , cv2.CHAIN_APPROX_SIMPLE)
                largestContour = max(contours, key=lambda ctr: ctr.size)
                x, y, w, h = cv2.boundingRect(largestContour)
                extraSpace = 10
                for img in threshImages:
                    currentCellImg = img[cellRowBounds[0]:cellRowBounds[1], cellColBounds[0]:cellColBounds[1]][y:y+h, x:x+w]
                    paddedCellImg = None
                    paddedCellImg = cv2.copyMakeBorder(currentCellImg, extraSpace, extraSpace, extraSpace, extraSpace, cv2.BORDER_CONSTANT | cv2.BORDER_ISOLATED, value=255)
                    readString = pt.image_to_string(paddedCellImg, config='-c tessedit_char_whitelist="123456789" --psm 10').strip()
                    if len(readString) == 1:
                        readPuzzle.setCellValue(int(readString), col+1, row+1, False)
                        break
    return readPuzzle