import root_utils
import calc_utils
import os
import ROOT
import matplotlib.pyplot as plt
import numpy as np
x,y = calc_utils.readTRCFiles(os.path.join("dataset","4000"),correct_offset=True)
ymean = np.mean(y,0)
for i in  range(len(x)):
    print str(x[i])+"    "+str(y[0][i])
plt.plot(x,ymean)
plt.show()

