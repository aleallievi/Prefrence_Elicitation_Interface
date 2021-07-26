import numpy as np
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

# n_correct = [2,7,6,4,9,8,9,6,4,7,7,4,9,5,4,7,4,7,7,4,5,7,8,6,4,7,5]
n_correct = [2,5.5,5.5,2,7,6,6.5,5,3,5.5,5,3.5,6.5,4,3.5,5.5,3,5.5,5.5,2.5,4,5.5,6,4.5,3.5,6,3.5]
bins = [0.5*i for i in range(16)]
print (bins)
percent_correct = [n/9 for n in n_correct]
workers = [i for i in range(len(percent_correct))]

plt.hist(x=n_correct,bins=bins)
plt.savefig("exp2_worker_analysis.png")
