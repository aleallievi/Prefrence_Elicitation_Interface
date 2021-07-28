import cv2
import numpy as np
import PILasOPENCV as Image
import PILasOPENCV as ImageDraw
import PILasOPENCV as ImageFont
import cv2
import os
import json

def is_in_gated_area(x,y):
    val = board[x][y]
    if  val >= 6:
        return True
    else:
        return False

def is_in_blocked_area(x,y):
    val = board[x][y]
    if val == 2 or val == 8:
        return True
    else:
        return False

def find_end_state(traj):
    in_gated =False
    traj_ts_x = traj[0][0]
    traj_ts_y = traj[0][1]
    if is_in_gated_area(traj_ts_x,traj_ts_y):
        in_gated = True

    for i in range (1,4):

        if traj_ts_x + traj[i][0] >= 0 and traj_ts_x + traj[i][0] < 10 and traj_ts_y + traj[i][1] >=0 and traj_ts_y + traj[i][1] < 10:
            if not is_in_blocked_area(traj_ts_x + traj[i][0], traj_ts_y + traj[i][1]):
                next_in_gated = is_in_gated_area(traj_ts_x + traj[i][0], traj_ts_y + traj[i][1])
                if in_gated == False or  (in_gated and next_in_gated):
                    traj_ts_x += traj[i][0]
                    traj_ts_y += traj[i][1]


    # traj1_ts_x = traj1[0][0] + traj1[1][0] + traj1[2][0] + traj1[3][0]
    # traj1_ts_y = traj1[0][1] + traj1[1][1] + traj1[2][1] + traj1[3][1]
    return traj_ts_x, traj_ts_y

def displayVF(v_s0, v_st,img_path):
    traj_img = cv2.imread(img_path)
    font = ImageFont.truetype('/Users/stephanehatgiskessell/Desktop/Kivy_stuff/MTURK_interface/assets/fonts/SUPERBOOM.ttf', 27)
    img = Image.new("RGB", (500, 180), "white")
    draw = ImageDraw.Draw(img)
    # text = "Some text in arial"
    draw.text((10, 65), 'Best Possible From ', font=font, fill=(0, 0, 0))
    draw.text((300, 35), 'Start: ', font=font, fill=(0, 0, 0))
    draw.text((400, 35), '$' + str(int(v_s0)), font=font, fill=(65, 117, 55))#fill=(115,120,140)

    draw.text((300, 95), 'End: ', font=font, fill=(0, 0, 0))
    draw.text((400, 95), '$' + str(int(v_st)), font=font, fill=(65, 117, 55))
    im_numpy = img.getim()
    #reformat original image
    h,w,_ = traj_img.shape
    traj_img = traj_img[0:540,0:w]
    #reformat vf image so it has the same width
    vf_h,vf_w,_ = im_numpy.shape
    im_numpy = cv2.copyMakeBorder(im_numpy, 0,0,int((w-vf_w)/2), int((w-vf_w)/2), cv2.BORDER_CONSTANT,value=[255,255,255])
    traj_img = np.vstack([traj_img,im_numpy])

    img_name = img_path.split("/")[-1]
    img_path = img_path.replace(img_name,"")
    new_img_name = "vf_" + img_name
    new_img_path = img_path + new_img_name

    print (new_img_path)
    cv2.imwrite(new_img_path, traj_img)
    # cv2.imshow("img",traj_img)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    # assert False


# displayVF(30, 50)
dsdt_data = "/Users/stephanehatgiskessell/Desktop/Kivy_stuff/saved_data/ex3_dsdt.json"
dsst_data = "/Users/stephanehatgiskessell/Desktop/Kivy_stuff/saved_data/ex3_dsst.json"
ssst_data = "/Users/stephanehatgiskessell/Desktop/Kivy_stuff/saved_data/ex3_ssst.json"
sss_data = "/Users/stephanehatgiskessell/Desktop/Kivy_stuff/saved_data/ex3_sss.json"
board_vf = "/Users/stephanehatgiskessell/Desktop/Kivy_stuff/MTURK_interface/assets/boards/test_single_goal_mud_value_function.json"
board = "/Users/stephanehatgiskessell/Desktop/Kivy_stuff/MTURK_interface/assets/boards/test_single_goal_mud_board.json"

with open(dsdt_data, 'r') as j:
    dsdt_data = json.loads(j.read())
with open(dsst_data, 'r') as j:
    dsst_data = json.loads(j.read())
with open(ssst_data, 'r') as j:
    ssst_data = json.loads(j.read())
with open(sss_data, 'r') as j:
    sss_data = json.loads(j.read())
with open(board, 'r') as j:
    board = json.loads(j.read())


with open(board_vf, 'r') as j:
    board_vf = json.loads(j.read())

for root, dirs, files in os.walk("/Users/stephanehatgiskessell/Desktop/Kivy_stuff/all_formatted_imgs/"):
    # for name in files:
    for root2, dirs2, files2 in os.walk(root):
        for name in files2:
            if len(root.split("/")) == 7:
                continue
            name_split = name.split("_")
            if (len(name_split)==2 or name_split[0]=="vf"):
                continue
            img_path = root2 + "/"+name

            pt =root.split("/")[-1]
            quad = root.split("/")[6].split("_")[0]

            last_char = name_split[-1].replace(".png","")
            pt_index = name_split[1].replace(".png","")
            #make sure we only are using one of the flipped images
            if (len(name_split) == 3):
                traj_root = root2 + "/" + name
                if quad == "dsdt":
                    traj_pairs = dsdt_data.get(pt)
                if quad == "dsst":
                    traj_pairs = dsst_data.get(pt)
                if quad == "ssst":
                    traj_pairs = ssst_data.get(pt)
                if quad == "sss":
                    traj_pairs = sss_data.get(pt)

                # assert(len(traj_pairs) > 0) #make sure we are not accesing the dict from an invalid key
                poi = traj_pairs[int(pt_index)]
                # traj1 = poi[0]
                # traj2 = poi[1]

                pair_id = int(name.split("_")[-1].replace(".png",""))

                traj = poi[pair_id]
                traj_ts_x,traj_ts_y =find_end_state(traj)

                assert (traj_ts_x >= 0 and traj_ts_x < 10 and traj_ts_y>= 0 and traj_ts_y < 10)

                traj_v_s0 = board_vf[traj[0][0]][traj[0][1]]
                traj_v_st = board_vf[traj_ts_x][traj_ts_y]
                displayVF(traj_v_s0,traj_v_st,img_path)

                # assert False
