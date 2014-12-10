class CheckList(list):
    """@brief Check List Class.
    
    @param app Parent tank app. (tank.platform.Application)
    """
    def __init__(self, app, *args, **kwargs):
        super(CheckList, self).__init__(*args, **kwargs)
        
        self.app = app
        self._status = "OK"
        
    # status
    def _getStatus(self):
        """@brief Return the status of the check List.
        
        @return status The status of the check list. (string)
        """
        self._status = "OK"
        
        for check in self :
            if check.status == "WARNING" and self._status == "OK":
                self._status = "WARNING"
            elif check.status == "ERROR" :
                self._status = "ERROR"
                break
        
        return self._status
    
    status = property(_getStatus)
    
    def resetAll (self):
        """@brief Reset all the checks.
        """
        self._status = "OK"
        
        for check in self :
            check.reset()
        
    def runAll(self):
        """@brief Run all the checks of the check list and return the status.
        
        @return status The status of the check list. (string)
        """
        self.resetAll()
        
        for check in self :
            check.run()
            
        return self.status
            
    def runCheckBlocking(self):
        """@brief Run all the checks that block the publish.
        
        @return status The status of the check list. (string)
        """
        self.resetAll()
        
        for check in self :
            if check.errorMode == "ERROR":
                check.run()
                
        return self.status
    
    def runCheckWarning(self):
        """@brief Run all the checks where error mode is False and return the status.
        
        @return status The status of the check list. (string)
        """
        self.resetAll()
        
        for check in self :
            if check.errorMode == "WARNING" :
                check.run()
                
        return self.status
            
            
if __name__ == "__main__" :
    foo = CheckList()
    foo.append(object)
            
    
                
