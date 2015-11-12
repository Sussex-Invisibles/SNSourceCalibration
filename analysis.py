import root_utils
import calc_utils
import os
import sys
import ROOT
import matplotlib.pyplot as plt
import numpy as np

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

dacValues = []
peakValues = []
peakErrors = []
FWHMValues = []
FWHMErrors = []
areaValues = []
areaErrors = []
topFolder = sys.argv[1]
os.chdir(topFolder)
items  =  os.listdir(".")
folders = []
for dacfolder in items:
    if os.path.isdir(dacfolder) and is_number(dacfolder):
        folders.append(dacfolder)

folders.sort(key=int)
print folders
for dacFolder in folders:
    print "THIS IS DAC FOLDER: "+str(dacFolder)
    x,y = calc_utils.readTRCFiles(dacFolder,False)
    output = ROOT.TFile(dacFolder+".root","recreate")
    areaHisto, area, areaErr = root_utils.plot_area(x,y,"area")
    widthHisto, width, widthErr = root_utils.plot_width(x,y,"FWHM")
    peakHisto, meanPeak, peakErr = root_utils.plot_peak(x,y,"peak")
    areaHisto.Write()
    widthHisto.Write()
    peakHisto.Write()
    output.Close()
    peakValues.append(meanPeak)
    peakErrors.append(peakErr)
    FWHMValues.append(width)
    FWHMErrors.append(widthErr)
    areaValues.append(area)
    areaErrors.append(areaErr)
    dacValues.append(float(dacFolder))


plt.figure(0)
plt.errorbar(dacValues,peakValues,yerr=peakErrors)
plt.title("dacValues vs peakValues")
plt.savefig("peaks.png")

plt.figure(1)
plt.errorbar(dacValues,FWHMValues,yerr=FWHMErrors)
plt.title("dacValues vs FWHMValues")
plt.savefig("FWHM.png")

plt.figure(2)
plt.errorbar(dacValues,areaValues,yerr=areaErrors)
fitWeights = []
for iError in range(len(areaErrors)):
    fitWeights.append(1.0/np.sqrt(areaErrors[iError]**2))
fitValues = np.polyfit(dacValues,areaValues,1,w=fitWeights)
poly = np.poly1d(fitValues)
plt.plot(dacValues,poly(dacValues))
plt.title("dacValues vs areaValues")
plt.savefig("area.png")

#print "Number of Photons: "+str(calc_utils.get_photons(area,0.5))
