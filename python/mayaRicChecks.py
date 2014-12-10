"""
Check classes to perform checks related to Richard
"""
import re
import os
import itertools


from pymel.core import *
import tank

from checkClasses import CheckMayaAbstract


class CheckShotStartEnd(CheckMayaAbstract):
    """@brief Check if the start and end frame of the shot match with the start and end frame in shotgun.
    """
    _name = "Shots start end match shotgun"
    _category = "Shots"

    _asSelection = False
    _asFix = True
    
    def check(self):
        """@brief Check if the start and end frame of the shot match with the start and end frame of shotgun.
        """
        # get the data from shotgun
        app = self.parent.app
        context = app.context
        self.shot = app.shotgun.find_one("Shot", [  ["project", "is", context.project], 
                                                ["id", 'is', context.entity["id"] ],
                                                ], ["sg_head_in", "sg_tail_out", "sg_cut_out", "sg_cut_in", "code", 
                                                    "sg_shot" ]) 

        
        frMin = playbackOptions(q = 1, min = 1)
        frAst = playbackOptions(q = 1, ast = 1)
        frMax = playbackOptions(q = 1, max = 1)
        frAet = playbackOptions(q = 1, aet = 1)

        error = self.shot["sg_head_in"] != frMin or frMin != frAst or (self.shot["sg_tail_out"]) != frMax or frMax != frAet

        
                
        if not error :
            self.status = "OK"
        else :
            self.status = self.errorMode
            self.errorNodes = None
            self.addError("Playback range does not match the framerange in shotgun.")
            self.errorMessage = "Playback range does not match the framerange in shotgun."

    def fix(self):
        playbackOptions(e = 1, min=self.shot["sg_head_in"], ast = self.shot["sg_head_in"], 
                        max = self.shot["sg_tail_out"], aet = self.shot["sg_tail_out"])


class CheckSoundOffset(CheckMayaAbstract):
    """@brief Check if sound offset matches the start frame
    """
    _name = "Sound starts at cut in"
    _category = "Shots"

    _asSelection = True
    _asFix = True
    
    def check(self):
        """@brief Check if sound offset matches the start frame
        """
        # get the data from shotgun
        app = self.parent.app
        context = app.context
        self.shot = app.shotgun.find_one("Shot", [  ["project", "is", context.project], 
                                                ["id", 'is', context.entity["id"] ],
                                                ], ["sg_head_in", "sg_tail_out", "sg_cut_out", "sg_cut_in", "code", 
                                                    "sg_shot" ]) 

        #get the sound node
        aPlayBackSliderPython = mel.eval('$tmpVar=$gPlayBackSlider')
        self.soundNode = timeControl(aPlayBackSliderPython, q = 1, displaySound = 1, sound = 1)
        if not self.soundNode:
            if ls(type = "audio"):
                self.soundNode = ls(type = "audio")[0]
                timeControl(aPlayBackSliderPython, e = 1, displaySound = 1, sound = soundNode)
            else:
                self.status = "OK"
                return
        else:
            self.soundNode = PyNode(self.soundNode)
        soundCutin = self.soundNode.offset.get()

        error = self.shot["sg_cut_in"] != soundCutin        
                
        if not error :
            self.status = "OK"
        else :
            self.status = self.errorMode
            self.errorNodes = [self.soundNode]
            self.addError("Sound does not start at cut in.")
            self.errorMessage = "Sound does not start at cut in."

    def select(self):
        """@brief Select the error nodes.
        """
        select(self.errorNodes)
        pass

    def fix(self):
        if self.soundNode:
            self.soundNode.offset.set(self.shot["sg_cut_in"])
