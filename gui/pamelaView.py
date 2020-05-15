#!/usr/bin/env python

"""PySide port of the opengl/samplebuffers example from Qt v4.x"""

import math
import sys
import time

from PyQt5 import QtOpenGL, QtCore
from PyQt5.QtCore import QThread, pyqtSignal, pyqtSlot, QCoreApplication
from PyQt5.QtWidgets import QApplication, QAction, QMainWindow, QGridLayout, QWidget, QMenu, QFileDialog, \
    QMessageBox
from PyQt5.uic.Compiler.qtproxies import QtGui
from pandas import np

from agents.agent import Agent
from gui.CustomWidget.editorWidget import EditorWidget
from gui.CustomWidget.settingWidget import SettingWidget
from gui.CustomWidget.zoomPanel import ZoomPanelWidget
from helper.util import inspectAgents
from helper.vector2D import Vector2D

try:
    from OpenGL import GL
except ImportError:
    app = QtGui.QApplication(sys.argv)
    QtGui.QMessageBox.critical(None, "PAMELA View",
                            "PyOpenGL must be installed to run this example.",
                            QtGui.QMessageBox.Ok | QtGui.QMessageBox.Default,
                            QtGui.QMessageBox.NoButton)
    sys.exit(1)


class GLWidget(QtOpenGL.QGLWidget):
    GL_MULTISAMPLE = 0x809D
    rot = 0.0

    def __init__(self, env = None, parent=None):
        QtOpenGL.QGLWidget.__init__(self, QtOpenGL.QGLFormat(QtOpenGL.QGL.SampleBuffers), parent)

        self.environment=env

        self.startTimer(40)
        self.setWindowTitle(self.tr("PAMELA View"))
        self.agentColor = {}
        self.printFustrum = False
        self.printVel = False
        self.printInfo = False
        self.printInfoMouse = False
        self.width = 1280
        self.height = 720
        self.scaleFactor = 1
        self.translation = Vector2D()
        self.printGrid = True
        self.step=50



    def initializeGL(self):
        GL.glMatrixMode(GL.GL_PROJECTION)
        GL.glLoadIdentity()
        GL.glOrtho( 0, self.width, self.height, 0, -1000, 1000)
        GL.glMatrixMode(GL.GL_MODELVIEW)
        GL.glLoadIdentity()
        GL.glClearColor(1.0, 1.0, 1.0, 1.0)



    def resizeGL(self, w, h):
        GL.glViewport(0, 0, w, h)
        self.width = w
        self.height = h
        GL.glMatrixMode(GL.GL_PROJECTION)
        GL.glLoadIdentity()
        print(" RS :"+str(w)+" "+str(h))
        GL.glOrtho(0, self.width, self.height, 0, -1000, 1000)
        GL.glMatrixMode(GL.GL_MODELVIEW)
        GL.glLoadIdentity()
        GL.glClearColor(1.0, 1.0, 1.0, 1.0)


    def paintGL(self):
        t = time.time()
        GL.glClear(GL.GL_COLOR_BUFFER_BIT)

        for b in self.environment.agents:
            self.drawAgent(b)
        for o in self.environment.objects:
            self.drawObject(o)


        if self.printGrid:
            self.drawGrid()
        dt = time.time() - t



    def drawGrid(self):


        GL.glPushMatrix()
        GL.glBegin(GL.GL_LINES)
        GL.glColor3f(0.863, 0.863, 0.863)
        for x in np.arange(self.translation.x%(self.step/self.scaleFactor),self.width,self.step/self.scaleFactor):
            GL.glVertex3f(x, 0.0, 0.0)
            GL.glVertex3f(x, float(self.height), 0.0)

        for y in np.arange(self.translation.y%(self.step/self.scaleFactor),self.height,self.step/self.scaleFactor):
            GL.glVertex3f( 0.0,y, 0.0)
            GL.glVertex3f( float(self.width), y, 0.0)

        GL.glEnd()
        GL.glPopMatrix()

    def draw_center(self):
        GL.glPushMatrix()
        GL.glColor3f(1,0,0)
        GL.glBegin(GL.GL_TRIANGLES)
        GL.glVertex2f(-(1) / self.scaleFactor, 0.0)
        GL.glVertex2f(1 / self.scaleFactor, 0.0)
        GL.glVertex2f(0.0, 1 * 3.0 / self.scaleFactor)
        GL.glEnd()
        GL.glPopMatrix()

    def drawObject(self, o):
        GL.glPushMatrix()
        # apply the transformation for the boid

        if hasattr(o, 'aabb'):
            GL.glTranslatef(self.translation.x+o.aabb.uperLeftLocation.x / self.scaleFactor, self.translation.y + o.aabb.uperLeftLocation.y / self.scaleFactor, 0.0)
            self.renderObject(o)
        else:
            GL.glTranslatef(self.translation.x+o.location.x/self.scaleFactor, self.translation.y+o.location.y/self.scaleFactor, 0.0)
            self.renderObject(o)

        # render the object itself

        GL.glPopMatrix()

    def drawAgent(self, b):
        GL.glPushMatrix()
        # apply the transformation for the boid

        GL.glTranslatef(self.translation.x+b.body.location.x/self.scaleFactor, self.translation.y+b.body.location.y/self.scaleFactor, 0.0)


        # a = signedAngle()
        GL.glRotatef(math.degrees(math.atan2(b.body.velocity.x, b.body.velocity.y)), 0.0, 0.0, -1.0)

        # render the boid's velocity
        if self.printVel:
            self.render_velocity(b)

        # render the boid's view
        if self.printFustrum:
            self.render_view(b)

        # render the boid itself
        self.render_agent(b)
        GL.glPopMatrix()

    def render_velocity(self, b):
        GL.glColor3f(0.6, 0.6, 0.6)
        GL.glBegin(GL.GL_LINES)
        GL.glVertex2f(0.0, 0.0)
        GL.glVertex2f(0.0, 10/self.scaleFactor)
        GL.glEnd()

    def render_view(self, b):
        GL.glColor3f(0.6, 0.1, 0.1)
        GL.glBegin(GL.GL_LINE_LOOP)

        step = 10
        # render a circle for the boid's view
        for i in range(-b.body.fustrum.angle, b.body.fustrum.angle + step, step):
            GL.glVertex2f(b.body.fustrum.radius/self.scaleFactor * math.sin(math.radians(i)),
                       (b.body.fustrum.radius/self.scaleFactor * math.cos(math.radians(i))))
        #glVertex2f(0.0, 0.0)
        GL.glEnd()
    #TODO couleur agent
    def render_agent(self, b):
        if hasattr(b,'color'):
            if isinstance(b.color, str):
                b.color = b.color.replace("[", "").replace(']', "").split(",")
                x = np.array(b.color)
                b.color= x.astype(np.float)
            GL.glColor3f(b.color[0],b.color[1],b.color[2])

        GL.glBegin(GL.GL_TRIANGLES)
        GL.glVertex2f(-(1) / self.scaleFactor, 0.0)
        GL.glVertex2f(1 / self.scaleFactor, 0.0)
        GL.glVertex2f(0.0, 1 * 3.0 / self.scaleFactor)
        GL.glEnd()

    def renderObject(self, b):
        GL.glBegin(GL.GL_POLYGON)
        GL.glVertex2f(-(1)/ self.scaleFactor, -1/ self.scaleFactor)
        GL.glVertex2f(1/ self.scaleFactor, -1/ self.scaleFactor)
        GL.glVertex2f(1/ self.scaleFactor, 1/ self.scaleFactor)
        GL.glVertex2f(-1/ self.scaleFactor, 1/ self.scaleFactor)
        GL.glEnd()


    def timerEvent(self, event):
        self.update()


class MainWindow(QMainWindow):
    signalStart = pyqtSignal(str, str, int)
    signalPause = pyqtSignal(str, str, bool)

    def __init__(self, simu = None, control = None, parent=None):

        super(MainWindow, self).__init__(parent)
        self.setWindowTitle("Pamela Simulation")
        self.setMouseTracking(True)
        self.simulation = simu
        self.controlSim = control
        self.gui=True
        self.pauseS=False
        self.gl=GLWidget(simu.environment)


        #TOGGLE
        self.viewStatAct = None
        self.viewVel = None
        self.viewInfo = None
        self.actPause = None
        self.viewGrid = None

        #otherWidget
        self.settingWidget = None
        self.editorWidget = None


        # TODO Event Menu
        self.__createFileMenu()
        self.__createDisplayMenu()
        self.__createConfMenu()
        self.__createEnvMenu()
        self.__createAgentMenu()
        self.__createMetriqueMenu()

        self.signalStart.connect(self.controlSim.startSim)
        self.signalPause.connect(self.controlSim.pauseSim)

        layout = QGridLayout()
        layout.addWidget(self.gl,0,0)


        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(self.gl)





        self.setMinimumSize(1280,720)
        self.__createControl()
        self._popframe.show()
        self.show()




    def __createControl(self):
        self._popframe = ZoomPanelWidget(self)
        self._popframe.move(10, 50)
        self._popframe.resize(50, 170)
        self._popframe.SIGNALS.zoomIn.connect(self.zoomIn)
        self._popframe.SIGNALS.zoomOut.connect(self.zoomOut)
        self._popframe.SIGNALS.raz.connect(self.razZoom)
        self.drag = False
        self.oldMousePos=Vector2D()



    def __createFileMenu(self):
        actOpen = QAction(  "&Configuration", self)
        actOpen.triggered.connect(self.settingTrigger)
        self.settingWidget = SettingWidget(self)

        actAide = QAction("&Aide", self)


        actExit = QAction("&Quit", self)
        actExit.setShortcut("Ctrl+Q")
        actExit.setStatusTip("Exit application")
        actExit.triggered.connect(self.close)

        menuBar = self.menuBar()
        file = menuBar.addMenu("&Pamela")
        file.addAction(actOpen)
        file.addAction(actAide)
        file.addSeparator()
        file.addAction(actExit)

    def __createConfMenu(self):
        actOpen = QAction(  "&Load Scenario", self)
        actOpen.triggered.connect(self.showDialog)


        self.actPause = QAction("Pause Scenario", self,checkable=True)
        self.actPause.setChecked(self.pauseS)
        self.actPause.triggered.connect(self.pauseSim)

        actStop = QAction(  "S&top Scenario", self)

        actCre = QAction("Create Scenario", self)
        actCre.triggered.connect(self.editorTrigger)
        self.editorWidget = EditorWidget(self)

        #TODO STOP

        menuBar = self.menuBar()
        scenario = menuBar.addMenu("&Scenario")
        scenario.addAction(actOpen)
        scenario.addAction(self.actPause)
        scenario.addAction(actStop)
        scenario.addAction(actCre)

    def __createDisplayMenu(self):

        self.viewStatAct = QAction('View Fustrum', self, checkable=True)
        self.viewStatAct.setChecked(self.gl.printFustrum)
        self.viewStatAct.triggered.connect(self.toggleFustrum)

        self.viewVel = QAction('View Velocity', self, checkable=True)
        self.viewVel.setChecked(self.gl.printVel)
        self.viewVel.triggered.connect(self.toggleVel)

        self.viewInfo = QAction('View Info', self, checkable=True)
        self.viewInfo.setChecked(self.gl.printInfoMouse)
        self.viewInfo.triggered.connect(self.toggleInfo)

        self.viewGrid = QAction('View Grid', self, checkable=True)
        self.viewGrid.setChecked(self.gl.printGrid)
        self.viewGrid.triggered.connect(self.toggleGrid)

        menuBar = self.menuBar()
        environment = menuBar.addMenu("&View")
        environment.addAction(self.viewStatAct)
        environment.addAction(self.viewVel)
        environment.addAction(self.viewInfo)
        environment.addAction(self.viewGrid)


    def __createEnvMenu(self):
        actOpen = QAction(  "&Load Image Environment", self)
        actOpen.triggered.connect(self.showDialogEnv)

        actSave = QAction(  "&Load json Environment", self)
        actSave.triggered.connect(self.showDialogEnv)

        actStop = QAction(  "Clear Environment", self)
        actStop.triggered.connect(self.clearEnv)

        menuBar = self.menuBar()
        environment = menuBar.addMenu("&Environment")
        environment.addAction(actOpen)
        environment.addAction(actSave)
        environment.addAction(actStop)

    def __createAgentMenu(self):

        impMenu = QMenu('Add Agent', self)
        impMenuR = QMenu('Remove Agent', self)
        impActR = QAction("All", self)
        impMenuR.addAction(impActR)
        impMenuR.addSeparator()

        n = inspectAgents(Agent)
        for a in n :

            impAct = QAction(a.__name__, self)
            impMenu.addAction(impAct)

            impActR = QAction(a.__name__, self)
            impMenuR.addAction(impActR)






        menuBar = self.menuBar()

        agents = menuBar.addMenu("&Agents")
        agents.addMenu(impMenu)
        agents.addMenu(impMenuR)

    def __createMetriqueMenu(self):

        actOpen = QAction("&Agents Population (graph)", self)

        actSave = QAction("&Agent Observer (csv)", self)


        menuBar = self.menuBar()
        environment = menuBar.addMenu("&Metrique")
        environment.addAction(actOpen)
        environment.addAction(actSave)


    def mousePressEvent(self, event):
        self.drag = True
        self.oldMousePos=Vector2D(event.x(),event.y())


    def mouseReleaseEvent(self, event):
       self.drag=False

    def wheelEvent(self, event):
        if event.angleDelta().y() < 0 :
            self.zoomOut()
        else:
            if event.angleDelta().y() > 0 :
                self.zoomIn()

    def mouseMoveEvent(self, event):
        dxy = Vector2D(event.x()-self.oldMousePos.x, event.y()-self.oldMousePos.y)
        self.oldMousePos= Vector2D(event.x(), event.y())

        print("in env: "+str(int((event.x()-self.gl.translation.x)*self.gl.scaleFactor))+" "+str(int((event.y()-self.gl.translation.y)*self.gl.scaleFactor)))
        print(self.gl.translation)
        print(str(event.x())+" "+str(event.y()))
        if event.buttons() == QtCore.Qt.LeftButton :
            print("left")
            #TODO Corriger drag & drop
            self.gl.translation.x += dxy.x
            self.gl.translation.y += dxy.y

        else :
            print("right")
            o = self.simulation.environment.getFirstObjectByName("Attractor")
            if o is not None:

                o.location.x = (event.x()-self.gl.translation.x)*self.gl.scaleFactor
                o.location.y = (event.y()-self.gl.translation.y)*self.gl.scaleFactor

    def zoomIn(self):
        print("zoom In")
        self.gl.scaleFactor-=.1
        if self.gl.scaleFactor <=0:
            self.gl.scaleFactor = .1

    def zoomOut(self):
        print("zoom Out")
        self.gl.scaleFactor += .1

    def razZoom(self):
        print("zoom Out")
        self.gl.scaleFactor =1
        self.gl.translation = Vector2D()

    def startSim(self):
        self.signalStart.emit("foo", "baz", 10)


    def pauseSim(self,state):
        self.pauseS = state
        self.actPause.setChecked(state)
        self.signalPause.emit("foo","baz",state)
        self.simulation.pause = state


    def editorTrigger(self):
        self.editorWidget.show()

    def settingTrigger(self):
        self.settingWidget.show()

    def toggleFustrum(self,state):
        self.gl.printFustrum = state
        self.viewStatAct.setChecked(state)

    def toggleVel(self,state):
        self.gl.printVel = state
        self.viewVel.setChecked(state)

    def toggleInfo(self, state):
        self.gl.printInfoMouse = state
        self.viewInfo.setChecked(state)

    def toggleGrid(self, state):
        self.gl.printGrid = state
        self.viewGrid.setChecked(state)

    def startSimu(self):
        self.startSim()

    def clearEnv(self):
        buttonReply = QMessageBox.question(self, 'Pamela message', "Clear environment? ("+str(len(self.simulation.environment.objects))+" object(s)).",
                                           QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if buttonReply == QMessageBox.Yes:
            self.simulation.environment.objects = []
            self.simulation.environment.zone = {}
        else:
            print('No clicked.')

    def showDialogEnv(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file', '.')

        if fname[0]:
            self.simulation.loadEnvironment(fname[0])
            msg = QMessageBox()
            msg.setWindowTitle("Pamela message")
            msg.setText(str(len(self.simulation.environment.objects))+" object(s) imported")
            x = msg.exec_()

    def showDialog(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file', '.')

        if fname[0]:
            retour,m,data = self.simulation.loadScenario(fname[0])
            if retour == -1:
                msg = QMessageBox()
                msg.setWindowTitle("Pamela Error")
                msg.setText(m)
                msg.setIcon(QMessageBox.Critical)
                msg.setDetailedText(data)
                x = msg.exec_()
            else:

                if len(data)>0:
                    if "printFustrum" in data:
                        self.toggleFustrum(bool(data["printFustrum"]))
                    if "printInfoMouse" in data:
                        self.toggleInfo(bool(data["printInfoMouse"]))
                    if "gui" in data:
                        self.gui = bool(data["gui"])
                    if "printVel" in data:
                        self.toggleVel(bool(data["printVel"]))
                    if "autorun" in data:
                        if data["autorun"]==1:
                            self.startSim()
                        else :
                            self.startSim()
                            time.sleep(1)
                            self.pauseSim(True)


    def close(self):
        print("Exit menu item clicked")
        QCoreApplication.quit()
        QCoreApplication.quit()

class PamGui():
    def __init__(self,simu):
        app = QApplication(sys.argv)
        g = getUpdateThread(simu)

        window = MainWindow(simu, g)


        g.start()
        sys.exit(app.exec_())




class getUpdateThread(QThread):

    def __init__(self, simu ,parent=None):
        QThread.__init__(self)
        super(getUpdateThread, self).__init__(parent)
        self.simulation = simu
        self.dt=.1
        self.running = True

    def __del__(self):
        self.wait()

    @pyqtSlot(str, str, int)
    def startSim(self):
        self.running = True
        self.simulation.start()

    @pyqtSlot(str, str, bool)
    def pauseSim(self):
        self.running = not self.running


    def run(self):
        print("run")
        while True:

            if self.running:

                t = time.time()
                self.simulation.environment.update(self.dt)
                self.msleep(25)
                self.dt= time.time() - t
            else:
                self.dt = .1
                self.msleep(25)



