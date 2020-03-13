from utils import *
import math

def generate_tree(n=1,r_e=0,R_0=10,mu=0,sigma=2,tree_size=100000):
    success = False
    while not success:
        tree = Tree(n=n,r_e=r_e,R_0=R_0)
        success, time = tree.simulate(mu, sigma, tree_size)
    print('Success. Tree length is %f' % time)
    return tree, time

'''Studying the effect of sigma'''
sigmas = [0, 1, 1.5, 2.0, 2.5, 3.0]
powers = [1, 5, 9]
tree_size = 1000000
trees = []
for i in range(len(sigmas)):
    for j in powers:
        sigma = sigmas[i]
        tree, time = generate_tree(sigma=sigma, R_0=10**j,
                tree_size=tree_size)
        tree.prune_tree()
        misc = np.array(tree.get_misc())
        np.savetxt("./niche_R_0=%d_%d"%(j,i), misc, delimiter=",")
        #j labels the value of R_0. i labels sigma.

