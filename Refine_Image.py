import numpy as np
from PIL import Image
import timeit
import math
import cv2
import os
import random
from skimage import measure


def chooseImage(img1, img2, img_name, return_image):
    if img1.shape[0]*img1.shape[1] == 1 and img2.shape[0]*img2.shape[1] == 1:
        print("Image Rendered Invalid (Both empty)")
        img_chosen = np.zeros((1,1),np.uint8)
        return "Invalid"
    elif img1.shape[0]*img1.shape[1] == 1:
        img_chosen = img2
    elif img2.shape[0]*img2.shape[1] == 1:
        img_chosen = img1
    else:
        black_pixels1 = img1.shape[0]*img1.shape[1] - np.sum(img1 == 255)
        black_pixels2 = img2.shape[0]*img2.shape[1] - np.sum(img2 == 255)
        if black_pixels2 > black_pixels1:
            if black_pixels2*0.4 < black_pixels1:
                img_chosen = img1
            else:
                img_chosen = img2
        else:
            img_chosen = img1

    if img_chosen.shape[0]*img_chosen.shape[1] != 1:
        #cv2.imshow('Chosen',img_chosen)
        #cv2.moveWindow('Chosen', 100, 100)
        #cv2.waitKey(0)
        #cv2.destroyAllWindows()

        img = img_chosen
        img = cv2.resize(img, (20, 20))

        if return_image == False:
            if 'ComputerGenerated' in img_name:
                path = 'C:/Users/Kaden McKeen/Desktop/Programming/Python/Machine Learning/Captcha Neural Network/ComputerGenerated'
                cv2.imwrite(os.path.join(path , "T" + str(img_name[18:])), img)
            else:
                cv2.imwrite("T" + str(img_name),img)
                print("Refined image T{0}".format(str(img_name)))
        else:
            return img
    else:
        return "Invalid"


def find_if_close(cnt1,cnt2):
    row1,row2 = cnt1.shape[0],cnt2.shape[0]
    for i in range(row1):
        for j in range(row2):
            dist = np.linalg.norm(cnt1[i]-cnt2[j])
            if abs(dist) < 50 :
                return True
            elif i==row1-1 and j==row2-1:
                return False

def analyzeImages1(img, show_process):
    if True:
        if show_process:
            cv2.imshow('Original',img)
            cv2.moveWindow('Original', 100, 100)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
        
        img = cv2.Canny(img,100,150,apertureSize = 7)

        if show_process:
            cv2.imshow('Canny',img)
            cv2.moveWindow('Canny', 100, 100)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

        kernel = np.ones((3, 3),np.uint8)
        img = cv2.dilate(img,kernel,iterations = 1)

        if show_process:
            cv2.imshow('Morph Dilate',img)
            cv2.moveWindow('Morph Dilate', 100, 100)
            cv2.waitKey(0)
            cv2.destroyAllWindows()


        kernel = np.ones((3, 3),np.uint8)
        img = cv2.erode(img,kernel,iterations = 1)

        if show_process:
            cv2.imshow('Morph Erode',img)
            cv2.moveWindow('Morph Erode', 100, 100)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

        kernel = np.ones((4, 4),np.uint8)
        img = cv2.dilate(img,kernel,iterations = 1)

        if show_process:
            cv2.imshow('Morph Dilate',img)
            cv2.moveWindow('Morph Dilate', 100, 100)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

        kernel = np.ones((2, 2),np.uint8)
        img = cv2.erode(img,kernel,iterations = 1)

        if show_process:
            cv2.imshow('Morph Erosion',img)
            cv2.moveWindow('Morph Erosion', 100, 100)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
        
        labels = measure.label(img, neighbors=8, background=255)
        mask = np.zeros(img.shape, dtype="uint8")

        for label in np.unique(labels):
            if label == 0:
                continue

            labelMask = np.zeros(img.shape, dtype="uint8")
            labelMask[labels == label] = 255
            numPixels = cv2.countNonZero(labelMask)
     
            if numPixels > 1000:
                mask = cv2.add(mask, labelMask)

        img = 255 - mask

        if show_process:
            cv2.imshow('Blob Deletion',img)
            cv2.moveWindow('Blob Deletion', 100, 100)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

        kernel = np.ones((3, 3),np.uint8)
        img = cv2.dilate(img,kernel,iterations = 1)

        if show_process:
            cv2.imshow('Morph Dilate',img)
            cv2.moveWindow('Morph Dilate', 100, 100)
            cv2.waitKey(0)
            cv2.destroyAllWindows()


        labels = measure.label(img, neighbors=8, background=255)
        mask = np.zeros(img.shape, dtype="uint8")

        for label in np.unique(labels):
            if label == 0:
                continue

            labelMask = np.zeros(img.shape, dtype="uint8")
            labelMask[labels == label] = 255
            numPixels = cv2.countNonZero(labelMask)
     
            if numPixels > 200:
                mask = cv2.add(mask, labelMask)

        img = 255 - mask

        if show_process:
            cv2.imshow('Blob Deletion',img)
            cv2.moveWindow('Blob Deletion', 100, 100)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

        kernel = np.ones((4, 4),np.uint8)
        img = cv2.dilate(img,kernel,iterations = 1)

        if show_process:
            cv2.imshow('Morph Dilate',img)
            cv2.moveWindow('Morph Dilate', 100, 100)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
        
        for i in range(2):
            kernel = np.ones((4, 4),np.uint8)
            img = cv2.erode(img,kernel,iterations = 1)
            img = cv2.blur(img,(3,3))
            kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
            img = cv2.filter2D(img, -1, kernel)
            kernel = np.ones((4, 4),np.uint8)
            img = cv2.dilate(img,kernel,iterations = 1)

        ret, ing = cv2.threshold(img,127,255,0)

        if show_process:
            cv2.imshow('Smooth',img)
            cv2.moveWindow('Smooth', 100, 100)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
        
        labels = measure.label(img, neighbors=8, background=255)
        mask = np.zeros(img.shape, dtype="uint8")

        for label in np.unique(labels):
            if label == 0:
                continue

            labelMask = np.zeros(img.shape, dtype="uint8")
            labelMask[labels == label] = 255
            numPixels = cv2.countNonZero(labelMask)
            if numPixels > 400:
                mask = cv2.add(mask, labelMask)

        img = 255 - mask

        if show_process:
            cv2.imshow('Blob Deletion',img)
            cv2.moveWindow('Blob Deletion', 100, 100)
            cv2.waitKey(0)
            cv2.destroyAllWindows()


        row, col= img.shape[:2]
        bottom= img[row-2:row, 0:col]
        mean = 255

        bordersize=10
        img = cv2.copyMakeBorder(img, top=bordersize, bottom=bordersize, left=bordersize, right=bordersize, borderType= cv2.BORDER_CONSTANT, value=[mean,mean,mean] )

        
        ret,img = cv2.threshold(img,127,255,0)
        _,contours,hierarchy = cv2.findContours(img,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)

        if len(contours) > 1:
            for cnt in contours:
                x,y,w,h = cv2.boundingRect(cnt)
                M = cv2.moments(cnt)
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])
                if w < 90 and h < 90:
                    if math.sqrt(math.pow(cX-img.shape[1],2)+math.pow(cY-img.shape[0],2)) > (img.shape[0]+img.shape[1])/2:
                        cv2.drawContours(img, [cnt], -1, 255, -1)
        
        if show_process:
            cv2.imshow('Perimeter/Distance Away Restriction',img)
            cv2.moveWindow('Perimeter Restriction', 100, 100)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

        _,contours,hierarchy = cv2.findContours(img,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)

        if np.sum(img == 255) < img.shape[0]*img.shape[1]*0.99:
            kernel = np.ones((6, 6),np.uint8)
            img = cv2.erode(img,kernel,iterations = 1)

            if show_process:
                cv2.imshow('Morph Erode',img)
                cv2.moveWindow('Morph Erode', 100, 100)
                cv2.waitKey(0)
                cv2.destroyAllWindows()
            
            img = 255-img
            for side in range(4):
                while True:
                    if side == 0:
                        numPixels = cv2.countNonZero(img)
                        img = img[0:img.shape[0], 0:img.shape[1]-1]
                        if  abs(numPixels - cv2.countNonZero(img)) > 3:
                            break
                    if side == 1:
                        numPixels = cv2.countNonZero(img)
                        img = img[0:img.shape[0], 1:img.shape[1]]
                        if abs(numPixels - cv2.countNonZero(img)) > 3:
                            break
                    if side == 2:
                        numPixels = cv2.countNonZero(img)
                        img = img[0:img.shape[0]-1, 0:img.shape[1]]
                        if  abs(numPixels - cv2.countNonZero(img)) > 3:
                            break
                    if side == 3:
                        numPixels = cv2.countNonZero(img)
                        img = img[1:img.shape[0], 0:img.shape[1]]
                        if  abs(numPixels - cv2.countNonZero(img)) > 3:
                            break 

            img = 255-img

            if show_process:
                cv2.imshow('Centered',img)
                cv2.moveWindow('Centered', 100, 100)
                cv2.waitKey(0)
                cv2.destroyAllWindows()

            max_dimension = max(img.shape[0],img.shape[1])
            img_large = np.zeros((max_dimension*2,max_dimension*2),np.uint8)
            img_large[:] = 255
            x_offset = int(max_dimension/2)
            y_offset = int(max_dimension/2)
            img_large[y_offset:y_offset+img.shape[0], x_offset:x_offset+img.shape[1]] = img
            img = img_large

            if show_process:
                cv2.imshow('Resized',img)
                cv2.moveWindow('Resized', 100, 100)
                cv2.waitKey(0)
                cv2.destroyAllWindows()

            ret,thresh = cv2.threshold(img,127,255,0)
            _,contours,hier = cv2.findContours(thresh,cv2.RETR_LIST,2)
            contours = contours[:]
            LENGTH = len(contours)
            status = np.zeros((LENGTH,1))

            for i,cnt1 in enumerate(contours):
                x = i    
                if i != LENGTH-1:
                    for j,cnt2 in enumerate(contours[i+1:]):
                        x = x+1
                        dist = find_if_close(cnt1,cnt2)
                        if dist == True:
                            val = min(status[i],status[x])
                            status[x] = status[i] = val
                        else:
                            if status[x]==status[i]:
                                status[x] = i+1

            unified = []
            maximum = int(status.max())+1
            for i in range(maximum):
                pos = np.where(status==i)[0]
                if pos.size != 0:
                    cont = np.vstack(contours[i] for i in pos)
                    hull = cv2.convexHull(cont)
                    unified.append(hull)

            img_boundaries = img.copy()
            cv2.drawContours(img_boundaries,unified,-1,(0,255,0),2)
            cv2.drawContours(thresh,unified,-1,255,-1)

            img_boundaries = img_boundaries[8:img_boundaries.shape[0]-8,8:img_boundaries.shape[1]-8]

            if show_process:
                cv2.imshow('Unified/Fix Rotation',img_boundaries)
                cv2.moveWindow('Unified/Fix Rotation', 100, 100)
                cv2.waitKey(0)
                cv2.destroyAllWindows()

            _, contours, hierarchy = cv2.findContours(img_boundaries,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
            contours = contours[1:]
            areas = [cv2.contourArea(c) for c in contours]
            max_index = np.argmax(areas)
            cnt=contours[max_index]
            rect = cv2.minAreaRect(cnt)
            box = cv2.boxPoints(rect)
            box = np.int0(box)
            cv2.drawContours(img_boundaries,[box],0,(0,0,255),-1)

            if show_process:
                cv2.imshow('Bounding Box',img_boundaries)
                cv2.moveWindow('Bounding Box', 100, 100)
                cv2.waitKey(0)
                cv2.destroyAllWindows()

            angle = rect[2]
            
            if angle < -45:
                angle += 90

            (h, w) = img_boundaries.shape[:2]
            center = (w // 2, h // 2)
            M = cv2.getRotationMatrix2D(center, angle, 1.0)
            img = cv2.warpAffine(img, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)

            if show_process:
                cv2.imshow('Rotated',img)
                cv2.moveWindow('Rotated', 100, 100)
                cv2.waitKey(0)
                cv2.destroyAllWindows()

            img = 255-img
            for side in range(4):
                while True:
                    if side == 0:
                        numPixels = cv2.countNonZero(img)
                        img = img[0:img.shape[0], 0:img.shape[1]-1]
                        if  abs(numPixels - cv2.countNonZero(img)) > 3:
                            break
                    if side == 1:
                        numPixels = cv2.countNonZero(img)
                        img = img[0:img.shape[0], 1:img.shape[1]]
                        if abs(numPixels - cv2.countNonZero(img)) > 3:
                            break
                    if side == 2:
                        numPixels = cv2.countNonZero(img)
                        img = img[0:img.shape[0]-1, 0:img.shape[1]]
                        if  abs(numPixels - cv2.countNonZero(img)) > 3:
                            break
                    if side == 3:
                        numPixels = cv2.countNonZero(img)
                        img = img[1:img.shape[0], 0:img.shape[1]]
                        if  abs(numPixels - cv2.countNonZero(img)) > 3:
                            break

            img = 255-img

            if show_process:
                cv2.imshow('Refined',img)
                cv2.moveWindow('Refined', 100, 100)
                cv2.waitKey(0)
                cv2.destroyAllWindows()

            #image_square = np.zeros((max(img.shape),max(img.shape)),np.uint8)
            #image_square[:] = 255
            #x_offset = int(img.shape[0]/max(img.shape[0],img.shape[1])*img.shape[1]/max(img.shape[0],img.shape[1])/2)
            #y_offset = int(img.shape[0]/max(img.shape[0],img.shape[1])*img.shape[1]/max(img.shape[0],img.shape[1])/2)

            #image_square[y_offset:y_offset+img.shape[0], x_offset:x_offset+img.shape[1]] = img
            #img = image_square

            max_dimension = max(img.shape[0],img.shape[1])
            img_square = np.zeros((int(max_dimension*1.5),int(max_dimension*1.5)),np.uint8)
            img_square[:] = 255
            if img.shape[0] == max_dimension:
                x_offset = int(max_dimension/2)
                y_offset = int(max_dimension/3)
            if img.shape[1] == max_dimension:
                x_offset = int(max_dimension/3)
                y_offset = int(max_dimension/2)
            
            img_square[y_offset:y_offset+img.shape[0], x_offset:x_offset+img.shape[1]] = img
            img = img_square

            if show_process:
                cv2.imshow('Square',img)
                cv2.moveWindow('Square', 100, 100)
                cv2.waitKey(0)
                cv2.destroyAllWindows()

            return img

        else:
            print("Nothing left - 1")
            return np.zeros((1,1),np.uint8)


def analyzeImages2(img, show_process):
    if True:
        if show_process:
            cv2.imshow('Original',img)
            cv2.moveWindow('Original', 100, 100)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
        
        img = cv2.Canny(img,100,150,apertureSize = 7)

        if show_process:
            cv2.imshow('Canny',img)
            cv2.moveWindow('Canny', 100, 100)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

        kernel = np.ones((4, 4),np.uint8)
        img = cv2.dilate(img,kernel,iterations = 1)

        if show_process:
            cv2.imshow('Morph Dilate',img)
            cv2.moveWindow('Morph Dilate', 100, 100)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

        cv2.fastNlMeansDenoising(img, None, h=30, templateWindowSize=7, searchWindowSize=21)

        if show_process:
                cv2.imshow('Denoise',img)
                cv2.moveWindow('Denoise', 100, 100)
                cv2.waitKey(0)
                cv2.destroyAllWindows()
        
        labels = measure.label(img, neighbors=8, background=255)
        mask = np.zeros(img.shape, dtype="uint8")

        for label in np.unique(labels):
            if label == 0:
                continue

            labelMask = np.zeros(img.shape, dtype="uint8")
            labelMask[labels == label] = 255
            numPixels = cv2.countNonZero(labelMask)
     
            if numPixels > 200:
                mask = cv2.add(mask, labelMask)

        img = 255 - mask

        if show_process:
            cv2.imshow('Blob Deletion',img)
            cv2.moveWindow('Blob Deletion', 100, 100)
            cv2.waitKey(0)
            cv2.destroyAllWindows()


        kernel = np.ones((3, 3),np.uint8)
        img = cv2.erode(img,kernel,iterations = 1)

        if show_process:
            cv2.imshow('Morph Erode',img)
            cv2.moveWindow('Morph Erode', 100, 100)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

        cv2.fastNlMeansDenoising(img, None, h=20, templateWindowSize=7, searchWindowSize=21)

        if show_process:
                cv2.imshow('Denoise',img)
                cv2.moveWindow('Denoise', 100, 100)
                cv2.waitKey(0)
                cv2.destroyAllWindows()

        kernel = np.ones((3, 3),np.uint8)
        img = cv2.dilate(img,kernel,iterations = 1)

        if show_process:
            cv2.imshow('Morph Dilate',img)
            cv2.moveWindow('Morph Dilate', 100, 100)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
        
        for i in range(2):
            kernel = np.ones((5, 5),np.uint8)
            img = cv2.erode(img,kernel,iterations = 1)

            if show_process:
                cv2.imshow('Morph Erode',img)
                cv2.moveWindow('Morph Erode', 100, 100)
                cv2.waitKey(0)
                cv2.destroyAllWindows()

            kernel = np.ones((5, 5),np.uint8)
            img = cv2.dilate(img,kernel,iterations = 1)

            if show_process:
                cv2.imshow('Morph Dilate',img)
                cv2.moveWindow('Morph Dilate', 100, 100)
                cv2.waitKey(0)
                cv2.destroyAllWindows()

            kernel = np.ones((2, 2),np.uint8)
            img = cv2.erode(img,kernel,iterations = 1)

        if show_process:
            cv2.imshow('Morph Erosion',img)
            cv2.moveWindow('Morph Erosion', 100, 100)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
        
        labels = measure.label(img, neighbors=8, background=255)
        mask = np.zeros(img.shape, dtype="uint8")

        for label in np.unique(labels):
            if label == 0:
                continue

            labelMask = np.zeros(img.shape, dtype="uint8")
            labelMask[labels == label] = 255
            numPixels = cv2.countNonZero(labelMask)
     
            if numPixels > 1000:
                mask = cv2.add(mask, labelMask)

        img = 255 - mask

        if show_process:
            cv2.imshow('Blob Deletion',img)
            cv2.moveWindow('Blob Deletion', 100, 100)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

        kernel = np.ones((3, 3),np.uint8)
        img = cv2.erode(img,kernel,iterations = 1)

        if show_process:
            cv2.imshow('Morph Erosion',img)
            cv2.moveWindow('Morph Erosion', 100, 100)
            cv2.waitKey(0)
            cv2.destroyAllWindows()


        labels = measure.label(img, neighbors=8, background=255)
        mask = np.zeros(img.shape, dtype="uint8")

        for label in np.unique(labels):
            if label == 0:
                continue

            labelMask = np.zeros(img.shape, dtype="uint8")
            labelMask[labels == label] = 255
            numPixels = cv2.countNonZero(labelMask)
     
            if numPixels > 200:
                mask = cv2.add(mask, labelMask)

        img = 255 - mask

        if show_process:
            cv2.imshow('Blob Deletion',img)
            cv2.moveWindow('Blob Deletion', 100, 100)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

        kernel = np.ones((3, 3),np.uint8)
        img = cv2.dilate(img,kernel,iterations = 1)

        if show_process:
            cv2.imshow('Morph Dilate',img)
            cv2.moveWindow('Morph Dilate', 100, 100)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
        
        for i in range(2):
            kernel = np.ones((4, 4),np.uint8)
            img = cv2.erode(img,kernel,iterations = 1)
            img = cv2.blur(img,(3,3))
            kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
            img = cv2.filter2D(img, -1, kernel)
            kernel = np.ones((3, 3),np.uint8)
            img = cv2.dilate(img,kernel,iterations = 1)

        ret, ing = cv2.threshold(img,127,255,0)

        if show_process:
            cv2.imshow('Smooth',img)
            cv2.moveWindow('Smooth', 100, 100)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
        
        labels = measure.label(img, neighbors=8, background=255)
        mask = np.zeros(img.shape, dtype="uint8")

        for label in np.unique(labels):
            if label == 0:
                continue

            labelMask = np.zeros(img.shape, dtype="uint8")
            labelMask[labels == label] = 255
            numPixels = cv2.countNonZero(labelMask)
            if numPixels > 400:
                mask = cv2.add(mask, labelMask)

        img = 255 - mask

        if show_process:
            cv2.imshow('Blob Deletion',img)
            cv2.moveWindow('Blob Deletion', 100, 100)
            cv2.waitKey(0)
            cv2.destroyAllWindows()


        row, col= img.shape[:2]
        bottom= img[row-2:row, 0:col]
        mean = 255

        bordersize=10
        img = cv2.copyMakeBorder(img, top=bordersize, bottom=bordersize, left=bordersize, right=bordersize, borderType= cv2.BORDER_CONSTANT, value=[mean,mean,mean] )

        
        ret,img = cv2.threshold(img,127,255,0)
        _,contours,hierarchy = cv2.findContours(img,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)

        if len(contours) > 1:
            for cnt in contours:
                x,y,w,h = cv2.boundingRect(cnt)
                M = cv2.moments(cnt)
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])
                if w < 100 and h < 100:
                    if math.sqrt(math.pow(cX-img.shape[1],2)+math.pow(cY-img.shape[0],2)) > (img.shape[0]+img.shape[1])/2.2:
                        cv2.drawContours(img, [cnt], -1, 255, -1)
        
        if show_process:
            cv2.imshow('Perimeter/Distance Away Restriction',img)
            cv2.moveWindow('Perimeter Restriction', 100, 100)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

        _,contours,hierarchy = cv2.findContours(img,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)

        if np.sum(img == 255) < img.shape[0]*img.shape[1]*0.99:
            kernel = np.ones((4, 4),np.uint8)
            img = cv2.erode(img,kernel,iterations = 1)
            
            if show_process:
                cv2.imshow('Morph Erode',img)
                cv2.moveWindow('Morph Erode', 100, 100)
                cv2.waitKey(0)
                cv2.destroyAllWindows()
            
            img = 255-img
            for side in range(4):
                while True:
                    if side == 0:
                        numPixels = cv2.countNonZero(img)
                        img = img[0:img.shape[0], 0:img.shape[1]-1]
                        if  abs(numPixels - cv2.countNonZero(img)) > 3:
                            break
                    if side == 1:
                        numPixels = cv2.countNonZero(img)
                        img = img[0:img.shape[0], 1:img.shape[1]]
                        if abs(numPixels - cv2.countNonZero(img)) > 3:
                            break
                    if side == 2:
                        numPixels = cv2.countNonZero(img)
                        img = img[0:img.shape[0]-1, 0:img.shape[1]]
                        if  abs(numPixels - cv2.countNonZero(img)) > 3:
                            break
                    if side == 3:
                        numPixels = cv2.countNonZero(img)
                        img = img[1:img.shape[0], 0:img.shape[1]]
                        if  abs(numPixels - cv2.countNonZero(img)) > 3:
                            break 

            img = 255-img

            if show_process:
                cv2.imshow('Centered',img)
                cv2.moveWindow('Centered', 100, 100)
                cv2.waitKey(0)
                cv2.destroyAllWindows()

            max_dimension = max(img.shape[0],img.shape[1])
            img_large = np.zeros((max_dimension*2,max_dimension*2),np.uint8)
            img_large[:] = 255
            x_offset = int(max_dimension/2)
            y_offset = int(max_dimension/2)
            img_large[y_offset:y_offset+img.shape[0], x_offset:x_offset+img.shape[1]] = img
            img = img_large

            if show_process:
                cv2.imshow('Resized',img)
                cv2.moveWindow('Resized', 100, 100)
                cv2.waitKey(0)
                cv2.destroyAllWindows()

            ret,thresh = cv2.threshold(img,127,255,0)
            _,contours,hier = cv2.findContours(thresh,cv2.RETR_LIST,2)
            contours = contours[:]
            LENGTH = len(contours)
            status = np.zeros((LENGTH,1))

            for i,cnt1 in enumerate(contours):
                x = i    
                if i != LENGTH-1:
                    for j,cnt2 in enumerate(contours[i+1:]):
                        x = x+1
                        dist = find_if_close(cnt1,cnt2)
                        if dist == True:
                            val = min(status[i],status[x])
                            status[x] = status[i] = val
                        else:
                            if status[x]==status[i]:
                                status[x] = i+1

            unified = []
            maximum = int(status.max())+1
            for i in range(maximum):
                pos = np.where(status==i)[0]
                if pos.size != 0:
                    cont = np.vstack(contours[i] for i in pos)
                    hull = cv2.convexHull(cont)
                    unified.append(hull)

            img_boundaries = img.copy()
            cv2.drawContours(img_boundaries,unified,-1,(0,255,0),2)
            cv2.drawContours(thresh,unified,-1,255,-1)

            img_boundaries = img_boundaries[8:img_boundaries.shape[0]-8,8:img_boundaries.shape[1]-8]

            if show_process:
                cv2.imshow('Unified/Fix Rotation',img_boundaries)
                cv2.moveWindow('Unified/Fix Rotation', 100, 100)
                cv2.waitKey(0)
                cv2.destroyAllWindows()

            _, contours, hierarchy = cv2.findContours(img_boundaries,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
            contours = contours[1:]
            areas = [cv2.contourArea(c) for c in contours]
            max_index = np.argmax(areas)
            cnt=contours[max_index]
            rect = cv2.minAreaRect(cnt)
            box = cv2.boxPoints(rect)
            box = np.int0(box)
            cv2.drawContours(img_boundaries,[box],0,(0,0,255),-1)

            if show_process:
                cv2.imshow('Bounding Box',img_boundaries)
                cv2.moveWindow('Bounding Box', 100, 100)
                cv2.waitKey(0)
                cv2.destroyAllWindows()

            angle = rect[2]
            
            if angle < -50:
                angle += 90

            angle = int(angle/2)

            (h, w) = img_boundaries.shape[:2]
            center = (w // 2, h // 2)
            M = cv2.getRotationMatrix2D(center, angle, 1.0)
            img = cv2.warpAffine(img, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)

            if show_process:
                cv2.imshow('Rotated',img)
                cv2.moveWindow('Rotated', 100, 100)
                cv2.waitKey(0)
                cv2.destroyAllWindows()

            img = 255-img
            for side in range(4):
                while True:
                    if side == 0:
                        numPixels = cv2.countNonZero(img)
                        img = img[0:img.shape[0], 0:img.shape[1]-1]
                        if  abs(numPixels - cv2.countNonZero(img)) > 3:
                            break
                    if side == 1:
                        numPixels = cv2.countNonZero(img)
                        img = img[0:img.shape[0], 1:img.shape[1]]
                        if abs(numPixels - cv2.countNonZero(img)) > 3:
                            break
                    if side == 2:
                        numPixels = cv2.countNonZero(img)
                        img = img[0:img.shape[0]-1, 0:img.shape[1]]
                        if  abs(numPixels - cv2.countNonZero(img)) > 3:
                            break
                    if side == 3:
                        numPixels = cv2.countNonZero(img)
                        img = img[1:img.shape[0], 0:img.shape[1]]
                        if  abs(numPixels - cv2.countNonZero(img)) > 3:
                            break

            img = 255-img

            if show_process:
                cv2.imshow('Refined',img)
                cv2.moveWindow('Refined', 100, 100)
                cv2.waitKey(0)
                cv2.destroyAllWindows()

            #image_square = np.zeros((max(img.shape),max(img.shape)),np.uint8)
            #image_square[:] = 255
            #x_offset = int((max(img.shape[0],img.shape[1]))*2/2)
            #y_offset = int((max(img.shape[0],img.shape[1]))*2/2)
            #image_square[y_offset:y_offset+img.shape[0], x_offset:x_offset+img.shape[1]] = img
            #img = image_square
                
            max_dimension = max(img.shape[0],img.shape[1])
            img_square = np.zeros((int(max_dimension*1.5),int(max_dimension*1.5)),np.uint8)
            img_square[:] = 255
            if img.shape[0] == max_dimension:
                x_offset = int(max_dimension/2)
                y_offset = int(max_dimension/3)
            if img.shape[1] == max_dimension:
                x_offset = int(max_dimension/3)
                y_offset = int(max_dimension/2)
            
            img_square[y_offset:y_offset+img.shape[0], x_offset:x_offset+img.shape[1]] = img
            img = img_square
            
            if show_process:
                cv2.imshow('Square',img)
                cv2.moveWindow('Square', 100, 100)
                cv2.waitKey(0)
                cv2.destroyAllWindows()

            return img

        else:
            print("Nothing left - 2")
            return np.zeros((1,1),np.uint8)
