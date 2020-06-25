# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'designer/Login.ui'
#
# Created by: PyQt5 UI code generator 5.14.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_credentialsDialog(object):
    def setupUi(self, credentialsDialog):
        credentialsDialog.setObjectName("credentialsDialog")
        credentialsDialog.setWindowModality(QtCore.Qt.ApplicationModal)
        credentialsDialog.resize(200, 76)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(credentialsDialog.sizePolicy().hasHeightForWidth())
        credentialsDialog.setSizePolicy(sizePolicy)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        credentialsDialog.setWindowIcon(icon)
        self.formLayout = QtWidgets.QFormLayout(credentialsDialog)
        self.formLayout.setObjectName("formLayout")
        self.emailLabel = QtWidgets.QLabel(credentialsDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.emailLabel.sizePolicy().hasHeightForWidth())
        self.emailLabel.setSizePolicy(sizePolicy)
        self.emailLabel.setObjectName("emailLabel")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.emailLabel)
        self.emailInput = QtWidgets.QLineEdit(credentialsDialog)
        self.emailInput.setObjectName("emailInput")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.emailInput)
        self.passwordLabel = QtWidgets.QLabel(credentialsDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.passwordLabel.sizePolicy().hasHeightForWidth())
        self.passwordLabel.setSizePolicy(sizePolicy)
        self.passwordLabel.setObjectName("passwordLabel")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.passwordLabel)
        self.passwordInput = QtWidgets.QLineEdit(credentialsDialog)
        self.passwordInput.setEchoMode(QtWidgets.QLineEdit.Password)
        self.passwordInput.setObjectName("passwordInput")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.passwordInput)
        self.cancelButton = QtWidgets.QPushButton(credentialsDialog)
        self.cancelButton.setObjectName("cancelButton")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.cancelButton)
        self.loginButton = QtWidgets.QPushButton(credentialsDialog)
        self.loginButton.setObjectName("loginButton")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.loginButton)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.formLayout.setItem(2, QtWidgets.QFormLayout.SpanningRole, spacerItem)

        self.retranslateUi(credentialsDialog)
        QtCore.QMetaObject.connectSlotsByName(credentialsDialog)

    def retranslateUi(self, credentialsDialog):
        _translate = QtCore.QCoreApplication.translate
        credentialsDialog.setWindowTitle(_translate("credentialsDialog", "Log-In"))
        self.emailLabel.setText(_translate("credentialsDialog", "Email:"))
        self.passwordLabel.setText(_translate("credentialsDialog", "Password:"))
        self.cancelButton.setText(_translate("credentialsDialog", "Cancel"))
        self.loginButton.setText(_translate("credentialsDialog", "Log-In"))
import resources_rc
