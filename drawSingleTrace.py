import root_utils
import calc_utils
import os
import ROOT
import matplotlib.pyplot as plt
import numpy as np
x,y = calc_utils.readTRCFiles(os.path.join("dataset","40000"))
print x
ymean = np.mean(y,0)
print ymean
plt.plot(x,ymean)
plt.show()

