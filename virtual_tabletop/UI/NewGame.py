from virtual_tabletop.UI.NewGame_UI import Ui_newGame
from PyQt5 import QtWidgets
from typing import Mapping

class NewGame(QtWidgets.QDialog, Ui_newGame):
    '''Simple wrapper class for auto-generated NewGame_UI file'''

    def __init__(self, game:Mapping, *args, **kwargs):
        super(NewGame, self).__init__(*args, **kwargs)
        self.setupUi(self)

        #get game dict reference
        self.game = game
    
    