import Settings
from message_handler import LoggingMessageHandler
from netmiko import ConnectHandler
from netmiko.ssh_exception import NetMikoTimeoutException, NetMikoAuthenticationException
from PyQt5.QtCore import (QThread, pyqtSignal)
from PyQt5.QtWidgets import (QGridLayout, QLineEdit, QPlainTextEdit, QPushButton, QWidget)

__author__ = "Jason Hernandez"
__copyright__ = "Copyright 2018"
__credits__ = ["KTByers - Netmiko", "PyQt5"]
__license__ = "MIT"
__version__ = "1.0"
__email__ = "JThern@github"


class CommandThread(QThread):
    signal = pyqtSignal('PyQt_PyObject')
    # This Class threads the connection so we don't freeze the entire program waiting on the connection to take place.

    def __init__(self):
        QThread.__init__(self)
        self.command = ''

    # run method gets called when we start() the thread
    def run(self):
        if self.command == '':
            self.signal.emit("No command to run.")
            return
        if Settings.device == []:
            self.signal.emit("Enter Credentials on Router Info tab.")
            self.signal.emit("Once entered click Verify.")
            return
        if Settings.device['device_type'] == 'cisco_ios_serial':
            device = Settings.device
            try:
                router = ConnectHandler(**device)  # Connect to the Device
                router.enable()
                result = router.send_command(self.command)
                self.signal.emit(result)
                router.disconnect()
            except ValueError:
                self.signal.emit("Console Error: Make sure you have connectivity and try again.")
            except TimeoutError:
                self.signal.emit("Timeout Error: Make sure you are still connected")
            except NetMikoTimeoutException:
                self.signal.emit("Timeout Error: Make sure you are still connected")
            except NetMikoAuthenticationException:
                self.signal.emit("Check your username/password. Make sure you have an account on this device.")
        else:
            device = Settings.device
            try:
                router = ConnectHandler(**device)  # Connect to the Device
                router.enable()
                result = router.send_command(self.command)
                self.signal.emit(result)
                router.disconnect()
            except ValueError:
                self.signal.emit("User does not have permission to make these changes.")
            except TimeoutError:
                self.signal.emit("Telnet Error: Make sure the IP address is correct.")
            except NetMikoTimeoutException:
                self.signal.emit("SSH Error: Make sure the IP address is correct.")
            except NetMikoAuthenticationException:
                self.signal.emit("Check your username/password. Make sure you have an account on this device.")


class Troubleshoot(QWidget):
    """ The GUI for the build page of a project. """

    # The page's label.
    label = "Troubleshooting"

    def __init__(self):
        """ Initialise the page. """

        super().__init__()
        layout = QGridLayout()

        self._log_viewer = QPlainTextEdit(readOnly=True)  # the message window
        layout.addWidget(self._log_viewer, 0, 0, 3, 5)

        self.ping = QPushButton("Ping", clicked=self._ping)
        self.ping.setToolTip("ping [x.x.x.x]")
        layout.addWidget(self.ping, 4, 0)

        self.traceroute = QPushButton("Traceroute", clicked=self._traceroute)
        self.traceroute.setToolTip("traceroute [x.x.x.x]")
        layout.addWidget(self.traceroute, 4, 1)

        self.ip = QLineEdit()
        self.ip.setToolTip("[x.x.x.x]")
        layout.addWidget(self.ip, 4, 2, 1, 3)

        self.routes = QPushButton("Routes", clicked=self._routes)
        self.routes.setToolTip("show ip route")
        layout.addWidget(self.routes, 5, 0)

        self.interfaces = QPushButton("Interfaces", clicked=self._interfaces)
        self.interfaces.setToolTip("show ip interface brief")
        layout.addWidget(self.interfaces, 5, 1)

        self.dmvpn = QPushButton("DMVPN", clicked=self._dmvpn)
        self.dmvpn.setToolTip("show crypto ikev2 sa")
        layout.addWidget(self.dmvpn, 5, 2)

        self.ospf = QPushButton("OSPF", clicked=self._ospf)
        self.ospf.setToolTip("show ip ospf neighbor")
        layout.addWidget(self.ospf, 5, 3)

        self.eigrp = QPushButton("EIGRP", clicked=self._eigrp)
        self.eigrp.setToolTip("show ip eigrp neigh")
        layout.addWidget(self.eigrp, 5, 4)

        self.command_thread = CommandThread()
        self.command_thread.signal.connect(self.finished)

        self.setLayout(layout)  # Displays the layout

    '''The fields below allow for actions to take place based on the above input and button pushes.'''

    def _ping(self, _):
        """ Invoked when the user clicks the ping button. """
        logger = LoggingMessageHandler(bool(), self._log_viewer)
        if self.ip.text() == '':
            logger.clear()
            logger.status_message("No IP to ping.")
            return
        else:
            command = f'ping {self.ip.text()}'
            self.command_thread.command = command
            logger.status_message("Running....")
            self.command_thread.start()

    def _traceroute(self, _):
        """ Invoked when the user clicks the traceroute button. """
        logger = LoggingMessageHandler(bool(), self._log_viewer)
        if self.ip.text() == '':
            logger.clear()
            logger.status_message("No IP to traceroute.")
            return
        else:
            command = f'traceroute {self.ip.text()}'
            self.command_thread.command = command
            logger.status_message("Running....")
            self.command_thread.start()

    def _routes(self, _):
        """ Invoked when the user clicks the routes button. """
        logger = LoggingMessageHandler(bool(), self._log_viewer)
        command = 'show ip route'
        self.command_thread.command = command
        logger.clear()
        logger.status_message("Running....")
        self.ping.setEnabled(False)
        self.traceroute.setEnabled(False)
        self.ip.setEnabled(False)
        self.routes.setEnabled(False)
        self.interfaces.setEnabled(False)
        self.dmvpn.setEnabled(False)
        self.ospf.setEnabled(False)
        self.eigrp.setEnabled(False)
        self.command_thread.start()

    def _interfaces(self, _):
        """ Invoked when the user clicks the interfaces button. """
        logger = LoggingMessageHandler(bool(), self._log_viewer)
        command = 'show ip interface brief'
        self.command_thread.command = command
        logger.clear()
        logger.status_message("Running....")
        self.ping.setEnabled(False)
        self.traceroute.setEnabled(False)
        self.ip.setEnabled(False)
        self.routes.setEnabled(False)
        self.interfaces.setEnabled(False)
        self.dmvpn.setEnabled(False)
        self.ospf.setEnabled(False)
        self.eigrp.setEnabled(False)
        self.command_thread.start()

    def _dmvpn(self, _):
        """ Invoked when the user clicks the dmvpn button. """
        logger = LoggingMessageHandler(bool(), self._log_viewer)
        command = 'show crypto ikev2 sa'
        self.command_thread.command = command
        logger.clear()
        logger.status_message("Running....")
        self.ping.setEnabled(False)
        self.traceroute.setEnabled(False)
        self.ip.setEnabled(False)
        self.routes.setEnabled(False)
        self.interfaces.setEnabled(False)
        self.dmvpn.setEnabled(False)
        self.ospf.setEnabled(False)
        self.eigrp.setEnabled(False)
        self.command_thread.start()

    def _ospf(self, _):
        """ Invoked when the user clicks the ospf button. """
        logger = LoggingMessageHandler(bool(), self._log_viewer)
        command = 'show ip ospf neigh'
        self.command_thread.command = command
        logger.clear()
        logger.status_message("Running....")
        self.ping.setEnabled(False)
        self.traceroute.setEnabled(False)
        self.ip.setEnabled(False)
        self.routes.setEnabled(False)
        self.interfaces.setEnabled(False)
        self.dmvpn.setEnabled(False)
        self.ospf.setEnabled(False)
        self.eigrp.setEnabled(False)
        self.command_thread.start()

    def _eigrp(self, _):
        """ Invoked when the user clicks the eigrp button. """
        logger = LoggingMessageHandler(bool(), self._log_viewer)
        command = 'show ip eigrp neigh'
        self.command_thread.command = command
        logger.clear()
        logger.status_message("Running....")
        self.ping.setEnabled(False)
        self.traceroute.setEnabled(False)
        self.ip.setEnabled(False)
        self.routes.setEnabled(False)
        self.interfaces.setEnabled(False)
        self.dmvpn.setEnabled(False)
        self.ospf.setEnabled(False)
        self.eigrp.setEnabled(False)
        self.command_thread.start()

    def finished(self, result):  # Pull all messages into the main thread so we can see them.
        logger = LoggingMessageHandler(bool(), self._log_viewer)
        self.ping.setEnabled(True)
        self.traceroute.setEnabled(True)
        self.ip.setEnabled(True)
        self.routes.setEnabled(True)
        self.interfaces.setEnabled(True)
        self.dmvpn.setEnabled(True)
        self.ospf.setEnabled(True)
        self.eigrp.setEnabled(True)
        if result == '':
            logger.status_message('Process not running.')
        else:
            logger.status_message(result)
