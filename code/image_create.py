import numpy as np
import matplotlib.pyplot as plt
from utils import save_image
import os

if __name__ == '__main__':

    if not os.path.exists("../Images"):
        os.mkdir("../Images")

    i=np.load('../data/cylinder_u.npy')
    output=np.load('../output/200.npy')

    img_list=[0,100,200,300]

    save_image(i,output,img_list)