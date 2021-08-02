import json
import codecs
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import os
import numpy as np
def plot_quad(quad,name):
    fig = plt.figure()
    ax = fig.add_subplot(111)

    ax.spines['top'].set_color('none')
    ax.spines['left'].set_position('zero')
    ax.spines['right'].set_color('none')
    ax.spines['bottom'].set_position('zero')
    plt.axis([-10, 10, -5, 5])

    for key in quad.keys():
        n_points = len(quad.get(key))
        key_ = key.replace("(","")
        key_ = key_.replace(")","")
        key_ = key_.replace(" ","")
        key_ = key_.split(",")
        x = float(key_[0])
        y = float(key_[1])

        plt.scatter(x,y,s=40)
        ax.annotate(str(n_points), (x, y))
    plt.savefig(name + "_chosen_points.png")


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

def print_n_points(quad,name):
    for key in quad:
        arr = quad.get(key)
        print (name + "_" + key + " # of pairs: " + str(len(arr)))


def fix_n_append(point,correct_point,quad):
    fixed = []
    for pairs in quad.get(point):
        traj1 = pairs[0]
        traj2 = pairs[1]
        fixed.append([traj2,traj1])
    quad[correct_point] = fixed
    return fixed

def remove_less_than(n):
    quads = [ex1_dsst,ex1_ssst,ex1_sss,ex1_dsdt]
    pruned_ex1_dsdt = ex1_dsdt.copy()
    pruned_ex1_dsst = ex1_dsst.copy()
    pruned_ex1_ssst = ex1_ssst.copy()
    pruned_ex1_sss = ex1_sss.copy()
    for quad in quads:
        for key in quad.keys():
            n_points = len(quad.get(key))
            if n_points <= n:
                pruned_ex1_dsdt.pop(key,None)
                pruned_ex1_dsst.pop(key,None)
                pruned_ex1_ssst.pop(key,None)
                pruned_ex1_sss.pop(key,None)
                continue
    return pruned_ex1_dsdt, pruned_ex1_dsst, pruned_ex1_ssst, pruned_ex1_sss

ex1_dsst = {}
ex1_ssst = {}
ex1_sss = {}
ex1_dsdt = {}

ex1_dsdt["(0.0, 0.0)"] = q1.get("(0.0, 0.0)")
ex1_dsdt["(0.0, -1.0)"] = q1.get("(0.0, -1.0)")
ex1_dsdt["(0.0, -2.0)"] = q1.get("(0.0, -2.0)")
ex1_dsdt["(0.0, -3.0)"] = q1.get("(0.0, -3.0)")
ex1_dsdt["(0.0, -4.0)"] = q1.get("(0.0, -4.0)")
ex1_dsdt["(0.0, -5.0)"] = q1.get("(0.0, -5.0)")
ex1_dsdt["(1.0, 1.0)"] = q1.get("(1.0, 1.0)")
ex1_dsdt["(1.0, 0.0)"] = q1.get("(1.0, 0.0)")
ex1_dsdt["(1.0, -1.0)"] = q1.get("(1.0, -1.0)")
ex1_dsdt["(1.0, -2.0)"] = q1.get("(1.0, -2.0)")
ex1_dsdt["(1.0, -3.0)"] = q1.get("(1.0, -3.0)")
ex1_dsdt["(1.0, -5.0)"] = q1.get("(1.0, -3.0)")
ex1_dsdt["(2.0, 2.0)"] = q1.get("(2.0, 2.0)")
ex1_dsdt["(2.0, 0.0)"] = q1.get("(2.0, 0.0)")
ex1_dsdt["(2.0, -1.0)"] = q1.get("(2.0, -1.0)")
ex1_dsdt["(2.0, -2.0)"] = q1.get("(2.0, -2.0)")
ex1_dsdt["(2.0, -3.0)"] = q1.get("(2.0, -3.0)")
ex1_dsdt["(3.0, 3.0)"] = q1.get("(3.0, 3.0)")
ex1_dsdt["(3.0, 0.0)"] = q1.get("(3.0, 0.0)")
ex1_dsdt["(3.0, -1.0)"] = q1.get("(3.0, -1.0)")
ex1_dsdt["(3.0, -2.0)"] = q1.get("(3.0, -2.0)")
ex1_dsdt["(3.0, -3.0)"] = q1.get("(3.0, -3.0)")
ex1_dsdt["(4.0, -1.0)"] = q1.get("(4.0, -1.0)")
ex1_dsdt["(4.0, -4.0)"] = q1.get("(4.0, -4.0)")
ex1_dsdt["(5.0, 0.0)"] = q1.get("(5.0, 0.0)")
ex1_dsdt["(5.0, -1.0)"] = q1.get("(5.0, -1.0)")
ex1_dsdt["(5.0, -2.0)"] = q1.get("(5.0, -2.0)")
ex1_dsdt["(7.0, -1.0)"] = q1.get("(7.0, -1.0)")
ex1_dsdt["(7.0, -2.0)"] = q1.get("(7.0, -2.0)")
ex1_dsdt["(8.0, 0.0)"] = q1.get("(8.0, 0.0)")
ex1_dsdt["(8.0, -1.0)"] = q1.get("(8.0, -1.0)")

for key in ex1_dsdt.keys():
    dsst_item = q2.get(key)
    if dsst_item != None:
        ex1_dsst[key] = dsst_item

    ssst_item = q3.get(key)
    if ssst_item != None:
        ex1_ssst[key] = ssst_item

    sss_item =q4.get(key)
    if sss_item != None:
        ex1_sss[key] = sss_item


#ex1_dsdt["(1.0, -5.0)"] = q1.get("(1.0, -3.0)")
#ex1_dsdt["(3.0, -3.0)"] = q1.get("(3.0, -3.0)")
#ex1_dsdt["(8.0, -1.0)"] = q1.get("(8.0, -1.0)")


# ex1_dsst["(0.0, 0.0)"] = q2.get("(0.0, 0.0)")
# ex1_dsst["(0.0, -1.0)"] = q2.get("(0.0, -1.0)")
# ex1_dsst["(0.0, -2.0)"] = q2.get("(0.0, -2.0)")
# ex1_dsst["(0.0, -3.0)"] = q2.get("(0.0, -3.0)")
# ex1_dsst["(1.0, 1.0)"] = q2.get("(1.0, 1.0)")
# ex1_dsst["(1.0, 0.0)"] = q2.get("(1.0, 0.0)")
# ex1_dsst["(1.0, -1.0)"] = q2.get("(1.0, -1.0)")
# ex1_dsst["(1.0, -2.0)"] = q2.get("(1.0, -2.0)")
# ex1_dsst["(1.0, -3.0)"] = q2.get("(1.0, -3.0)")
# ex1_dsst["(2.0, 2.0)"] = q2.get("(2.0, 2.0)")
# ex1_dsst["(2.0, 0.0)"] = q2.get("(2.0, 0.0)")
# ex1_dsst["(2.0, -1.0)"] = q2.get("(2.0, -1.0)")
# ex1_dsst["(2.0, -2.0)"] = q2.get("(2.0, -2.0)")
# ex1_dsst["(2.0, -3.0)"] = q2.get("(2.0, -3.0)")
# ex1_dsst["(3.0, 0.0)"] = q2.get("(3.0, 0.0)")
# ex1_dsst["(3.0, -1.0)"] = q2.get("(3.0, -1.0)")
# ex1_dsst["(3.0, -2.0)"] = q2.get("(3.0, -2.0)")
# ex1_dsst["(3.0, -3.0)"] = q2.get("(3.0, -3.0)")
# ex1_dsst["(4.0, -1.0)"] = q2.get("(4.0, -1.0)")
# ex1_dsst["(5.0, 0.0)"] = q2.get("(5.0, 0.0)")
# ex1_dsst["(5.0, -1.0)"] = q2.get("(5.0, -1.0)")
# ex1_dsst["(6.0, -1.0)"] = q2.get("(6.0, -1.0)")
# ex1_dsst["(8.0, 0.0)"] = q2.get("(8.0, 0.0)")
#
# # #
# ex1_ssst["(0.0, 0.0)"] = q3.get("(0.0, 0.0)")
# ex1_ssst["(0.0, -1.0)"] = q3.get("(0.0, -1.0)")
# ex1_ssst["(0.0, -2.0)"] = q3.get("(0.0, -2.0)")
# ex1_ssst["(0.0, -3.0)"] = q3.get("(0.0, -3.0)")
#
# ex1_sss["(0.0, 0.0)"] = q4.get("(0.0, 0.0)")
# ex1_sss["(0.0, -1.0)"] = q4.get("(0.0, -1.0)")
# ex1_sss["(0.0, -2.0)"] = q4.get("(0.0, -2.0)")
# ex1_sss["(0.0, -3.0)"] = q4.get("(0.0, -3.0)")
# ex1_sss["(0.0, -4.0)"] = q4.get("(0.0, -4.0)")
# ex1_sss["(0.0, -5.0)"] = q4.get("(0.0, -5.0)")
# ex1_sss["(1.0, 1.0)"] = q4.get("(1.0, 1.0)")
# ex1_sss["(1.0, 0.0)"] = q4.get("(1.0, 0.0)")
# ex1_sss["(1.0, -1.0)"] = q4.get("(1.0, -1.0)")
# ex1_sss["(1.0, -2.0)"] = q4.get("(1.0, -2.0)")
# ex1_sss["(1.0, -3.0)"] =  q4.get("(1.0, -3.0)")
# ex1_sss["(1.0, -5.0)"] = q4.get("(1.0, -5.0)")
# ex1_sss["(2.0, 2.0)"] = q4.get("(2.0, 2.0)")
# ex1_sss["(2.0, 0.0)"] = q4.get("(2.0, 0.0)")
# ex1_sss["(2.0, -1.0)"] = q4.get("(2.0, -1.0)")
# ex1_sss["(2.0, -2.0)"] = q4.get("(2.0, -2.0)")
# ex1_sss["(2.0, -3.0)"] = q4.get("(2.0, -3.0)")
# ex1_sss["(3.0, 3.0)"] = q4.get("(3.0, 3.0)")
# ex1_sss["(3.0, 0.0)"] = q4.get("(3.0, 0.0)")
# ex1_sss["(3.0, -1.0)"] = q4.get("(3.0, -1.0)")
# ex1_sss["(3.0, -2.0)"] = q4.get("(3.0, -2.0)")
# ex1_sss["(3.0, -3.0)"] = q4.get("(3.0, -3.0)")
# ex1_sss["(4.0, -1.0)"] = q4.get("(4.0, -1.0)")
# ex1_sss["(4.0, -4.0)"] = q4.get("(4.0, -4.0)")
# ex1_sss["(5.0, 0.0)"] = q4.get("(5.0, 0.0)")
# ex1_sss["(5.0, -1.0)"] = q4.get("(5.0, -1.0)")
# ex1_sss["(5.0, -2.0)"] = q4.get("(5.0, -2.0)")
# ex1_sss["(6.0, -1.0)"] = q4.get("(6.0, -1.0)")
# ex1_sss["(6.0, -2.0)"] = q4.get("(6.0, -2.0)")
# ex1_sss["(7.0, -1.0)"] = q4.get("(7.0, -1.0)")
# ex1_sss["(7.0, -2.0)"] = q4.get("(7.0, -2.0)")
# ex1_sss["(8.0, 0.0)"] = q4.get("(8.0, 0.0)")
# ex1_sss["(8.0, -1.0)"] = q4.get("(8.0, -1.0)")
ex1_dsdt,ex1_dsst,ex1_ssst,ex1_sss = remove_less_than(8)
plot_quad(ex1_dsdt,"2021_07_29_dsdt")
plot_quad(ex1_dsst,"2021_07_29_dsst")
plot_quad(ex1_ssst,"2021_07_29_ssst")
plot_quad(ex1_sss,"2021_07_29_sss")

with open("/Users/stephanehatgiskessell/Desktop/Kivy_stuff/saved_data/2021_07_29_dsdt_chosen.json", 'w') as fp:
    json.dump(ex1_dsdt,fp)
with open("/Users/stephanehatgiskessell/Desktop/Kivy_stuff/saved_data/2021_07_29_dsst_chosen.json", 'w') as fp:
    json.dump(ex1_dsst,fp)
with open("/Users/stephanehatgiskessell/Desktop/Kivy_stuff/saved_data/2021_07_29_ssst_chosen.json", 'w') as fp:
    json.dump(ex1_ssst,fp)
with open("/Users/stephanehatgiskessell/Desktop/Kivy_stuff/saved_data/2021_07_29_sss_chosen.json", 'w') as fp:
    json.dump(ex1_sss,fp)
