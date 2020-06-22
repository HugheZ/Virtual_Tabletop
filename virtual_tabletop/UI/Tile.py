from virtual_tabletop.UI.Tile_UI import Ui_Tile
from PyQt5 import QtWidgets

class Tile(QtWidgets.QWidget, Ui_Tile):
    '''
    A generic tile UI class to hold information about a shown board.

    The tile will display a preview image of the board, an icon to show whether or not it is stored locally, and a name.

    Collection tiles will alternatively display a folder icon and omit a game image and a 'displayed locally' icon
    '''

    def __init__(self, *args, **kwargs):
        super(Tile, self).__init__(*args, **kwargs)
        self.setupUi(self)