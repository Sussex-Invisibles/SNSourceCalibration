import matplotlib.pyplot as plt
import csv
import sys
import os
import numpy as np
import ROOT

fileArray = []
doFit = []
lowFitLimits = []
upFitLimits = []
afterFit = False
afterFitNum  = 0
for i in range(1,len(sys.argv)):
        if sys.argv[i] == "fit":
            afterFit = True
            afterFitNum = i+1
            break
        fileArray.append(sys.argv[i])
        doFit.append(False)

for i in range(afterFitNum,len(sys.argv),3):
        fileArray.append(sys.argv[i])
        doFit.append(True)
        lowFitLimits.append(float(sys.argv[i+1]))
        upFitLimits.append(float(sys.argv[i+2]))

fitCounter = 0
for textFile in fileArray:
    inputFile = open(textFile,"r")
    xVals = []
    yVals = []
    yErrs = []
    read = csv.reader(inputFile,delimiter=" ")
    for row in read:
        xVals.append( float(row[0]))
        yVals.append( float(row[1]))
        yErrs.append( float(row[2]))
    print textFile
    print os.path.basename(textFile)
    plt.errorbar(xVals,np.fabs(yVals),yerr=yErrs,label=str(os.path.basename(textFile)))
    if doFit:
        fitWeights = []
        for iError in range(len(yErrs)):
            fitWeights.append(1.0/(yErrs[iError]**2))
        lowIndex = 0
        upIndex = 0
        
        for i in range(len(xVals)):
            if xVals[i] > lowFitLimits[fitCounter]:
                lowIndex = i 
                break
        
        for i in range(len(xVals)-1,0,-1):
            if xVals[i] < upFitLimits[fitCounter]:
                upIndex = i+1
                break
        fitCounter += 1
       
        fitValues = np.polyfit(xVals[lowIndex:upIndex],np.fabs(yVals[lowIndex:upIndex]),1,w=fitWeights[lowIndex:upIndex])
        poly = np.poly1d(fitValues)
        plt.plot(xVals[lowIndex:upIndex],poly(xVals[lowIndex:upIndex]),label="Fit to: "+os.path.basename(textFile))
        chi_squared = np.sum(((np.polyval(poly, xVals[lowIndex:upIndex]) - np.fabs(yVals[lowIndex:upIndex])) ** 2)/fitWeights[lowIndex:upIndex])
        reduced_chi_squared = chi_squared/(len(xVals[lowIndex:upIndex])-len(fitValues))
        print "Parameters for fit to: "+str(os.path.basename(textFile))+"    "+str(fitValues)
        print "Number of Degrees of Freedom is: "+str(len(xVals[lowIndex:upIndex])-len(fitValues))
        print "Reduced chi squared is: "+str(reduced_chi_squared)
        print "Likelihood of fit for no aging is is: "+str(ROOT.TMath.Prob(chi_squared,len(xVals[lowIndex:upIndex])-len(fitValues)))

plt.legend(loc="lower right")
plt.show()

