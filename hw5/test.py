import matplotlib.path as mplPath
import numpy as np

poly = [0, 50]
bbPath = mplPath.Path(np.array([[111, 90],
                     [258,90],
                     [258,73],
                     [258,73],
                     [285,90],
                     [405,90],
                     [405,119],
                     [285,119],
                     [285,155],
                     [258,155],
                     [258,119],
                     [175,119],
                     [175,193],
                     [230,193],
                     [230,293],
                     [102,293],
                     [102,192],
                     [148,192],
                     [148,119],
                     [111,119]]))

print(bbPath.contains_point((200, 100)))
print(bbPath.contains_point((1, 25)))
print(bbPath.contains_point((25, 25)))