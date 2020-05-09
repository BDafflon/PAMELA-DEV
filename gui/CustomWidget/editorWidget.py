import json
import types
from inspect import isfunction

from PyQt5 import sip
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtWidgets import QApplication, QAction, QMainWindow, QHBoxLayout, QSplitter, QFrame, QWidget, QTreeWidget, \
    QGridLayout, QTreeWidgetItem, QComboBox, QSpacerItem, QSizePolicy, QPushButton, QTableWidget, QHeaderView, \
    QTableWidgetItem, QFileDialog
from PyQt5.QtCore import *

from agents.agent import Agent
from environment.object import Object
from helper.util import inspectAgents, inspectAgentsDict, id_generator


class EditorWidget(QMainWindow):
    def __init__(self, *args, **kwargs):
        QWidget.__init__(self, *args, **kwargs)
        self.qw = QWidget()
        self.entity= {}

        #futur widget
        self.cb = None
        self.tw = None
        self.newButton = None
        self.removeButton = None
        self.tableWidget = QTableWidget()
        self.root = None
        self.sim = None

        #Layer
        hbox = QHBoxLayout(self.qw)

        splitter1 = QSplitter(self.qw)
        splitter1.setOrientation(Qt.Horizontal)

        left = QFrame(splitter1)
        left.setFrameShape(QFrame.StyledPanel)

        self.__createTree()


        self.myLayoutLeft = QGridLayout()
        self.myLayoutLeft.addWidget(self.tw)
        left.setLayout(self.myLayoutLeft)


        right = QFrame(splitter1)
        right.setFrameShape(QFrame.StyledPanel)

        self.myLayoutRight = QGridLayout()
        right.setLayout(self.myLayoutRight)



        self.__createComboBoxAgent()


        hbox.addWidget(splitter1)


        self.addSpacer()
        self.__createFileMenu()


        self.setCentralWidget(self.qw)
        self.setMinimumSize(1280, 720)



    def addSpacer(self):

        self.newButton = QPushButton("&Add")
        self.newButton.setDefault(True)
        self.newButton.clicked.connect(self.addEntity)

        self.removeButton = QPushButton("&Remove")

        self.removeButton.clicked.connect(self.removeEntity)

        self.myLayoutRight.addWidget(self.newButton)
        self.myLayoutRight.addWidget(self.removeButton)



    def __createTree(self):
        self.tw = QTreeWidget()
        self.tw.itemClicked.connect(self.triggerItem)

        self.tw.setColumnCount(4)
        self.tw.setHeaderLabels(['ID',"Entity", "Time spawn", "Type"])

        self.root = QTreeWidgetItem(self.tw, ["Start"])
        self.sim = QTreeWidgetItem(self.tw, ["Simulation"])



    def __createComboBoxAgent(self):
        self.cb = QComboBox()

        n = inspectAgents(Agent)
        for a in n:
            self.cb.addItem(a.__name__)
        n = inspectAgents(Object)
        for a in n:
            self.cb.addItem(a.__name__)
        self.cb.currentIndexChanged.connect(self.selectionchange)

        self.myLayoutRight.addWidget(self.cb)

        self.tableWidget.setRowCount(4)
        self.tableWidget.setColumnCount(2)
        header = self.tableWidget.horizontalHeader()
        headerV=self.tableWidget.verticalHeader()

        header.setStretchLastSection(True)
        headerV.setVisible(False)
        self.myLayoutRight.addWidget(self.tableWidget)







    def __createFileMenu(self):
        actNew = QAction("&New", self)
        actNew.triggered.connect(self.newTrigger)

        actOpen = QAction("&Open", self)
        actOpen.triggered.connect(self.openTrigger)

        actSave = QAction("&Save", self)
        actSave.triggered.connect(self.saveTrigger)

        actSaveAs = QAction("&Save as", self)

        actExit = QAction("&Quit", self)
        actExit.setShortcut("Ctrl+Q")
        actExit.setStatusTip("Exit application")
        actExit.triggered.connect(self.close)

        menuBar = self.menuBar()
        file = menuBar.addMenu("&File")
        file.addAction(actNew)
        file.addAction(actOpen)
        file.addSeparator()
        file.addAction(actSave)
        file.addAction(actSave)
        file.addSeparator()
        file.addAction(actExit)


    def saveTrigger(self):
        fname = QFileDialog.getSaveFileName(self, 'Open file', '.')

        if fname[0]:

            try:
                export={}
                export['start']=[]
                export['simulation'] = []
                e = self.entity.copy()
                for k,v in e.items():
                    del e[k]['item']
                    if int(e[k]['timelaunch']) == 0:
                        export['start'].append(e[k])
                    else:
                        export['simulation'].append(e[k])


                with open(fname[0], "w", encoding='utf-8') as jsonfile:
                    json.dump(export, jsonfile, ensure_ascii=False)
            except Exception as e:
                print(e)

    def openTrigger(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file', '.')

        if fname[0]:
            try:
                with open(fname[0], 'r') as f:
                    jsonEnv = json.load(f)

                print(json)
                self.newTrigger()
                if "start" in jsonEnv:
                    start= jsonEnv['start']
                if "simulation" in jsonEnv:
                    simulation = jsonEnv['simulation']

                for e in start :
                    self.entity[e['id']]=e
                    i = self.addTreeItem(e,self.root)
                    self.entity[e['id']]['item']=i
                    print(self.entity[e['id']])

                for e in simulation :
                    self.entity[e['id']]=e
                    i = self.addTreeItem(e,self.sim)
                    self.entity[e['id']]['item']=i
                    print(self.entity[e['id']])
            except Exception as e:
                print(e)

    def addTreeItem(self,e,tree):
        print(e)
        barA = QTreeWidgetItem(tree, [e["id"], e['entity'], str(e['timelaunch']), e['type']])
        return barA

    def newTrigger(self):
        try:
            self.delItemTree(self.root)
            self.delItemTree(self.sim)
            self.root = QTreeWidgetItem(self.tw, ["Start"])
            self.sim = QTreeWidgetItem(self.tw, ["Simulation"])
            self.entity={}
            for k,v in self.entity.items():
                self.delItemTree(self.entity[k]["item"])
                self.entity[k] = None
        except Exception as e:
            print(e)

    def selectionchange(self, i):
        print ("Current index", i, "selection changed ", self.cb.currentText())
        try:
            n = inspectAgentsDict(Agent)

            type = self.cb.currentText()
            a = n[type]()
            members = [attr for attr in dir(a) if not hasattr(getattr(a, attr), '__dict__') and  not callable(getattr(a, attr)) and not attr.startswith("__")]

            print()
            self.updateSettingLayout(members,"agent")
            self.newButton.setText("Add")
        except Exception as e:
            print(e)
            try:
                n = inspectAgentsDict(Object)
                a = n[type]()
                type = self.cb.currentText()
                members = [attr for attr in dir(a) if not callable(getattr(a, attr)) and not attr.startswith("__")]
                print(members)
                self.updateSettingLayout(members, "objet")
                self.newButton.setText("Add")
            except Exception as e1:
                print(e1)


    def removeEntity(self):
        try :
            column = 1
            for row in range(3,self.tableWidget.rowCount()):
                # item(row, 0) Returns the item for the given row and column if one has been set; otherwise returns nullptr.
                _item = self.tableWidget.item(row, 0)
                _item2 = self.tableWidget.item(row, 1)
                if _item and _item2:
                    if _item.text() == "id":
                        if _item2.text() in self.entity:

                            self.delItemTree(self.entity[_item2.text()]['item'])
                            del self.entity[_item2.text()]
                            print("ok")
        except Exception as e1:
            print(e1)


    def delItemTree(self,item):
        sip.delete(item)
        self.newButton.setText("Add")
        self.updateSettingLayout([])

    def addEntity(self, a=""):

        try:


            type = self.cb.currentText()
            n = inspectAgentsDict(Agent)
            if type in n:
                a="agent"

            else:
                n = inspectAgentsDict(Object)
                if type in n:
                    a='objet'

            event = {'entity': a, 'type': type}
            timelaunch = self.tableWidget.item(0, 1).text()
            event["timelaunch"]=int(timelaunch)
            _item = self.tableWidget.item(1, 1).text()
            event["number"] = int(_item)
            _item = self.tableWidget.item(2, 1).text()
            _item=_item.replace("[", "").replace(']', "").split(",")
            if a == "agent":
                event["randomPosision"] = [[int(_item[0]),int(_item[1])],[int(_item[2]),int(_item[3])]]
            else :
                if a =='objet':
                    event["aabb"] = [int(_item[0]), int(_item[1]), int(_item[2]), int(_item[3])]

            event["customArgs"] = {}



            column = 1
            for row in range(3,self.tableWidget.rowCount()):
                # item(row, 0) Returns the item for the given row and column if one has been set; otherwise returns nullptr.
                _item = self.tableWidget.item(row, 0)
                _item2 = self.tableWidget.item(row, 1)
                if _item and _item2:
                    if _item.text() == "id":
                        if _item2.text() in self.entity:
                            id = _item2.text()
                    else:
                        item = self.tableWidget.item(row, column).text()
                        print(f'row: {row}, column: {column}, item={item}')
                        event["customArgs"][_item]=_item2

            print(event)
            if self.newButton.text() == "Add":
                id=id_generator()
            else :
                self.delItemTree(self.entity[id]["item"])
                self.entity[id] = None
            print(id)


            event["id"]=id
            self.entity[id] = event

            if int(timelaunch) == 0:
                barA = QTreeWidgetItem(self.root, [id,a, "0", self.cb.currentText()])
                event['item'] =barA
            else :
                barA = QTreeWidgetItem(self.sim, [id,a, timelaunch, self.cb.currentText()])
                self.tw.sortItems(2, Qt.AscendingOrder)
                event['item'] = barA
            self.newButton.setText("Add")
        except Exception as e:
            print(e)
                #self.sim.sortChildren(2)




    def triggerItem(self,item):
        print(item.text(0))
        if item.text(0) in self.entity:
            e = self.entity[item.text(0)]
            print(e)

            self.updateSetting(e)

    def updateSetting(self,e):

        try :
            if e["entity"] == "agent":
                n = inspectAgentsDict(Agent)
            else:
                if e["entity"] == "objet":
                    n = inspectAgentsDict(Object)

            type = e['type']
            a = n[type]()
            members = [attr for attr in dir(a) if
                       not hasattr(getattr(a, attr), '__dict__') and not callable(getattr(a, attr)) and not attr.startswith(
                           "__")]

            self.tableWidget.setRowCount(0)
            self.tableWidget.setRowCount(len(members)+2)
            self.tableWidget.setItem(0, 0, QTableWidgetItem("Spawn time"))
            self.tableWidget.setItem(0, 1, QTableWidgetItem(str(e["timelaunch"])))

            self.tableWidget.setItem(1, 0, QTableWidgetItem("Number of "+e["entity"]))
            self.tableWidget.setItem(1, 1, QTableWidgetItem(str(e["number"])))

            if e["entity"]=="agent":
                self.tableWidget.setItem(2, 0, QTableWidgetItem("randomPosision"))
                self.tableWidget.setItem(2, 1, QTableWidgetItem(str(e["randomPosision"])))
            else:
                if e['entity'] == "objet":
                    self.tableWidget.setItem(2, 0, QTableWidgetItem("AABB"))
                    self.tableWidget.setItem(2, 1, QTableWidgetItem(str(e["aabb"])))

            i = 3
            for m in members:
                if m != "aabb" and m != "randomPosision" :
                    print(m)
                    customArgs = e["customArgs"]
                    if m in customArgs:
                        self.tableWidget.setItem(i, 1, QTableWidgetItem(str(customArgs[m])))
                    else :
                        self.tableWidget.setItem(i, 1,QTableWidgetItem(""))
                    if m == "id":
                        if "id" in e:
                            self.tableWidget.setItem(i, 1, QTableWidgetItem(e[m]))
                    self.tableWidget.setItem(i, 0, QTableWidgetItem(m))

                i += 1
            self.newButton.setText("Update")
        except Exception as e:
            print(e)


    def updateSettingLayout(self,membre,a=""):
            self.tableWidget.setRowCount(0)
            self.tableWidget.setRowCount(len(membre))
            self.tableWidget.setItem(0, 0, QTableWidgetItem("Spawn time"))
            self.tableWidget.setItem(0, 1, QTableWidgetItem("0"))

            self.tableWidget.setItem(1, 0, QTableWidgetItem("Number of "+a))
            self.tableWidget.setItem(1, 1, QTableWidgetItem("1"))

            if a=="agent":
                self.tableWidget.setItem(2, 0, QTableWidgetItem("randomPosision"))
                self.tableWidget.setItem(2, 1, QTableWidgetItem("[0,100],[1,100]"))
            else :
                self.tableWidget.setItem(2, 0, QTableWidgetItem("AABB"))
                self.tableWidget.setItem(2, 1, QTableWidgetItem("[0,0,1,100]"))

            i=3
            for m in membre:
                print(m)
                if m != "aabb":
                    self.tableWidget.setItem(i,0, QTableWidgetItem(m))
                    i+=1



    def close(self):
        print("Exit menu item clicked")
        QCoreApplication.quit()