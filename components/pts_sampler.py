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

    def triangulate_face(self, verts, face):
        triangles = []

        for i in range(1, len(face) - 1):
            triangles.append((face[0], face[i], face[i + 1]))

        return triangles

    def __call__(self, verts, faces):
        verts = np.array(verts)
        total_area = 0
        face_triangles = []

        for face in faces:
            if len(face) == 3:
                triangles = [(face[0], face[1], face[2])]
            else:
                triangles = self.triangulate_face(verts, face)
            face_triangles.extend(triangles)
            for tri in triangles:
                total_area += self.triangle_area(verts[tri[0]], verts[tri[1]], verts[tri[2]])

        sampled_points = []

        for tri in face_triangles:
            area = self.triangle_area(verts[tri[0]], verts[tri[1]], verts[tri[2]])
            points_in_face = int(np.round(self.output_size * (area / total_area)))

            for _ in range(points_in_face):
                sampled_points.append(self.sample_point(verts[tri[0]], verts[tri[1]], verts[tri[2]]))

        # Adjust the number of sampled points due to rounding errors, as before
        while len(sampled_points) > self.output_size:
            sampled_points.pop()

        while len(sampled_points) < self.output_size:
            tri = random.choice(face_triangles)
            sampled_points.append(self.sample_point(verts[tri[0]], verts[tri[1]], verts[tri[2]]))

        pcd = np.array(sampled_points)
        pcd = pc_normalize(pcd)  # Normalize

        return pcd
