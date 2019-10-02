import Settings
import serial.tools.list_ports
import re
from message_handler import LoggingMessageHandler
from netmiko import ConnectHandler
from netmiko.ssh_exception import NetMikoTimeoutException, NetMikoAuthenticationException
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtWidgets import (QCheckBox, QHBoxLayout, QGridLayout, QGroupBox, QLabel, QLineEdit, QPlainTextEdit,
                             QPushButton, QWidget)

__author__ = "Jason Hernandez"
__copyright__ = "Copyright 2018"
__credits__ = ["KTByers - Netmiko", "PyQt5"]
__license__ = "MIT"
__version__ = "1.0"
__email__ = "JThern@github"


class Thread(QThread):
    signal = pyqtSignal('PyQt_PyObject')
    # This Class threads the connection so we don't freeze the entire program waiting on the connection to take place.

    def __init__(self):
        QThread.__init__(self)
        self.device = {}

    @staticmethod
    def get_version_cisco(show_ver):
        match = re.search(r"1.*", show_ver)
        return float(match.group(0))

    # run method gets called when we start() the thread
    def run(self):
        if self.device['device_type'] == 'cisco_ios_serial':
            try:
                console = ConnectHandler(**self.device)  # Connect to the Device to verify credentials.
                config_mode = console.check_config_mode()
                if config_mode is True:
                    console.exit_config_mode()
                    self.signal.emit('Router was in config mode try again.')
                    return
                console.enable()  # Enter Enable Mode
                show_ver = console.send_command('show run | inc version 1')
                self.signal.emit(show_ver)
                version = self.get_version_cisco(show_ver)
                if version >= 15.4:
                    pass
                else:
                    show_flash = console.send_command('dir flash: | i .bin')
                    self.signal.emit('----ERROR----\n'
                                     ' Old version of IOS Detected\n'
                                     ' Correct version may be in flash:')
                    self.signal.emit(show_flash)
                    self.signal.emit('\n>========== Reminder ==========<\n'
                                     'Ensure the config you plan to load is compatible\n'
                                     ' with the version of IOS you are using.\n '
                                     'If not contact the help desk.\n'
                                     '>========== Reminder ==========<\n')
                console.disconnect()  # disconnect so it can be modified later on the LoadTab
                self.signal.emit('Credentials Verified on Console!')  # Congrats you made it
            except ValueError:  # most likely com port fault.
                self.signal.emit('...COM Port does not appear to be working. \nTry one of these:')
                ports = list(serial.tools.list_ports.comports())  # You used the wrong one here let me help you.
                for p in ports:  # may just automate this in the future using this method if only one port is found
                    self.signal.emit(p[0])
                return
            except NetMikoAuthenticationException:  # Exactly what it says in the error.
                self.signal.emit("Check your username/password. Make sure you have an account on this device.")
                return
        elif self.device['device_type'] == 'cisco_ios_telnet':
            try:
                telnet = ConnectHandler(**self.device)  # Connect to the Device to verify credentials.
                telnet.enable()  # Enter Enable Mode
                if telnet == True:
                    telnet.send_command('exit')
                show_ver = telnet.send_command('show run | inc version 1')
                self.signal.emit(show_ver)
                version = self.get_version_cisco(show_ver)
                if version >= 15.4:
                    pass
                else:
                    show_flash = telnet.send_command('dir flash: | i .bin')
                    self.signal.emit('----ERROR----\n'
                                     ' Old version of IOS Detected\n'
                                     ' Correct version may be in flash:')
                    self.signal.emit(show_flash)
                    self.signal.emit('\n>========== Reminder ==========<\n'
                                     'Ensure the config you plan to load is compatible\n'
                                     ' with the version of IOS you are using.\n '
                                     'If not contact the help desk.\n'
                                     '>========== Reminder ==========<\n')
                telnet.disconnect()
                self.signal.emit('Credentials Verified on Telnet!')
            except TimeoutError:  # Exactly what it says in the error.
                self.signal.emit("Telnet Error: Make sure the IP address is correct.")
                return
            except NetMikoAuthenticationException:  # Exactly what it says in the error.
                self.signal.emit("Check your username/password. Make sure you have an account on this device.")
                return
        elif self.device['device_type'] == 'cisco_ios':
            try:
                ssh = ConnectHandler(**self.device)  # Connect to the Device to verify credentials.
                ssh.enable()  # Enter Enable Mode
                if ssh == True:
                    ssh.send_command('exit')
                show_ver = ssh.send_command('show run | inc version 1')
                self.signal.emit(show_ver)
                version = self.get_version_cisco(show_ver)
                if version >= 15.4:
                    pass
                else:
                    show_flash = ssh.send_command('dir flash: | i .bin')
                    self.signal.emit('----ERROR----\n'
                                     ' Old version of IOS Detected\n'
                                     ' Correct version may be in flash:')
                    self.signal.emit(show_flash)
                    self.signal.emit('\n>========== Reminder ==========<\n'
                                     'Ensure the config you plan to load is compatible\n'
                                     ' with the version of IOS you are using.\n '
                                     'If not contact the help desk.\n'
                                     '>========== Reminder ==========<\n')
                ssh.disconnect()
                self.signal.emit('Credentials Verified on SSH!')
            except NetMikoTimeoutException:  # Exactly what it says in the error.
                self.signal.emit("SSH Error: Make sure the IP address is correct.")
                return
            except NetMikoAuthenticationException:  # Exactly what it says in the error.
                self.signal.emit("Check your username/password. Make sure you have an account on this device.")
                return
        else:
            return


class RouterInfo(QWidget):
    label = "RouterInfo"

    def __init__(self, parent=None):
        """ Initialise the page. """

        super().__init__(parent)
        '''sets up a grid layout for the tab'''
        layout = QGridLayout()  # Page will use a grid layout.

        '''Connection method'''
        self.con_method = ''  # Once the connection method is selected it is stored in this variable.
        con_method_sel = QGroupBox("Connection method")
        con_method_sel_layout = QHBoxLayout()  # Lays out the below buttons horizontally.

        self._console_button = QCheckBox("Console", checked=False, stateChanged=self._console_button)
        self._console_button.setToolTip("If connecting over Serial - COM port needed.")
        con_method_sel_layout.addWidget(self._console_button)

        self._telnet_button = QCheckBox("Telnet", checked=False, stateChanged=self._telnet_button)
        self._telnet_button.setToolTip("If connecting over Telnet. - IP needed")
        con_method_sel_layout.addWidget(self._telnet_button)

        self._ssh_button = QCheckBox("SSH", checked=False, stateChanged=self._ssh_button)
        self._ssh_button.setToolTip("If connecting over SSH. - IP needed")
        con_method_sel_layout.addWidget(self._ssh_button)

        con_method_sel.setLayout(con_method_sel_layout)
        layout.addWidget(con_method_sel, 0, 1)

        '''The username field and label'''
        label1 = QLabel('           Username')
        layout.addWidget(label1, 1, 0)
        self.username = QLineEdit()
        layout.addWidget(self.username, 1, 1)

        '''The password field and label'''
        label2 = QLabel('           Password')
        layout.addWidget(label2, 2, 0)
        self.password = QLineEdit()
        self.password.setEchoMode(QLineEdit.Password)  # turn off echo mode for password

        layout.addWidget(self.password, 2, 1)

        '''The ip field and label'''
        label3 = QLabel('     COM Port or IP')
        layout.addWidget(label3, 3, 0)
        self.ip = QLineEdit()
        self.ip.setToolTip("Com Port = COM1 or IP = 192.168.0.1")
        layout.addWidget(self.ip, 3, 1)

        '''The verify pushbutton'''
        self.verify_button = QPushButton("Verify", clicked=self._verify)
        self.verify_button.setToolTip("Verify - Connects using provided credentials.")
        layout.addWidget(self.verify_button, 3, 2)
        self.verify_thread = Thread()
        self.verify_thread.signal.connect(self.finished)

        label0 = QLabel('Once credentials are set click Verify.') # label at bottom of screen
        layout.addWidget(label0, 4, 1)

        '''The output screen'''
        self._log_viewer = QPlainTextEdit(readOnly=True)
        layout.addWidget(self._log_viewer, 5, 1, 1, 1)

        self.setLayout(layout)  # Displays the layout

    '''The fields below allow for actions to take place based on the above input and button pushes.'''

    def _verify(self):  # We want to verify the information in a new thread so we don't freeze up the entire app.
        logger = LoggingMessageHandler(bool(), self._log_viewer)
        if self.ip.text() == '' or self.username.text() == '' or self.password.text() == '':
            logger.clear()
            logger.status_message("All Fields must be Completed.")
            return
        if self.con_method == 'cisco_ios_serial':
            if 'COM' not in self.ip.text().upper():
                logger.clear()
                logger.status_message("Com Port field requires COM1 or COM2 or COM3 etc...")
                return
            device = {
                'device_type': self.con_method,
                'global_delay_factor': 2,
                'username': self.username.text(),
                'password': self.password.text(),
                'serial_settings': {
                    'port': self.ip.text()}
            }
            Settings.device = device
            self.verify_thread.device = device
        elif self.con_method == 'cisco_ios_telnet':
            device = {
                'device_type': self.con_method,
                'ip': self.ip.text(),
                'username': self.username.text(),
                'password': self.password.text()
            }
            Settings.device = device
            self.verify_thread.device = device
        elif self.con_method == 'cisco_ios':
            device = {
                'device_type': self.con_method,
                'ip': self.ip.text(),
                'username': self.username.text(),
                'password': self.password.text()
            }
            Settings.device = device
            self.verify_thread.device = device
        else:
            logger.clear()
            logger.status_message("Please select a connection method.")
            return

        self.verify_button.setEnabled(False)  # Disables the pushButton
        logger.status_message("Verifying... (This may take a while on Console)")
        self.verify_thread.start()

    def finished(self, result):
        logger = LoggingMessageHandler(bool(), self._log_viewer)
        logger.status_message(result)
        self.verify_button.setEnabled(True)  # Enable the pushButton

    def _console_button(self, state):
        """ if console is checked uncheck the others """

        if state == Qt.Checked:
            self._telnet_button.setCheckState(Qt.Unchecked)
            self._ssh_button.setCheckState(Qt.Unchecked)
            self.con_method = 'cisco_ios_serial'

    def _telnet_button(self, state):
        """ if telnet is checked uncheck the others """

        if state == Qt.Checked:
            self._console_button.setCheckState(Qt.Unchecked)
            self._ssh_button.setCheckState(Qt.Unchecked)
            self.con_method = 'cisco_ios_telnet'

    def _ssh_button(self, state):
        """ if ssh is checked uncheck the others """

        if state == Qt.Checked:
            self._console_button.setCheckState(Qt.Unchecked)
            self._telnet_button.setCheckState(Qt.Unchecked)
            self.con_method = 'cisco_ios'
