import matplotlib.pyplot as plt
import csv
import sys
import os
import numpy as np
import ROOT
from scipy.optimize import minimize 
from scipy.optimize import fmin
import calc_utils

def scaleFunction(data,offset,NDFValue):
    scaledData = []
    for dataPoint in data:
        scaledData.append((dataPoint-offset)*(10**np.fabs(NDFValue)))
    return scaledData

#data : Data we are trying to find the parameters for
#scaledFitData : data which has been scaled and we are trying to fit to
#offset 
def getChiSquared(offsetNDFValue,data,scaledFitData):
    scaledTestData = scaleFunction(data,offsetNDFValue[0],offsetNDFValue[1])
#evaluating chi squared
    chi_squared = 0
    for i in range(len(data)):
        chi_squared += (scaledFitData[i]-scaledTestData[i])**2
    return chi_squared*1e9


NDF3Offset = 1e-6 
NDF3Scale = 3.



fileArray = []
labelArray = []
xCutArray = [27000,25000,22000,15000,8000]
NDFArray = [3,2.5,2,1.5,1.0]
fitNDFs = [3]
labelArray.append("NDF3")
labelArray.append("NDF2.5")
labelArray.append("NDF2")
labelArray.append("NDF1.5")
labelArray.append("NDF1")
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

totYValsScaled = []
totXValsScaled = []
#doing scaling
for iteration in range(len(fileArray)):
    if iteration == 0:
        xValSliced = []
        yValSliced = []
        for i in range(len(totXVals[iteration])):
            if totXVals[iteration][i] > xCutArray[iteration]:
                xValSliced = totXVals[iteration][:i]
                yValSliced = totYVals[iteration][:i]
                break
        totXValsScaled.append(xValSliced)
        yScaled = scaleFunction(yValSliced,NDF3Offset,NDF3Scale)
        print yValSliced
        print yScaled
        totYValsScaled.append(yScaled)

    else:
        xValSliced = []
        yValSliced = []
        for i in range(len(totXVals[iteration])):
            if totXVals[iteration][i] > xCutArray[iteration]:
                xValSliced = totXVals[iteration][:i]
                yValSliced = totYVals[iteration][:i]
                break
        print xValSliced
        totXValsScaled.append(xValSliced)
        #minim = minimize(getChiSquared,(0,NDFArray[iteration]),args=(yValSliced,totYValsScaled[0][:len(yValSliced)]),method= "TNC",bounds=[(None,None),(0,3)], options={'maxiter':10000,"maxfun":10000})
        minim = fmin(getChiSquared,(0,NDFArray[iteration]),args=(yValSliced,totYValsScaled[0][:len(yValSliced)]), maxiter=10000,maxfun=10000)

        print minim
        offsetNDFValue = minim
        yScaled = scaleFunction(yValSliced,offsetNDFValue[0],offsetNDFValue[1])
        totYValsScaled.append(yScaled)
        fitNDFs.append(offsetNDFValue[1])
        



for iteration in range(len(fileArray)):
    print fileArray[iteration]
    print os.path.basename(fileArray[iteration])
    plt.figure(0)
    plt.plot(totXValsScaled[iteration],np.multiply(totYValsScaled[iteration],-1),label=str((labelArray[iteration])))
    negyValsScaled = np.multiply(totYValsScaled[iteration],-1.0)
    plt.figure(1)
    #print np.divide(yErrs,yVals)
    if doFit[iteration]:
        plt.figure(0)
        fitWeights = []
        for iError in range(len(yErrs)):
            fitWeights.append(1.0/(yErrs[iError]))
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
        fitResults = np.polyfit(xVals[lowIndex:upIndex],np.multiply(yVals[lowIndex:upIndex],-1.0),2,w=fitWeights[lowIndex:upIndex],full=True)
        fitValues = fitResults[0]
        chi_squared = fitResults[1]
        poly = np.poly1d(fitValues)
        plt.plot(xVals[lowIndex:upIndex],poly(xVals[lowIndex:upIndex]),label="Fit to: "+(labelArray[iteration]))
        reduced_chi_squared = chi_squared/(len(xVals[lowIndex:upIndex])-len(fitValues))
        print "Parameters for fit to: "+str(os.path.basename(fileArray[iteration]))+"    "+str(fitValues)
        print "Number of Degrees of Freedom is: "+str(len(xVals[lowIndex:upIndex])-len(fitValues))
        print "chi squared is: "+str(chi_squared)
        print "Reduced chi squared is: "+str(reduced_chi_squared)
        print "Likelihood of fit for no aging is is: "+str(ROOT.TMath.Prob(chi_squared,len(xVals[lowIndex:upIndex])-len(fitValues)))

plt.figure(0)
plt.legend(loc="lower right")
plt.figure(1)
print fitNDFs
plt.plot(NDFArray,fitNDFs)
plt.show()

