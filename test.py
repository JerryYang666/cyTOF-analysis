# Copyright (c) 2023.
# -*-coding:utf-8 -*-
"""
@file: test.py
@author: Jerry(Ruihuang)Yang
@email: rxy216@case.edu
@time: 5/4/23 23:59
"""
import numpy as np
import matplotlib.pyplot as plt
data = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
d = np.array(data)
heatmap = plt.imshow(d, cmap='gist_earth_r', vmin=0, vmax=10)
plt.colorbar(heatmap)
plt.show()
