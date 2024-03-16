import numpy as np


def AND(x1,x2):
    x = np.array([x1,x2])
    w = np.array([0.5, 0.5])
    b = -0.7
    tmp = np.sum(x*w) + b
    if tmp > 0:
        return 1
    else:
        return 0

def NAND(x1,x2):
    x = np.array([x1,x2])
    w = np.array([-0.5, -0.5])
    b = 0.7
    tmp = np.sum(x*w) + b
    if tmp > 0:
        return 1
    else:
        return 0

print(NAND(1,1))
print(NAND(0,1))
print(NAND(1,0))
print(NAND(0,0))
