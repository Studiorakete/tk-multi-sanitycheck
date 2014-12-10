import sys
import os
import platform

from tank.platform import Application

class AboutTank(Application):
    
    def init_app(self):
        """@brief Called as the application is being initialized
        """
        sanityCheckModule = self.import_module("sanityCheck")

        # register commands:
        self._sanityCheckHandler = sanityCheckModule.sanityCheck(self)
        self.engine.register_command("Sanity Check...", self._sanityCheckHandler.showDialog)
        
        
    def buildCheckList(self):
        """@brief Read the settings and return a CheckList object that contains all the checks
        listed in the settings.
        
        @return checkList Check list object that contains all the check listed in the settings. (CheckList)
        """
        checkList = self.import_module("checkList")
        
        # import the check needed for the current engine
        if self.engine.name == "tk-maya" :
            mayaDefaultChecks = self.import_module("mayaDefaultChecks")
            mayaRicChecks = self.import_module("mayaRicChecks")
        
        # get the checks settings
        checks = self.get_setting("checks")
        checkList = checkList.CheckList(self)
        
        for check in checks :
            sourceModul = locals()[check["source"]]
            checkList.append(getattr(sourceModul, check["type"])(checkList , check["blockPublish"]))
             
        return checkList
        
    def destroy_app(self):
        """@brief Call the app is destroyed
        """
        self.log_debug("Destroying tk-multi-sanityCheck")
        self._sanityCheckHandler = None
    
