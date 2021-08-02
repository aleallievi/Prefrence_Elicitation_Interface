import cv2
import numpy as np
import os
import glob
import pickle


# img = cv2.imread("/Users/stephanehatgiskessell/Desktop/sample10.png")

#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#TODO: subtract (0,1), (0,2), (7,0)
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

quadrant = "2021_07_29_sss"
if not os.path.exists(quadrant + "_formatted_imgs"):
    os.makedirs(quadrant + "_formatted_imgs")

def format_img(img):
    img = cv2.resize(img,(1240,800))
    game_screen = img[160:700,360:880]
    gas_icon = img[220:290,915:1050]

    # cv2.imshow("img",img)
    # cv2.waitKey(0)
    # return

    score = img[150:190,890:1100]
    coin_icon = img[290:360,915:1050]
    blockade_icon = img[360:430,915:1055]
    person_icon = img[430:500,915:1050]
    flag_icon = img[510:580,915:1050]
    #
    row1 = np.hstack([gas_icon,coin_icon,blockade_icon])
    # #
    row2 = np.hstack([person_icon,flag_icon])

    h1,w1,_ = row1.shape
    h2,w2,_ = row2.shape
    border =int((w1-w2)/2)
    row2 = cv2.copyMakeBorder(row2, 0,0,border, border, cv2.BORDER_CONSTANT,value=[255,255,255])
    scoreScreen = np.vstack([row1,row2])

    h3,w3,_ = game_screen.shape
    screen_border = int((w3-w1)/2)
    scoreScreen = cv2.copyMakeBorder(scoreScreen, 0,0,screen_border, screen_border, cv2.BORDER_CONSTANT,value=[255,255,255])

    h4,w4,_ = score.shape
    score_border = int((w3-w4)/2)
    score = cv2.copyMakeBorder(score, 0,0,score_border, score_border, cv2.BORDER_CONSTANT,value=[255,255,255])


    screen = np.vstack([game_screen,scoreScreen,score])

    return screen
path = "/Users/stephanehatgiskessell/Desktop/Kivy_stuff/all_unformatted_imgs/"
filenames = [img for img in glob.glob(path + quadrant + "_unformatted_imgs/*.png")]
filenames.sort()

for i in range (0,len(filenames),2):
    n1 = filenames[i]
    n2 = filenames[i+1]


    if ("fixed" in quadrant):
        index = 2
    else:
        index = 7
    #get rid of filepath

    n1 = n1.replace("/","x")
    n1 = n1.replace(".png","x")
    n1 = n1.split("x")[index]

    n2 = n2.replace("/","x")
    n2 = n2.replace(".png","x")
    n2 = n2.split("x")[index]

    # #get rid of the pair indicator
    n1 = n1.split("_")
    n2 = n2.split("_")


    # make sure we are always using images that corrospond to the same points
    name = n1[0] + "_" + n1[1] + ".png"
    name1 = n1[0] + "_" + n1[1] + "_0.png"
    name2 = n1[0] + "_" + n1[1] + "_1.png"
    print (n1)
    print (n2)
    print ("\n")

    assert (n1[2] == "0" and n2[2] == "1" and n1[0] == n2[0] and n1[1] == n2[1])

    img1 = cv2.imread(filenames[i])
    img2 = cv2.imread(filenames[i+1])

    res1 = format_img(img1)
    res2 = format_img(img2)
    res = np.hstack([res2,res1])

    dir = quadrant + "_formatted_imgs/" + n1[0]


    if not os.path.exists(dir):
        os.makedirs(dir)
    cv2.imwrite(dir + "/" + str(name),res)
    cv2.imwrite(dir + "/" + str(name1),res2)
    cv2.imwrite(dir + "/" + str(name2),res1)

# img1 = format_img(cv2.imread("/Users/stephanehatgiskessell/Desktop/sample40.png"))
# cv2.imwrite("sample40.png",img1)
