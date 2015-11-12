import root_utils
import calc_utils
import os
import sys
import ROOT
import matplotlib.pyplot as plt
import numpy as np
x,y = calc_utils.readTRCFiles(os.path.join(sys.argv[1]),correct_offset=False)
ymean = np.mean(y,0)
for i in  range(len(x)):
    print str(x[i])+"    "+str(y[0][i])
plt.plot(x,ymean)
plt.show()

