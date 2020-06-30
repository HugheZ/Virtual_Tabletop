from virtual_tabletop.UI.NewGame_UI import Ui_newGame
from PyQt5 import QtWidgets, QtCore, QtGui
from typing import Mapping
from functools import partial

class NewGame(QtWidgets.QDialog, Ui_newGame):
    '''Simple wrapper class for auto-generated NewGame_UI file'''

    def __init__(self, game:Mapping, *args, **kwargs):
        super(NewGame, self).__init__(*args, **kwargs)
        self.setupUi(self)

        #get button references
        self.save = self.dialogButtons.button(QtWidgets.QDialogButtonBox.Save)
        self.save.setEnabled(False)
        self.cancel = self.dialogButtons.button(QtWidgets.QDialogButtonBox.Cancel)

        #get game dict reference
        self.game = game

        #connect button actions
        self.save.clicked.connect(self.__save)
        self.cancel.clicked.connect(self.__cancel)
        self.previewUpload.clicked.connect(partial(self.__choose_image, True))
        self.BoardUpload.clicked.connect(partial(self.__choose_image, False))
        self.nameEdit.textChanged.connect(self.__validate)
    
    @QtCore.pyqtSlot()
    def __validate(self):
        '''Validator for boards. Note that only the board source and name are required, since previews can be defaulted and size must be in range [0,99] by UI restrictions
        '''
        if self.boardImgSource.text() != '' and self.nameEdit.text() != '':
            self.save.setEnabled(True)
        else: self.save.setEnabled(False)
    
    @QtCore.pyqtSlot()
    def __choose_image(self, preview):
        '''Launches a file selector to be used for choosing a game image\n
        preview: are we choosing the preview image? If not, choose board image
        '''
        filt = "Images (*.png *.jpeg *.jpg)" if preview else "Images (*.png *.jpeg *.jpg *.gif)"
        path = QtWidgets.QFileDialog.getOpenFileName(self, caption='Select Firebase key', filter=filt)[0]

        if preview:
            self.previewImgSource.setText(path)
            self.previewImg.setPixmap(QtGui.QPixmap(path))
        else:
            self.boardImgSource.setText(path)
            self.boardImg.setPixmap(QtGui.QPixmap(path))
            self.__validate()
    
    @QtCore.pyqtSlot()
    def __save(self):
        '''Saves the dialog components and returns it with a save message to the caller, defaults preview image to null if none is provided
        '''
        self.game['name'] = self.nameEdit.text()
        self.game['width'] = self.widthSpin.value()
        self.game['height'] = self.heightSpin.value()
        self.game['board'] = self.boardImgSource.text()
        self.game['preview_image'] = self.previewImgSource.text()
        if self.game['preview_image'] == '': self.game['preview_image'] = None
        self.done(QtWidgets.QMessageBox.Save)

    @QtCore.pyqtSlot()
    def __cancel(self):
        '''Nulls the stored game and returns a cancel message to the caller
        '''
        self.game = None
        self.done(QtWidgets.QMessageBox.Cancel)