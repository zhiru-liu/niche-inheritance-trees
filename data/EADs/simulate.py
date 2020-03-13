""" 
Use this script to generate the EADs with different sigmas.
Need to either copy utils.py to this folder or modify the line importing utils.
Both repetitions and the averaged EAD are saved. Averaged EADs are used in
the final plot.

"""

from utils import *
import matplotlib.pyplot as plt
import math

def generate_tree(n=1,r_e=0,R_0=10,mu=0,sigma=2,tree_size=100000):
    success = False
    while not success:
        tree = Tree(n=n,r_e=r_e,R_0=R_0)
        success, time = tree.simulate(mu, sigma, tree_size)
    print('Success. Tree length is %f' % time)
    return tree, time

def build_dict(data):
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
    return result

def average_dict(tp_dic):
    result = []
    for a in tp_dic:
        result.append([a, np.mean(tp_dic[a])])
    return np.array(result)

def get_data(tree, time):
    tree.prune_tree()
    AC = tree.get_AC_list()
    EAD = tree.get_EAD(time)
    return average_dict(build_dic(AC)), sum_dict(build_dic(EAD))

'''Studying the effect of sigma'''
sigmas = [0, 1, 1.5, 2.0, 2.5, 3.0]
all_EAD = []
repeat = 10
tree_size = 1000000
trees = []
threshold = 200
for i in range(len(sigmas)):
    sigma = sigmas[i]
    eads = []
    for j in range(repeat):
        tree, time = generate_tree(sigma=sigma, R_0=10, tree_size=tree_size)
        tree.prune_tree()
        trees.append(tree) #Remove this line when averaging
        if sigma==0:
            curr_ead = np.array(tree.get_EAD_list(time, 0))
        else:
            curr_ead = np.array(tree.get_EAD_list(time, threshold))
        curr_ead[:,1] = curr_ead[:,1]/np.sum(curr_ead[:,1]) #S(k) is normalized by the sum of S(k)
        curr_ead = sum_dict(build_dict(curr_ead))
        np.savetxt("./reps/EAD_sigma_%d_rep_%d.csv"%(i,j),curr_ead, delimiter=",")
        eads += curr_ead
    ead = average_dict(build_dict(eads))
    np.savetxt("./average/EAD_average_sigma_%d.csv"%(i),ead,delimiter=",")
    all_EAD.append(ead)
