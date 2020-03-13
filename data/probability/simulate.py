from utils import *
import time
import numpy as np
# Need to move the utils file or modify the import line


def get_success_rate(sigma, threshold, N):
    count = 0
    failures = []
    for i in range(N):
        tree = Tree(n=1,r_e=0,R_0=10)
        success, size = tree.simulate(0, sigma, threshold)
        count = count + 1 if success else count
        if not success:
            failures.append(size)
    return count/N, failures


start = time.time()
sigmas = [2.8, 3, 3.5] #[0.5, 0.8, 1.2, 1.4, 1.6, 1.8, 2, 2.2, 2.5, 3, 3.5]
rates = []
all_fails = []
for sigma in sigmas:
    rate, fails = get_success_rate(sigma, 10000, 1000)
    rates.append(rate)
    all_fails.append(fails)
    if len(fails) != 0:
        print('Sigma=%.1f: Success rate is %.3f, maximum failures is %d\n' % (sigma, rate, max(fails)))
    else:
        print('Success rate is %.3f' % (rate))
    print(time.time()-start)

data = np.array([sigmas, rates]).T
np.savetxt('./data/probability/probability.txt', data, delimiter=',')
