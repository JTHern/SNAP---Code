from message_handler import LoggingMessageHandler
from PyQt5.QtWidgets import (QGridLayout, QPlainTextEdit, QWidget)

__author__ = "Jason Hernandez"
__copyright__ = "Copyright 2018"
__credits__ = ["KTByers - Netmiko", "PyQt5"]
__license__ = "MIT"
__version__ = "1.0"
__email__ = "JThern@github"


def creds():
    global device
    device = []


class AboutTab(QWidget):
    label = "RouterInfo"

    def __init__(self, parent=None):
        """ Initialise the page. """

        super().__init__(parent)
        '''sets up a grid layout for the tab'''
        layout = QGridLayout()  # Page will use a grid layout.

        self._log_viewer = QPlainTextEdit(readOnly=True)
        self._log_viewer.setStyleSheet("background-color: #1E1E1E")
        layout.addWidget(self._log_viewer, 0, 0, 5, 1)

        self.logger = LoggingMessageHandler(bool(), self._log_viewer)
        self.logger.clear()
        self.logger.title('SNAP')  # Description of the application the different message types create different colors.
        self.logger.user_exception('Version: 1.0')
        self.logger.message('Author: Jason Hernandez')
        self.logger.user_exception('\nMIT License:         Copyright (c) 2018 Jason Hernandez\n'
                                   'Permission is hereby granted, free of charge, to any person obtaining a copy\n'
                                   'of this software and associated documentation files (the "Software"), to deal\n'
                                   'in the Software without restriction, including without limitation the rights\n'
                                   'to use, copy, modify, merge, publish, distribute, sublicense, and/or sell\n'
                                   'copies of the Software, and to permit persons to whom the Software is\n'
                                   'furnished to do so, subject to the following conditions:\n\n'
                                   'The above copyright notice and this permission notice shall be included in all\n'
                                   'copies or substantial portions of the Software.\n\n'
                                   'THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, \n'
                                   'EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES \n'
                                   'OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND \n'
                                   'NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT \n'
                                   'HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, \n'
                                   'WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, \n'
                                   'OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER \n'
                                   'DEALINGS IN THE SOFTWARE.\n')

        self.setLayout(layout)  # Displays the layout
