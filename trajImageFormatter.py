import cv2
import numpy as np
import glob


def format(img,name,save=True):
    img = cv2.resize(img,(1240,800))
    game_screen = img[160:700,360:880]
    score_screen_1 = img[150:230,880:1110]
    score_screen_2 = img[260:370,900:1145]

    score_screen_1 = cv2.resize(score_screen_1, (150,55))
    score_screen_2 = cv2.resize(score_screen_2, (225,90))
    # cv2.imshow("score_screen_1",score_screen_1)
    # cv2.imshow("score_screen_2",score_screen_2)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    # (80, 220, 3)
    # (110, 145, 3)
    # return
    h1,w1,_ = game_screen.shape
    h2,w2,_ = score_screen_1.shape
    h3,w3,_ = score_screen_2.shape
    # collage = np.hstack([col_1, col_2]

    # #add border so everything is the same size
    if (h3 > h2):
        deltah1 = h3-h2
    else:
        deltah1 = 0
    if (h2 > h3):
        deltah2 = h2-h3
    else:
        deltah2 = 0


    # print (score_screen_1.shape)
    # print (score_screen_2.shape)
    score_screen_1 = cv2.copyMakeBorder(score_screen_1, 0,deltah1, 0, 50, cv2.BORDER_CONSTANT,value=[255,255,255])
    score_screen_2 = cv2.copyMakeBorder(score_screen_2, 0,deltah2,50, 0, cv2.BORDER_CONSTANT,value=[255,255,255])
    score_screen = np.hstack([score_screen_1, score_screen_2])

    h4,w4,_ = score_screen.shape

    left_border = int((w1-w4)/2)
    right_border = int((w1-w4)/2)
    if (left_border+right_border < w1):
        left_border+=1

    score_screen = cv2.copyMakeBorder(score_screen, 0,0,left_border, right_border, cv2.BORDER_CONSTANT,value=[255,255,255])
    res = np.vstack([game_screen, score_screen])
    if save:
        cv2.imwrite("assets/trajImages/" + str(name),res)

    # cv2.imshow("res",res)
    # cv2.imshow("score_screen_1",score_screen)
    # # cv2.imshow("score_screen_2",score_screen_2)
    # cv2.imshow("game_screen",game_screen)
    #
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    return res

filenames = [img for img in glob.glob("/Users/stephanehatgiskessell/Desktop/same_ss_same_term/*.png")]
filenames.sort()

for i in range (0,len(filenames),2):
    n1 = filenames[i]
    n2 = filenames[i+1]

    #get rid of filepath
    n1 = n1.replace("/",".")
    n2 = n2.replace("/",".")
    n1 = n1.split(".")[5]
    n2 = n2.split(".")[5]

    #get rid of the pair indicator
    n1 = n1.split("_")
    n2 = n2.split("_")

    #make sure we are always using images that corrospond to the same points
    assert(n1[2] == "0" and n2[2] == "1" and n1[0] == n2[0] and n1[1] == n2[1])
    name = n1[0] + "_" + n1[1] + ".png"

    img1 = cv2.imread(filenames[i])
    img2 = cv2.imread(filenames[i+1])

    res1 = format(img1,filenames[i],save=False)
    res2 = format(img2,filenames[i+1],save=False)
    res = np.hstack([res1, res2])
    print (name)
    cv2.imwrite("/Users/stephanehatgiskessell/Desktop/Kivy_stuff/formatted_same_ss_same_term/" + str(name),res)
