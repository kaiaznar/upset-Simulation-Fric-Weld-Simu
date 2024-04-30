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
        print "Processing remesh number ",remeshNumber
        if remeshNumber == 0:
            fileName = baseName + ".odb"
        else:
            fileName = baseName + "_remesh_" + "%i" % (remeshNumber) + ".odb"
        try:
            odb = session.openOdb(name=fileName)
            frameCount = 0
            for frame in odb.steps['Weld step'].frames:
                maxTemp = 0.0
                stepTime = frame.frameValue
                for value in frame.fieldOutputs['NT11'].values:
                    thisTemp = value.data
                    if thisTemp > maxTemp:
                        maxTemp = thisTemp
                if frameCount != 0: # The first frame is redundant with the previous job's last frame
                    totalList.append((stepTime+totalTime,maxTemp))
                if frameCount == 1 and remeshNumber > 0:
                    remeshPointsList.append((stepTime+totalTime,maxTemp))
                frameCount = frameCount + 1
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

MakeXY(baseName,'maxTemp',True)

try:
    xyp = session.XYPlot(xyPlotName)
except:
    xyp = session.xyPlots[xyPlotName]
chartName = xyp.charts.keys()[0]
chart = xyp.charts[chartName]
xy0 = session.xyDataObjects['maxTemp']
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
    title='Maximum Temperature (C)')
session.charts['Chart-1'].axes2[0].axisData.setValues(maxValue=1400, 
    maxAutoCompute=False)
session.charts['Chart-1'].axes2[0].axisData.setValues(minValue=0, 
    minAutoCompute=False)
session.charts['Chart-1'].axes2[0].axisData.setValues(labelFormat=DECIMAL)
session.charts['Chart-1'].axes2[0].axisData.setValues(labelNumDigits=0)
session.printToFile(fileName=baseName + '_maxtemp_plot', format=PNG,
    canvasObjects=(session.viewports['Viewport: 1'], ))
