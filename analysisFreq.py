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

freqValues = []
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
for freqfolder in items:
    if os.path.isdir(freqfolder) and is_number(freqfolder[:-3]):
        print freqfolder[:-3]
        folders.append(freqfolder)

folders = sorted(folders,key=lambda x:int(x[:-2]))
print folders
for freqFolder in folders:
    print "THIS IS FREQ FOLDER: "+str(freqFolder)
    x,y = calc_utils.readTRCFiles(freqFolder,False)
    output = ROOT.TFile(freqFolder+".root","recreate")
    areaHisto, area, areaErr = root_utils.plot_area(x,y,"area")
    widthHisto, width, widthErr = root_utils.plot_width(x,y,"FWHM")
    peakHisto, meanPeak, peakErr = root_utils.plot_peak(x,y,"peak")
    numSqrt = np.sqrt(len(os.listdir(freqFolder)))
    areaHisto.Write()
    widthHisto.Write()
    peakHisto.Write()
    output.Close()
    peakValues.append(meanPeak)
    peakErrors.append(peakErr/numSqrt)
    FWHMValues.append(width)
    FWHMErrors.append(widthErr/numSqrt)
    areaValues.append(area)
    areaErrors.append(areaErr/numSqrt)
    freqValues.append(float(freqFolder[:-3]))

areaFile = open("areas.txt","w")
peakFile = open("peaks.txt","w")
widthFile = open("FWHM.txt","w")

for i in range(len(areaValues)):
    areaLine = str(freqValues[i])+" "+str(areaValues[i])+" "+str(areaErrors[i])+"\n"
    peakLine = str(freqValues[i])+" "+str(peakValues[i])+" "+str(peakErrors[i])+"\n"
    FWHMLine = str(freqValues[i])+" "+str(FWHMValues[i])+" "+str(FWHMErrors[i])+"\n"
    areaFile.write(areaLine)
    peakFile.write(peakLine)
    widthFile.write(FWHMLine)

areaFile.close()
peakFile.close()
widthFile.close()

plt.figure(0)
plt.errorbar(freqValues,peakValues,yerr=peakErrors)
plt.title("freqValues vs peakValues")
plt.savefig("peaks.png")

plt.figure(1)
plt.errorbar(freqValues,FWHMValues,yerr=FWHMErrors)
plt.title("freqValues vs FWHMValues")
plt.savefig("FWHM.png")

plt.figure(2)
plt.errorbar(freqValues,areaValues,yerr=areaErrors)
fitWeights = []
#for iError in range(len(areaErrors)):
#    fitWeights.append(1.0/np.sqrt(areaErrors[iError]**2))
#fitValues = np.polyfit(freqValues,areaValues,1,w=fitWeights)
#poly = np.poly1d(fitValues)
#plt.plot(freqValues,poly(freqValues))
plt.title("freqValues vs areaValues")
plt.xscale("log")
plt.savefig("area.png") 
#print "Number of Photons: "+str(calc_utils.get_photons(area,0.5))
