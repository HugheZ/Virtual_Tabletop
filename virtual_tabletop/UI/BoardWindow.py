from PyQt5 import QtWidgets, QtCore

class BoardWindow(QtWidgets.QMdiSubWindow):
    '''A simple wrapper for QMdiSubWindow that provides additional movement functions\n
    with help from: https://riverbankcomputing.com/pipermail/pyqt/2016-August/037895.html
    '''

    def __init__(self, *args, **kwargs):
        super(BoardWindow, self).__init__(*args, **kwargs)
        self.picked = False
    
    def mousePressEvent(self, event):
        '''On press, set this widget to be movable'''
        if event.buttons() == QtCore.Qt.LeftButton:
            self.dragPos = event.globalPos()
            self.picked = True
            event.accept()
    
    def mouseReleaseEvent(self, event):
        '''On release, set to nonmovable if was movable'''
        if event.buttons() == QtCore.Qt.LeftButton and self.picked:
            self.picked = False
            event.accept()
    
    def mouseMoveEvent(self, event):
        '''On mouse move, move if was picked'''
        #TODO:reject if outside parent
        if self.picked:
            self.move(self.pos() + event.globalPos() - self.dragPos)
            self.dragPos = event.globalPos()
            event.accept()