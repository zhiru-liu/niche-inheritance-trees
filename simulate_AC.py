from utils import *
import math
import numpy as np
""" Script for generating all the AC data. For example those used in Fig. 2, 3, 4"""

def generate_tree(n=1,r_e=0,R_0=10,mu=0,sigma=2,tree_size=100000):
    success = False
    while not success:
        tree = Tree(n=n,r_e=r_e,R_0=R_0)
        success, time = tree.simulate(mu, sigma, tree_size)
    print('Success. Tree length is %f' % time)
    return tree, time

def build_dic(data):
    tp_dic = dict()
    for i in range(len(data)):
        a,c = data[i]
        if a in tp_dic:
            c_list = tp_dic[a]
            c_list.append(c)
            tp_dic[a] = c_list
        else:
            tp_dic[a] = [c]
    return tp_dic

def sum_dict(tp_dic):
    result = []
    for a in tp_dic:
        result.append([a, np.sum(tp_dic[a])])
    return np.array(result)

def average_dict(tp_dic):
    result = []
    for a in tp_dic:
        result.append([a, np.mean(tp_dic[a])])
    return np.array(result)


'''Studying the effect of r_e or sigmas'''
sigmas = [0, 1, 1.5, 2.0, 2.5, 3.0]
r_es = [0.1, 0.05, 0.01, 0.005, 0.001, 0.0005, 0.0001]
repeat = 10
tree_size = 1000000
r_e = 0
for i in range(len(sigmas)):
    sigma = sigmas[i]
    ac = []
    for j in range(repeat):
        tree, time = generate_tree(sigma=sigma, r_e=r_e, R_0=10, tree_size=tree_size)
        tree.prune_tree()
        curr_ac = tree.get_AC_list(0)
        #np.savetxt("./data/model_change/constant_poisson/reps/AC_sigma_%d_rep_%d.csv"%(i,j),curr_ac, delimiter=",")
        ac += curr_ac
    ac = average_dict(build_dic(ac))
    np.savetxt("./data/fluctuation/AC/AC_average_sigma=%d.csv"%(i),ac,delimiter=",")
