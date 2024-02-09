import pickle

import numpy as np


def pcd2csv(fpath):

    with open(fpath, 'rb') as f:
        pcd = pickle.load(f)

    save_path = fpath.replace('.pcd', '.csv')
    with open(save_path, 'w') as f:

        for pt in pcd:
            f.write(f'{str(pt[0])},{str(pt[1])},{str(pt[2])}\n')



if __name__ == '__main__':
    fpath = '/home/sm00th/Projects/upwork/flopo/matapp/data/input/pcd/model_metal_009.pcd'
    pcd2csv(fpath)