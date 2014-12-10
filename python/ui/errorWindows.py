
import traceback
import sys

from tank.platform.qt import QtCore, QtGui

class ErrorWindowDetailed (QtGui.QMessageBox):
    """@brief Detailed Error window.

    @param errorMessage text that explain the error (string)
    @param parent Parent Qt widget (QtGui.Widget)

    @code{.py}
    try :
        import lalala
    except Exception, e:
        win = ErrorWindowDetailed("Error",e,parent=self)
        win.exec_()
    @endcode
    """
    def __init__(self, errorMessage, e=None, parent=None):
        errorMessage = "<font color=red size=3><B>%s :</B></font><br>" % errorMessage

        # replace < > symbol from the error otherwise pyqt think that's some special code
        errorE = str(e).replace("<", "").replace(">", "")
        if e.args :
            errorArgs = str(e.args).replace("<", "*").replace(">", "*")
        else :
            errorArgs = ""

        errorMessage += "<font color=orange size=5><B>%s %s</B></font><br>" % (errorE, errorArgs)
        errorMessage += "<B>If you want to report the error please also include the text in yellow :<br><\B>"
        errorMessage += "<font color=yellow size=1>%s</font><br>" % sys.exc_info()[0].__name__
        txtTraceBack = traceback.format_exc(sys.exc_info()[2]).replace("\\", "/").replace("<", "*").replace(">", "*").replace("\n", "<br>")
        errorMessage += "<font color=yellow size=1>%s<br></font>" % txtTraceBack
        QtGui.QMessageBox.__init__(self, QtGui.QMessageBox.Warning, "GRID : ERROR", \
                                   errorMessage, QtGui.QMessageBox.NoButton, parent=parent)
        self.setWindowTitle("ERROR")
        self.addButton("OK", QtGui.QMessageBox.AcceptRole)

class ErrorWindowDetailedScroll (QtGui.QDialog):
    """@brief Detailed error window with a scroll.

    @param errorMessage text that explain the error (string)
    @param e (exceptions.Exception)
    @param parent parent Qt widget (QtGui.Widget)

    @code{.py}
    try :
        import lalala
    except Exception:
        win = ErrorWindowDetailed("Error",self)
        win.exec_()
    @endcode
    """
    def __init__(self, errorMessage, e=None, parent=None):
        super(ErrorWindowDetailedScroll, self).__init__(parent)

        self.setWindowTitle("ERROR")
        mainLayout = QtGui.QVBoxLayout()
        self.setLayout(mainLayout)

        #error message
        errorMessage = "<font color=red size=6><B>%s :</B></font><br>" % errorMessage
        errorMessageLabel = QtGui.QLabel(errorMessage)
        mainLayout.addWidget(errorMessageLabel)

        # error scrolling
        scrollingWidget = QtGui.QWidget()
        scrollingLayout = QtGui.QVBoxLayout()
        scrollingWidget.setLayout(scrollingLayout)
        scrollArea = QtGui.QScrollArea()
        scrollArea.setWidgetResizable(True)
        scrollArea.setEnabled(True)
        scrollArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        scrollArea.setWidget(scrollingWidget)
        mainLayout.addWidget(scrollArea)


        errorMessage = ""
        errorMessage += "<B>If you want to report the error please also include the text in yellow :<br><\B>"
        errorMessage += "<font color=yellow size=2>%s</font><br>" % sys.exc_info()[0].__name__
        txtTraceBack = traceback.format_exc(sys.exc_info()[2]).replace("\\", "/").replace("<", "*").replace(">", "*").replace("\n", "<br>")
        errorMessage += "<font color=yellow size=2>%s<br></font>" % txtTraceBack
        detailledErrorLabel = QtGui.QLabel(errorMessage)
        detailledErrorLabel.setTextInteractionFlags(QtCore.Qt.TextSelectableByMouse)
        scrollingLayout.addWidget(detailledErrorLabel)



class ErrorWindow (QtGui.QMessageBox):
    """@brief Basic error window.

    @param errorMessage text that explain the error (string)
    @param parent parent Qt widget (QtGui.Widget)
    """
    def __init__(self, errorMessage, parent=None):
        errorMessage = "<font color=red>%s</font><br>" % errorMessage
        QtGui.QMessageBox.__init__(self, QtGui.QMessageBox.Warning, "ERROR", \
                                   errorMessage, QtGui.QMessageBox.NoButton, parent=parent)
        self.setWindowTitle("ERROR")
        self.addButton("OK", QtGui.QMessageBox.AcceptRole)


class ErrorWindowNoFormat(QtGui.QMessageBox):
    """@brief Basic error window without any text formating.

    @param errorMessage text that explain the error (string)
    @param parent parent Qt widget (QtGui.Widget)
    """
    def __init__(self, errorMessage, parent=None):
        QtGui.QMessageBox.__init__(self, QtGui.QMessageBox.Warning, "ERROR", \
                                   errorMessage, QtGui.QMessageBox.NoButton, parent=parent)
        self.setWindowTitle("ERROR")
        self.addButton("OK", QtGui.QMessageBox.AcceptRole)
