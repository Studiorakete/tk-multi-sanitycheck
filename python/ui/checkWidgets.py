import traceback
import sys

from tank.platform.qt import QtCore, QtGui
import tank

import errorWindows

from resources.booleanRc import *
from resources.glossyBallsRc import *
from resources.darkOrangeRc import *
from resources.checkRc import *



class CheckWidget(QtGui.QWidget):
    """@brief Widget for the check.

    @param checkObject (subclass of CheckAbstract)
    @param parent Parent widget. (subclass of QtGui.QWidget)
    """
    def __init__(self, checkObject, parent=None):
        super(CheckWidget, self).__init__(parent)
        
        self._checkObject = checkObject

        self.mainLayout = QtGui.QHBoxLayout()
        self.mainLayout.setContentsMargins(4, 4, 4, 4) 
        self.setLayout(self.mainLayout)
        # self.setMinimumHeight(40)

        # status
        self.statusLabel = QtGui.QLabel()
        self.statusPixmap = QtGui.QPixmap(":/glossyBalls/white.png")
        self.statusPixmap = self.statusPixmap.scaled(14, 14, QtCore.Qt.KeepAspectRatio, QtCore.Qt.FastTransformation)
        self.statusLabel.setPixmap(self.statusPixmap)
        self.mainLayout.addWidget(self.statusLabel)

        # title
        self.titleLabel = QtGui.QLabel(str(self._checkObject))
        self.mainLayout.addWidget(self.titleLabel)

        # spacer
        spacerItem = QtGui.QSpacerItem(10, 10, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.mainLayout.addSpacerItem(spacerItem)

        # fix button
        self.fixButton = QtGui.QPushButton()
        self.fixButton.setMaximumSize(18, 18)
        self.fixButton.setIcon(QtGui.QIcon(":/images/fix.png"))
        self.fixButton.setToolTip("Fix")
        self.mainLayout.addWidget(self.fixButton)

        # select button
        self.selectButton = QtGui.QPushButton()
        self.selectButton.setMaximumSize(18, 18)
        self.selectButton.setIcon(QtGui.QIcon(":/images/select.png"))
        self.selectButton.setToolTip("Select")
        self.mainLayout.addWidget(self.selectButton)

        # connect the signal
        self.selectButton.clicked.connect(self.selectButtonCommand)
        self.fixButton.clicked.connect(self.fixButtonCommand)

        self.refresh()

    def refreshStatus(self):
        """@brief Refresh the status ball to illustrate the value of the checkObject.
        """
        # status
        checkStatus = self._checkObject.status
        if checkStatus == "WAITING" :
            image = ":/glossyBalls/white.png"
        elif checkStatus == "RUNNING" :
            image = ":/glossyBalls/blue.png"
        elif checkStatus == "WARNING" :
            image = ":/glossyBalls/orange.png"
        elif checkStatus == "ERROR" :
            image = ":/glossyBalls/red.png"
        elif checkStatus == "OK" :
            image = ":/glossyBalls/green.png"
        else :
            raise AttributeError, "%s is not a valid status for a check object" % checkStatus

        # update the status ball
        self.statusPixmap = QtGui.QPixmap(image)
        self.statusPixmap = self.statusPixmap.scaled(14, 14, QtCore.Qt.KeepAspectRatio, QtCore.Qt.FastTransformation)
        self.statusLabel.setPixmap(self.statusPixmap)

    def refreshButtons(self):
        """@brief Refresh the button to illustrate the value of the checkObject.
        """
        # the object that are not subclass of checkMayaAbstract
        # don't have a asSelection and asFix property catch
        # the error and hide the button
        try :
            if self._checkObject.asSelection :
                self.selectButton.setVisible(True)
            else :
                self.selectButton.setVisible(False)
        except AttributeError :
            self.selectButton.setVisible(False)

        try :
            if self._checkObject.asFix :
                self.fixButton.setVisible(True)
            else :
                self.fixButton.setVisible(False)
        except AttributeError :
            self.fixButton.setVisible(False)


    def refreshTitle(self):
        """@brief Refresh the title to illustrate the value of the checkObject.
        """
        self.titleLabel.setText(str(self._checkObject))


    def refresh(self):
        """@brief Refresh the check widget to illustrate the value of the checkObject.
        """
        self.refreshStatus()
        self.refreshTitle()
        self.refreshButtons()

    def selectButtonCommand(self):
        """@brief Select the error nodes.
        """
        try :
            self._checkObject.select()
        except Exception, e :
            errorMsh = "Error in check selection"
            errorWin = errorWindows.ErrorWindowDetailed(errorMsh, e, self)
            errorWin.setModal(True)
            errorWin.show()
            errorWin.raise_()
            raise


    def fixButtonCommand(self):
        """@brief Run the fix function of the checkObject.
        """
        try :
            self._checkObject.fix()
            self.refresh()
        except Exception, e :
            errorMsh = "Error in check fix"
            errorWin = errorWindows.ErrorWindowDetailed(errorMsh, e, self)
            errorWin.setModal(True)
            errorWin.show()
            errorWin.raise_()
            raise

    def runCheck(self):
        try :
            self._checkObject.run()
            self.refresh()
        except Exception, e :
            errorMsh = "Error during check"
            errorWin = errorWindows.ErrorWindowDetailed(errorMsh, e, self)
            errorWin.setModal(True)
            errorWin.show()
            errorWin.raise_()
            raise

class SanityCheckWidget(QtGui.QWidget):
    """@brief Main widget of the sanity check dialog.
    
    @param app Parent tank app. (tank.platform.Application)
    @param checkList Check List object that contains all the check. (CheckList)
    @param Parent Parent Widget. (QtGui.QWidget)
    """
    def __init__(self, app, checkList, *args):
        super(SanityCheckWidget, self).__init__(*args)
        self._checkList = checkList
        # ui setup
        self.mainLayout = QtGui.QVBoxLayout()
        self.setLayout(self.mainLayout)
        
        self.checksListWidget = QtGui.QListWidget()
        self.checksListWidget.setSelectionMode(self.checksListWidget.ExtendedSelection)
        self.checksListWidget.contextMenuEvent = self.checksListWidgetContextMenuEvent
        self.mainLayout.addWidget(self.checksListWidget)
        self.fillChecksListWidget()
        
    def addCheckWidget(self, checkObject):
        """@brief Add a check widget to checksListWidget.
        
        @param checkObject (subclass of CheckAbstract)
        """
        checkWidget = CheckWidget(checkObject)
        listWidgetItem = QtGui.QListWidgetItem()
        listWidgetItem.setBackground(QtGui.QColor(50, 50, 50))
        listWidgetItem.setSizeHint(checkWidget.sizeHint())
        self.checksListWidget.addItem(listWidgetItem)
        self.checksListWidget.setItemWidget(listWidgetItem, checkWidget)
        
    def fillChecksListWidget(self):
        """@brief Fill the checks List Widget with the checks from the checkList object.
        """
        for checkObject in self._checkList :
            self.addCheckWidget(checkObject)
            
    def checksListWidgetContextMenuEvent(self, event):
        """@brief Context menu for the checksListWidget display a menu to run the checks
        """
        menu = QtGui.QMenu(self)
 
        # run selected
        runSelectedAction = QtGui.QAction("Run selected check(s)", self)
        runSelectedAction.triggered.connect(self.runSelectedActionCommand)
        menu.addAction(runSelectedAction)
 
        # run all
        runAllAction = QtGui.QAction("Run all check(s)", self)
        runAllAction.triggered.connect(self.runAllChecks)
        menu.addAction(runAllAction)
        menu.exec_(self.mapToGlobal(event.pos()))
 
    def runAllChecks(self):
        """@brief Run all the checks.
        """
        for i in range(self.checksListWidget.count()) :
            listWidgetItem = self.checksListWidget.item(i)
            # query the checksListWidget to get the checks widget
            # linked to the selected listWidgetItem
            self.checksListWidget.itemWidget(listWidgetItem).runCheck()
            
            # force the refresh of the gui
            QtCore.QCoreApplication.processEvents()
 
    def runSelectedActionCommand(self):
        """@brief Run the selected checks
        """
        for listWidgetItem in  self.checksListWidget.selectedItems() :
            # query the checksListWidget to get the checks widget
            # linked to the selected listWidgetItem
            self.checksListWidget.itemWidget(listWidgetItem).runCheck()
            
            # force the refresh of the gui
            QtCore.QCoreApplication.processEvents()
