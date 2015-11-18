import os
import sys
import ROOT
import matplotlib.pyplot as plt
import numpy as np
import readTrc
folder =(sys.argv[1])
x = []
y = []
first = True
for trcFile in os.listdir(folder):
   xSin, ySin, m = readTrc.readTrc(os.path.join(folder,trcFile))
   if first:
       print(m)
       first = False
   x = xSin
   y.append(ySin)
histo = ROOT.TH1D("amp histo","amp histo",100,-0.05,0.05)
areaHisto = ROOT.TH1D("area histo","area histo",100,-2,2)
output = ROOT.TFile("amplitudeHisto.root","recreate")
ymean = np.mean(y,0)
print(ymean)
for i in range(len(y)):
    plt.plot(x,y[i])
    areaHisto.Fill(np.trapz(y[i],np.multiply(x,1e9)))
for i in range(len(y)):
    for j in range(len(x)):
        histo.Fill(y[i][j])
plt.show()
plt.figure(1)
plt.plot(x,ymean)
plt.show()
print ("MEAN VALUE IS: "+str(np.mean(ymean)))
histo.Write()
areaHisto.Write()
output.Close()
