from abaqus import *
from abaqusConstants import *
import odbAccess
import annotationToolset
from odbAccess import *
from caeModules import *
from driverUtils import executeOnCaeStartup
executeOnCaeStartup()

def MakeXY(baseName,historyVariable,remeshPoints):
    remeshNumber = 0
    totalTime = 0.0
    cont = True
    totalList = []
    remeshPointsList = []
    while cont:
        if remeshNumber == 0:
            fileName = baseName + ".odb"
        else:
            fileName = baseName + "_remesh_" + "%i" % (remeshNumber) + ".odb"
        try:
            odb = session.openOdb(name=fileName)
            xyName = baseName + "_remesh_" + "%i" % (remeshNumber)
            session.XYDataFromHistory(name=xyName, odb=odb, 
                                      outputVariableName=historyVariable,
                                      steps=('Weld step', ), )
            dataObject = session.xyDataObjects[xyName]
            viewport.setValues(displayedObject=odb)
            step = odb.steps['Weld step']
            frameCount = 0
            for xyPair in dataObject:
                if frameCount != 0: # The first frame is redundant with the previous job's last frame
                    totalList.append((xyPair[0]+totalTime,xyPair[1]))
                if frameCount == 1:
                    remeshPointsList.append((xyPair[0]+totalTime,xyPair[1]))
                frameCount = frameCount + 1
                stepTime = xyPair[0]
            del session.xyDataObjects[xyName]
            remeshNumber = remeshNumber + 1
            totalTime = totalTime + stepTime
            session.odbs[fileName].close()
        except:
            cont = False
        
    xQuantity = visualization.QuantityType(type=NONE)
    yQuantity = visualization.QuantityType(type=NONE)
    session.XYData(name=historyVariable, data=tuple(totalList),
                   axis1QuantityType=xQuantity, 
                   axis2QuantityType=yQuantity, )
    if remeshPoints == True:
        session.XYData(name='RemeshPoints', data=tuple(remeshPointsList),
                       axis1QuantityType=xQuantity, 
                       axis2QuantityType=yQuantity, )
    

baseName = "inertia_weld"
xyPlotName = 'XYPlot-1'

viewport = session.viewports['Viewport: 1']
viewport.makeCurrent()
viewport.restore()

MakeXY(baseName,'Kinetic energy: ALLKE for Whole Model',True)
MakeXY(baseName,'External work: ALLWK for Whole Model',False)

try:
    xyp = session.XYPlot(xyPlotName)
except:
    xyp = session.xyPlots[xyPlotName]
chartName = xyp.charts.keys()[0]
chart = xyp.charts[chartName]
xy0 = session.xyDataObjects['External work: ALLWK for Whole Model']
c0 = session.Curve(xyData=xy0)
xy1 = session.xyDataObjects['Kinetic energy: ALLKE for Whole Model']
c1 = session.Curve(xyData=xy1)
xy2 = session.xyDataObjects['RemeshPoints']
c2 = session.Curve(xyData=xy2)
#chart.setValues(curvesToPlot=(c1, c2, ), )
chart.setValues(curvesToPlot=(c0, c1, c2, ), )
session.viewports['Viewport: 1'].setValues(displayedObject=xyp)
session.curves['RemeshPoints'].symbolStyle.setValues(show=True)
session.curves['RemeshPoints'].lineStyle.setValues(show=False)
session.curves['RemeshPoints'].symbolStyle.setValues(size=2)
session.printToFile(fileName=baseName + '_energy_plot', format=PNG,
    canvasObjects=(session.viewports['Viewport: 1'], ))
