import sys
import Settings
from LoadTab import LoadPage
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (QApplication, QMainWindow, QTabWidget, QVBoxLayout, QWidget)
from RouterTab import RouterInfo
from TroubleshootTab import Troubleshoot

__author__ = "Jason Hernandez"
__copyright__ = "Copyright 2018"
__credits__ = ["KTByers - Netmiko", "PyQt5"]
__license__ = "MIT"
__version__ = "1.0"
__email__ = "JThern@github"


class SNAPWindow(QMainWindow):
    def __init__(self, parent=None):
        super(SNAPWindow, self).__init__(parent)
        central_widget = QWidget()
        self.setWindowTitle('SNAP')
        self.setWindowIcon(QIcon('icon2.png'))
        lay = QVBoxLayout(central_widget)
        self.setCentralWidget(central_widget)
        Settings.creds()
        tab_widget = QTabWidget()
        lay.addWidget(tab_widget)  # Tab Layout below.
        tab_widget.addTab(RouterInfo(), "Router Info")
        tab_widget.addTab(LoadPage(), "Load Page")
        tab_widget.addTab(Troubleshoot(), "Troubleshoot")
        tab_widget.addTab(Settings.AboutTab(), "About")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    snap = SNAPWindow()
    snap.show()
    sys.exit(app.exec_())
