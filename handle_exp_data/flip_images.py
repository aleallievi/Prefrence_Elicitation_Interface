import glob
import os
import pickle
import random
import cv2
import numpy as np

dsdt_pts2img = {}
dsst_pts2img = {}
ssst_pts2img = {}
sss_pts2img = {}

quad2points = {"dsdt":[],"dsst":[],"ssst":[],"sss":[]}

fps = []
for root, dirs, files in os.walk("/Users/stephanehatgiskessell/Desktop/Kivy_stuff/all_formatted_imgs/"):
    # for name in files:
    for root2, dirs2, files2 in os.walk(root):
        for name in files2:
            name_split = name.split("_")
            if name == ".DS_Store" or len(name_split) == 2:
                continue
            #/Users/stephanehatgiskessell/Desktop/Kivy_stuff/MTURK_interface/all_formatted_imgs/ssst_formatted_imgs/(0, -1.0)
            sub_dir = root.split("/")[7]
            pt =root.split("/")[-1]
            quad = sub_dir.split("_")[0]

            # traj_root = root2 + "/" + name
            quad_id = name_split[1]

            fp = root + "/" + name
            root_split = root.split("/")
            if len(root_split) == 9:
                fps.append(fp)
fps = sorted(fps)
for i in range(0,len(fps),2):
    imgs =  [fps[i],fps[i+1]]

    #merge these images in a random order
    left = random.choice(imgs)
    imgs.remove(left)
    right = imgs[0]

    if fps[i+1] != right:
        reversed = True
    else:
        reversed = False
    left_img = cv2.imread(left)
    right_img = cv2.imread(right)
    res = np.hstack([left_img, right_img])
    #ceate new file path name
    #/Users/stephanehatgiskessell/Desktop/Kivy_stuff/MTURK_interface/all_formatted_imgs/ssst_formatted_imgs/(0.0, 0.0)/(0.0, 0.0)_9_0.png
    pt_name = fps[i].split("/")[-1]
    pt_name = pt_name.replace("_0.png","")
    if reversed:
        pt_name += "_L"
    else:
        pt_name += "_R"
    quad = fps[i].split("/")[7].split("_")[0]
    save_fp = "all_formatted_imgs/" + quad + "_formatted_imgs/" +fps[i].split("/")[8] + "/" + pt_name + ".png"
    cv2.imwrite(save_fp,res)
