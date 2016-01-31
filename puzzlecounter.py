import cv2
import numpy as np
import sys

# Setup the image(s)
img = cv2.imread(sys.argv[1], 0); # Finding contours requires grayscale
img2 = cv2.imread(sys.argv[1]);  # Draw colors on this one

ret,thresh = cv2.threshold(img, 150, 255, 0);
contours,hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE);

contourAreaList = []
# declare vars

numSweet = 0
numLess = 0
numGreater = 0
area = 0

# Extract the area
for contour in contours:
    area = cv2.contourArea(contour)
    contourAreaList.append(area);

aMedian = np.median(contourAreaList);

# Color the pieces. Green = Good, Red = Bigger, Blue = Smaller
for index, contourArea in enumerate(contourAreaList, start=0):
    if contourArea > aMedian * 1.5 :
        # OpenCV using BGR hence this is Red, not Blue in RGB
        cv2.drawContours(img2, contours, index, (0, 0, 255), -1)
        numGreater += 1
    elif contourArea < aMedian / 2 :
        cv2.drawContours(img2, contours, index, (255, 0, 0), -1)
        numLess += 1
    else :
        numSweet += 1
        cv2.drawContours(img2, contours, index, (0, 255, 0), -1)


# Plop out results, because plopping out is the best
print 'Number of objects within acceptable range:', numSweet
print 'Number of objects > 1.5 * Median:', numGreater
print 'Number of objects < 2 * Median:', numLess
print 'Number of objects total:', numSweet + numGreater + numLess
print 'Median:', aMedian
print 'Mean:', np.mean(contourAreaList)

cv2.imwrite('piuz-2.jpg', img2);
