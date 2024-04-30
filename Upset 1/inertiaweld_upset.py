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
    totalUpset = 0.0
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
            for key in odb.steps['Weld step'].historyRegions.keys():
                if key.find('TOPPIPE') != -1:
                    dataObject = odb.steps['Weld step'].historyRegions[key].historyOutputs['U2'].data
            xyName = baseName + "_remesh_" + "%i" % (remeshNumber)
            frameCount = 0
            for xyPair in dataObject:
                jobUpset = -xyPair[1]
                if frameCount != 0: # The first frame is redundant with the previous job's last frame
                    totalList.append((xyPair[0]+totalTime,totalUpset + jobUpset))
                if frameCount == 1 and remeshNumber > 0:
                    remeshPointsList.append((xyPair[0]+totalTime,totalUpset + jobUpset))
                frameCount = frameCount + 1
                stepTime = xyPair[0]
            del session.xyDataObjects[xyName]
            remeshNumber = remeshNumber + 1
            totalTime = totalTime + stepTime
            totalUpset = totalUpset + jobUpset
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

MakeXY(baseName,'Upset',True)

try:
    xyp = session.XYPlot(xyPlotName)
except:
    xyp = session.xyPlots[xyPlotName]
chartName = xyp.charts.keys()[0]
chart = xyp.charts[chartName]
xy0 = session.xyDataObjects['Upset']
c0 = session.Curve(xyData=xy0)
xy2 = session.xyDataObjects['RemeshPoints']
c2 = session.Curve(xyData=xy2)
chart.setValues(curvesToPlot=(c0, c2, ), )
session.viewports['Viewport: 1'].setValues(displayedObject=xyp)
session.curves['RemeshPoints'].symbolStyle.setValues(show=True)
session.curves['RemeshPoints'].lineStyle.setValues(show=False)
session.curves['RemeshPoints'].symbolStyle.setValues(size=2)
session.charts['Chart-1'].axes1[0].axisData.setValues(useSystemTitle=False, 
    title='Time (s)')
session.charts['Chart-1'].axes2[0].axisData.setValues(useSystemTitle=False, 
    title='Axial shortening (mm)')
session.printToFile(fileName=baseName + '_upset_plot', format=PNG,
    canvasObjects=(session.viewports['Viewport: 1'], ))
