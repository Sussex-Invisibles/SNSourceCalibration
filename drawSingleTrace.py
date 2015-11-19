import root_utils
import calc_utils
import os
import sys
import ROOT
import matplotlib.pyplot as plt
import numpy as np
x,y = calc_utils.readTRCFiles(os.path.join(sys.argv[1]),correct_offset=False)
histo = ROOT.TH1D("amp histo","amp histo",100,-0.05,0.05)
output = ROOT.TFile("amplitudeHisto.root","recreate")
ymean = np.mean(y,0)
for i in  range(len(x)):
    print str(x[i])+"    "+str(y[0][i])
for i in range(len(y)):
    plt.plot(x,y[i])
for i in range(len(y)):
    for j in range(len(x)):
        histo.Fill(y[i][j])
plt.show()
plt.figure(1)
plt.plot(x,ymean)
plt.show()
print "MEAN VALUE IS: "+str(np.mean(ymean))
histo.Write()
output.Close()
