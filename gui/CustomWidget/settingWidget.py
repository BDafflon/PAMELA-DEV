from PyQt5.QtWidgets import QApplication, QAction, QMainWindow

class SettingWidget(QMainWindow):
    def __init__(self, parent=None):
        super(SettingWidget, self).__init__(parent)
        self.setWindowTitle("Pamela Settings")


