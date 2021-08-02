import numpy as np
import os
import re
import pickle
import json

q1 = "/Users/stephanehatgiskessell/Desktop/Kivy_stuff/saved_data/ex3_dsdt.json"
q2 = "/Users/stephanehatgiskessell/Desktop/Kivy_stuff/saved_data/ex3_dsst.json"
q3 = "/Users/stephanehatgiskessell/Desktop/Kivy_stuff/saved_data/ex3_ssst.json"
q4 = "/Users/stephanehatgiskessell/Desktop/Kivy_stuff/saved_data/ex3_sss.json"

with open(q1, 'r') as j:
    q1 = json.loads(j.read())
with open(q2, 'r') as j:
    q2 = json.loads(j.read())
with open(q3, 'r') as j:
    q3 = json.loads(j.read())
with open(q4, 'r') as j:
    q4 = json.loads(j.read())

rootdir = "/Users/stephanehatgiskessell/Desktop/Kivy_stuff/MTURK_interface/exp3_data_samples"

for subdir, dirs, files in os.walk(rootdir):
    if len(subdir.split("/")) == 7:
        continue
    temp = re.findall(r'\d+', subdir.split("/")[-1])
    id = list(map(int, temp))[0]

    dict_path = subdir + "/" + "sample" + str(id) + "_dict.pkl"
    with open(dict_path, 'rb') as fp:
        sample_dict = pickle.load(fp)

    for sample_key in sample_dict.keys():
        sample = sample_dict.get(sample_key)
        dom_val = sample.get("dom_val")

        name = sample.get("name")
        point = name.split("/")[-1].split("_")
        index = int(point[-1])
        if (point[0] == "vf" or point[0] == "none" or point[0] == "all"):
            point = point[1]
        else:
            point = point[0]
        point_ = point.replace("(","")
        point_ = point_.replace(")","")
        point_ = point_.split(",")
        expected_x = float(point_[0])
        expected_y = float(point_[1])
        if expected_x == 0:
            expected_x = int(expected_x)
        if expected_y == 0:
            expected_y = int(expected_y)
        quad = sample.get("quadrant")

        #always going to be path1 - path2
        if quad == "dsdt":
            toi = q1.get(str((expected_x,expected_y)))[index]
        if quad == "dsst":
            toi = q2.get(str((expected_x,expected_y)))[index]
        if quad == "ssst":
            toi = q3.get(str((expected_x,expected_y)))[index]
        if quad == "sss":
            toi = q4.get(str((expected_x,expected_y)))[index]
        #checks to make sure that all points are from the correct coordinates (ie: nothing got jumbled around)
        assert expected_x == toi[2] and expected_y == toi[3]

        #TODO: now we need to check that the ordering of the trajectory pair is correct
        if dom_val == "R":
            path1 = name + "_1_" + dom_val + ".png"
            path2 = name + "_0_" + dom_val + ".png"
        if dom_val == "L":
            path1 = name + "_0_" + dom_val + ".png"
            path2 = name + "_1_" + dom_val + ".png"
