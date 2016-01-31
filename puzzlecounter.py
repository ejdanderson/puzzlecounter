import cv2

# Setup the image(s)
img = cv2.imread('dots4.jpg', 0); # Finding contours requires grayscale
img2 = cv2.imread('dots4.jpg'); # Draw colors on this one
ret,thresh = cv2.threshold(img, 127, 255, 0);
contours,hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE);

# declare vars
aTot = 0
lTot = 0
numObj = 0
aAvg = 0
lAvg = 0
aSumDeviation = 0
lSumDeviation = 0

# Math
for contour in contours:
    aTot += cv2.contourArea(contour)
    lTot += cv2.arcLength(contour, True)
    numObj += 1

aAvg = aTot / numObj
lAvg = lTot / numObj

# Calc Std Deviation
for contour in contours:
    aSumDeviation += (cv2.contourArea(contour) - aAvg) ** 2
    lSumDeviation += (cv2.arcLength(contour, True) - lAvg ) ** 2

aStdDev = ( aSumDeviation / numObj ) ** 0.5
lStdDev = ( lSumDeviation / numObj ) ** 0.5

# Color the pieces. Green = Good,  Red = Bigger then 1 std dev. Blue = Smaller than 1 Std Dev
for index, contour in enumerate(contours, start=0):
    if cv2.contourArea(contour) > aAvg + aStdDev :
        # OpenCV using BGR hence this is Red, not Blue in RGB
        cv2.drawContours(img2, contours, index, (0, 0, 255), -1);
    elif cv2.contourArea(contour) < aAvg - aStdDev :
        cv2.drawContours(img2, contours, index, (255, 0, 0), -1);
    else :
        cv2.drawContours(img2, contours, index, (0, 255, 0), -1);

# Plop out results, because plopping out is the best
# print aTot,aAvg
# print lTot, lAvg
# print aStdDev,lStdDev
print 'Number of objects:', numObj

cv2.imwrite('dotsp.jpg', img2);
