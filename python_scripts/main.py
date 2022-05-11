# script: Zemax zos api and pythonnet interface
# created: 7 May 2022, 5/7/2022 11:40:06 PM
# author: abhi sukumari

# NOTES & CAUTIONS:
# Zemax parameter Radius of Curvature ROC is represented as Curvature in tolerancing operands; c = 1/r

# SCM cheats:
# forking from github→Bitbucket: http://stackoverflow.com/questions/8137997/forking-from-github-to-bitbucket



# python library imports
import matplotlib.pyplot as plt, numpy as np, pandas as pd  # Python visualization and numerical analysis
import os, sys, winreg
from pip import main  # Access zemax opticstudio win registry
from pythonStandaloneAppClass import PythonStandaloneApplication

if __name__ == '__main__':
    zos = PythonStandaloneApplication()  # create object instance

    # use http://matplotlib.org/ to plot line graph
    # need to install this package before running this code

    # load local variables
    ZOSAPI = zos.ZOSAPI
    TheApplication = zos.TheApplication
    TheSystem = zos.TheSystem
    sampleDir = TheApplication.SamplesDir

    # ! [e04s01_py]
    # Open file
    testFile = sampleDir + '\\Sequential\\Objectives\\Cooke 40 degree field.zos'
    TheSystem.LoadFile(testFile, False)
    # ! [e04s01_py]

    # ! [e04s02_py]
    # Create analysis
    TheAnalyses = TheSystem.Analyses
    newWin = TheAnalyses.New_FftMtf()
    # insert next analysis method (TDE)
    
    # ! [e04s02_py]

    # ! [e04s03_py]
    # Settings
    newWin_Settings = newWin.GetSettings()
    newWin_Settings.MaximumFrequency = 50
    newWin_Settings.SampleSize = ZOSAPI.Analysis.SampleSizes.S_256x256
    # ! [e04s03_py]

    # ! [e04s04_py]
    # Run Analysis
    newWin.ApplyAndWaitForCompletion()
    # Get Analysis Results
    newWin_Results = newWin.GetResults()
    # ! [e04s04_py]

    # ! [e04s05_py]
    # Read and plot data series
    # NOTE: numpy functions are used to unpack and plot the 2D tuple for Sagittal & Tangential MTF
    # You will need to import the numpy module to get this part of the code to work
    colors = ('b', 'g', 'r', 'c', 'm', 'y', 'k')
    for seriesNum in range(0, newWin_Results.NumberOfDataSeries, 1):
        data = newWin_Results.GetDataSeries(seriesNum)

        # get raw .NET data into numpy array
        xRaw = data.XData.Data
        yRaw = data.YData.Data

        x = list(xRaw)
        y = zos.reshape(yRaw, yRaw.GetLength(0), yRaw.GetLength(1), True)

        plt.plot(x, y[0], color=colors[seriesNum])
        plt.plot(x, y[1], linestyle='--', color=colors[seriesNum])
        # ! [e04s05_py]

    # If you want to use numpy, you can replace the last 4 commands in the for loop with:
    #     x = np.array(tuple(xRaw))
    #     y = np.array(np.asarray(tuple(yRaw)).reshape(data.YData.Data.GetLength(0), data.YData.Data.GetLength(1)))
    #    
    #     plt.plot(x[:],y[:,0],color=colors[seriesNum])
    #     plt.plot(x[:],y[:,1],linestyle='--',color=colors[seriesNum])

    # format the plot
    plt.title('FFT MTF: ' + os.path.basename(testFile))
    plt.xlabel('Spatial Frequency in cycles per mm')
    plt.ylabel('Modulus of the OTF')
    plt.legend([r'$0^\circ$ tangential', r'$0^\circ$ sagittal', r'$14^\circ$ tangential', r'$14^\circ$ sagittal',
                r'$20^\circ$ tangential', r'$20^\circ$ sagittal'])
    plt.grid(True)

    # This will clean up the connection to OpticStudio.
    # Note that it closes down the server instance of OpticStudio, so you for maximum performance do not do
    # this until you need to.
    del zos
    zos = None

    # place plt.show() after clean up to release OpticStudio from memory
    plt.show()
