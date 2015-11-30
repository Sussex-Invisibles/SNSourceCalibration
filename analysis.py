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
areaFWHM = []
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
    areaHisto,photonHisto, area, areaErr,areaErrOnMean = root_utils.plot_area(x,y,"area",lower_limit=9.e-8,upper_limit=9.e-8)
    widthHisto, width, widthErr, widthErrOnMean = root_utils.plot_width(x,y,"FWHM")
    peakHisto, meanPeak, peakErr, peakErrOnMean = root_utils.plot_peak(x,y,"peak")
    #numSqrt = np.sqrt(len(os.listdir(dacFolder)))
    photonHisto.Write()
    areaHisto.Write()
    widthHisto.Write()
    peakHisto.Write()
    output.Close()
    peakValues.append(meanPeak)
    peakErrors.append(peakErrOnMean)
    FWHMValues.append(width)
    FWHMErrors.append(widthErrOnMean)
    areaValues.append(area)
    areaErrors.append(areaErrOnMean)
    print "Area MEAN is: "+str(area)
    print "Area RMS is: "+str(areaErr)
    areaFWHM.append(2*np.sqrt(2*np.log(2))*areaErr)
    dacValues.append(float(dacFolder))

areaFile = open("areas.txt","w")
peakFile = open("peaks.txt","w")
widthFile = open("FWHM.txt","w")

for i in range(len(areaValues)):
    areaLine = str(dacValues[i])+" "+str(areaValues[i])+" "+str(areaErrors[i])+" "+str(areaFWHM[i])+"\n"
    peakLine = str(dacValues[i])+" "+str(peakValues[i])+" "+str(peakErrors[i])+"\n"
    FWHMLine = str(dacValues[i])+" "+str(FWHMValues[i])+" "+str(FWHMErrors[i])+"\n"
    areaFile.write(areaLine)
    peakFile.write(peakLine)
    widthFile.write(FWHMLine)

areaFile.close()
peakFile.close()
widthFile.close()

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
