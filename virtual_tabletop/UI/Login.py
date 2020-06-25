from PyQt5 import QtWidgets, QtCore, QtGui
from virtual_tabletop.UI.Login_UI import Ui_credentialsDialog
from typing import Mapping

class LoginDialog(QtWidgets.QDialog, Ui_credentialsDialog):
    '''A simple wrapper for the auto-generated login dialog'''

    def __init__(self, creds: Mapping, *args, **kwargs):
        super(LoginDialog, self).__init__(*args, **kwargs)
        self.creds = creds

        self.setupUi(self)

        #diable sign-in by default
        self.loginButton.setEnabled(False)

        #validation, adapted from https://www.walletfox.com/course/qlineeditemailvalidation.php
        expression = QtCore.QRegularExpression("\\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\\.[A-Z]{2,4}\\b",
                          QtCore.QRegularExpression.CaseInsensitiveOption)
        self.emailInput.setValidator(QtGui.QRegularExpressionValidator(expression, self))

        #connect validation
        self.emailInput.textChanged.connect(self.__validate)
        self.passwordInput.textChanged.connect(self.__validate)
        self.loginButton.clicked.connect(self.__login)
        self.cancelButton.clicked.connect(self.__cancel)
    
    @QtCore.pyqtSlot(str)
    def __validate(self, text:str):
        '''Validates the text boxes for enabling the sign-in button'''
        if self.emailInput.hasAcceptableInput() and self.passwordInput.text() != '':
            self.loginButton.setEnabled(True)
        else:
            self.loginButton.setEnabled(False)
    
    @QtCore.pyqtSlot()
    def __login(self):
        '''Logs in by sending confirm signal and saving data to creds'''
        self.creds['email'] = self.emailInput.text()
        self.creds['password'] = self.passwordInput.text()
        self.done(QtWidgets.QMessageBox.Ok)

    @QtCore.pyqtSlot()
    def __cancel(self):
        '''Cancels the log in dialog'''
        self.creds = None
        self.done(QtWidgets.QMessageBox.Cancel)