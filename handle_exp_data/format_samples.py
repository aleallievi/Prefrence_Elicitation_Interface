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


for root, dirs, files in os.walk("/Users/stephanehatgiskessell/Desktop/Kivy_stuff/all_formatted_imgs/"):
    # for name in files:
    for root2, dirs2, files2 in os.walk(root):
        for name in files2:


        # print (name)
        # print (root)
        # print ("\n")
        #/Users/stephanehatgiskessell/Desktop/Kivy_stuff/MTURK_interface/all_formatted_imgs/ssst_formatted_imgs/(0, -1.0)
            sub_dir = root.split("/")[7]
            pt =root.split("/")[-1]
            quad = sub_dir.split("_")[0]

            # traj_root = root2 + "/" + name
            name_split = name.split("_")
            last_char = name_split[-1].replace(".png","")
            if (len(name_split) == 3 and last_char.isalpha()):
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


n_samples = 35
n_traj_pairs = len(dsdt_pts2img.keys()) + len(dsst_pts2img.keys()) + len(ssst_pts2img.keys())  + len(sss_pts2img.keys()) - 4
for i in range(n_samples):
    print ("building sample " + str(i))
    sample = []
    sample_dict = {}
    seen_sample_numbers = []
    sample_dir = "/Users/stephanehatgiskessell/Desktop/Kivy_stuff/MTURK_interface/exp3_data_samples/sample" + str(i) + "/"
    #make sample directory if it does not exist
    if not os.path.exists(sample_dir):
        os.makedirs(sample_dir)
    for quad in quad2points.keys():
        pts = quad2points.get(quad)[1:]
        for pt in pts:
            if quad == "dsdt":
                pts_traj_pairs = dsdt_pts2img.get(pt)
            elif quad == "dsst":
                pts_traj_pairs = dsst_pts2img.get(pt)
            elif quad == "ssst":
                pts_traj_pairs = ssst_pts2img.get(pt)
            elif quad == "sss":
                pts_traj_pairs = sss_pts2img.get(pt)

            chosen = random.choice(pts_traj_pairs)
            chosen_name = chosen.split("/")[9]
            while (chosen_name == ".DS_Store"):
                chosen = random.choice(pts_traj_pairs)
                chosen_name = chosen.split("/")[9]

            sample.append(chosen)

            query_number = random.randint(0, n_traj_pairs-1)
            while query_number in seen_sample_numbers:
                query_number = random.randint(0, n_traj_pairs-1)
            seen_sample_numbers.append(query_number)

            #save image
            dom_val = chosen.split("/")[9].split("_")[-1].replace(".png","")
            chosen_ = chosen.replace(".png","")
            chosen_ = chosen_.replace("_L","")
            chosen_ = chosen_.replace("_R","")
            # print (chosen_)
            img1 = cv2.imread(chosen_ + "_0.png")
            img2 = cv2.imread(chosen_ + "_1.png")

            cv2.imwrite(sample_dir + "s" + str(query_number) + "_0.png",img1)
            cv2.imwrite(sample_dir + "s" + str(query_number) + "_1.png",img2)

            sample_dict[query_number] = {"query":query_number,"name":chosen_name,"quadrant":quad,"dom_val":dom_val}

    # save pickled dictionary
    with open(sample_dir +"/sample" + str(i) + "_dict" + '.pkl', 'wb') as f:
        pickle.dump(sample_dict, f, pickle.HIGHEST_PROTOCOL)






    # random.choice()

#
# def format_samples(dir):
#     filenames = [img for img in glob.glob(dir + "/*.png")]
#     filenames.sort()
#
#     numbers2choosefrom = []
#     for i in range (0,len(filenames),3):
#          numbers2choosefrom.append(int(i/3))
#
#     sample_dict = {}
#     for i in range (0,len(filenames),3):
#         n = filenames[i]
#         n0 = filenames[i+1]
#         n1 = filenames[i+2]
#
#         n_split = n.split("/")[2]
#         quadrant = n_split.split("_")[0]
#
#         query_number = random.choice(numbers2choosefrom)
#         numbers2choosefrom.remove(query_number)
#         #s0_0...
#         os.rename(n0, dir + "/" + "s"+ str(query_number) + "_0.png")
#         os.rename(n1,  dir + "/" + "s"+ str(query_number) + "_1.png")
#
#         sample_dict[n] = {"query":str(query_number),"name":n,"s"+ str(query_number) + "_0.png":n0,"s"+ str(query_number) + "_1.png":n1,"quadrant":quadrant}
#     with open(dir + "_dict" + '.pkl', 'wb') as f:
#         pickle.dump(sample_dict, f, pickle.HIGHEST_PROTOCOL)
#
#
# format_samples("exp1_data_samples/sample0")
