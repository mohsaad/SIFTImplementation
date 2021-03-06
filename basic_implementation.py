# Mohammad Saad and Saad Paya
# An implementation of SIFT which uses OpenCV
# For the demo on 3/10/2015

import numpy as np
import cv2
import math
import io

def main():
	img = cv2.imread("test.jpg")
	img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

	template = cv2.imread("waldo.jpg")
	template = cv2.cvtColor(template,cv2.COLOR_BGR2GRAY)

	sift = cv2.SIFT()
	kp_img, des_img = sift.detectAndCompute(img, None)
	kp_temp, des_temp = sift.detectAndCompute(template, None)

	bf = cv2.BFMatcher()

	matches = bf.knnMatch(des_img, des_temp, k=2)
	good = []
	for m,n in matches:
	    if m.distance < 0.25*n.distance:
	        good.append([m,n])

	
	drawMatches(img, kp_img, template, kp_temp, good[:20])





def drawMatches(img1, kp1, img2, kp2, matches):
    """
    Taken from http://stackoverflow.com/questions/20259025/module-object-has-no-attribute-drawmatches-opencv-python
    My own implementation of cv2.drawMatches as OpenCV 2.4.9
    does not have this function available but it's supported in
    OpenCV 3.0.0

    This function takes in two images with their associated 
    keypoints, as well as a list of DMatch data structure (matches) 
    that contains which keypoints matched in which images.

    An image will be produced where a montage is shown with
    the first image followed by the second image beside it.

    Keypoints are delineated with circles, while lines are connected
    between matching keypoints.

    img1,img2 - Grayscale images
    kp1,kp2 - Detected list of keypoints through any of the OpenCV keypoint 
              detection algorithms
    matches - A list of matches of corresponding keypoints through any
              OpenCV keypoint matching algorithm
    """

    # Create a new output image that concatenates the two images together
    # (a.k.a) a montage
    rows1 = img1.shape[0]
    cols1 = img1.shape[1]
    rows2 = img2.shape[0]
    cols2 = img2.shape[1]

    out = np.zeros((max([rows1,rows2]),cols1+cols2,3), dtype='uint8')

    # Place the first image to the left
    out[:rows1,:cols1,:] = np.dstack([img1, img1, img1])

    # Place the next image to the right of it
    out[:rows2,cols1:cols1+cols2,:] = np.dstack([img2, img2, img2])

    # For each pair of points we have between both images
    # draw circles, then connect a line between them
    for mat in matches:

        # Get the matching keypoints for each of the images
        img1_idx = mat[0].queryIdx
        img2_idx = mat[1].trainIdx

        # x - columns
        # y - rows
        (x1,y1) = kp1[img1_idx].pt
        (x2,y2) = kp2[img2_idx].pt

        # Draw a small circle at both co-ordinates
        # radius 4
        # colour blue
        # thickness = 1
        cv2.circle(out, (int(x1),int(y1)), 4, (255, 0, 0), 1)   
        cv2.circle(out, (int(x2)+cols1,int(y2)), 4, (255, 0, 0), 1)

        # Draw a line in between the two points
        # thickness = 1
        # colour blue
        cv2.line(out, (int(x1),int(y1)), (int(x2)+cols1,int(y2)), (255, 0, 0), 1)


    # Show the image
    cv2.imshow('Matched Features', out)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == '__main__':
	main()