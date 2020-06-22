from virtual_tabletop.UI.MainWindow_UI import Ui_VTTMainWindow
from virtual_tabletop.UI.Tile import Tile
from PyQt5 import QtWidgets

class MainWindow(QtWidgets.QMainWindow, Ui_VTTMainWindow):
    '''A simple wrapper class for the auto-generated MainWindow_UI-defined main window class'''

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)

        #temp add in some game tiles
        for i in range(6):
            litem = QtWidgets.QListWidgetItem()
            t = Tile()
            litem.setSizeHint(t.sizeHint())
            self.gamesList.addItem(litem)
            self.gamesList.setItemWidget(litem, t)
        