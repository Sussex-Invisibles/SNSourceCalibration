import matplotlib.pyplot as plt
import csv
import sys
import os
import numpy as np

fileArray = []

for i in range(1,len(sys.argv)):
    fileArray.append(sys.argv[i])

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

plt.legend(loc="lower right")
plt.show()

