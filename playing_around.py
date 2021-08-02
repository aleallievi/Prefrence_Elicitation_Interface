import numpy as np
import json
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import os

q1 = "/Users/stephanehatgiskessell/Desktop/Kivy_stuff/saved_data/2021_07_29_dsdt.json"
q2 = "/Users/stephanehatgiskessell/Desktop/Kivy_stuff/saved_data/2021_07_29_dsst.json"
q3 = "/Users/stephanehatgiskessell/Desktop/Kivy_stuff/saved_data/2021_07_29_ssst.json"
q4 = "/Users/stephanehatgiskessell/Desktop/Kivy_stuff/saved_data/2021_07_29_sss.json"



with open(q1, 'r') as j:
    q1 = json.loads(j.read())
with open(q2, 'r') as j:
    q2 = json.loads(j.read())
with open(q3, 'r') as j:
    q3 = json.loads(j.read())
with open(q4, 'r') as j:
    q4 = json.loads(j.read())

def plot_quad(quad,name):
    fig = plt.figure()
    ax = fig.add_subplot(111)

    ax.spines['top'].set_color('none')
    ax.spines['left'].set_position('zero')
    ax.spines['right'].set_color('none')
    ax.spines['bottom'].set_position('zero')
    # plt.axis([-15, 15, -15, 15])

    for key in quad.keys():
        print (key)
        n_points = len(quad.get(key))

        key_ = key.replace("(","")
        key_ = key_.replace(")","")
        key_ = key_.replace(" ","")
        key_ = key_.split(",")
        x = float(key_[0])
        y = float(key_[1])

        plt.scatter(x,y,s=40)
        ax.annotate(str(n_points), (x, y),fontsize=10)
    plt.savefig(name + "_all_#_points.png")

plot_quad(q1,"2021_07_29_dsdt")
plot_quad(q2,"2021_07_29_dsst")
plot_quad(q3,"2021_07_29_ssst")
plot_quad(q4,"2021_07_29_sss")

# vf =[[42,43,44,45,46,47,46,45,44,43],
# [43,0,0,0,0,48,0,0,0,44],
# [44,0,0,0,0,49,0,0,0,45],
# [45,0,0,0,0,50,0,0,0,46],
# [46,47,48,49,50,0,49,48,47],
# [45,0,0,0,0,50,0,0,0,46],
# [44,0,0,0,0,49,0,0,0,45],
# [43,0,0,0,0,48,0,0,0,44],
# [42,0,0,0,0,47,0,0,0,43],
# [41,42,43,44,45,46,45,44,43,42]]
#
# with open("/Users/stephanehatgiskessell/Desktop/Kivy_stuff/MTURK_interface/assets/boards/player_board_5_board_value_function.json", 'w') as fp:
#     json.dump(vf,fp)

# fps = []
# for root, dirs, files in os.walk("/Users/stephanehatgiskessell/Desktop/Kivy_stuff/all_formatted_imgs/"):
#     # for name in files:
#     for root2, dirs2, files2 in os.walk(root):
#         for name in files2:
#             name_split = name.split("_")
#             if len(name_split) == 3:
#                 last_char = name_split[-1].replace(".png","")
#                 if last_char.isalpha():
#                     path = root2 +"/"+name
#                     os.remove(path)


#----
# dsdt_target_pts = [(0,-4),(0,-5),(1,1),(1,0),(2,2),(2,0),(5,0),(5,-1),(5,-2),(7,-1),(8,0),(9,-1),(10,-1),(13,-1)]
# dsst_target_pts = [(0,1),(1,0),(1,1),(2,0),(2,2),(3,0),(4,-1),(5,0),(7,0),(8,0)]
# sss_target_pts = [(0,-4),(0,-5),(1,1),(1,0),(1,-1),(1,-3),(2,2),(2,0),(5,0),(5,-1),(5,-2),(6,-1),(6,-2),(8,0),(9,-1),(11,-1)]
#
# def mod_pts(q1,name,targets):
#     with open(q1, 'r') as j:
#         q1 = json.loads(j.read())
#     mod_q1 = {}
#     for k in q1.keys():
#         k_ = k.replace("(","")
#         k_ = k_.replace(")","")
#         k_ = k_.split(",")
#         pt = (float(k_[0]),float(k_[1]))
#         if pt in targets:
#             mod_q1[k] = q1.get(k)
#     with open("/Users/stephanehatgiskessell/Desktop/Kivy_stuff/saved_data/" + name + ".json", 'w') as fp:
#         json.dump(mod_q1,fp)
#
# q1 = "/Users/stephanehatgiskessell/Desktop/Kivy_stuff/saved_data/app_ql_passing_spaces.json"
# mod_pts(q1,"ex3_dsdt_app",dsdt_target_pts)
#
# q2 = "/Users/stephanehatgiskessell/Desktop/Kivy_stuff/saved_data/app_dsst_ql_passing_spaces.json"
# mod_pts(q2,"ex3_dsst_app",dsst_target_pts)
#
# q3 = "/Users/stephanehatgiskessell/Desktop/Kivy_stuff/saved_data/app_sss_ql_passing_spaces.json"
# mod_pts(q3,"ex3_sss_app",sss_target_pts)
# q1 = "/Users/stephanehatgiskessell/Downloads/app_sss_ql_passing_spaces.json"
# with open(q1, 'r') as j:
#     q1 = json.loads(j.read())
#
# print (q1.keys())
#--------------------------------------------------------------------------------------------------------------#
# q1 = "/Users/stephanehatgiskessell/Desktop/Kivy_stuff/saved_data/ex3_dsdt.json"
# q2 = "/Users/stephanehatgiskessell/Desktop/Kivy_stuff/saved_data/ex3_dsst.json"
# # q3 = "/Users/stephanehatgiskessell/Desktop/Kivy_stuff/saved_data/ex3_ssst.json"
# # q4 = "/Users/stephanehatgiskessell/Desktop/Kivy_stuff/saved_data/ex3_sss.json"
#
# #
# # additonal_q1 = "/Users/stephanehatgiskessell/Desktop/Kivy_stuff/saved_data/dsdt_points2fix.json"
# additonal_q2 = "/Users/stephanehatgiskessell/Desktop/Kivy_stuff/saved_data/dsst_points2fix.json"
# # additonal_q4 = "/Users/stephanehatgiskessell/Desktop/Kivy_stuff/saved_data/sss_points2fix.json"
# #
# #
# # with open(q1, 'r') as j:
# #     q1 = json.loads(j.read())
# with open(q2, 'r') as j:
#     q2 = json.loads(j.read())
# # for k in q2.keys():
# #     k_ = k.replace("(","")
# #     k_ = k_.replace(")","")
# #     k_ = k_.split(",")
# #     x = float(k_[0])
# #     y = float(k_[1])
# #
# #     if y == 0 and (x == -1 or x == -2 or x == -3 or x == -5 or x == -7 or x == -8):
# #         x = abs(x)
# #         q2[str((x,y))] = q2.get(k)
# #         q2.pop(k, None)
# #
# #     #     reversed_traj_pairs = []
# #     #     traj_pairs =
# #     #     for trajs in traj_pairs:
# #     #         traj1 = trajs[0]
# #     #         traj2 = trajs[1]
# #     #
# #     #         reversed = [traj2,traj1]
# #     #         reversed_traj_pairs.append(reversed)
# #     #     q2[k] = reversed_traj_pairs
# with open("/Users/stephanehatgiskessell/Desktop/Kivy_stuff/saved_data/ex3_dsst.json", 'w') as fp:
#     json.dump(q2,fp)


# with open(q3, 'r') as j:
#     q3 = json.loads(j.read())
# with open(q4, 'r') as j:
#     q4 = json.loads(j.read())
#
# with open(additonal_q1, 'r') as j:
#     additonal_q1 = json.loads(j.read())
# with open(additonal_q2, 'r') as j:
#     additonal_q2 = json.loads(j.read())
# with open(additonal_q4, 'r') as j:
#     additonal_q4 = json.loads(j.read())
#
# def appendnreplace(appendee, quad):
#     for key in appendee.keys():
#         # if key in quad.keys():
#         quad[key] = appendee.get(key)
#
# appendnreplace(additonal_q1,q1)
# appendnreplace(additonal_q2,q2)
# appendnreplace(additonal_q4,q4)
#
# with open("/Users/stephanehatgiskessell/Desktop/Kivy_stuff/saved_data/ex3_dsdt.json", 'w') as fp:
#     json.dump(q1,fp)
# with open("/Users/stephanehatgiskessell/Desktop/Kivy_stuff/saved_data/ex3_dsst.json", 'w') as fp:
#     json.dump(q2,fp)
# with open("/Users/stephanehatgiskessell/Desktop/Kivy_stuff/saved_data/ex3_ssst.json", 'w') as fp:
#     json.dump(q3,fp)
# with open("/Users/stephanehatgiskessell/Desktop/Kivy_stuff/saved_data/ex3_sss.json", 'w') as fp:
#     json.dump(q4,fp)
#--------------------------------------------------------------------------------------------------------------#
#
# def plot_quad(xs,ys,name):
#     fig = plt.figure()
#     ax = fig.add_subplot(111)
#
#     ax.spines['top'].set_color('none')
#     ax.spines['left'].set_position('zero')
#     ax.spines['right'].set_color('none')
#     ax.spines['bottom'].set_position('zero')
#     # plt.axis([-5, 5, -5, 5])
#     plt.scatter(xs, ys)
#     plt.savefig(name)
#
# def rand_jitter(arr):
#     stdev = .01 * (max(arr) - min(arr))
#     return arr + np.random.randn(len(arr)) * stdev
#
# fig = plt.figure()
# ax = fig.add_subplot(111)
#
# ax.spines['top'].set_color('none')
# ax.spines['left'].set_position('zero')
# ax.spines['right'].set_color('none')
# ax.spines['bottom'].set_position('zero')
# # plt.axis([-5, 5, -5, 5])
#
# dsdt_xs = [0,  0, 0,0,1,1,1,2,2,2,3,3,3,3,3,5,7,9,11,13,5,7,0,0,1,2,5,8,1,2]
# dsdt_ys = [-1,-2,-3,0,-1,-2,-3,-1,-2,-3,-1,-2,-3,0,3,-1,-1,-1,-1,-1,-2,-2,-4,-5,0,0,0,0,1,2]
# # plot_quad (dsdt_xs,dsdt_ys,"exp3_dsdt_prop.png")
# plt.scatter(rand_jitter(dsdt_xs), rand_jitter(dsdt_ys),color="brown",alpha = 1,s=20)
#
# dsst_xs = [0,0,0,1,1,2,3,4,1,2,5,8,1,2,3]
# dsst_ys = [-1,-2,0,-1,-2,-1,-1,-1,0,0,0,0,1,2,0]
# # plot_quad (dsst_xs,dsst_ys,"exp3_dsst_prop.png")
# plt.scatter(rand_jitter(dsst_xs), rand_jitter(dsst_ys),color="red",alpha = 1,s=20)
#
# ssst_xs = [0,0,0]
# ssst_ys = [-1,-2,0]
# plt.scatter(rand_jitter(ssst_xs), rand_jitter(ssst_ys),color="yellow",alpha = 1,s=20)
#
# # plot_quad (ssst_xs,ssst_ys,"exp3_ssst_prop.png")
# sss_xs = [ 0, 0, 0,0,1,2,2,2,3,3,3,3,3,5,7,9,11,1,1,5,7,0,0,1,2,5,8,1,2]
# sss_ys = [-1,-2,-3,0,-2,-1,-2,-3,-1,-2,-3,0,3,-1,-1,-1,-1,-1,-3,-2,-2,-4,-5,0,0,0,0,1,2]
# plt.scatter(rand_jitter(sss_xs), rand_jitter(sss_ys),color="blue",alpha = 1,s=20)
#
#
#
# # plot_quad (sss_xs,sss_ys,"exp3_sss_prop.png")
# plt.savefig("exp3_prop.png")
