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



fileArray = ["Idlesweep5_5GSs_0offset_Nov.18_GOOD/NDF 3/dataset/areas.txt","Idlesweep5_5GSs_0offset_Nov.18_GOOD/NDF 2.5/dataset/areas.txt","Idlesweep5_5GSs_0offset_Nov.18_GOOD/NDF2/dataset/areas.txt","Idlesweep5_5GSs_0offset_Nov.18_GOOD/NDF 1.5/dataset/areas.txt","Idlesweep5_5GSs_0offset_Nov.18_GOOD/NDF 1/dataset/areas.txt"]
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
totYValsScaled = []
totXValsScaled = []
totYErrScaled = []
totXVals = []
totYVals = []
totYErr = []

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
#doing scaling
for iteration in range(len(fileArray)):
    if iteration == 0:
        xValSliced = []
        yValSliced = []
        yErrSliced = []
        for i in range(len(totXVals[iteration])):
            if totXVals[iteration][i] > xCutArray[iteration]:
                xValSliced = totXVals[iteration][:i]
                yValSliced = totYVals[iteration][:i]
                yErrSliced = totYErr[iteration][:i]
                break
        totXValsScaled.append(xValSliced)
        yScaled = scaleFunction(yValSliced,NDF3Offset,NDF3Scale)
        yErrScaled = scaleFunction(yErrSliced,NDF3Offset,NDF3Scale)
        totYValsScaled.append(yScaled)
        totYErrScaled.append(yErrScaled)

    else:
        xValSliced = []
        yValSliced = []
        yErrSliced = []
        for i in range(len(totXVals[iteration])):
            if totXVals[iteration][i] > xCutArray[iteration]:
                xValSliced = totXVals[iteration][:i]
                yValSliced = totYVals[iteration][:i]
                yErrSliced = totYErr[iteration][:i]
                break
        totXValsScaled.append(xValSliced)
        #minim = minimize(getChiSquared,(0,NDFArray[iteration]),args=(yValSliced,totYValsScaled[0][:len(yValSliced)]),method= "TNC",bounds=[(None,None),(0,3)], options={'maxiter':10000,"maxfun":10000})
        minim = fmin(getChiSquared,(0,NDFArray[iteration]),args=(yValSliced,totYValsScaled[0][:len(yValSliced)]), maxiter=10000,maxfun=10000)

        offsetNDFValue = minim
        yScaled = scaleFunction(yValSliced,offsetNDFValue[0],offsetNDFValue[1])
        yErrScaled = scaleFunction(yErrSliced,offsetNDFValue[0],offsetNDFValue[1])
        totYValsScaled.append(yScaled)
        totYErrScaled.append(yErrScaled)
        print "The fitted NDF Value is: "+str(offsetNDFValue[1])
        print "The y offset is: "+str(offsetNDFValue[0])
        fitNDFs.append(offsetNDFValue[1])
        



for iteration in range(len(fileArray)):
    print fileArray[iteration]
    print os.path.basename(fileArray[iteration])
    with open(os.path.split(fileArray[iteration])[0]+"SCALEDDATA"+os.path.basename(fileArray[iteration]),"w") as outputFile:
        for scaledVals in range(len(totXValsScaled[iteration])):
            outputFile.write(str(totXValsScaled[iteration][scaledVals])+" "+str(totYValsScaled[iteration][scaledVals])+" "+str(totYErrScaled[iteration][scaledVals])+"\n")
        outputFile.close()
    plt.figure(0)
    plt.plot(totXValsScaled[iteration],np.multiply(totYValsScaled[iteration],-1),label=str((labelArray[iteration])))

plt.figure(0)
plt.legend(loc="lower right")
plt.figure(1)
plt.xlabel("NDF Values")
plt.ylabel("Fitted NDF Values")
print fitNDFs
plt.plot(NDFArray,fitNDFs)
plt.show()

