# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'DRT.ui'
##
## Created by: Qt User Interface Compiler version 6.5.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QComboBox, QDialog, QGridLayout,
    QGroupBox, QLabel, QLineEdit, QPushButton,
    QSizePolicy, QVBoxLayout, QWidget)

class Ui_DRT(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(388, 348)
        self.gridLayout = QGridLayout(Dialog)
        self.gridLayout.setObjectName(u"gridLayout")
        self.groupBox = QGroupBox(Dialog)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setStyleSheet(u"QGroupBox\n"
"{\n"
"border: 1px solid black;\n"
"}")
        self.verticalLayout = QVBoxLayout(self.groupBox)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label_8 = QLabel(self.groupBox)
        self.label_8.setObjectName(u"label_8")

        self.verticalLayout.addWidget(self.label_8)

        self.label = QLabel(self.groupBox)
        self.label.setObjectName(u"label")
        font = QFont()
        font.setBold(True)
        self.label.setFont(font)

        self.verticalLayout.addWidget(self.label)

        self.data_type = QComboBox(self.groupBox)
        self.data_type.addItem("")
        self.data_type.addItem("")
        self.data_type.addItem("")
        self.data_type.addItem("")
        self.data_type.setObjectName(u"data_type")
        self.data_type.setEditable(False)

        self.verticalLayout.addWidget(self.data_type)

        self.label_2 = QLabel(self.groupBox)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setFont(font)

        self.verticalLayout.addWidget(self.label_2)

        self.data_used = QComboBox(self.groupBox)
        self.data_used.addItem("")
        self.data_used.addItem("")
        self.data_used.addItem("")
        self.data_used.setObjectName(u"data_used")

        self.verticalLayout.addWidget(self.data_used)

        self.mark_data = QPushButton(self.groupBox)
        self.mark_data.setObjectName(u"mark_data")

        self.verticalLayout.addWidget(self.mark_data)

        self.current_data = QPushButton(self.groupBox)
        self.current_data.setObjectName(u"current_data")

        self.verticalLayout.addWidget(self.current_data)

        self.label_show = QLabel(self.groupBox)
        self.label_show.setObjectName(u"label_show")

        self.verticalLayout.addWidget(self.label_show)

        self.label_4 = QLabel(self.groupBox)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setFont(font)

        self.verticalLayout.addWidget(self.label_4)

        self.ind_cap = QComboBox(self.groupBox)
        self.ind_cap.addItem("")
        self.ind_cap.addItem("")
        self.ind_cap.addItem("")
        self.ind_cap.addItem("")
        self.ind_cap.addItem("")
        self.ind_cap.setObjectName(u"ind_cap")

        self.verticalLayout.addWidget(self.ind_cap)

        self.label_9 = QLabel(self.groupBox)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setFont(font)

        self.verticalLayout.addWidget(self.label_9)

        self.removeButton = QPushButton(self.groupBox)
        self.removeButton.setObjectName(u"removeButton")

        self.verticalLayout.addWidget(self.removeButton)


        self.gridLayout.addWidget(self.groupBox, 0, 0, 1, 1)

        self.groupBox_2 = QGroupBox(Dialog)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.groupBox_2.setStyleSheet(u"QGroupBox\n"
"{\n"
"border: 1px solid black\n"
"}")
        self.verticalLayout_2 = QVBoxLayout(self.groupBox_2)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.label_12 = QLabel(self.groupBox_2)
        self.label_12.setObjectName(u"label_12")

        self.verticalLayout_2.addWidget(self.label_12)

        self.label_3 = QLabel(self.groupBox_2)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setFont(font)

        self.verticalLayout_2.addWidget(self.label_3)

        self.discre_method = QComboBox(self.groupBox_2)
        self.discre_method.addItem("")
        self.discre_method.addItem("")
        self.discre_method.setObjectName(u"discre_method")

        self.verticalLayout_2.addWidget(self.discre_method)

        self.label_6 = QLabel(self.groupBox_2)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setFont(font)

        self.verticalLayout_2.addWidget(self.label_6)

        self.reg_par = QLineEdit(self.groupBox_2)
        self.reg_par.setObjectName(u"reg_par")

        self.verticalLayout_2.addWidget(self.reg_par)

        self.label_7 = QLabel(self.groupBox_2)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setFont(font)

        self.verticalLayout_2.addWidget(self.label_7)

        self.reg_deriv = QComboBox(self.groupBox_2)
        self.reg_deriv.addItem("")
        self.reg_deriv.addItem("")
        self.reg_deriv.setObjectName(u"reg_deriv")

        self.verticalLayout_2.addWidget(self.reg_deriv)

        self.label_11 = QLabel(self.groupBox_2)
        self.label_11.setObjectName(u"label_11")
        self.label_11.setFont(font)

        self.verticalLayout_2.addWidget(self.label_11)

        self.rbf_shape = QComboBox(self.groupBox_2)
        self.rbf_shape.addItem("")
        self.rbf_shape.addItem("")
        self.rbf_shape.setObjectName(u"rbf_shape")

        self.verticalLayout_2.addWidget(self.rbf_shape)

        self.label_10 = QLabel(self.groupBox_2)
        self.label_10.setObjectName(u"label_10")
        self.label_10.setFont(font)

        self.verticalLayout_2.addWidget(self.label_10)

        self.coeff_edit = QLineEdit(self.groupBox_2)
        self.coeff_edit.setObjectName(u"coeff_edit")

        self.verticalLayout_2.addWidget(self.coeff_edit)

        self.simple_run = QPushButton(self.groupBox_2)
        self.simple_run.setObjectName(u"simple_run")
        self.simple_run.setCheckable(False)

        self.verticalLayout_2.addWidget(self.simple_run)


        self.gridLayout.addWidget(self.groupBox_2, 0, 1, 1, 1)


        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"compute DRT", None))
        self.groupBox.setTitle("")
        self.label_8.setText(QCoreApplication.translate("Dialog", u"Data Options", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"Data Type", None))
        self.data_type.setItemText(0, QCoreApplication.translate("Dialog", u"Impedance", None))
        self.data_type.setItemText(1, QCoreApplication.translate("Dialog", u"Dielectric Permittivity", None))
        self.data_type.setItemText(2, QCoreApplication.translate("Dialog", u"Electric Modulus", None))
        self.data_type.setItemText(3, QCoreApplication.translate("Dialog", u"Admitance", None))

        self.label_2.setText(QCoreApplication.translate("Dialog", u"Data Used", None))
        self.data_used.setItemText(0, QCoreApplication.translate("Dialog", u"Complex Data", None))
        self.data_used.setItemText(1, QCoreApplication.translate("Dialog", u"Real Part Data", None))
        self.data_used.setItemText(2, QCoreApplication.translate("Dialog", u"Imaginary Part Data", None))

        self.mark_data.setText(QCoreApplication.translate("Dialog", u"New Data", None))
        self.current_data.setText(QCoreApplication.translate("Dialog", u"Current Data", None))
        self.label_show.setText(QCoreApplication.translate("Dialog", u"------", None))
        self.label_4.setText(QCoreApplication.translate("Dialog", u"Fitting with Artifact", None))
        self.ind_cap.setItemText(0, QCoreApplication.translate("Dialog", u"n=0", None))
        self.ind_cap.setItemText(1, QCoreApplication.translate("Dialog", u"n=1; j", None))
        self.ind_cap.setItemText(2, QCoreApplication.translate("Dialog", u"n=-1; j", None))
        self.ind_cap.setItemText(3, QCoreApplication.translate("Dialog", u"n=2", None))
        self.ind_cap.setItemText(4, QCoreApplication.translate("Dialog", u"n=-2", None))

        self.label_9.setText(QCoreApplication.translate("Dialog", u"Removes Negatives", None))
        self.removeButton.setText(QCoreApplication.translate("Dialog", u"Remove", None))
        self.groupBox_2.setTitle("")
        self.label_12.setText(QCoreApplication.translate("Dialog", u"Method Settings", None))
        self.label_3.setText(QCoreApplication.translate("Dialog", u"Discretization Method", None))
        self.discre_method.setItemText(0, QCoreApplication.translate("Dialog", u"Guassian", None))
        self.discre_method.setItemText(1, QCoreApplication.translate("Dialog", u"Piecewise Linear", None))

        self.label_6.setText(QCoreApplication.translate("Dialog", u"Regularization Parameter", None))
        self.reg_par.setText(QCoreApplication.translate("Dialog", u"0.001", None))
        self.label_7.setText(QCoreApplication.translate("Dialog", u"Regularization Derivatives", None))
        self.reg_deriv.setItemText(0, QCoreApplication.translate("Dialog", u"1st order", None))
        self.reg_deriv.setItemText(1, QCoreApplication.translate("Dialog", u"2nd order", None))

        self.label_11.setText(QCoreApplication.translate("Dialog", u"RBF Shape Control", None))
        self.rbf_shape.setItemText(0, QCoreApplication.translate("Dialog", u"FWHM Coefficient", None))
        self.rbf_shape.setItemText(1, QCoreApplication.translate("Dialog", u"Shape Factor", None))

        self.label_10.setText(QCoreApplication.translate("Dialog", u"Shape Coefficient", None))
        self.coeff_edit.setText(QCoreApplication.translate("Dialog", u"0.5", None))
        self.simple_run.setText(QCoreApplication.translate("Dialog", u"Simple Run", None))
    # retranslateUi

