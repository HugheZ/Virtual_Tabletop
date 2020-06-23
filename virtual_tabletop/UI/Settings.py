from PyQt5 import QtWidgets, QtCore
from virtual_tabletop.UI.Settings_UI import Ui_settingsDialog
from typing import Optional, Mapping
from functools import partial

class Settings(QtWidgets.QDialog, Ui_settingsDialog):
    '''A simple wrapper class for the translated settings dialog .ui file
    '''

    def __init__(self, config: Optional[Mapping] = None, *args, **kwargs):
        super(Settings, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.config = config

        #set checkboxes
        self.autologinCheckbox.setChecked(config.get("login_on_startup"))
        self.autouploadCheckbox.setChecked(config.get("auto_upload"))
        self.saveondownloadCheckbox.setChecked(config.get("store_on_download"))
        self.storecredsCheckbox.setChecked(config.get("storecreds"))

        #set store location
        store = self.config.get("savedir")
        if store == "./localboards":
            self.saveLocationPath.setText("")
        else:
            self.saveLocationPath.setText(store)

        #link slots
        self.autologinCheckbox.toggled.connect(partial(self.__toggle_setting, "login_on_startup"))
        self.autouploadCheckbox.toggled.connect(partial(self.__toggle_setting, "auto_upload"))
        self.saveondownloadCheckbox.toggled.connect(partial(self.__toggle_setting, "store_on_download"))
        self.storecredsCheckbox.toggled.connect(partial(self.__toggle_setting, "storecreds"))
        self.changeSaveLocationButton.clicked.connect(self.__choose_new_local_storage)
    
    @QtCore.pyqtSlot(bool)
    def __toggle_setting(self, setting:str, val:bool):
        '''A function that toggles a specific setting given\n
        setting: the string setting to toggle in the config file\n
        val: the new value of the setting
        '''
        self.config[setting] = val
    
    @QtCore.pyqtSlot()
    def __choose_new_local_storage(self):
        '''Logic for choosing a new local storage directory
        '''
        loc = str(QtWidgets.QFileDialog.getExistingDirectory(self, caption='Select Storage Location', options=QtWidgets.QFileDialog.ShowDirsOnly))

        #set UI and config
        self.config['savedir'] = loc
        self.saveLocationPath.setText(loc)