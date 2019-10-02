import Settings
from datetime import datetime
from time import sleep
from message_handler import LoggingMessageHandler
from netmiko import ConnectHandler
from netmiko.ssh_exception import NetMikoTimeoutException, NetMikoAuthenticationException
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QFileDialog, QGridLayout, QPlainTextEdit, QPushButton, QWidget, QMessageBox
from serial.serialutil import SerialException

__author__ = "Jason Hernandez"
__copyright__ = "Copyright 2018"
__credits__ = ["KTByers - Netmiko", "PyQt5"]
__license__ = "MIT"
__version__ = "1.0"
__email__ = "JThern@github"


class LoadThread(QThread):
    signal = pyqtSignal('PyQt_PyObject')
    # This Class threads the connection so we don't freeze the entire program waiting on the connection to take place.

    def __init__(self):
        QThread.__init__(self)
        self.config = ''

    # run method gets called when we start() the thread
    def run(self):
        if self.config == '':
            self.signal.emit("No config to load.")
            return
        if Settings.device == []:
            self.signal.emit("Enter Credentials on Router Info tab.")
            self.signal.emit("Once entered click Verify.")
            return
        if Settings.device['device_type'] == 'cisco_ios_serial':
            device = Settings.device
            try:
                router = ConnectHandler(**device)  # Connect to the Device
                self.signal.emit('...connected...')
                router.enable()
                router.config_mode()
                for line in self.config.splitlines():
                    self.signal.emit(line)
                    router.send_command(line, delay_factor=3, auto_find_prompt=False)
                router.exit_config_mode()
                new_config = router.send_command('show run')
                self.signal.emit(new_config)
                router.send_command('wr')
                router.config_mode()
                router.disconnect()
                self.signal.emit('Load Complete')
            except SerialException:
                self.signal.emit("Console Error: Make sure you have connectivity.")
            except OSError:
                self.signal.emit("Console Error: Make sure you have connectivity.")
            except ValueError:
                self.signal.emit("Console Error: Make sure you have connectivity.")
            except NetMikoTimeoutException:
                self.signal.emit("Timeout Error: Make sure you are still connected")
            except NetMikoAuthenticationException:
                self.signal.emit("Check your username/password. Make sure you have an account on this device.")
        else:
            device = Settings.device
            try:
                router = ConnectHandler(**device)  # Connect to the Device
                self.signal.emit('...connected...')
                router.enable()
                self.signal.emit('...this may take a while...')
                router.config_mode()
                for line in self.config.splitlines():
                    self.signal.emit(line)
                    router.send_command(line, delay_factor=2, auto_find_prompt=False)
                router.exit_config_mode()
                new_config = router.send_command('show run')
                self.signal.emit(new_config)
                router.send_command('wr')
                router.disconnect()
                self.signal.emit('Load Complete')
            except OSError:
                self.signal.emit("Verify connection")
            except ValueError:
                self.signal.emit("User does not have permission to make these changes.")
            except NetMikoTimeoutException:
                self.signal.emit("SSH Error: Make sure the IP address is correct.")
            except NetMikoAuthenticationException:
                self.signal.emit("Check your username/password. Make sure you have an account on this device.")


class BackupThread(QThread):
    signal = pyqtSignal('PyQt_PyObject')
    # This Class threads the connection so we don't freeze the entire program waiting on the connection to take place.

    def __init__(self):
        QThread.__init__(self)

    # run method gets called when we start() the thread
    def run(self):
        today = datetime.now().strftime('%Y%m%d-%H%M')
        if Settings.device == []:
            self.signal.emit("Enter Credentials on Router Info tab.")
            self.signal.emit("Once entered click Verify.")
            return
        if Settings.device['device_type'] == 'cisco_ios_serial':
            device = Settings.device
            try:
                save_file = open(f'Backup Config {today}.txt', mode='w')
                router = ConnectHandler(**device)  # Connect to the Device
                self.signal.emit('...connected...')
                router.enable()
                self.signal.emit('...this may take a while...')
                config = router.send_command('show run')
                self.signal.emit(config)
                save_file.write(config)
                save_file.close()
                router.disconnect()
                self.signal.emit('Configuration pulled')
            except SerialException:
                self.signal.emit("Console Error: Make sure you have connectivity.")
            except OSError:
                self.signal.emit("Console Error: Make sure you have connectivity.")
            except ValueError:
                self.signal.emit("Console Error: Make sure you have connectivity.")
            except NetMikoTimeoutException:
                self.signal.emit("Timeout Error: Make sure you are still connected")
            except NetMikoAuthenticationException:
                self.signal.emit("Check your username/password. Make sure you have an account on this device.")
        else:
            device = Settings.device
            try:
                save_file = open(f'Backup Config {today}.txt', mode='w')
                self.signal.emit('Connecting....')
                router = ConnectHandler(**device)  # Connect to the Device
                self.signal.emit('...connected...')
                router.enable()
                self.signal.emit('...this may take a while...')
                config = router.send_command('show run')
                self.signal.emit(config)
                save_file.write(config)
                save_file.close()
                router.disconnect()
                self.signal.emit('Configuration pulled')
            except ValueError:
                self.signal.emit("User does not have permission to make these changes.")
            except TimeoutError:
                self.signal.emit("Telnet Error: Make sure the IP address is correct.")
            except NetMikoTimeoutException:
                self.signal.emit("SSH Error: Make sure the IP address is correct.")
            except NetMikoAuthenticationException:
                self.signal.emit("Check your username/password. Make sure you have an account on this device.")


class ZeroizeThread(QThread):
    signal = pyqtSignal('PyQt_PyObject')
    # This Class threads the connection so we don't freeze the entire program waiting on the connection to take place.

    def __init__(self):
        QThread.__init__(self)

    # run method gets called when we start() the thread
    def run(self):
        if Settings.device == []:
            self.signal.emit("Enter Credentials on Router Info tab.")
            self.signal.emit("Once entered click Verify.")
            return
        if Settings.device['device_type'] == 'cisco_ios_serial':
            device = Settings.device
            try:
                router = ConnectHandler(**device)  # Connect to the Device
                router.enable()
                self.signal.emit('...connected...')
                erase = router.send_command_timing('wr er')
                if 'Erasing' in erase:
                    router.send_command_timing('y')
                    self.signal.emit('Erase succeed')
                else:
                    self.signal.emit('erase fail')
                sleep(5)
                reload = router.send_command_timing('reload')
                if 'Proceed' in reload:
                    router.send_command_timing('y')
                    self.signal.emit('Reload succeed')
                else:
                    self.signal.emit('Reload fail')
                self.signal.emit('Router reloading....\n'
                                 'After Reboot, username and password can be anything.\n'
                                 'Ensure the correct com port is selected.\n'
                                 'Reboot times may vary allow for 3-5 minutes.')
                router.disconnect()
            except SerialException:
                self.signal.emit("Console Error: Make sure you have connectivity.")
            except OSError:
                self.signal.emit("Console Error: Make sure you have connectivity.")
            except ValueError:
                self.signal.emit("Console Error: Make sure you have connectivity.")
            except NetMikoTimeoutException:
                self.signal.emit("Timeout Error: Make sure you are still connected")
            except NetMikoAuthenticationException:
                self.signal.emit("Check your username/password. Make sure you have an account on this device.")
        else:
            self.signal.emit("Zeroize only possible over Console.")


class LoadPage(QWidget):
    label = "Load"

    def __init__(self, parent=None):
        """ Initialise the page. """

        super().__init__(parent)
        layout = QGridLayout()  # page will use a grid layout

        self.config = ''  # this variable overwritten after config is opened.
        '''Pulls from router tab hopefully'''

        self._log_viewer = QPlainTextEdit(readOnly=True)
        layout.addWidget(self._log_viewer, 0, 0, 5, 1)

        self.openfile = QPushButton("Open", clicked=self._open)
        self.openfile.setToolTip("Open a text Config.")
        layout.addWidget(self.openfile, 0, 1)

        self._backup_config = QPushButton("Pull Current\nConfiguration", clicked=self._backup)
        self._backup_config.setToolTip("Optional - Pull the current config from the device will save as Backup Config.")
        layout.addWidget(self._backup_config, 1, 1)
        self.backup_thread = BackupThread()
        self.backup_thread.signal.connect(self.finished)

        self.load = QPushButton("Load", clicked=self._load)  # The load button which carries out the load logic.
        self.load.setToolTip("Load a new configuration.")
        layout.addWidget(self.load, 2, 1)
        self.load_thread = LoadThread()
        self.load_thread.signal.connect(self.finished)

        self.zero = QPushButton("Zeroize", clicked=self._zero)  # The Zero button which carries out the zeroize logic.
        self.zero.setToolTip("Restore the router to factory default settings.")
        layout.addWidget(self.zero, 4, 1)
        self.zero_thread = ZeroizeThread()
        self.zero_thread.signal.connect(self.finished)

        self.setLayout(layout)  # Displays the layout

    '''The fields below allow for actions to take place based on the above input and button pushes.'''

    def _open(self, _):
        """ Invoked when the user clicks the open button. """
        logger = LoggingMessageHandler(bool(), self._log_viewer)
        fltr = "Text or Config (*.txt *.cfg)"
        obj = QFileDialog.getOpenFileName(self, 'Config to Load', '', fltr)
        if obj[0] == '':
            return
        with open(obj[0], 'r') as file:
            config = file.read()
            logger.clear()
            logger.status_message('>======= Configuration Preview ======<\n')
            logger.status_message(config)
            logger.status_message('>============= Reminder =============<\n'
                                  'Remove extra lines from the text file, such as:\n '
                                  ' enable \n config t \n building \n etc...')
            self.load_thread.config = config

    def _backup(self, state):  # backup button triggers the backup thread to start
        logger = LoggingMessageHandler(bool(), self._log_viewer)
        logger.clear()
        logger.status_message('Connecting....')
        self.openfile.setEnabled(False)
        self._backup_config.setEnabled(False)  # turn off the buttons so accidents don't happen.
        self.load.setEnabled(False)
        self.zero.setEnabled(False)
        self.backup_thread.start()

    def _load(self):  # load button triggers the backup thread to start
        logger = LoggingMessageHandler(bool(), self._log_viewer)
        logger.clear()
        logger.status_message('Loading Configuration....')
        self.openfile.setEnabled(False)
        self._backup_config.setEnabled(False)  # turn off the buttons so accidents don't happen.
        self.load.setEnabled(False)
        self.zero.setEnabled(False)
        self.load_thread.start()

    def _zero(self,):
        zero_msg = "Are you sure you want Zero the router?"
        reply = QMessageBox.question(self, 'Zero?', zero_msg, QMessageBox.Yes, QMessageBox.No)

        if reply == QMessageBox.Yes:
            logger = LoggingMessageHandler(bool(), self._log_viewer)
            logger.clear()
            logger.status_message('Zeroizing router...')
            self.openfile.setEnabled(False)
            self._backup_config.setEnabled(False)  # turn off the buttons so accidents don't happen.
            self.load.setEnabled(False)
            self.zero.setEnabled(False)
            self.zero_thread.start()
        else:
            return

    def finished(self, result):  # Pull all messages into the main thread so we can see them.
        logger = LoggingMessageHandler(bool(), self._log_viewer)
        logger.status_message(result)
        self.openfile.setEnabled(True)
        self._backup_config.setEnabled(True)  # turn the buttons on again.
        self.load.setEnabled(True)
        self.zero.setEnabled(True)
