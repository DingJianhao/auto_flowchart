import sys, win32com.client
from collections import deque
import copy
import re
import os
import analyze as az
G=az.get_graph("sample2.cpp")

# Visio constants
visCharacterColor  = 1
visCharacterFont = 20
visSectionCharacter = 3
visCharacterSize = 7
visCharacterDblUnderline = 8
visSectionFirstComponent = 10

visSectionObject =  1
visRowPrintProperties =  25

visPrintPropertiesPageOrientation =  16
visRowPage =  10
visPageWidth =  0
visPageHeight =  1

# Visio must be open and I used a "Basic Diagram" template
visio = win32com.client.Dispatch("Visio.Application")

FlowchartTemplateName = "Basic Flowchart.vst"
docFlowTemplate = visio.Documents.Add(FlowchartTemplateName)

pg = docFlowTemplate.Pages.Item(1)

# Change page from landscape to portrait but this works sometimes
visio.Application.ActiveWindow.Page.PageSheet.CellsSRC(visSectionObject, visRowPrintProperties, visPrintPropertiesPageOrientation).FormulaForceU = "1"
visio.Application.ActiveWindow.Page.PageSheet.CellsSRC(visSectionObject, visRowPage, visPageWidth).FormulaU = "8.5 in"
visio.Application.ActiveWindow.Page.PageSheet.CellsSRC(visSectionObject, visRowPage, visPageHeight).FormulaU = "11 in"


# Place a Visio shape on the Visio document
def dropShape (shapeType, posX, posY, theText):

    print("Shape type = %s" % shapeType)
    print("X = %i" % posX)
    print("Y = %i" % posY)

    vsoShape = pg.Drop(shapeType, posX, posY)

    setDefaultShapeValues(vsoShape)
    vsoShape.Text = theText

    return vsoShape   # Returns the shape that was created

# Draw connector from bottom of one shape to another shape with autoroute
def connectShapes(shape1, shape2, theText):
    conn = visio.Application.ConnectorToolDataObject
    shpConn = pg.Drop(conn, 0, 0)

    shpConn.CellsU("BeginX").GlueTo(shape1.CellsU("PinX"))
    shpConn.CellsU("EndX").GlueTo(shape2.CellsU("PinX"))

    setDefaultShapeValues(shpConn)
    shpConn.Text = theText

# Specify which part of a shape to draw a connector from
#     one shape to another shape.
def connectShapes2(shape1, shape2, glueBegin, glueEnd, theText):

    conn = visio.Application.ConnectorToolDataObject
    shpConn = pg.Drop(conn, 0, 0)

    shpConn.CellsU("BeginX").GlueTo(shape1.CellsU(glueBegin))
    shpConn.CellsU("EndX").GlueTo(shape2.CellsU(glueEnd))

    setDefaultShapeValues(shpConn)
    shpConn.Text = theText

# Set the default color, font and ect for a shape
def setDefaultShapeValues(vsoShape):

    vsoShape.Cells("LineColor").FormulaU = 0
    vsoShape.Cells("LineWeight").FormulaU = "2.0 pt"
    vsoShape.FillStyle  = "None"
    vsoShape.Cells("Char.size").FormulaU = "12 pt"

    vsoShape.CellsSRC(visSectionCharacter, 0, visCharacterDblUnderline).FormulaU = False
    vsoShape.CellsSRC(visSectionCharacter, 0, visCharacterColor).FormulaU = "THEMEGUARD(RGB(0,0,0))"
    vsoShape.CellsSRC(visSectionCharacter, 0, visCharacterFont).FormulaU = 100

    return vsoShape

# Get the stencil object
def getStencilName(): # Name of Visio stencil containing shapes

    FlowchartStencilName = "BASFLO_U.VSSX" # Basic Flow Chart
    docFlowStencil = ""

    for doc in visio.Documents:
        print ("Doc name = %s" % doc)
        if doc.Name == FlowchartStencilName or doc.Name == "BASFLO_M.VSSX" :

            docFlowStencil = doc

    print ("docFlowStencil = %s" % docFlowStencil)  # Print installed stencils
    return docFlowStencil


MasterProcessName = "Process"
MasterDecisionName = "Decision"
MasterStartEnd = "Start/End"

docFlowStencil = getStencilName()

# Get masters for Process and Decision:
mstProcess = docFlowStencil.Masters.ItemU(MasterProcessName)
mstDecision =  docFlowStencil.Masters.ItemU(MasterDecisionName)
mstStartEnd = docFlowStencil.Masters.ItemU(MasterStartEnd)
x = 1
y = 10

queue = deque()
queue.append(0)
shape = 0
visited=[0 for i in range(0,len(G))]
posed=[0 for i in range(0,len(G))]
layout_x=[0 for i in range(0,len(G))]
layout_y = [0 for i in range(0, len(G))]
tag={}
print(G)
while len(queue)!=0:
    pos = queue[0]
    print(G[pos].content)
    queue.popleft()
    if visited[pos] == 1:
        continue
    #choose shape
    if G[pos].type==1:
        shape=mstProcess
    elif G[pos].type==2:
        shape=mstDecision
    elif G[pos].type==3:
        shape = mstStartEnd
    if pos==0:
        layout_x[pos]=x
        layout_y[pos]=y
        posed[0]=1
    tag[pos] = dropShape(shape, layout_x[pos], layout_y[pos], G[pos].content)
    visited[pos] = 1
    if G[pos].yes!=-1 and posed[G[pos].yes]==0:
        queue.append(G[pos].yes)
        posed[G[pos].yes] = 1
        layout_x[G[pos].yes]=layout_x[pos]
        layout_y[G[pos].yes] = layout_y[pos]-1.2
    if G[pos].no!=-1 and posed[G[pos].no]==0:
        queue.append(G[pos].no)
        posed[G[pos].no] = 1
        layout_x[G[pos].no] = layout_x[pos]+2
        layout_y[G[pos].no] = layout_y[pos]
# Add connectors to the shapes
queue = deque()
queue.append(0)
shape = 0
visited=[0 for i in range(0,len(G))]
while len(queue)!=0:
    pos = queue[0]
    print(G[pos].content)
    queue.popleft()
    if visited[pos] == 1:
        continue
    if G[pos].type==2:
        if G[pos].yes != -1:
            connectShapes(tag[pos], tag[G[pos].yes], "YES")
        if G[pos].no != -1:
            connectShapes2(tag[pos], tag[G[pos].no], "Connections.X2", "PinX", "NO")
    else:
        if G[pos].yes != -1:
            connectShapes(tag[pos], tag[G[pos].yes], "")
        if G[pos].no != -1:
            connectShapes(tag[pos], tag[G[pos].no], "")
    visited[pos] = 1
    if G[pos].yes!=-1:
        queue.append(G[pos].yes)
    if G[pos].no!=-1:
        queue.append(G[pos].no)

