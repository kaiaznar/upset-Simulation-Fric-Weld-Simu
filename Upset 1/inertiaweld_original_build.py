# build initial CAE model and input file

from abaqus import *
from abaqusConstants import *
session.Viewport(name='Viewport: 1')
session.viewports['Viewport: 1'].makeCurrent()
session.viewports['Viewport: 1'].maximize()
from caeModules import *
from driverUtils import executeOnCaeStartup
executeOnCaeStartup()


#-------------------------GEOMETRY
#Upset 
s = mdb.models['Model-1'].ConstrainedSketch(name='__profile__',
    sheetSize=200.0)
g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints
s.sketchOptions.setValues(viewStyle=AXISYM)
s.setPrimaryObject(option=STANDALONE)
s.ConstructionLine(point1=(0.0, -100.0), point2=(0.0, 100.0))
s.FixedConstraint(entity=g[2])

s.Line(point1=(50.801,30.), point2=(50.801,100.0))
s.Line(point1=(50.801,100.0), point2=(63.5,100.0))
s.Line(point1=(63.5,100.0), point2=(59.83,30.0))
s.Line(point1=(59.83,30.0), point2=(50.801,30.0))

p = mdb.models['Model-1'].Part(name='topPipe_weld',
    dimensionality=AXISYMMETRIC, type=DEFORMABLE_BODY, twist=ON)
p = mdb.models['Model-1'].parts['topPipe_weld']
p.BaseShell(sketch=s)
s.unsetPrimaryObject()
p = mdb.models['Model-1'].parts['topPipe_weld']
p.ReferencePoint(point=(0.0, 21.0, 0.0))
session.viewports['Viewport: 1'].setValues(displayedObject=p)
del mdb.models['Model-1'].sketches['__profile__']

#Glove e pipe
s1 = mdb.models['Model-1'].ConstrainedSketch(name='__profile__',
    sheetSize=200.0)
g, v, d, c = s1.geometry, s1.vertices, s1.dimensions, s1.constraints
s1.sketchOptions.setValues(viewStyle=AXISYM)
s1.setPrimaryObject(option=STANDALONE)
s1.ConstructionLine(point1=(0.0, -100.0), point2=(0.0, 100.0))
s1.FixedConstraint(entity=g[2])

s1.Line(point1=(42.8,-30.0), point2=(42.8,100.0))
s1.Line(point1=(42.8,100.0), point2=(50.8,100.0))
s1.Line(point1=(50.8,100.0), point2=(50.8,30.0))
s1.Line(point1=(50.8,30.0), point2=(60.1, 30.0))
s1.Line(point1=(60.1,30.0), point2=(63.5,100.0))
s1.Line(point1=(63.5,100.0), point2=(68.5,100.0))
s1.Line(point1=(68.5,100.0), point2=(68.5,20.0))
s1.Line(point1=(68.5,20.0), point2=(55.3,20.0))
s1.Arc3Points(point1=(55.3,20.0), point2=(50.8,15.5), 
    point3=(53.98,16.82))
s1.Line(point1=(50.8,15.5), point2=(50.8,-30.0))
s1.Line(point1=(50.8,-30.0), point2=(42.8,-30.0))

p = mdb.models['Model-1'].Part(name='bottomPipe_weld',
    dimensionality=AXISYMMETRIC, type=DEFORMABLE_BODY, twist=ON)
p = mdb.models['Model-1'].parts['bottomPipe_weld']
p.BaseShell(sketch=s1)
s1.unsetPrimaryObject()
p = mdb.models['Model-1'].parts['bottomPipe_weld']
p.ReferencePoint(point=(0.0, -21.0, 0.0))
session.viewports['Viewport: 1'].setValues(displayedObject=p)
del mdb.models['Model-1'].sketches['__profile__']


#-------------------MATERIAL 
session.viewports['Viewport: 1'].partDisplay.setValues(sectionAssignments=ON,
    engineeringFeatures=ON)
mdb.models['Model-1'].Material(name='Material-1')
mdb.models['Model-1'].materials['Material-1'].Elastic(table=((1.0, 0.2), ))
mdb.models['Model-1'].Material('astroloy')
mdb.models['Model-1'].materials['astroloy'].Density(table=((7.8e-09, ), ))
mdb.models['Model-1'].materials['astroloy'].Conductivity(
    temperatureDependency=ON, table=((0.014854, 20), (0.01587, 100), (0.01714, 200), 
    (0.01841, 300), (0.01968, 400), (0.02095, 500), (0.02222, 600), (0.02349, 700), 
    (0.02476, 800), (0.02603, 900), (0.0273, 1000), (0.02857, 1100), (0.02984, 1200)))
	
#mdb.models['Model-1'].materials['astroloy'].InelasticHeatFraction()
mdb.models['Model-1'].materials['astroloy'].SpecificHeat(law=CONSTANTPRESSURE, 
    temperatureDependency=ON, table=((455.484672, 20), (475.224, 100), (495.432, 200), 
    (511.428, 300), (524.016, 400), (534, 500), (542.184, 600), (549.372, 700), 
    (556.368, 800), (563.976, 900), (573, 1000), (584.244, 1100), (598.512, 1200)))
mdb.models['Model-1'].materials['astroloy'].Expansion(table=((0.0, ), ))

mdb.models['Model-1'].materials['astroloy'].Elastic(
    temperatureDependency=ON, table=((190000, 0.3, 20), (182400, 0.3, 100), 
    (174800, 0.3, 200), (167200, 0.3, 300), (159600, 0.3, 400), (152000, 0.3, 500), 
    (144400, 0.3, 600), (134900, 0.3, 700), (119700, 0.3, 800), (85500, 0.3, 900), 
    (38000, 0.3, 1000), (19000, 0.3, 1100)))
	
mdb.models['Model-1'].materials['astroloy'].Plastic(temperatureDependency=ON, rate=ON, 
    table=((600.01,0.0,0.0,20),(597.18,0.0,0.0,25),(583.02,0.0,0.0,50),(568.86,0.0,0.0,75),
    (554.7,0.0,0.0,100),(540.54,0.0,0.0,125),(526.39,0.0,0.0,150),(512.23,0.0,0.0,175),
    (498.07,0.0,0.0,200),(483.91,0.0,0.0,225),(469.75,0.0,0.0,250),(455.59,0.0,0.0,275),
    (441.44,0.0,0.0,300),(427.28,0.0,0.0,325),(413.12,0.0,0.0,350),(398.96,0.0,0.0,375),
    (384.8,0.0,0.0,400),(370.65,0.0,0.0,425),(356.49,0.0,0.0,450),(342.33,0.0,0.0,475),
    (328.17,0.0,0.0,500),(314.01,0.0,0.0,525),(299.85,0.0,0.0,550),(285.7,0.0,0.0,575),
    (271.54,0.0,0.0,600),(257.38,0.0,0.0,625),(243.22,0.0,0.0,650),(229.06,0.0,0.0,675),
    (214.91,0.0,0.0,700),(200.75,0.0,0.0,725),(186.59,0.0,0.0,750),(172.43,0.0,0.0,775),
    (158.27,0.0,0.0,800),(144.11,0.0,0.0,825),(129.96,0.0,0.0,850),(115.8,0.0,0.0,875),
    (101.64,0.0,0.0,900),(87.48,0.0,0.0,925),(73.32,0.0,0.0,950),(59.17,0.0,0.0,975),
    (45.01,0.0,0.0,1000),(41.25,0.0,0.0,1025),(37.5,0.0,0.0,1050),(33.75,0.0,0.0,1075),
    (30,0.0,0.0,1100),(26.25,0.0,0.0,1125),(22.5,0.0,0.0,1150),(18.75,0.0,0.0,1175),
    (15,0.0,0.0,1200),(11.25,0.0,0.0,1225),(7.5,0.0,0.0,1250),(3.74,0.0,0.0,1275),
    (600.01,0.0,0.1,20),(597.18,0.0,0.1,25),(583.02,0.0,0.1,50),(568.86,0.0,0.1,75),
    (554.7,0.0,0.1,100),(540.54,0.0,0.1,125),(526.39,0.0,0.1,150),(512.23,0.0,0.1,175),
    (498.07,0.0,0.1,200),(483.91,0.0,0.1,225),(469.75,0.0,0.1,250),(455.59,0.0,0.1,275),
    (441.44,0.0,0.1,300),(427.28,0.0,0.1,325),(413.12,0.0,0.1,350),(398.96,0.0,0.1,375),
    (384.8,0.0,0.1,400),(370.65,0.0,0.1,425),(356.49,0.0,0.1,450),(342.33,0.0,0.1,475),
    (328.17,0.0,0.1,500),(314.01,0.0,0.1,525),(299.85,0.0,0.1,550),(285.7,0.0,0.1,575),
    (271.54,0.0,0.1,600),(257.38,0.0,0.1,625),(243.22,0.0,0.1,650),(229.06,0.0,0.1,675),
    (214.91,0.0,0.1,700),(200.75,0.0,0.1,725),(186.59,0.0,0.1,750),(172.43,0.0,0.1,775),
    (158.27,0.0,0.1,800),(144.11,0.0,0.1,825),(129.96,0.0,0.1,850),(115.8,0.0,0.1,875),
    (101.64,0.0,0.1,900),(87.48,0.0,0.1,925),(73.32,0.0,0.1,950),(59.17,0.0,0.1,975),
    (45.01,0.0,0.1,1000),(41.25,0.0,0.1,1025),(37.5,0.0,0.1,1050),(33.75,0.0,0.1,1075),
    (30,0.0,0.1,1100),(26.25,0.0,0.1,1125),(22.5,0.0,0.1,1150),(18.75,0.0,0.1,1175),
    (15,0.0,0.1,1200),(11.25,0.0,0.1,1225),(7.5,0.0,0.1,1250),(3.74,0.0,0.1,1275),
    (1e5, 0.0, 200, 20), (1e5, 0.0, 200, 1200),
    (1e8, 0.0, 1000, 20), (1e8, 0.0, 1000, 1200)))
mdb.models['Model-1'].HomogeneousSolidSection(name='pipe material',
    material='astroloy', thickness=1.0)


p = mdb.models['Model-1'].parts['bottomPipe_weld']
f = p.faces
faces = f.getSequenceFromMask(mask=('[#1 ]', ), )
region = regionToolset.Region(faces=faces)
p = mdb.models['Model-1'].parts['bottomPipe_weld']
p.SectionAssignment(region=region, sectionName='pipe material', offset=0.0)
p = mdb.models['Model-1'].parts['topPipe_weld']
session.viewports['Viewport: 1'].setValues(displayedObject=p)
p = mdb.models['Model-1'].parts['topPipe_weld']
f = p.faces
faces = f.getSequenceFromMask(mask=('[#1 ]', ), )
region = regionToolset.Region(faces=faces)
p = mdb.models['Model-1'].parts['topPipe_weld']
p.SectionAssignment(region=region, sectionName='pipe material', offset=0.0)

#---------------ASSEMBLY
a = mdb.models['Model-1'].rootAssembly
session.viewports['Viewport: 1'].setValues(displayedObject=a)
a = mdb.models['Model-1'].rootAssembly
a.DatumCsysByThreePoints(coordSysType=CYLINDRICAL, origin=(0.0, 0.0, 0.0),
    point1=(1.0, 0.0, 0.0), point2=(0.0, 0.0, -1.0))
p = mdb.models['Model-1'].parts['bottomPipe_weld']
a.Instance(name='bottomPipe_weld-1', part=p, dependent=OFF)
a = mdb.models['Model-1'].rootAssembly
p = mdb.models['Model-1'].parts['topPipe_weld']
a.Instance(name='topPipe_weld-1', part=p, dependent=OFF)

#----------------#SETS
#refPoints
a = mdb.models['Model-1'].rootAssembly
r1 = a.instances['topPipe_weld-1'].referencePoints
refPoints1=(r1[2], )
a.Set(referencePoints=refPoints1, name='topFlywheelAttachment')

a = mdb.models['Model-1'].rootAssembly
r1 = a.instances['bottomPipe_weld-1'].referencePoints
refPoints1=(r1[2], )
a.Set(referencePoints=refPoints1, name='bottomFlywheelAttachment')

#edges -
a = mdb.models['Model-1'].rootAssembly
e1 = a.instances['topPipe_weld-1'].edges
edges1 = e1.getSequenceFromMask(mask=('[#4 ]', ), )
a.Set(edges=edges1, name='topAttachment')
a = mdb.models['Model-1'].rootAssembly
e1 = a.instances['bottomPipe_weld-1'].edges
edges1 = e1.getSequenceFromMask(mask=('[#4 ]', ), )
a.Set(edges=edges1, name='bottomAttachment')

a3 = mdb.models['Model-1'].rootAssembly
s1 = a3.instances['topPipe_weld-1'].edges
side1Edges1 = s1.getSequenceFromMask(mask=('[#b ]', ), )
a3.Surface(side1Edges=side1Edges1, name='topWeldSurface')

a3 = mdb.models['Model-1'].rootAssembly
s1 = a3.instances['bottomPipe_weld-1'].edges
side1Edges1 = s1.getSequenceFromMask(mask=('[#b ]', ), )
a3.Surface(side1Edges=side1Edges1, name='bottomWeldSurface')


#-------------STEP
mdb.models['Model-1'].CoupledTempDisplacementStep(name='Weld step',
    previous='Initial', description="Weld step", response=TRANSIENT,
    creepIntegration=CREEP_OFF, timePeriod=timeRemaining, maxNumInc=10000, stabilization=None,
    timeIncrementationMethod=AUTOMATIC, initialInc=0.02, minInc=2e-05, maxInc=outputFrequency,
    deltmx=300, cetol=None, amplitude=STEP,
    extrapolation=PARABOLIC, matrixStorage=UNSYMMETRIC,nlgeom=ON)
mdb.models['Model-1'].steps['Weld step'].Restart(frequency=1,
    numberIntervals=0, overlay=ON, timeMarks=OFF)
mdb.models['Model-1'].FieldOutputRequest(name='F-Output-1',
    createStepName='Weld step', variables=('S', 'U', 'NT', 'PEEQ', 'HFL', 'CSTATUS','CSTRESS'))
mdb.models['Model-1'].HistoryOutputRequest(name='H-Output-1',
    createStepName='Weld step', variables=('ALLWK', 'ALLKE' ))
regionDef=mdb.models['Model-1'].rootAssembly.sets['topFlywheelAttachment']
mdb.models['Model-1'].HistoryOutputRequest(name='upset',
    createStepName='Weld step', variables=('U2', ), region=regionDef,
    sectionPoints=DEFAULT, rebar=EXCLUDE)

mdb.saveAs(primaryJobName)


#-------------------------INTERACTIONS
#-----Properties
#Weld contact
mdb.models['Model-1'].ContactProperty('weld contact')
mdb.models['Model-1'].interactionProperties['weld contact'].NormalBehavior(
    pressureOverclosure=TABULAR, table=((0.0, 0.0), (weldContactPressure, weldContactDistance)),
    constraintEnforcementMethod=DEFAULT)
	
mdb.models['Model-1'].interactionProperties['weld contact'].TangentialBehavior(
    formulation=USER_DEFINED, nStateDependentVars=0, useProperties=ON, table=((
    360., ), ))

#self contact	
mdb.models['Model-1'].ContactProperty('self contact')
mdb.models['Model-1'].interactionProperties['self contact'].NormalBehavior(
    pressureOverclosure=TABULAR, table=((0.0, -selfContactDistance), (selfContactPressure, 0.0)),
    constraintEnforcementMethod=DEFAULT)
	
#-----contact interaction
a4 = mdb.models['Model-1'].rootAssembly
region1=a4.surfaces['bottomWeldSurface']
a4 = mdb.models['Model-1'].rootAssembly
region2=a4.surfaces['topWeldSurface']
#Node to surface- contato de bottom master surface and top node
mdb.models['Model-1'].SurfaceToSurfaceContactStd(name='weld contact 1',
    createStepName='Weld step', master=region1, slave=region2,
    sliding=FINITE,
    enforcement=NODE_TO_SURFACE,
    interactionProperty='weld contact', adjustMethod=NONE, smooth=0.2,
    initialClearance=OMIT, datumAxis=None, clearanceRegion=None)
	
mdb.models['Model-1'].SurfaceToSurfaceContactStd(name='weld contact 2',
    createStepName='Weld step', master=region2, slave=region1,
    sliding=FINITE,
    enforcement=NODE_TO_SURFACE,
    interactionProperty='weld contact', adjustMethod=NONE, smooth=0.2,
    initialClearance=OMIT, datumAxis=None, clearanceRegion=None)

#selfcontact
a5 = mdb.models['Model-1'].rootAssembly
region=a5.surfaces['bottomWeldSurface']
mdb.models['Model-1'].SelfContactStd(name='Bottom self contact', createStepName='Initial',
    enforcement=NODE_TO_SURFACE,
    surface=region, interactionProperty='self contact', smooth=0.2)

region=a5.surfaces['topWeldSurface']
mdb.models['Model-1'].SelfContactStd(name='Top self contact', createStepName='Initial',
    enforcement=NODE_TO_SURFACE,
    surface=region, interactionProperty='self contact', smooth=0.2)
#------constraints
mdb.models['Model-1'].Equation(name='topFlywheelAttachment', terms=((1.0,
    'topAttachment', 5), (-1.0, 'topFlywheelAttachment', 5)))
mdb.models['Model-1'].Equation(name='topFlywheelAttachment2', terms=((1.0,
    'topAttachment', 2), (-1.0, 'topFlywheelAttachment', 2)))
mdb.models['Model-1'].Equation(name='bottomFlywheelAttachment5', terms=((1.0,
    'bottomAttachment', 5), (-1.0, 'bottomFlywheelAttachment', 5)))
mdb.models['Model-1'].Equation(name='bottomFlywheelAttachment2', terms=((1.0,
    'bottomAttachment', 2), (-1.0, 'bottomFlywheelAttachment', 2)))

#?
mdb.models['Model-1'].ActuatorSensorProp(name='flywheel inertia',
                                         realProperties=(flywheelInertia, maxUpset
    ), integerProperties=())
#: The interaction property "IntProp-3" has been created.
a5 = mdb.models['Model-1'].rootAssembly
region=a5.sets['topFlywheelAttachment']
mdb.models['Model-1'].ActuatorSensor(name='top flywheel', createStepName='Initial',
    point=region, interactionProperty='flywheel inertia', noCoordComponents=3,
    unsymm=OFF, noSolutionDepVar=2, userSubUel='U1', dof='5,2', solutionDepVars=(
    flywheelStartVelocity, 0.0))
region=a5.sets['bottomFlywheelAttachment']
mdb.models['Model-1'].ActuatorSensor(name='bottom flywheel', createStepName='Initial',
    point=region, interactionProperty='flywheel inertia', noCoordComponents=3,
    unsymm=OFF, noSolutionDepVar=2, userSubUel='U2', dof='5', solutionDepVars=(
    0.0, 0.0))
mdb.save()


#-------------------------BOUNDARY CONDITIONS
#BC
a6 = mdb.models['Model-1'].rootAssembly
region = a6.sets['bottomFlywheelAttachment']
mdb.models['Model-1'].EncastreBC(name='BC-1', createStepName='Initial',
    region=region)

a6 = mdb.models['Model-1'].rootAssembly
s1 = a6.instances['topPipe_weld-1'].edges
side1Edges1 = s1.getSequenceFromMask(mask=('[#4 ]', ), )
a6.Surface(side1Edges=side1Edges1, name='pressureSurface')
#Load Parameters	
region = a6.surfaces['pressureSurface']
mdb.models['Model-1'].Pressure(name='Load-1', createStepName='Weld step',
    region=region, distributionType=UNIFORM, field='', magnitude=appliedPressure,
    amplitude=UNSET)

#predefined fields
f1 = a6.instances['bottomPipe_weld-1'].faces
faces1 = f1.getSequenceFromMask(mask=('[#1 ]', ), )
f2 = a6.instances['topPipe_weld-1'].faces
faces2 = f2.getSequenceFromMask(mask=('[#1 ]', ), )
region = regionToolset.Region(faces=faces1+faces2)
mdb.models['Model-1'].Temperature(name='Predefined Field-1',
    createStepName='Initial', region=region, distributionType=UNIFORM,
    crossSectionDistribution=CONSTANT_THROUGH_THICKNESS, magnitudes=(20.0, ))


#----------------------MESH

a6 = mdb.models['Model-1'].rootAssembly
partInstances =(a6.instances['topPipe_weld-1'],
    a6.instances['bottomPipe_weld-1'], )
a6.seedPartInstance(regions=partInstances, size=meshSize, deviationFactor=0.1)

elemType1 = mesh.ElemType(elemCode=CGAX4HT, elemLibrary=STANDARD)
elemType2 = mesh.ElemType(elemCode=CGAX3T, elemLibrary=STANDARD)
a6 = mdb.models['Model-1'].rootAssembly
f1 = a6.instances['topPipe_weld-1'].faces
faces1 = f1.getSequenceFromMask(mask=('[#1 ]', ), )
f2 = a6.instances['bottomPipe_weld-1'].faces
faces2 = f2.getSequenceFromMask(mask=('[#1 ]', ), )
pickedRegions =((faces1+faces2), )
a6.setElementType(regions=pickedRegions, elemTypes=(elemType1, elemType2))
a6 = mdb.models['Model-1'].rootAssembly
partInstances =(a6.instances['bottomPipe_weld-1'],
    a6.instances['topPipe_weld-1'], )
a6 = mdb.models['Model-1'].rootAssembly
a1 = mdb.models['Model-1'].rootAssembly
f1 = a1.instances['topPipe_weld-1'].faces
faces1 = f1.getSequenceFromMask(mask=('[#1 ]', ), )
f2 = a1.instances['bottomPipe_weld-1'].faces
faces2 = f2.getSequenceFromMask(mask=('[#1 ]', ), )
pickedRegions = faces1+faces2
a1.setMeshControls(regions=pickedRegions, technique=FREE, allowMapped=False)
a6 = mdb.models['Model-1'].rootAssembly

#partitions
#
# Find the lowest point on the top pipe
#+
e = a.instances['topPipe_weld-1'].edges
upperCutPosition = 0
lowestLocation = 99999
for k in range(len(e)):
    ((x,y,z),) = e[k].pointOn
    if y < lowestLocation:
	lowestLocation = y
upperCutPosition = nearWeldZone+lowestLocation
upperCutPosition = sliceTopInstance('topPipe_weld-1',upperCutPosition)
surfaceNearBottom('topPipe_weld-1','topWeldSurface',upperCutPosition - 0.001)

# Find the highest point on the lower pipe
e = a.instances['bottomPipe_weld-1'].edges
highestLocation = -99999
for k in range(len(e)):
    ((x,y,z),) = e[k].pointOn
    if y > highestLocation:
	highestLocation = y
lowerCutPosition = highestLocation-nearWeldZone
lowerCutPosition = sliceBottomInstance('bottomPipe_weld-1',lowerCutPosition)
surfaceNearTop('bottomPipe_weld-1','bottomWeldSurface',lowerCutPosition + 0.001)

#mesh seeds
removeEdgeSeeds('topPipe_weld-1')
removeEdgeSeeds('bottomPipe_weld-1')
seedNearZero('topPipe_weld-1',nearWeldMeshSize,(0.25*nearWeldZone) + upperCutPosition)
seedNearZero('bottomPipe_weld-1',nearWeldMeshSize,abs(lowerCutPosition - (0.25*nearWeldZone)))

#generate mesh
partInstances =(a6.instances['bottomPipe_weld-1'],
    a6.instances['topPipe_weld-1'], )
a6.generateMesh(regions=partInstances)
mdb.save()
session.viewports['Viewport: 1'].view.fitView()

#: The model database has been saved to "D:\users\yhn\Projects\rezone\M_M.cae".

import job
# mdb.models['Model-1'].keywordBlock.synchVersions(storeNodesAndElements=False)
# mdb.models['Model-1'].keywordBlock.setValues(edited = 0)
# mdb.models['Model-1'].keywordBlock.synchVersions(storeNodesAndElements=False)
# historyBlock = whereIsLastBlock("*End Step") - 1
# remeshCard = "*remesh trigger,distortion = " + "%g" % (distortionLimit, )
# mdb.models['Model-1'].keywordBlock.insert(historyBlock, remeshCard)

mdb.Job(name=primaryJobName, model='Model-1', type=ANALYSIS, explicitPrecision=SINGLE,
        nodalOutputPrecision=SINGLE, description='',
        parallelizationMethodExplicit=DOMAIN, multiprocessingMode=DEFAULT,
        numDomains=1, userSubroutine=userSubFileName, numCpus=1, scratch='',
        echoPrint=OFF, modelPrint=OFF, contactPrint=OFF, historyPrint=OFF)

mdb.models['Model-1'].setValues(noPartsInputFile=OFF)
mdb.jobs[primaryJobName].writeInput(consistencyChecking=OFF)
mdb.save()
