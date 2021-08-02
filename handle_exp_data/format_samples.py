import glob
import os
import pickle
import random
import cv2

dsdt_pts2img = {}
dsst_pts2img = {}
ssst_pts2img = {}
sss_pts2img = {}

quad2points = {"dsdt":[],"dsst":[],"ssst":[],"sss":[]}
point2index = {}

#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#TODO: subtract (0,1), (0,2), (7,0)
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
handling_vf_bucket = False
handling_all_bucket = False
handling_none_bucket = True

def build_sample(worker_1_cords,n):
    sample_1 = []
    sample_dict_1 = {}
    seen_sample_numbers_1 = []
    if handling_vf_bucket:
        sample_dir_1 = "/Users/stephanehatgiskessell/Desktop/Kivy_stuff/2021_07_29_data_samples/vf_sample" + str(n) + "/"
    elif handling_all_bucket:
        sample_dir_1 = "/Users/stephanehatgiskessell/Desktop/Kivy_stuff/2021_07_29_data_samples/all_sample" + str(n) + "/"
    elif handling_none_bucket:
        sample_dir_1 = "/Users/stephanehatgiskessell/Desktop/Kivy_stuff/2021_07_29_data_samples/none_sample" + str(n) + "/"
    else:
        sample_dir_1 = "/Users/stephanehatgiskessell/Desktop/Kivy_stuff/2021_07_29_data_samples/pr_sample" + str(n) + "/"
    #make sample directory if it does not exist
    if not os.path.exists(sample_dir_1):
        os.makedirs(sample_dir_1)

    for point in worker_1_cords:
        point_ = point.split("_")
        quad = point_[0]
        pt = point_[1]
        if quad == "dsdt":
            pts_traj_pairs = dsdt_pts2img.get(pt)
        elif quad == "dsst":
            pts_traj_pairs = dsst_pts2img.get(pt)
        elif quad == "ssst":
            pts_traj_pairs = ssst_pts2img.get(pt)
        elif quad == "sss":
            pts_traj_pairs = sss_pts2img.get(pt)

        #second layer of randomness - choose random points for each coordinate
        index = point2index.get(quad + "_" + str(pt))
        chosen = pts_traj_pairs[index]

        chosen_name = chosen.split("/")[8]
        if (chosen_name == ".DS_Store"):
            index+=1
            if (index == len(pts_traj_pairs)):
                index = 0
            chosen = pts_traj_pairs[index]
            chosen_name = chosen.split("/")[8]
        index+=1

        #reshuffle array and reset index if we have chosen all samples
        if (index == len(pts_traj_pairs)):
            random.shuffle(pts_traj_pairs)
            if quad == "dsdt":
                dsdt_pts2img[pt] = pts_traj_pairs
            elif quad == "dsst":
                dsst_pts2img[pt] = pts_traj_pairs
            elif quad == "ssst":
                ssst_pts2img[pt] = pts_traj_pairs
            elif quad == "sss":
                sss_pts2img[pt] = pts_traj_pairs
            index = 0
        point2index[quad + "_" + str(pt)] = index

        sample_1.append(chosen)

        query_number = random.randint(0, len(worker_1_cords)-1)
        while query_number in seen_sample_numbers_1:
            query_number = random.randint(0, len(worker_1_cords)-1)
        seen_sample_numbers_1.append(query_number)

        #save image
        dom_val = chosen.split("/")[8].split("_")[-1].replace(".png","")
        chosen_2 = chosen.replace("0_" + dom_val + ".png", "1_"+ dom_val +".png")

        #
        img1 = cv2.imread(chosen)
        img2 = cv2.imread(chosen_2)
        chosen_name = chosen.replace("_0_" + dom_val + ".png","")

        cv2.imwrite(sample_dir_1 + "s" + str(query_number) + "_0.png",img1)
        cv2.imwrite(sample_dir_1 + "s" + str(query_number) + "_1.png",img2)

        if handling_vf_bucket:
            disp_type = 1
        elif handling_all_bucket:
            disp_type = 2
        elif handling_none_bucket:
            disp_type = 3
        else:
            disp_type = 0

        sample_dict_1[query_number] = {"query":query_number,"name":chosen_name,"quadrant":quad,"dom_val":dom_val,"disp_type":disp_type}
        with open(sample_dir_1 +"/sample" + str(n) + "_dict" + '.pkl', 'wb') as f:
            pickle.dump(sample_dict_1, f, pickle.HIGHEST_PROTOCOL)

for root, dirs, files in os.walk("/Users/stephanehatgiskessell/Desktop/Kivy_stuff/2021_07_29_all_formatted_imgs/"):
    # for name in files:
    for root2, dirs2, files2 in os.walk(root):
        for name in files2:

            if len(root.split("/")) == 7:
                continue
            # print (len(root.split("/")))

            pt =root.split("/")[-1]
            quad = root.split("/")[6].split("_")[0]

            # traj_root = root2 + "/" + name
            name_split = name.split("_")
            if name_split[0] == "vf" and handling_vf_bucket == False:
                continue
            if name_split[0] != "vf" and handling_vf_bucket == True:
                continue

            if name_split[0] == "all" and handling_all_bucket == False:
                continue
            if name_split[0] != "all" and handling_all_bucket == True:
                continue

            if name_split[0] == "none" and handling_none_bucket == False:
                continue
            if name_split[0] != "none" and handling_none_bucket == True:
                continue

            # print (pt)
            last_char = name_split[-1].replace(".png","")
            if (len(name_split) > 2 and last_char.isalpha()):
                 if int(name_split[2]) == 1 and not (handling_vf_bucket or handling_all_bucket or handling_none_bucket):
                     continue
                 if ".png" not in name_split[3] and int(name_split[3]) == 1 and (handling_vf_bucket or handling_all_bucket or handling_none_bucket):
                     continue
                 traj_root = root2 + "/" + name
                 # if (pt == "dsdt_formatted_imgs"):
                 #     continue
                 if quad == "dsdt":
                     arr = quad2points.get("dsdt")

                     if pt not in arr:
                         arr.append(pt)
                         quad2points["dsdt"] = arr
                         dsdt_pts2img[pt] = [traj_root]

                     pt_arr = dsdt_pts2img.get(pt)
                     pt_arr.append(traj_root)
                     dsdt_pts2img[pt] = pt_arr

                 elif quad == "dsst":
                     arr = quad2points.get("dsst")
                     if pt not in arr:
                         arr.append(pt)
                         quad2points["dsst"] = arr
                         dsst_pts2img[pt] = [traj_root]

                     pt_arr = dsst_pts2img.get(pt)
                     pt_arr.append(traj_root)
                     dsst_pts2img[pt] = pt_arr

                 elif quad == "ssst":
                     arr = quad2points.get("ssst")
                     if pt not in arr:
                         arr.append(pt)
                         quad2points["ssst"] = arr
                         ssst_pts2img[pt] = [traj_root]

                     pt_arr = ssst_pts2img.get(pt)
                     pt_arr.append(traj_root)
                     ssst_pts2img[pt] = pt_arr

                 elif quad == "sss":
                     arr = quad2points.get("sss")
                     if pt not in arr:
                         arr.append(pt)
                         quad2points["sss"] = arr
                         sss_pts2img[pt] = [traj_root]

                     pt_arr = sss_pts2img.get(pt)
                     pt_arr.append(traj_root)
                     sss_pts2img[pt] = pt_arr
                 #create index dictionary for sampling
                 point2index[quad + "_" + str(pt)] = 0

n_samples = 30
n_traj_pairs = len(dsdt_pts2img.keys()) + len(dsst_pts2img.keys()) + len(ssst_pts2img.keys())  + len(sss_pts2img.keys()) - 4
#build a list of all unique points
all_cords = []
for quad in quad2points.keys():
    pts = quad2points.get(quad)[1:]
    for pt in pts:
        all_cords.append(quad + "_" + pt)

for i in range(0,n_samples,2):
    #first layer of randomness - choose random coordinates for worker
    random.shuffle(all_cords)
    worker_1_cords = all_cords[0:int(len(all_cords)/2)]
    worker_2_cords = all_cords[int(len(all_cords)/2):len(all_cords)]

    print ("building sample " + str(i))
    build_sample(worker_1_cords,i)

    print ("building sample " + str(i+1))
    build_sample(worker_2_cords,i+1)


#
# for i in range(n_samples):
#     print ("building sample " + str(i))
#     sample = []
#     sample_dict = {}
#     seen_sample_numbers = []
#     if handling_vf_bucket:
#         sample_dir = "/Users/stephanehatgiskessell/Desktop/Kivy_stuff/exp3_data_samples/vf_sample" + str(i) + "/"
#     else:
#         sample_dir = "/Users/stephanehatgiskessell/Desktop/Kivy_stuff/exp3_data_samples/pr_sample" + str(i) + "/"
#     #make sample directory if it does not exist
#     if not os.path.exists(sample_dir):
#         os.makedirs(sample_dir)
#     for quad in quad2points.keys():
#         pts = quad2points.get(quad)[1:]
#         for pt in pts:
#             if quad == "dsdt":
#                 pts_traj_pairs = dsdt_pts2img.get(pt)
#             elif quad == "dsst":
#                 pts_traj_pairs = dsst_pts2img.get(pt)
#             elif quad == "ssst":
#                 pts_traj_pairs = ssst_pts2img.get(pt)
#             elif quad == "sss":
#                 pts_traj_pairs = sss_pts2img.get(pt)
#             index = point2index.get(quad + "_" + str(pt))
#             chosen = pts_traj_pairs[index]
#             chosen_name = chosen.split("/")[8]
#             if (chosen_name == ".DS_Store"):
#                 index+=1
#                 if (index == len(pts_traj_pairs)):
#                     index = 0
#                 chosen = pts_traj_pairs[index]
#                 chosen_name = chosen.split("/")[8]
#             index+=1
#
#             #reshuffle array and reset index if we have chosen all samples
#             if (index == len(pts_traj_pairs)):
#                 random.shuffle(pts_traj_pairs)
#                 if quad == "dsdt":
#                     dsdt_pts2img[pt] = pts_traj_pairs
#                 elif quad == "dsst":
#                     dsst_pts2img[pt] = pts_traj_pairs
#                 elif quad == "ssst":
#                     ssst_pts2img[pt] = pts_traj_pairs
#                 elif quad == "sss":
#                     sss_pts2img[pt] = pts_traj_pairs
#                 index = 0
#             point2index[quad + "_" + str(pt)] = index
#
#             sample.append(chosen)
#             query_number = random.randint(0, n_traj_pairs-1)
#             while query_number in seen_sample_numbers:
#                 query_number = random.randint(0, n_traj_pairs-1)
#             seen_sample_numbers.append(query_number)
#
#             #save image
#             dom_val = chosen.split("/")[8].split("_")[-1].replace(".png","")
#             chosen_ = chosen.replace(".png","")
#             chosen_ = chosen_.replace("_L","")
#             chosen_ = chosen_.replace("_R","")
#             img1 = cv2.imread(chosen_ + "_0.png")
#             img2 = cv2.imread(chosen_ + "_1.png")
#
#
#             cv2.imwrite(sample_dir + "s" + str(query_number) + "_0.png",img1)
#             cv2.imwrite(sample_dir + "s" + str(query_number) + "_1.png",img2)
#
#             sample_dict[query_number] = {"query":query_number,"name":chosen_name,"quadrant":quad,"dom_val":dom_val}
#
#     # save pickled dictionary
#     with open(sample_dir +"/sample" + str(i) + "_dict" + '.pkl', 'wb') as f:
#         pickle.dump(sample_dict, f, pickle.HIGHEST_PROTOCOL)
