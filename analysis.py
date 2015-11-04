import root_utils
import calc_utils
import ROOT
import matplotlib.pyplot as plt
output = ROOT.TFile("test.root","recreate")
x,y = calc_utils.readTRCFiles("data")
plt.plot(x,y[0])
plt.show()

histo, area, areaErr = root_utils.plot_area(x,y,"test")
histo.Write()
print "Area : "+str(area)
print "Area Error : "+str(areaErr)
output.Close()
