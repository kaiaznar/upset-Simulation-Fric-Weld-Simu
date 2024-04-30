
#--------------------------------------------------------------------------
#  Moal and Massoni pipe inertia weld with remeshing
#  Axisymmetric model using axisymmetric twist element (CGAX4HT and CGAX3T)
#--------------------------------------------------------------------------

import os, sys, re, osutils
import driverUtils, sys
from driverConstants import *
from abaqusConstants import *
from driverExceptions import *
from driverStandard import StandardAnalysis
from analysis import AnalysisApplication
sys.path.append(os.getcwd())
from inertiaweld_utils import *
import uti

print "start inertiaweld.py"
platform = uti.getPlatform()

# Setup user subroutine file name

ftnSourceExt = ".f"
if platform == "win86_32" or platform == "win86_64":
   ftnSourceExt = ".for"
   osutils.copy( 'inertiaweld_sub.f','inertiaweld_sub.for', 1)
userSubFileName = "inertiaweld_sub" + ftnSourceExt
if not os.path.exists(userSubFileName):
   print "Error! User subroutine file '%s' is not in the current directory." % userSubFileName
   sys.exit(-1)

# define basic job parameters

execfile('inertiaweld_job_param.py')

# define initial solver parameters

execfile('inertiaweld_solver_param.py')

# define utility functions

execfile('inertiaweld_utils.py')

# Start from the beginning

logFile = openLogFile(primaryJobName)
writeHeading (logFile)
totalTime = 0.0
timeRemaining = simulationTime - totalTime

# Create the original analysis model

execfile('inertiaweld_original_build.py')

# Run the original analysis

#bad
#options = baseOptions
#options['job']   = primaryJobName
#options['input'] = primaryJobName
#options['user'] = userSubFileName 
#------------------------JOB RUN

cmd = []
cmd.append('-job')
cmd.append('%s' % primaryJobName )
cmd.append('-input')
cmd.append('%s' % primaryJobName )
cmd.append('-user')
cmd.append('%s' % userSubFileName )
cmd.append('-interactive')
sys.stdout = sys.__stdout__
job = AnalysisApplication(cmd)
try:
   job.run()
except:
   print "Oops..."

#analysis = StandardAnalysis(options)
#status = analysis.run()

writeModelInfo(logFile,primaryJobName,timeRemaining,0)

plotShape(primaryJobName)
totalTime = totalTime + elapsedTime(primaryJobName)
timeRemaining = simulationTime - totalTime
writeAnalysisInfo(logFile,primaryJobName,totalTime,timeRemaining)

# add U to odb for 2D plot

add_unew_odb(primaryJobName)

# Remesh, if necessary

remeshStart = 0
timeRemaining0 = timeRemaining

if timeRemaining >= 1.e-6:
    for remeshIndex in range(remeshStart,maxRemeshings):
	remeshNumber = remeshIndex + 1
	cleanupOldFiles(logFile,primaryJobName,remeshNumber)
	remeshJobName = newJobName(primaryJobName,remeshNumber)
	ancestorJobName = priorJobName(primaryJobName,remeshNumber)
	execfile('inertiaweld_remesh_build.py')
	writeModelInfo(logFile,remeshJobName,timeRemaining,remeshNumber)

        # bad
#         options = baseOptions
#         options['job']   = remeshJobName
#         options['input'] = remeshJobName
#         options['user'] = userSubFileName
#         options['rezone'] = ON
#         options['oldjob'] = ancestorJobName
        cmd = []
        cmd.append('-job')
        cmd.append('%s' % remeshJobName )
        cmd.append('-input')
        cmd.append('%s' % remeshJobName )
        cmd.append('-oldjob')
        cmd.append('%s' % ancestorJobName )
        cmd.append('-user')
        cmd.append('%s' % userSubFileName )
        cmd.append('-interactive')
        sys.stdout = sys.__stdout__
        remeshJob = AnalysisApplication(cmd)
        try:
           remeshJob.run()
        except:
           print "Ooops..."
#         remeshAnalysis = StandardAnalysis(options)
#         remeshAnalysis.run()
        plotShape(remeshJobName)
        totalTime = totalTime + elapsedTime(remeshJobName)
        timeRemaining = simulationTime - totalTime
	writeAnalysisInfo(logFile,remeshJobName,totalTime,timeRemaining)
        add_unew_odb(remeshJobName)
	if timeRemaining < 1.e-6:
	    break
# cleanup the last few files before exit
#-
Filename = primaryJobName + "_remesh_" + '%i' % remeshNumber
cleanupOldFiles(logFile,Filename,2)
remeshNumber=remeshNumber-1
Filename = primaryJobName + "_remesh_" + '%i' % remeshNumber
cleanupOldFiles(logFile,Filename,2)
#+
writeEnding(logFile)
print "Job completed successfully!"
sys.exit()
