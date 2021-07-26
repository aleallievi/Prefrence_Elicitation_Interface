import pickle
import json
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
# q1 = "/Users/stephanehatgiskessell/Desktop/Kivy_stuff/saved_data/fixed_dsst_ql_passing_spaces.json"
# q4 = "/Users/stephanehatgiskessell/Desktop/Kivy_stuff/saved_data/fixed_ql_passing_spaces.json"
# q3 = "/Users/stephanehatgiskessell/Desktop/Kivy_stuff/saved_data/fixed_sss_ql_passing_spaces.json"
#
# with open(q1, 'r') as j:
#     q1 = json.loads(j.read())
# with open(q3, 'r') as j:
#     q3 = json.loads(j.read())
# with open(q4, 'r') as j:
#     q4 = json.loads(j.read())
#

#
# dsdt_points2fix = {}
# dsst_points2fix = {}
# sss_points2fix = {}
#
# #get (0,0) from q4
# dsdt_points2fix["(0.0, 0.0)"] = q4.get("(0.0, 0.0)")
#
# #get (0,-1),(0,-2),(0,-3),(0,1),(0,3),(3,-3),(2,-2) from q3
# sss_points2fix["(0, -1.0)"] = q3.get("(0, -1.0)")
# sss_points2fix["(0, -2.0)"] = q3.get("(0, -2.0)")
# sss_points2fix["(0, -3.0)"] = q3.get("(0, -3.0)")
# sss_points2fix["(0, 1.0)"] = q3.get("(0, 1.0)")
# sss_points2fix["(0, 3.0)"] = q3.get("(0, 3.0)")
# sss_points2fix["(3.0, -3.0)"] = q3.get("(3.0, -3.0)")
# sss_points2fix["(2.0, -2.0)"] = q3.get("(2.0, -2.0)")
#
# #get (0,-2) from q1
# dsst_points2fix["(0, -2.0)"] = q1.get("(0, -2.0)")
#
# with open("/Users/stephanehatgiskessell/Desktop/Kivy_stuff/saved_data/sss_points2fix.json", 'w') as fp:
#     json.dump(sss_points2fix,fp)
# with open("/Users/stephanehatgiskessell/Desktop/Kivy_stuff/saved_data/dsst_points2fix.json", 'w') as fp:
#     json.dump(dsst_points2fix,fp)
# with open("/Users/stephanehatgiskessell/Desktop/Kivy_stuff/saved_data/dsdt_points2fix.json", 'w') as fp:
#     json.dump(dsdt_points2fix,fp)

# with open('/Users/stephanehatgiskessell/Desktop/Kivy_stuff/MTURK_interface/exp1_data_samples/sample0_dict.pkl', 'rb') as handle:
#     f = pickle.load(handle)
#
q1 = "/Users/stephanehatgiskessell/Desktop/Kivy_stuff/saved_data/uf_dsst_ql_passing_spaces.json"
q2 = "/Users/stephanehatgiskessell/Desktop/Kivy_stuff/saved_data/uf_ssst_ql_passing_spaces.json"
q3 = "/Users/stephanehatgiskessell/Desktop/Kivy_stuff/saved_data/uf_sss_ql_passing_spaces.json"
q4 = "/Users/stephanehatgiskessell/Desktop/Kivy_stuff/saved_data/uf_ql_passing_spaces.json"



with open(q1, 'r') as j:
    q1 = json.loads(j.read())
with open(q2, 'r') as j:
    q2 = json.loads(j.read())
with open(q3, 'r') as j:
    q3 = json.loads(j.read())
with open(q4, 'r') as j:
    q4 = json.loads(j.read())

def make_all_pts_plot(quad,remove_oob,quad_name):
    all_xs = []
    all_ys = []
    for cords in quad.keys():
        cords = cords.replace("(","")
        cords = cords.replace(")","")
        cords = cords.replace(" ","").split(",")
        x = float(cords[0])
        y = float(cords[1])
        if remove_oob and (abs(x) >=50 or abs(y)>=50):
            continue
        all_xs.append(x)
        all_ys.append(y)
    fig = plt.figure()
    ax = fig.add_subplot(111)

    ax.spines['top'].set_color('none')
    ax.spines['left'].set_position('zero')
    ax.spines['right'].set_color('none')
    ax.spines['bottom'].set_position('zero')
    # plt.axis([-5, 5, -5, 5])
    plt.scatter(all_xs, all_ys)
    plt.savefig("all_pts_" + quad_name + ".png")

make_all_pts_plot(q1,True,"dsst")
make_all_pts_plot(q2,True,"ssst")
make_all_pts_plot(q3,False,"sss")
make_all_pts_plot(q4,False,"dsdt")


#
# sss_points2fix = {}
# ssst_points2fix = {}
# dsst_points2fix = {}
# dsdt_points2fix = {}
#
# for key, value in f.items():
#     key = key.split("/")[2]
#     key = key.split("_")
#     #['sss', '(1.0, -2.0)', '0.png']
#     index = int(key[2].split(".")[0])
#     if (key[0] == "sss"):
#         quad = q3.get(key[1])[index]
#         if (key[1] in sss_points2fix):
#             temp = sss_points2fix.get(key[1])
#             temp.append(quad)
#             sss_points2fix[key[1]] = temp
#         else:
#             sss_points2fix[key[1]] = [quad]
#     elif (key[0] == "ssst"):
#         quad = q2.get(key[1])[index]
#         if (key[1] in ssst_points2fix):
#             temp = ssst_points2fix.get(key[1])
#             temp.append(quad)
#             ssst_points2fix[key[1]] = temp
#         else:
#             ssst_points2fix[key[1]] = [quad]
#     elif (key[0] == "dsst"):
#         quad = q1.get(key[1])[index]
#         if (key[1] in dsst_points2fix):
#             temp = dsst_points2fix.get(key[1])
#             temp.append(quad)
#             dsst_points2fix[key[1]] = temp
#         else:
#             dsst_points2fix[key[1]] = [quad]
#     elif (key[0] == "dsdt"):
#         quad = q4.get(key[1])[index]
#         if (key[1] in dsdt_points2fix):
#             temp = dsdt_points2fix.get(key[1])
#             temp.append(quad)
#             dsdt_points2fix[key[1]] = temp
#         else:
#             dsdt_points2fix[key[1]] = [quad]
#     else:
#         print ("somethings wrong")
#
# with open("/Users/stephanehatgiskessell/Desktop/Kivy_stuff/saved_data/sss_points2fix.json", 'w') as fp:
#     json.dump(sss_points2fix,fp)
# with open("/Users/stephanehatgiskessell/Desktop/Kivy_stuff/saved_data/ssst_points2fix.json", 'w') as fp:
#     json.dump(ssst_points2fix,fp)
# with open("/Users/stephanehatgiskessell/Desktop/Kivy_stuff/saved_data/dsst_points2fix.json", 'w') as fp:
#     json.dump(dsst_points2fix,fp)
# with open("/Users/stephanehatgiskessell/Desktop/Kivy_stuff/saved_data/dsdt_points2fix.json", 'w') as fp:
#     json.dump(dsdt_points2fix,fp)
