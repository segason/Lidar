import pptk
import pandas as pd
import numpy as np

def read_points(f):
    # reads Semantic3D .txt file f into a pandas dataframe
    col_names = ['x', 'y', 'z', 'deviation', 'amplitude', 'reflectance', 'r', 'g', 'b']
    col_dtype = {'x': np.float32, 'y': np.float32, 'z': np.float32, 'deviation': np.int32, 'amplitude': np.float32, 'reflectance': np.float32, 'r': np.uint8, 'g': np.uint8, 'b': np.uint8}
    return pd.read_csv(f, names=col_names, dtype=col_dtype, header=0, engine='python')

points = read_points('small_house.txt')
# print(points[['x', 'y', 'z', 'deviation', 'amplitude', 'reflectance', 'r', 'g', 'b']])
v = pptk.viewer(points[['x', 'y', 'z']])
v.attributes(points[['r', 'g', 'b']] / 255.)
v.set(point_size=0.001)

