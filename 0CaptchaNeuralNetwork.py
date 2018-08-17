import numpy as np
from PIL import Image
import math
#import cv2
import os
from os.path import join
import random
#import pickle

import Neural_Network
import Data_Creation
import Refine_Image

def openImage():
    global mode, trainImages, trainLabels, pixels, img_name, blacklist
    #Mode 1 prepares raw data (unrefined to refined)
    if mode == 1 or mode == 4:
        #Get blacklist of Torn images that don't work
        with open("BlackList.txt", "rb") as fp:
            blacklist = pickle.load(fp)
        
        #Collect images from Torn
        for i in range(9):
            notDone = True
            imageX = 0
            for imageX in range(1000):
                #If raw exists, but refined doesn't exist
                if os.path.isfile("{0}-{1}.png".format(str(i+1), str(imageX))) == True and "{0}-{1}.png".format(str(i+1), str(imageX)) not in blacklist:
                    if os.path.isfile("T{0}-{1}.png".format(str(i+1), str(imageX))) == False:
                        img=Image.open("{0}-{1}.png".format(str(i+1), str(imageX)))
                        img_name.append("{0}-{1}.png".format(str(i+1), str(imageX)))
                        print('Refining {0}'.format(img_name[-1]))
                        img = np.asarray(img.convert('L'))
                        pixels.append(img)

        #Collect generated images
        for i in range(9):
            notDone = True
            imageX = 0
            while notDone:
                #If raw exists, but refined doesn't exist
                if os.path.isfile("ComputerGenerated/{0}-{1}.png".format(str(i+1), str(imageX))) == True:
                    if os.path.isfile("ComputerGenerated/T{0}-{1}.png".format(str(i+1), str(imageX))) == False:
                        img=Image.open("ComputerGenerated/{0}-{1}.png".format(str(i+1), str(imageX)))
                        img_name.append("ComputerGenerated/{0}-{1}.png".format(str(i+1), str(imageX)))
                        img = np.asarray(img.convert('L'))
                        pixels.append(img)

                    imageX += 1
                else:
                    notDone = False
    
    #Mode 2 prepares refined data (refined to train)
    if mode == 2:
        if run == False:
            #Collect images from Torn (Allows for gap for images that didn't make it)
            for i in range(9):
                notDone = True
                imageX = 0
                while notDone:
                    max_gap = 0
                    while max_gap < 10:
                        if os.path.isfile("T{0}-{1}.png".format(str((i+1)), str(imageX))) == True:
                            img=Image.open("T{0}-{1}.png".format(str((i+1)), str(imageX)))
                            if img.width*img.height == 400:
                                trainLabels.append([0 for i in range(9)])
                                trainLabels[len(trainLabels)-1][i] = 1
                                trainImages.append([])
                                for a in range(img.width):
                                    for b in range(img.height):
                                        if img.getpixel((a,b)) == 0:
                                            trainImages[-1].append(0)
                                        else:
                                            trainImages[-1].append(1)
                            else:
                                print("T{0}-{1}.png".format(str((i+1)), str(imageX)))

                            imageX += 1
                        else:
                            max_gap += 1
                            imageX += 1

                    notDone = False

            print("Amount of Torn training images: {0}".format(len(trainImages)))
        
            #Collect generated images
            last_len = len(trainImages)
            path = 'C:/Users/Kaden McKeen/Desktop/Programming/Python/Machine Learning/Captcha Neural Network/SavedGenerated'
            for i in range(9):
                notDone = True
                imageX = 0
                while notDone:
                    if os.path.isfile(join(path, "T{0}-{1}.png".format(str((i+1)), str(imageX)))) == True:
                        img=Image.open(join(path, "T{0}-{1}.png".format(str((i+1)), str(imageX))))
                        if img.width*img.height == 400:
                            trainLabels.append([0 for i in range(9)])
                            trainLabels[len(trainLabels)-1][i] = 1
                            trainImages.append([])
                            for a in range(img.width):
                                for b in range(img.height):
                                    if img.getpixel((a,b)) == 0:
                                        trainImages[-1].append(0)
                                    else:
                                        trainImages[-1].append(1)
                        else:
                            print("T{0}-{1}.png".format(str((i+1)), str(imageX)))

                        imageX += 1
                    else:
                        notDone = False

            print("Amount of generated training images: {0}".format(len(trainImages)-last_len))


def clean():
    #Introduce new images
    #Count existing images
    img_count = [0 for i in range(9)]
    for i in range(9):
        for imageX in range(10000):
            if os.path.isfile("{0}-{1}.png".format(str(i+1), str(imageX))) == True:
                img_count[i] += 1

    #Transfer new images
    path_old = 'C:/Users/Kaden McKeen/Desktop/Programming/Python/Machine Learning/Captcha Neural Network/New'
    path_new = 'C:/Users/Kaden McKeen/Desktop/Programming/Python/Machine Learning/Captcha Neural Network'
    for i in range(9):
        for imageX in range(10000):
            title = '{0}-{1}.png'.format(str(i+1), str(imageX))
            if os.path.isfile(join(path_old, title)):
                os.rename(join(path_old, title), join(path_new, "{0}-{1}.png".format(str(i+1), str(img_count[i]))))
                print("Introduced {0}-{1}".format(str(i+1), str(imageX)))
                img_count[i] += 1

    
    #Find/Delete copies
    for x in range(4):
        copies = []
        images = []
        img_name = []
        for i in range(9):
            for imageX in range(10000):
                if os.path.isfile("{0}-{1}.png".format(str(i+1), str(imageX))) == True:
                    images.append(cv2.imread("{0}-{1}.png".format(str(i+1), str(imageX))))
                    img_name.append("{0}-{1}.png".format(str(i+1), str(imageX)))

        for i1 in range(len(images)-1):
            for i2 in range(len(images)-i1-1):
                a = images[i1]
                b = images[i1+i2+1]

                if a.shape == b.shape:
                    difference = cv2.subtract(a, b)    
                    result = not np.any(difference)
                    if result is True:
                        copies.append(img_name[i1+i2+1])

        for c in list(set(copies)):
            os.remove(c)
            print('Removed copy {0}'.format(c))

    images = []
    img_name = []
    for i in range(9):
        for imageX in range(10000):
            if os.path.isfile("{0}-{1}.png".format(str(i+1), str(imageX))) == True:
                images.append(cv2.imread("{0}-{1}.png".format(str(i+1), str(imageX))))
                img_name.append("{0}-{1}.png".format(str(i+1), str(imageX)))

    #Delete blacklisted images
    with open("BlackList.txt", "rb") as fp:
        blacklist = pickle.load(fp)

    for i in range(len(img_name)):
        if img_name[i] in blacklist:
            os.remove(img_name[i])
            print('Removed blacklisted {0}'.format(img_name[i]))

    blacklist = []
    with open("BlackList.txt", "wb") as fp:
        pickle.dump(blacklist, fp)

    #Delete refined photos without an unrefined counterpart
    t_img_name = []
    for i in range(9):
        notDone = True
        imageX = 0
        while notDone:
            max_gap = 0
            while max_gap < 10:
                if os.path.isfile("T{0}-{1}.png".format(str((i+1)), str(imageX))) == True:
                    t_img_name.append("T{0}-{1}.png".format(str((i+1)), str(imageX)))
                    imageX += 1
                else:
                    max_gap += 1
                    imageX += 1

            notDone = False

    for i in t_img_name:
        if i[1:] not in img_name:
            os.remove(i)
            print('Removed trained image {0} with no unrefined counterpart'.format(i))

    #Get existing images
    img_name = []
    for i in range(9):
        notDone = True
        imageX = 0
        while notDone:
            max_gap = 0
            while max_gap < 10:
                if os.path.isfile("{0}-{1}.png".format(str((i+1)), str(imageX))) == True:
                    img_name.append("{0}-{1}.png".format(str((i+1)), str(imageX)))
                    imageX += 1
                else:
                    max_gap += 1
                    imageX += 1

            notDone = False
            
    t_img_name = []
    for i in range(9):
        notDone = True
        imageX = 0
        while notDone:
            max_gap = 0
            while max_gap < 10:
                if os.path.isfile("T{0}-{1}.png".format(str((i+1)), str(imageX))) == True:
                    t_img_name.append("T{0}-{1}.png".format(str((i+1)), str(imageX)))
                    imageX += 1
                else:
                    max_gap += 1
                    imageX += 1

            notDone = False

    #Rename/Condense
    counterparts = []
    for i in range(len(img_name)):
        counterpart = False
        for j in range(len(t_img_name)):
            if img_name[i] == t_img_name[j][1:]:
                counterparts.append(t_img_name[j])
                counterpart = True

        if counterpart == False:
            counterparts.append(None)

    for i in range(len(img_name)):
        os.rename(img_name[i], 'temp'+img_name[i])
        if counterparts[i] != None:
            os.rename(counterparts[i], 'temp'+counterparts[i])

    current_number = 1
    subtract = 0
    for i in range(len(img_name)):
        if img_name[i][0] != str(current_number):
            current_number += 1
            subtract = i
        
        os.rename('temp'+img_name[i], img_name[i][:img_name[i].index('-')]+'-'+str(i-subtract)+'.png')
        if counterparts[i] != None:
            os.rename('temp'+counterparts[i], counterparts[i][:counterparts[i].index('-')]+'-'+str(i-subtract)+'.png')


#If mode = 4, run the program twice to refine the new images
mode = 2

run = False
testing = True
use_new_network = False

"""
Mode Types:
1 - Refine Captchas
2 - Train Neural Network // Run
3 - Generate Data
4 - Clean Up
"""

trainImages = []
trainLabels = []

pixels = []
img_name = []
openImage()

for i in trainImages:
    if len(i) != 400:
        print(len(i))

#Load new test images
if mode == 1 or mode == 4:
    for index in range(len(pixels)):
        img1 = Refine_Image.analyzeImages1(pixels[index], False)
        img2 = Refine_Image.analyzeImages2(pixels[index], False)
        invalid = Refine_Image.chooseImage(img1, img2, img_name[index], False)
        
        if invalid == "Invalid":
            blacklist.append(img_name[index])
            print("Append to blacklist: {0}".format(img_name[index]))
    
    with open("BlackList.txt", "wb") as fp:
        pickle.dump(blacklist, fp)

    if mode == 4:
        clean()

#Train neural network
if mode == 2:
    if use_new_network:
        import My_Neural_Network
        My_Neural_Network.run(trainImages, trainLabels)
        
    else:
        test_try = [[0.1,0.1],[0.1,0.1],[0.1,0.1],[0.2,0.1],[0.2,0.1],[0.2,0.1]]
  
        if run == False:
            #Shuffle (So they don't train all 1's, all 2's, all 3's, etc
            shuffleTraining = list(zip(trainImages, trainLabels))
            random.shuffle(shuffleTraining)
            trainImages[:], trainLabels[:] = zip(*shuffleTraining)

            if testing == True:
                test_group = int(len(trainImages)/15)
                testImages = trainImages[len(trainImages)-test_group:]
                testLabels = trainLabels[len(trainLabels)-test_group:]
                trainImages = trainImages[:len(trainImages)-test_group]
                trainLabels = trainLabels[:len(trainLabels)-test_group]
            
                print("Testing on {0} images\n\n".format(test_group))
        
                correct = 0
                incorrect = 0
                no_guess = 0

                print("Training on {0} images".format(len(trainImages)))
                h_nodes = 40
                print("Hidden layer nodes: {0}".format(h_nodes))
                print("Starting Alpha: {0}".format(test_run[0]))
                print("Starting Eta: {0}".format(test_run[1]))

        for trial in test_try:
            correct = 0
            incorrect = 0
            no_guess = 0

            if run:
                Neural_Network.train([], [], [], True, 0)
            else:
                Neural_Network.train([400, h_nodes, 9], trainImages, trainLabels, False, 1, trial[0], trial[1])

            if run == False and testing:
                for test in range(len(testImages)):
                    results = Neural_Network.guess(testImages[test], False)

                    if results == testLabels[test]:
                        correct += 1
                    elif results == [0,0,0,0,0,0,0,0,0]:
                        no_guess += 1
                    else:
                        incorrect += 1

                print("\n"*3)
                print("Correct: {0}".format(correct))
                print("Incorrect: {0}".format(incorrect))
                print("No Guess: {0}".format(no_guess))
                print("Accuracy: {0}%".format(((correct)/(correct+incorrect+no_guess))*100))
                print("\n"*5)


        #Run program
        if run == True:
            import Control
            while True:
                user_in = input("Enter 'run' to run once (Make sure Torn is visible): ")

                if user_in == "run":
                    #Control.captcha()

                    path = 'C:/Users/Kaden McKeen/Desktop/Programming/Python/Machine Learning/Captcha Neural Network/'
                    img = Image.open(join(path, "guess_image.png"))
                    img = np.asarray(img.convert('L'))
                    
                    img1 = Refine_Image.analyzeImages1(img, False)
                    img2 = Refine_Image.analyzeImages2(img, False)
                    invalid = Refine_Image.chooseImage(img1, img2, '', True)
                    
                    if invalid != 'Invalid':
                        img = []
                        for a in range(invalid.shape[0]):
                            for b in range(invalid.shape[1]):
                                if invalid[a][b] == 0:
                                    img.append(1)
                                else:
                                    img.append(0)

                    
                        string = ''
                        for i in range(len(img)):
                            if i % 20 == 0:
                                string += '\n'
                            string += str(img[i])
                        print(string)
                        
                        results = Neural_Network.guess(img, False)
                        print(results)
                        #Control.click_captcha(results)
                    else:
                        print("Image failed to refine")


    
#Synthesize new data
if mode == 3:
    #Cycles of numbers it will generate (A cycle being captchas 1-9)
    for i in range(600):
        Data_Creation.create(i)

