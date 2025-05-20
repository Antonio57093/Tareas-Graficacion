import cv2 as cv
import numpy as np

img = np.ones((500, 500, 3), dtype=np.uint8)*255 
cv.circle(img, (250, 250), 50, (0,234,21), -1)
cv.circle(img, (100, 100), 30, (0,0,0), -1)


#punto inicial,punto final,color,grosor
cv.line(img, (100,100), (300, 100), (0,234,21), 3   )
#punto inicial,punto final,color,grosor
cv.rectangle(img, (20,20), (50,60), (0,0,0), 3 )


cv.imshow('img', img)
cv.waitKey()
cv.destroyAllWindows()


