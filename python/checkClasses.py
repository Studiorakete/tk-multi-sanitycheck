"""
Tank sanity check app.

Abstract check class.

The CheckAbstract class also has some static method to perfom usual check.
"""
import re

import weakref

class CheckAbstract(object):
    """@brief Abstract class for all the check.
    
    @param errorMode Mode of the check, if Error mode is true the check will block the publish. (bool)
    """
    _possibleStatus = ("WAITING",
                       "RUNNING",
                       "WARNING",
                       "ERROR",
                       "OK")
    _name = ""
    _category = ""
    _asSelection = False
    _asFix = False


    def __init__(self, parent, errorMode=False):
        super(CheckAbstract, self).__init__()
        
        self._setParent(parent)
        self._errorMode = errorMode
        self._errorLog = list()
        self._status = "WAITING"
        self._errorMessage = ""
        
    def _getParent(self):
        """@brief Return the parent of the node
        if it exist otherwise return None.
        """
        return self._parent()

    def _setParent(self, parent):
        """@brief Set the parent of the node.
        Use weakref to avoid the circular reference problem.

        @param parent The parent node. (subclass of node)
        """
        self._parent = weakref.ref(parent)

    parent = property(_getParent, _setParent)
        
    # errorMode
    def _getErrorMode(self):
        """@brief Return the error mode.
        
        @return errorMode (string)
        """
        if self._errorMode :
            return "ERROR"
        else :
            return "WARNING"
    
    def _setErrorMode(self, errorMode):
        """@brief Set the error mode.
        
        @param errorMode (bool)
        """
        self._errorMode = errorMode
        
    errorMode = property(_getErrorMode, _setErrorMode)

    # errorLog
    def _getErrorLog(self):
        """@brief Return the error log.

        @return errorLog  (list of string)
        """
        return self._errorLog

    def _setErrorLog(self, errorList):
        """@brief Set the error log.

        @param errorList (list of string)
        """
        self._errorLog = errorList

    errorLog = property(_getErrorLog, _setErrorLog)

    def addError(self, error):
        """@brief Add a error to the error log.

        @param error (txt)
        """
        self._errorLog.append(error)

    def _getErrorTxt(self):
        """@brief Return the error log formated in a text.

        @return errorTxt (string)
        """
        return "\n".join(self._errorLog)

    errorTxt = property(_getErrorTxt)

    # status
    def _getStatus(self):
        """@brief Return the status of the instance.

        @return status The status. (string)
        """
        return self._status

    def _setStatus(self, status):
        """@brief Set the status of the instance.

        @param status The new status. (string)
        """
        if status in self._possibleStatus :
            self._status = status
        else :
            raise AttributeError, "%s is not a valid status" % status

    status = property(_getStatus, _setStatus)

    def __str__(self):
        if self.status in ("WAITING", "RUNNING", "OK") :
            return self.name
        elif self.status in ("WARNING", "ERROR") :
            return self.errorMessage

    #name
    def _getName(self):
        """
        Return the name of the check.

        @return:
        _name = (string)
        """
        return self._name

    name = property(_getName)

    # check category
    def _getCategory(self):
        """
        Return the type of the check.

        @return :
        checkType = (string)
        """
        return self._category

    category = property(_getCategory)

    def _getErrorMessage(self):
        """@brief Return the error message.

        @return errorMessage The error message. (string)
        """
        return self._errorMessage

    def _setErrorMessage(self, errorMessage):
        """@brief Set the error message.

        @param errorMessage The new error message. (string)
        """
        self._errorMessage = errorMessage

    errorMessage = property(_getErrorMessage, _setErrorMessage)

    def run(self):
        """@brief Call the check function.

        @return ok If the check is successful. (bool)
        """
        self.reset()
        self.check()

    def check(self):
        """@brief Perform the check this function need to be overided in the
        subclass
        """
        raise NotImplemented

    def reset(self):
        """@brief Reset the instance.

        Reset the status to WAITING and empty the error log.
        """
        self.status = "WAITING"
        self.errorLog = list()
        self.errorMessage = ""


    # checkFonction
    @staticmethod
    def checkAssetCode(assetCode):
        """
        Check if a asset code is legal.

        @param :
        assetCode = the asset code that need to be check (string)

        @return:
        legal = if the asset code is legal (bool)
        """
        if re.match("[A-Z]{4}[0-9]{2}", assetCode) :
            return True
        else :
            return False


class CheckMayaAbstract(CheckAbstract):
    """@brief Abstract class for all maya checks
    """
    _asSelection = False
    _asFix = False

    def __init__(self, *args):
        super(CheckMayaAbstract, self).__init__(*args)
        self._errorNodes = list()

    def _getAsSelection(self):
        """@brief Return if the Check can select the error nodes.

        @return asSelection If the nodes can select the error nodes. (bool)
        """
        return self._asSelection

    asSelection = property(_getAsSelection)

    def _getAsFix(self):
        """@brief Return if the check as some autofix.

        @return asFix If the check as autofix mecanisme. (bool)
        """
        return self._asFix

    asFix = property(_getAsFix)


    def _getErrorNodes(self):
        """@brief Return the error nodes.

        @return errorNodes The list of the nodes that fails the check. (list of pm.node)
        """
        return self._errorNodes

    def _setErrorNodes(self, errorNodes):
        """@brief Set the error nodes.

        @param errorNodes list of nodes that fails the check. (list of pm.node)
        """
        self._errorNodes = errorNodes

    errorNodes = property(_getErrorNodes, _setErrorNodes)

    def addErrorNodes(self, errorNode):
        """@brief Add a error node to errorNodes.

        @param errorNode A node that fails the check. (pm.node)
        """
        self.errorNodes.append(errorNode)

    def selectErrorNodes(self):
        """@brief select the nodes that fails the check.
        """
        pm.select(self.errorNodes)

    def fix(self):
        """@brief Run the fix.
        """
        raise NotImplemented

    def reset(self):
        """@brief Reset the instance.

        Reset the status to WAITING and empty the error log
        and empty the list of the error nodes
        """
        super(CheckMayaAbstract, self).reset()
        self.errorNodes = list()