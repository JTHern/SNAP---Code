from PyQt5.QtGui import (QColor)
from PyQt5.QtWidgets import QAbstractSlider


class MessageHandler:
    """ The MessageHandler class handles progress and verbose progress
    messages.  This base implementation issues messages to the console.
    """

    def __init__(self, quiet, verbose):
        """ Initialise the object.  quiet is set if all progress messages
        should be disabled.  verbose is set if verbose progress messages should
        be enabled.  Messages do not have trailing newlines.
        """

        self.quiet = quiet
        self.verbose = verbose

    def progress_message(self, message):
        """ Handle a progress message. """

        if not self.quiet:
            self.message(message)

    def verbose_message(self, message):
        """ Handle a verbose progress message. """

        if self.verbose:
            self.progress_message(message)

    def message(self, message):
        """ Handle a message.  This method may be reimplemented to send the
        message to somewhere other that stdout.
        """

        print(message)


class LoggingMessageHandler(MessageHandler):
    """ A message handler that captures user messages and displays them in a widget."""

    def __init__(self, verbose, viewer):
        """ Initialise the object. """

        super().__init__(quiet=False, verbose=verbose)

        self._viewer = viewer

        self._default_format = self._viewer.currentCharFormat()
        self._default_format.setForeground(QColor('#1E90FF'))  # blue

        self._error_format = self._viewer.currentCharFormat()
        self._error_format.setForeground(QColor('#F8F8FF'))  # white

        self._status_format = self._viewer.currentCharFormat()
        self._status_format.setForeground(QColor('#000000'))  # black

        self._title_format = self._viewer.currentCharFormat()
        self._title_format.setForeground(QColor('#1E90FF'))  # blue
        self._title_format.setFontPointSize(20)

    def clear(self):
        """ Clear the viewer. """

        self._viewer.setPlainText('')

    def status_message(self, message):
        """ Add a status message to the viewer. """

        self._append_text(message, self._status_format)

    def user_exception(self, e):
        """ Add a user exception to the viewer. """

        self._append_text(e, self._error_format)

        if self.verbose and e.detail != '':
            self._append_text(e.detail, self._error_format)

    def message(self, message):
        """ Reimplemented to handle progress messages. """

        self._append_text(message, self._default_format)

    def title(self, title):
        """ Reimplemented to handle progress messages. """

        self._append_text(title, self._title_format)

    def _append_text(self, text, char_format):
        """ Append text to the viewer using a specific character format. """

        viewer = self._viewer

        viewer.setCurrentCharFormat(char_format)
        viewer.appendPlainText(text)
        viewer.setCurrentCharFormat(self._default_format)

        # Make sure the new text is visible.
        viewer.verticalScrollBar().triggerAction(
                QAbstractSlider.SliderToMaximum)
