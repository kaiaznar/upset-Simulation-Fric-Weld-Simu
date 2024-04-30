# make animation avi from multiple odb files with the same base name

from abaqus import *
from abaqusConstants import *
import odbAccess
import animation
import annotationToolset
from odbAccess import *
from caeModules import *
from driverUtils import executeOnCaeStartup
executeOnCaeStartup()


baseName = "inertia_weld"
#baseName = getInput('basename')
session.imageAnimationOptions.setValues(vpDecorations=OFF, timeScale=1, frameRate=30)
m=session.imageAnimation()
if m!=None :
  m.close()
movie = session.ImageAnimation(fileName=baseName+"_animation", format=AVI)
viewport = session.viewports['Viewport: 1']
viewport.makeCurrent()
viewport.restore()
viewport.setValues(origin=(0.0, -101.821662902832), 
              width=214.481246948242, height=209.527496337891)
remeshNumber = 0
totalTime = 0.0
cont = True
while cont:
  if remeshNumber == 0:
    fileName = baseName + ".odb"
  else:
    fileName = baseName + "_remesh_" + "%i" % (remeshNumber) + ".odb"
  try:
    odb = session.openOdb(name=fileName)
    viewport.setValues(displayedObject=odb)
    viewport.odbDisplay.display.setValues(plotState=(CONTOURS_ON_DEF, ))
    viewport.odbDisplay.setPrimaryVariable(
      variableLabel='NT11', outputPosition=NODAL)
    viewport.odbDisplay.contourOptions.setValues(
      maxAutoCompute=OFF, maxValue=1300, minAutoCompute=OFF, minValue=0)
    viewport.view.setValues(cameraPosition=(45.8176,-0.182533, 180.4),
                            cameraTarget=(45.8176, -0.182533, 0))
    viewport.viewportAnnotationOptions.setValues(triad=OFF, 
                                                 title=OFF,
                                                 state=OFF,
                                                 statePosition=(50,99),
                                                 annotations=ON,
                                                 compass=OFF,
        legendFont='-*-verdana-medium-r-normal-*-*-100-*-*-p-*-*-*')
    countName = "Remesh counter: " + "%2i" % (remeshNumber) 
    countText = odb.userData.Text(name='remeshCount', text=countName,
                                                     offset=(145.0, 165.0))
    odb.userData.annotations['remeshCount'].setValues(font='-*-arial-medium-r-normal-*-*-140-*-*-p-*-*-*')
    viewport.plotAnnotation(annotation=countText)
    step = odb.steps['Weld step']
    frameCount = 0
    for frame in step.frames:
      frameCount = frameCount + 1
      stepTime = frame.frameValue
      timeName = "Time: " + "%5.2f" % (totalTime + stepTime) + "s"
      timeText = odb.userData.Text(name='timeText', text=timeName,
                                                      offset=(170.0, 170.0))
      odb.userData.annotations['timeText'].setValues(font='-*-arial-medium-r-normal-*-*-140-*-*-p-*-*-*')
      viewport.plotAnnotation(annotation=timeText)
      viewport.odbDisplay.setFrame(frame)
      try:
        viewport.odbDisplay.setDeformedVariable(variableLabel='UNEW')
      except:
        print "You must have UNEW created in odb ",fileName
      #Write all but the final frame, which is redundant with frame 0 of the next job
      if frameCount != len(step.frames):
        try:
          movie.writeFrame()
        except:
          pass
    remeshNumber = remeshNumber + 1
    totalTime = totalTime + stepTime
    session.odbs[fileName].close()
  except:
    cont = False
movie.close()
sys.exit()
