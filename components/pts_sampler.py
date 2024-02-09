import random

import numpy as np

from components.pointnet2.models.pointnet2_utils import pc_normalize


class PointSamplerEven(object):
    def __init__(self, output_size):
        assert isinstance(output_size, int)
        self.output_size = output_size

    def triangle_area(self, pt1, pt2, pt3):
        side_a = np.linalg.norm(pt1 - pt2)
        side_b = np.linalg.norm(pt2 - pt3)
        side_c = np.linalg.norm(pt3 - pt1)
        s = 0.5 * (side_a + side_b + side_c)
        return max(s * (s - side_a) * (s - side_b) * (s - side_c), 0) ** 0.5

    def sample_point(self, pt1, pt2, pt3):
        s, t = sorted([random.random(), random.random()])
        f = lambda i: s * pt1[i] + (t - s) * pt2[i] + (1 - t) * pt3[i]
        return (f(0), f(1), f(2))

    def __call__(self, verts, faces):
        verts = np.array(verts)
        total_area = sum(self.triangle_area(verts[face[0]], verts[face[1]], verts[face[2]]) for face in faces)

        sampled_points = []

        for face in faces:
            area = self.triangle_area(verts[face[0]], verts[face[1]], verts[face[2]])
            points_in_face = int(np.round(self.output_size * (area / total_area)))

            for _ in range(points_in_face):
                cl = face[-1]
                sampled_points.append(self.sample_point(verts[face[0]], verts[face[1]], verts[face[2]]))

        # In case rounding errors result in a different number of points, we adjust the number of sampled points
        while len(sampled_points) > self.output_size:
            sampled_points.pop()

        while len(sampled_points) < self.output_size:
            face = random.choice(faces)
            sampled_points.append(self.sample_point(verts[face[0]], verts[face[1]], verts[face[2]]))

        pcd = np.array(sampled_points)

        # Normalize
        pcd = pc_normalize(pcd)

        return pcd
