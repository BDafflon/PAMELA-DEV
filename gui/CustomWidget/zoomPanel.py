from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import QVBoxLayout, QShortcut


class TranslucentWidgetSignals(QtCore.QObject):
    # SIGNALS
    zoomIn = QtCore.pyqtSignal()
    zoomOut = QtCore.pyqtSignal()
    raz = QtCore.pyqtSignal()

class ZoomPanelWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(ZoomPanelWidget, self).__init__(parent)

        # make the window frameless
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        #self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        self.fillColor = QtGui.QColor(30, 30, 30, 120)
        self.penColor = QtGui.QColor("#333333")

        self.popup_fillColor = QtGui.QColor(240, 240, 240, 255)
        self.popup_penColor = QtGui.QColor(200, 200, 200, 255)

        self.zoomIn_btn = QtWidgets.QPushButton(self)
        rMyIcon = QtGui.QPixmap("gui/ressources/zoomIn.png");
        self.zoomIn_btn.setIcon(QtGui.QIcon(rMyIcon))
        font = QtGui.QFont()
        font.setPixelSize(30)
        font.setBold(True)
        self.zoomIn_btn.setFont(font)

        self.zoomIn_btn.setFixedSize(50, 50)
        self.zoomIn_btn.clicked.connect(self.zoomIn)
        self.shortcut_in = QShortcut("m", self)
        self.shortcut_in.activated.connect(self.zoomIn)



        self.zoomOut_btn = QtWidgets.QPushButton(self)
        rMyIcon = QtGui.QPixmap("gui/ressources/zoomOut.png");
        self.zoomOut_btn.setIcon(QtGui.QIcon(rMyIcon))

        font = QtGui.QFont()
        font.setPixelSize(30)
        font.setBold(True)
        self.zoomOut_btn.setFont(font)

        self.zoomOut_btn.setFixedSize(50, 50)
        self.zoomOut_btn.clicked.connect(self.zoomOut)
        self.shortcut_out = QShortcut("p", self)
        self.shortcut_out.activated.connect(self.zoomOut)


        self.razOut_btn = QtWidgets.QPushButton(self)
        rMyIcon = QtGui.QPixmap("gui/ressources/zoomRaz.png");
        self.razOut_btn.setIcon(QtGui.QIcon(rMyIcon))

        font = QtGui.QFont()
        font.setPixelSize(30)
        font.setBold(True)
        self.razOut_btn.setFont(font)

        self.razOut_btn.setFixedSize(50, 50)
        self.razOut_btn.clicked.connect(self.raz)
        self.shortcut_raz = QShortcut("o", self)
        self.shortcut_raz.activated.connect(self.raz)


        self.SIGNALS = TranslucentWidgetSignals()
        self.zoomIn_btn.move(0, 0)
        self.zoomOut_btn.move(0, 60)
        self.razOut_btn.move(0,120)



    def resizeEvent(self, event):
        s = self.size()
        popup_width = 105
        popup_height = 105

        self.zoomIn_btn.move(0, 0)
        self.zoomOut_btn.move(0, 60)
        self.razOut_btn.move(0, 120)



    def zoomIn(self):
        self.SIGNALS.zoomIn.emit()

    def zoomOut(self):
        self.SIGNALS.zoomOut.emit()

    def raz(self):
        self.SIGNALS.raz.emit()

