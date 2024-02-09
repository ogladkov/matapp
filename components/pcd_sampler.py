from pathlib import Path
import pickle

import numpy as np

from components.pts_sampler import PointSamplerEven

def read_off(file):

    with open(file, 'r') as f:
        off_header = f.readline().strip()

        if 'OFF' == off_header:
            n_verts, n_faces, __ = tuple([int(s) for s in f.readline().strip().split(' ')])
        else:
            n_verts, n_faces, __ = tuple([int(s) for s in off_header.split(' ')])

        verts = [[float(s) for s in f.readline().strip('(').strip(')').split()] for i_vert in range(n_verts)]
        verts = np.array(verts)

        faces = [[int(s) for s in f.readline().strip('(').strip(')').split()][1:] for i_face in range(n_faces)]
        faces = np.array(faces)

    return verts, faces


def off2pcd():
    datapath = Path('./data/input/off')
    save_dir = Path('./data/input/pcd')
    sampler = PointSamplerEven(8192)

    for file in datapath.glob('*.off'):
        verts, faces = read_off(file)
        point_set = sampler(verts, faces)

        save_path = save_dir / file.name.replace('.off', '.pcd')

        with open(save_path, 'wb') as f:
            pickle.dump(point_set, f)

        print(f'PCD saved to {save_path}')
