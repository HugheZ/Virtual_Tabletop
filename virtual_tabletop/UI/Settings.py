from PyQt5 import QtWidgets
from virtual_tabletop.UI.Settings_UI import Ui_settingsDialog
from typing import Optional, Mapping

class Settings(QtWidgets.QDialog, Ui_settingsDialog):
    '''A simple wrapper class for the translated settings dialog .ui file
    '''

    def __init__(self, config: Optional[Mapping] = None, *args, **kwargs):
        super(Settings, self).__init__(*args, **kwargs)
        self.setupUi(self)