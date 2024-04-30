# create remeshed model and restart input file


import os, sys
sys.path.append(os.getcwd())
from inertiaweld_utils import *

vp1 = session.Viewport(name='Viewport: 1')
vp1.makeCurrent()
session.viewports['Viewport: 1'].maximize()


Mdb()
#ancestorJobName = primaryJobName
openMdb(primaryJobName + '.cae')
mdb.saveAs(remeshJobName + '.cae')
openMdb(remeshJobName + '.cae')


model=mdb.models['Model-1']
a = model.rootAssembly
try:
    a.deleteFeatures(('Datum plane-2', 'Partition face-2', ))
    a.deleteFeatures(('Datum plane-1', 'Partition face-1', ))
except:
    pass
a.regenerate()


# Replace the pipes with the deformed configuration outlines

updateGeometry('bottomPipe_weld','BOTTOMPIPE_WELD-1',ancestorJobName + '.odb',remeshFeatureAngle)
updateGeometry('topPipe_weld',   'TOPPIPE_WELD-1',   ancestorJobName + '.odb',remeshFeatureAngle)
p = model.parts['bottomPipe_weld']
p.ReferencePoint(point=(0.0, -21.0, 0.0))
p = model.parts['topPipe_weld']
p.ReferencePoint(point=(0.0, 21.0, 0.0))
from part import *
from assembly import *
a = model.rootAssembly
a.backup()
a.regenerate()


# Re-establish attributes


# materials

from caeModules import *
p = model.parts['bottomPipe_weld']
f = p.faces
faces = f.getSequenceFromMask(mask=('[#1 ]', ), )
region = regionToolset.Region(faces=faces)
p = model.parts['bottomPipe_weld']
p.SectionAssignment(region=region, sectionName='pipe material', offset=0.0)
p = model.parts['topPipe_weld']
session.viewports['Viewport: 1'].setValues(displayedObject=p)
p = model.parts['topPipe_weld']
f = p.faces
faces = f.getSequenceFromMask(mask=('[#1 ]', ), )
region = regionToolset.Region(faces=faces)
p = model.parts['topPipe_weld']
p.SectionAssignment(region=region, sectionName='pipe material', offset=0.0)

# sets
from assembly import *
lowestEdgeSet(model.rootAssembly,'bottomPipe_weld-1','bottomAttachment')
highestEdgeSet('topPipe_weld-1','topAttachment')
refSet('topPipe_weld-1','topFlywheelAttachment')
refSet('bottomPipe_weld-1','bottomFlywheelAttachment')

# surfaces
highestSurface('topPipe_weld-1','pressureSurface')
perimeterSurface('topPipe_weld-1','topWeldSurface')
perimeterSurface('bottomPipe_weld-1','bottomWeldSurface')


# Redefine the step


from step import *
model.steps['Weld step'].setValues( 
    description='Weld step', timePeriod=timeRemaining,
    maxInc=timeRemaining, initialInc=1.e-5, minInc=2e-08)
try:
    del model.predefinedFields['Predefined Field-1']
except:
    pass


# Remesh


# Apply partitions
#
# Find the lowest point on the top pipe
e = a.instances['topPipe_weld-1'].edges
v = a.instances['topPipe_weld-1'].vertices
upperCutPosition = 0
lowestLocation = 99999
for k in range(len(v)):
    ((x,y,z),) = v[k].pointOn
    if y < lowestLocation:
	lowestLocation = y
upperCutPosition = nearWeldZone+lowestLocation
upperCutPosition = sliceTopInstance('topPipe_weld-1',upperCutPosition)
#surfaceNearBottom('topPipe_weld-1','topWeldSurface',upperCutPosition - 0.001)

# Find the highest point on the lower pipe

e = a.instances['bottomPipe_weld-1'].edges
v = a.instances['bottomPipe_weld-1'].vertices
highestLocation = -99999
for k in range(len(v)):
    ((x,y,z),) = v[k].pointOn
    if y > highestLocation:
	highestLocation = y
lowerCutPosition = highestLocation-nearWeldZone
lowerCutPosition = sliceBottomInstance('bottomPipe_weld-1',lowerCutPosition)
#surfaceNearTop('bottomPipe_weld-1','bottomWeldSurface',lowerCutPosition + 0.001)

removeEdgeSeeds('topPipe_weld-1')
removeEdgeSeeds('bottomPipe_weld-1')
seedNearZero('topPipe_weld-1',nearWeldMeshSize,(0.25*nearWeldZone) + upperCutPosition)
seedNearZero('bottomPipe_weld-1',nearWeldMeshSize,abs(lowerCutPosition - (0.25*nearWeldZone)))

a = model.rootAssembly
f1 = a.instances['topPipe_weld-1'].faces
faces1 = f1.getSequenceFromMask(mask=('[#1 ]', ), )
f2 = a.instances['bottomPipe_weld-1'].faces
faces2 = f2.getSequenceFromMask(mask=('[#1 ]', ), )
pickedRegions = faces1+faces2
a.setMeshControls(regions=pickedRegions, elemShape=QUAD, technique=FREE, 
    allowMapped=True)
partInstances =(a.instances['topPipe_weld-1'], 
    a.instances['bottomPipe_weld-1'], )
a.generateMesh(regions=partInstances)

##
## Add additional keywords
##

import job
from job import *
model.keywordBlock.synchVersions()
model.keywordBlock.setValues(edited = 0)
model.keywordBlock.synchVersions()
modelBlock = whereIsLastBlock("*Step") - 1
model.keywordBlock.insert(modelBlock, """*map solution""")
historyBlock = whereIsLastBlock("*End Step") - 1
model.keywordBlock.insert(historyBlock, """*controls,analysis=discontinuous""")
model.keywordBlock.insert(historyBlock, """,,,8.26e5""")
model.keywordBlock.insert(historyBlock, """*controls,parameters=field,field=rotation""")
model.keywordBlock.insert(historyBlock, """*contact controls,frictiononset=delayed,automatictolerances""")
mdb.models['Model-1'].setValues(noPartsInputFile=OFF)
mdb.jobs.changeKey(fromName=primaryJobName, toName=remeshJobName)
mdb.jobs[remeshJobName].writeInput()
mdb.save()
