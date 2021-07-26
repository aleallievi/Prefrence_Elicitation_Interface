import pickle
import re
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import numpy as np

with open('/Users/stephanehatgiskessell/Desktop/Kivy_stuff/exp2_results/woi_questions.data', 'rb') as f:
    questions = pickle.load(f)
with open('/Users/stephanehatgiskessell/Desktop/Kivy_stuff/exp2_results/woi_answers.data', 'rb') as f:
    answers = pickle.load(f)

dsdt_res = {}
dsst_res = {}
ssst_res = {}
sss_res = {}

for i in range(len(questions)):
    assignment_qs = questions[i]
    assignment_as = answers[i]
    sample_n = assignment_as[0]
    with open('/Users/stephanehatgiskessell/Desktop/Kivy_stuff/exp2_data_samples/sample' + str(sample_n) + "/sample"+ str(sample_n) + "_dict.pkl", 'rb') as f:
        sample_dict = pickle.load(f)
    for q,a in zip(assignment_qs, assignment_as):
        if q == "sampleNumber":
            continue


        num = int(q.replace("query",""))
        point = sample_dict.get(num)
        quad = point.get("quadrant")
        pt = point.get("name").split("_")[0]

        # if a_str == "left":
        #     a = -1
        # elif a_str == "right":
        #     a = 1
        # elif a_str == "same":
        #     a = 0
        # else:
        #     continue

        if quad == "dsdt":

            if pt not in dsdt_res:
                dsdt_res[pt] = [a]
            else:
                arr = dsdt_res.get(pt)
                arr.append(a)
                dsdt_res[pt] = arr
        elif quad == "dsst":
            if pt not in dsst_res:
                dsst_res[pt] = [a]
            else:
                arr = dsst_res.get(pt)
                arr.append(a)
                dsst_res[pt] = arr
        elif quad == "ssst":
            if pt not in ssst_res:
                ssst_res[pt] = [a]
            else:
                arr = ssst_res.get(pt)
                arr.append(a)
                ssst_res[pt] = arr
        elif quad == "sss":
            if pt not in sss_res:
                sss_res[pt] = [a]
            else:
                arr = sss_res.get(pt)
                arr.append(a)
                sss_res[pt] = arr

dif_xs = []
dif_ys = []
dif_s = []

def rand_jitter(arr):
    stdev = .03 * (max(arr) - min(arr))
    if (stdev == 0):
        stdev = .07
    return arr + np.random.randn(len(arr)) * stdev

def create_circle (x,y,colors):

    index = 0
    colors = sorted(colors)
    for i in range (5):
        for j in range (6):
            if index == len(colors):
                return
            c = colors[index]
            offset_x = i*0.18
            offset_y = j*0.15

            # if i > 2:
            #     plot_x = x + offset_x- ((i-1)*0.18)
            # else:
            #     plot_x = x - offset_x
            plot_x = x + offset_x - 0.15
            plot_y = y + offset_y - 0.15
            # if j >= 3:
            #     plot_y = y + offset_y- ((j-1)*0.15)
            # else:
            #     plot_y = y - offset_y
            plt.scatter(plot_x, plot_y, color=c,s=5)

            index +=1
    # plt.show()



def plot_quad(quad_dict,quad,n):
    xs = []
    ys = []
    colors = []
    s = []
    cord2colors = {}
    for cord in quad_dict.keys():
        cord2colors[cord] = []

    fig = plt.figure()
    ax = fig.add_subplot(111)

    ax.spines['top'].set_color('none')
    ax.spines['left'].set_position('zero')
    ax.spines['right'].set_color('none')
    ax.spines['bottom'].set_position('zero')
    plt.axis([-5, 5, -5, 5])


    for cord in quad_dict.keys():
        actions = quad_dict.get(cord)
        cord_ = cord.replace("(","")
        cord_ = cord_.replace(")","")
        cord_ = cord_.split(",")
        x = float(cord_[0])
        y = float(cord_[1])
        cord_colors = []
        for a in actions:
            if a == "left":
                c = "b"
            elif a == "right":
                c = "r"
            elif a == "same":
                c = "g"
            else:
                c = "black"
                # dif_xs.append(x)
                # dif_ys.append(y)
                # dif_s.append(15)
                # continue
            xs.append(x)
            ys.append(y)
            colors.append(c)
            cord_colors.append(c)
            s.append(0.5)

            temp = cord2colors.get(cord)
            temp.append(c)
            cord2colors[cord] = temp
        create_circle(x,y,cord_colors)

    # plt.show()
    # ax = fig.add_subplot(2,2,n)
    # fig = plt.figure()
    # ax = fig.add_subplot(111)
    #
    # ax.spines['top'].set_color('none')
    # # ax.spines['top'].set_bounds(0,10)
    # ax.spines['left'].set_position('zero')
    # # ax.spines['left'].set_bounds(0,10)
    # ax.spines['right'].set_color('none')
    # ax.spines['bottom'].set_position('zero')
    # # ax.spines['bottom'].set_bounds(0,-10)
    # xs = rand_jitter(xs)
    # ys = rand_jitter(ys)
    # plt.axis([-5, 5, -5, 5])

    # for i in range(len(xs)):
    #     plt.scatter(xs[i], ys[i], color=colors[i],s=s[i])
    plt.savefig("woi_exp2_" + quad + ".png")
plot_quad(dsdt_res,"dsdt",1)
# plot_quad(dsst_res,"dsst",2)
# plot_quad(ssst_res,"ssst",3)
# plot_quad(sss_res,"sss",4)

# fig = plt.figure()
# ax = fig.add_subplot(111)
# ax.spines['top'].set_color('none')
# ax.spines['left'].set_position('zero')
# ax.spines['right'].set_color('none')
# ax.spines['bottom'].set_position('zero')
# dif_xs = rand_jitter(dif_xs)
# dif_ys = rand_jitter(dif_ys)
# for i in range(len(dif_xs)):
#     plt.scatter(dif_xs[i], dif_ys[i], color="purple",alpha=0.5,s=dif_s[i])
