import numpy as np
import json
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

def plot_quad(xs,ys,name):
    fig = plt.figure()
    ax = fig.add_subplot(111)

    ax.spines['top'].set_color('none')
    ax.spines['left'].set_position('zero')
    ax.spines['right'].set_color('none')
    ax.spines['bottom'].set_position('zero')
    # plt.axis([-5, 5, -5, 5])
    plt.scatter(xs, ys)
    plt.savefig(name)

dsdt_xs = [0,0,0,0,0,0,1,1,1,2,2,2,3,3,3,3,3,5,7,9,11,13,5,7]
dsdt_ys = [-1,-2,-3,1,3,0,-1,-2,-3,-1,-2,-3,-1,-2,-3,0,3,-1,-1,-1,-1,-1,-2,-2]
plot_quad (dsdt_xs,dsdt_ys,"exp3_dsdt_prop.png")

dsst_xs = [0,0,0,1,1,2,3,4]
dsst_ys = [-1,-2,-0,-1,-2,-1,-1,-1]
plot_quad (dsst_xs,dsst_ys,"exp3_dsst_prop.png")

ssst_xs = [0,0,0]
ssst_ys = [-1,-2,0]
plot_quad (ssst_xs,ssst_ys,"exp3_ssst_prop.png")


sss_xs = [0,0,0,0,0,0,1,2,2,2,3,3,3,3,3,5,7,9,11,1,1,5,7]
sss_ys = [-1,-2,-3,1,3,0,-2,-1,-2,-3,-1,-2,-3,0,3,-1,-1,-1,-1,-1,-3,-2,-2]
plot_quad (sss_xs,sss_ys,"exp3_sss_prop.png")
