

import numpy as np

class Reference_point:

    def get_reference_points_from_IGD(self):
        points = []
        points.extend(self.get_reference_point_by_exis(0, [1, 2, 3], 0.05))
        points.extend(self.get_reference_point_by_exis(1, [0, 2, 3], 0.05))
        points.extend(self.get_reference_point_by_exis(2, [0, 1, 3], 0.05))
        points.extend(self.get_reference_point_by_exis(3, [0, 1, 2], 0.05))
        tpls = [tuple(x) for x in points]
        mylist = list(dict.fromkeys(tpls))
        points = [list(x) for x in mylist]
        return points

    def get_reference_point_by_exis(self, fixed_col, cols_to_modify, step):
        list = []
        x = np.arange(0, 1 + step, step, dtype=float)
        y = np.arange(0, 1 + step, step, dtype=float)
        z = np.arange(0, 1 + step, step, dtype=float)
        for i in x:
            for j in y:
                for k in z:
                    n = np.empty([4])
                    n[fixed_col] = 0
                    n[cols_to_modify[0]] = i
                    n[cols_to_modify[1]] = j
                    n[cols_to_modify[2]] = k
                    list.append(n)
        return list
