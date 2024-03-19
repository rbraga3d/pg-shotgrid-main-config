"""
Hook copied from {self}/scene_operation_tk-maya.py
"""
import maya.cmds as cmds

import sgtk
from sgtk.platform.qt import QtGui

HookClass = sgtk.get_hook_baseclass()


class OpenTkBreakdown(HookClass):
    """
    This hook is temporary. It is only for dealing with the tk-multi-breakdown2 app on MAYA.
    The idea here is to open the tk-multibreakdown window when a Maya scene is open if there's
    references outdated in the scene.

    I haven't found a better solution for now, but this will probably be a custom Tk App.
    """

    def execute(
        self,
        operation,
        file_path,
        context,
        parent_action,
        file_version,
        read_only,
        **kwargs
    ):


        result = super(OpenTkBreakdown, self).execute(
            operation,
            file_path,
            context,
            parent_action,
            file_version,
            read_only,
            **kwargs
        )
        
        if operation == "open":
            # return the current scene path
            #self.check_and_open_tk_breakdown()
            cmds.evalDeferred(lambda: self.check_and_open_tk_breakdown(), lp=True)
        
        return result


    def check_and_open_tk_breakdown(self):
        """
        Check if there's references outdated in the current scene and open the tk-breakdown app
        if so.
        """
        maya_engine = self.parent.engine
        tk_breakdown = maya_engine.apps.get("tk-multi-breakdown2")
        
        if not tk_breakdown:
            self.logger.info(
                 "tk-multi-breakdown2 not found in this environment. " +
                 "Skipping checking for outdated references...")
            return
        
        # close tk-breakdown app if it's already opened
        # than open it again
        tk_apps_dialog_opened = maya_engine.created_qt_dialogs
        for dialog_opened in tk_apps_dialog_opened:
            if "breakdown" in dialog_opened.windowTitle().lower():
                dialog_opened.close()     
        tk_breakdown.show_dialog()
