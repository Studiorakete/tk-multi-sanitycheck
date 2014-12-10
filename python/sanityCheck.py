import tank
from .ui import checkWidgets

class sanityCheck(object):
    def __init__(self, app):
        self._app = app
        self._checkList = app.buildCheckList()
        
    def showDialog(self):
        """@brief Show the Sanity Check Dialog
        """            
        self._app.engine.show_dialog("Sanity Check", self._app, checkWidgets.SanityCheckWidget, self._app, self._checkList)