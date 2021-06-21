import cv2
import numpy as np



def format(img,name):
    img = cv2.resize(img,(1240,800))
    game_screen = img[160:700,360:880]
    score_screen_1 = img[150:230,890:1110]
    score_screen_2 = img[260:370,1000:1145]
    #
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
    score_screen_1 = cv2.copyMakeBorder(score_screen_1, 0,deltah1, 0, 0, cv2.BORDER_CONSTANT,value=[255,255,255])
    score_screen_2 = cv2.copyMakeBorder(score_screen_2, 0,deltah2,0, 0, cv2.BORDER_CONSTANT,value=[255,255,255])
    score_screen = np.hstack([score_screen_1, score_screen_2])

    h4,w4,_ = score_screen.shape

    left_border = int((w1-w4)/2)
    right_border = int((w1-w4)/2)
    if (left_border+right_border < w1):
        left_border+=1

    score_screen = cv2.copyMakeBorder(score_screen, 0,0,left_border, right_border, cv2.BORDER_CONSTANT,value=[255,255,255])
    res = np.vstack([game_screen, score_screen])
    cv2.imwrite("assets/trajImages/"+str(name) + ".png",res)

    # cv2.imshow("res",res)
    # # cv2.imshow("score_screen_1",score_screen_1)
    # # cv2.imshow("score_screen_2",score_screen_2)
    # # cv2.imshow("game_screen",game_screen)
    #
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

for i in range (1,7):
    img = cv2.imread("/Users/stephanehatgiskessell/Desktop/ex"+str(i)+".png")
    format(img,"ex"+str(i))
