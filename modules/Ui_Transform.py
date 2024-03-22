# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Transform.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QDialog, QGroupBox,
    QLabel, QPushButton, QSizePolicy, QVBoxLayout,
    QWidget)

class Ui_Transform(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(250, 234)
        self.verticalLayout = QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.groupBox = QGroupBox(Dialog)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setStyleSheet(u"QGroupBox\n"
"{\n"
"border: 1px solid black;\n"
"}")
        self.verticalLayout_2 = QVBoxLayout(self.groupBox)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.label_8 = QLabel(self.groupBox)
        self.label_8.setObjectName(u"label_8")

        self.verticalLayout_2.addWidget(self.label_8)

        self.label = QLabel(self.groupBox)
        self.label.setObjectName(u"label")
        font = QFont()
        font.setBold(True)
        self.label.setFont(font)

        self.verticalLayout_2.addWidget(self.label)

        self.data_type = QComboBox(self.groupBox)
        self.data_type.addItem("")
        self.data_type.addItem("")
        self.data_type.addItem("")
        self.data_type.addItem("")
        self.data_type.setObjectName(u"data_type")
        self.data_type.setEditable(False)

        self.verticalLayout_2.addWidget(self.data_type)

        self.data_used = QComboBox(self.groupBox)
        self.data_used.addItem("")
        self.data_used.addItem("")
        self.data_used.addItem("")
        self.data_used.addItem("")
        self.data_used.setObjectName(u"data_used")

        self.verticalLayout_2.addWidget(self.data_used)

        self.label_2 = QLabel(self.groupBox)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setFont(font)

        self.verticalLayout_2.addWidget(self.label_2)

        self.mark_data = QPushButton(self.groupBox)
        self.mark_data.setObjectName(u"mark_data")

        self.verticalLayout_2.addWidget(self.mark_data)

        self.label_show = QLabel(self.groupBox)
        self.label_show.setObjectName(u"label_show")

        self.verticalLayout_2.addWidget(self.label_show)

        self.transformButton = QPushButton(self.groupBox)
        self.transformButton.setObjectName(u"transformButton")

        self.verticalLayout_2.addWidget(self.transformButton)


        self.verticalLayout.addWidget(self.groupBox)


        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"TIDRT", None))
        self.groupBox.setTitle("")
        self.label_8.setText(QCoreApplication.translate("Dialog", u"Tranformation by Intermediate DRT", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"Data Type", None))
        self.data_type.setItemText(0, QCoreApplication.translate("Dialog", u"Dielectric Permittivity", None))
        self.data_type.setItemText(1, QCoreApplication.translate("Dialog", u"Impedance", None))
        self.data_type.setItemText(2, QCoreApplication.translate("Dialog", u"Electric Modulus", None))
        self.data_type.setItemText(3, QCoreApplication.translate("Dialog", u"Admittance", None))

        self.data_used.setItemText(0, QCoreApplication.translate("Dialog", u"Time to Frequency", None))
        self.data_used.setItemText(1, QCoreApplication.translate("Dialog", u"Complex Frequency to Time", None))
        self.data_used.setItemText(2, QCoreApplication.translate("Dialog", u"Real Frequency to Time", None))
        self.data_used.setItemText(3, QCoreApplication.translate("Dialog", u"Imaginary Frequency to Time", None))

        self.label_2.setText(QCoreApplication.translate("Dialog", u"Data Used", None))
        self.mark_data.setText(QCoreApplication.translate("Dialog", u"Import Data", None))
        self.label_show.setText(QCoreApplication.translate("Dialog", u"------", None))
        self.transformButton.setText(QCoreApplication.translate("Dialog", u"Transform", None))
    # retranslateUi

