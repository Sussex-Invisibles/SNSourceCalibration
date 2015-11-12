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


def analyseVariousNDFs(topFolder):
    os.chdir(topFolder)
    ndfItems  =  os.listdir(".")
    NDFVals = []
    print topFolder
    for ndfItem in ndfItems:
        if os.path.isdir(os.path.join(os.getcwd(),ndfItem)):
            NDFVals.append(ndfItem)
    dacValuesVarious = []
    peaks = []
    peaksErrors = []
    widths =[]
    widthsErrors = []
    areas = []
    areasErrors = []
    for ndfFolder in NDFVals:
        folders = []
        ndfPath = os.path.join(os.getcwd(),ndfFolder)
        items = os.listdir(ndfPath)
        for dacfolder in items:
            if os.path.isdir(os.path.join(ndfPath,dacfolder)) and is_number(dacfolder):
                folders.append(dacfolder)
        dacValues = []
        peakValues = []
        peakErrors = []
        FWHMValues = []
        FWHMErrors = []
        areaValues = []
        areaErrors = []
        folders.sort(key=int)
        for dacFolder in folders:
            print "THIS IS DAC FOLDER: "+str(dacFolder)
            x,y = calc_utils.readTRCFiles(os.path.join(ndfPath,dacFolder),False)
            areaHisto, area, areaErr = root_utils.plot_area(x,y,"area")
            widthHisto, width, widthErr = root_utils.plot_width(x,y,"FWHM")
            peakHisto, meanPeak, peakErr = root_utils.plot_peak(x,y,"peak")
            peakValues.append(meanPeak)
            peakErrors.append(peakErr)
            FWHMValues.append(width)
            FWHMErrors.append(widthErr)
            areaValues.append(area)
            areaErrors.append(areaErr)
            dacValues.append(float(dacFolder))
        dacValuesVarious.append(dacValues) 
        peaks.append(peakValues)
        peaksErrors.append(peakErrors)
        areas.append(areaValues)
        areasErrors.append(areaErrors)
    return NDFVals,dacValuesVarious,peaks,peaksErrors,areas,areasErrors

topFolder = sys.argv[1]
NDFVals,dacValues,peaks,peaksErrors,areas,areaErrors = analyseVariousNDFs(topFolder)
print "NOW MAKING PLOTS"
plt.figure(0)
for i in range(len(NDFVals)):
    plt.errorbar(dacValues[i],peaks[i],yerr=peaksErrors[i],label="DATA: "+str(NDFVals[i]))
plt.title("dacValues vs peakValues")
plt.legend()
plt.savefig("NDFpeaks.png")

plt.figure(1)
for i in range(len(NDFVals)):
    plt.errorbar(dacValues[i],np.fabs(areas[i]),yerr=areaErrors[i],label="DATA: "+str(NDFVals[i]))
    fitWeights = []
    for iError in range(len(areaErrors[i])):
        fitWeights.append(1.0/np.sqrt(areaErrors[i][iError]**2))
    fitValues = np.polyfit(dacValues[i],np.fabs(areas[i]),1,w=fitWeights)
    poly = np.poly1d(fitValues)
    plt.plot(dacValues[i],poly(dacValues[i]),label="Fit NDF  "+str(NDFVals[i]))
plt.title("dacValues vs areaValues")
plt.legend(loc="lower right")
plt.savefig("NDFarea.png")
