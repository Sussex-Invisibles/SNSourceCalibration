import matplotlib.pyplot as plt
import csv
import sys
import os
import numpy as np
import ROOT
from scipy.optimize import curve_fit
import calc_utils

def linear_func(x, m, c):
    return m*x+c

fileArray = []
labelArray = []
scaleArray = []
scaleArray.append(number_for_firstNDF)
scaleArray.append(number_for_secondNDF)
scaleArray.append(number_for_thirdNDF)
labelArray.append("First Name here")
labelArray.append("Second name here")
labelArray.append(" and so on")
doFit = []
lowFitLimits = []
upFitLimits = []
dataPlot = plt.figure(0)
errorPlot = plt.figure(1)
afterFit = False
afterFitNum  = 999999999 
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
totYVals = []
totXVals = []
totYErr = []
fitCounter = 0
for iteration in range(len(fileArray)):
    inputFile = open(fileArray[iteration],"r")
    print inputFile
    xVals = []
    yVals = []
    yErrs = []
    read = csv.reader(inputFile,delimiter=" ")
    for row in read:
        xVals.append( float(row[0]))
        yVals.append( float(row[1]))
        yErrs.append( float(row[2]))
    totYVals.append(yVals)
    totXVals.append(xVals)
    totYErr.append(yErrs)

for iteration in range(len(fileArray)):
    print fileArray[iteration]
    print os.path.basename(fileArray[iteration])
    print totYVals[iteration]
    plt.figure(0)
    plt.errorbar(totXVals[iteration],np.multiply(totYVals[iteration],-1*scaleArray[iteration]),yerr=totYErr[iteration],label=str((labelArray[iteration])))
    negyVals = np.multiply(totYVals[iteration],-1.0)
    #print np.divide(yErrs,yVals)
    plt.figure(1)
    plt.plot(totXVals[iteration],np.divide(totYErr[iteration],negyVals),label="Error over area: "+str(labelArray[iteration]))
    if doFit[iteration]:
        plt.figure(0)
        fitWeights = []
        for iError in range(len(yErrs)):
            fitWeights.append(1.0/(yErrs[iError]))
        lowIndex = 0
        upIndex = 0
        
        for i in range(len(xVals)):
            if totXVals[iteration][i] > lowFitLimits[fitCounter]:
                lowIndex = i 
                break
        
        for i in range(len(xVals)-1,0,-1):
            if totXVals[iteration][i] < upFitLimits[fitCounter]:
                upIndex = i+1
                break
       
        fitCounter += 1
        fitResults = np.polyfit(totXVals[iteration][lowIndex:upIndex],np.multiply(yVals[lowIndex:upIndex],-1.0),2,w=fitWeights[lowIndex:upIndex],full=True)
        fitValues = fitResults[0]
        chi_squared = fitResults[1]
        poly = np.poly1d(fitValues)
        plt.plot(totXVals[iteration][lowIndex:upIndex],poly(totXVals[iteration][lowIndex:upIndex]),label="Fit to: "+(labelArray[iteration]))
        reduced_chi_squared = chi_squared/(len(totXVals[iteration][lowIndex:upIndex])-len(fitValues))
        print "Parameters for fit to: "+str(os.path.basename(fileArray[iteration]))+"    "+str(fitValues)
        print "Number of Degrees of Freedom is: "+str(len(xVals[lowIndex:upIndex])-len(fitValues))
        print "chi squared is: "+str(chi_squared)
        print "Reduced chi squared is: "+str(reduced_chi_squared)
        print "Likelihood of fit for no aging is is: "+str(ROOT.TMath.Prob(chi_squared,len(xVals[lowIndex:upIndex])-len(fitValues)))

plt.figure(0)
plt.legend(loc="lower right")

