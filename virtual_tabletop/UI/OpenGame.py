from virtual_tabletop.UI.OpenGame_UI import Ui_openGame
from PyQt5 import QtWidgets

class OpenGame(QtWidgets.QWidget, Ui_openGame):
    '''A simple wrapper class for the auto-generated OpenGame_UI-defined main window class'''

    def __init__(self, *args, **kwargs):
        super(OpenGame, self).__init__(*args, **kwargs)
        self.setupUi(self)