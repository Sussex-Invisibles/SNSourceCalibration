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

    print NDFVals
    dacValuesVarious = []
    peaks = []
    peaksErrors = []
    widths =[]
    widthsErrors = []
    areas = []
    areasErrors = []
    for ndfFolder in NDFVals:
        folders = []
        ndfPath = os.path.join(os.getcwd(),ndfFolder,"dataset")
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
            #numSqrt = np.sqrt(len(os.listdir(os.path.join(ndfPath,dacFolder))))
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

plt.figure(1)
for i in range(len(NDFVals)):
    peakOutput = open(str(NDFVals[i])+"peak.txt","w")
    areaOutput = open(str(NDFVals[i])+"area.txt","w")
    for j in range(len(dacValues[i])):
        arealine = str(dacValues[i][j])+" "+str(areas[i][j])+" "+str(areaErrors[i][j])+"\n"
        peakline = str(dacValues[i][j])+" "+str(peaks[i][j])+" "+str(peaksErrors[i][j])+"\n"
        peakOutput.write(peakline)
        areaOutput.write(arealine)
    peakOutput.close()
    areaOutput.close()
    plt.errorbar(dacValues[i],np.fabs(areas[i]),yerr=areaErrors[i],label="DATA: "+str(NDFVals[i]))
    fitWeights = []
    for iError in range(len(areaErrors[i])):
        fitWeights.append(1.0/np.sqrt(areaErrors[i][iError]**2))
        lower_index = 0
        upper_index = 0
        for index in range(len(dacValues[i])):
            if dacValues[i][index]>15000:
                lower_index = index
                break
        for index in range(len(dacValues[i])-1,0,-1):
            if dacValues[i][index]<22000:
                upper_index = index
                break
        xVals = dacValues[i][lower_index:upper_index]
        print xVals
        yVals = np.fabs(areas[i][lower_index:upper_index])
        print yVals
        weights = fitWeights[lower_index:upper_index]
        print weights
    fitValues = np.polyfit(xVals,yVals,1,w=weights)
    poly = np.poly1d(fitValues)
    plt.plot(dacValues[i],poly(dacValues[i]),label="Fit NDF  "+str(NDFVals[i]))
plt.title("dacValues vs areaValues")
plt.legend(loc="lower right")
plt.show()
plt.savefig("NDFarea.png")

plt.figure(0)
for i in range(len(NDFVals)):
    plt.errorbar(dacValues[i],peaks[i],yerr=peaksErrors[i],label="DATA: "+str(NDFVals[i]))
plt.title("dacValues vs peakValues")
plt.legend()
plt.show()
plt.savefig("NDFpeaks.png")
