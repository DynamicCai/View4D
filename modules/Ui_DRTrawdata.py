# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'DRTrawdata.ui'
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
from PySide6.QtWidgets import (QAbstractButton, QApplication, QDialog, QDialogButtonBox,
    QGridLayout, QHBoxLayout, QLabel, QListWidget,
    QListWidgetItem, QSizePolicy, QWidget)

class Ui_DRTrawdata(object):
    def setupUi(self, DRT_rawdata):
        if not DRT_rawdata.objectName():
            DRT_rawdata.setObjectName(u"DRT_rawdata")
        DRT_rawdata.resize(387, 243)
        self.gridLayout = QGridLayout(DRT_rawdata)
        self.gridLayout.setObjectName(u"gridLayout")
        self.label = QLabel(DRT_rawdata)
        self.label.setObjectName(u"label")

        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)

        self.label_2 = QLabel(DRT_rawdata)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout.addWidget(self.label_2, 0, 1, 1, 1)

        self.label_3 = QLabel(DRT_rawdata)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout.addWidget(self.label_3, 0, 2, 1, 1)

        self.buttonBox = QDialogButtonBox(DRT_rawdata)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.gridLayout.addWidget(self.buttonBox, 2, 0, 1, 4)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.plotlistWidget = QListWidget(DRT_rawdata)
        self.plotlistWidget.setObjectName(u"plotlistWidget")

        self.horizontalLayout.addWidget(self.plotlistWidget)

        self.xlistWidget = QListWidget(DRT_rawdata)
        self.xlistWidget.setObjectName(u"xlistWidget")

        self.horizontalLayout.addWidget(self.xlistWidget)

        self.listWidget_3 = QListWidget(DRT_rawdata)
        self.listWidget_3.setObjectName(u"listWidget_3")

        self.horizontalLayout.addWidget(self.listWidget_3)

        self.listWidget = QListWidget(DRT_rawdata)
        self.listWidget.setObjectName(u"listWidget")

        self.horizontalLayout.addWidget(self.listWidget)


        self.gridLayout.addLayout(self.horizontalLayout, 1, 0, 1, 4)

        self.label_4 = QLabel(DRT_rawdata)
        self.label_4.setObjectName(u"label_4")

        self.gridLayout.addWidget(self.label_4, 0, 3, 1, 1)


        self.retranslateUi(DRT_rawdata)
        self.buttonBox.accepted.connect(DRT_rawdata.accept)
        self.buttonBox.rejected.connect(DRT_rawdata.reject)

        QMetaObject.connectSlotsByName(DRT_rawdata)
    # setupUi

    def retranslateUi(self, DRT_rawdata):
        DRT_rawdata.setWindowTitle(QCoreApplication.translate("DRT_rawdata", u"Choose Data", None))
        self.label.setText(QCoreApplication.translate("DRT_rawdata", u"Sheet", None))
        self.label_2.setText(QCoreApplication.translate("DRT_rawdata", u"x col", None))
        self.label_3.setText(QCoreApplication.translate("DRT_rawdata", u"y real col", None))
        self.label_4.setText(QCoreApplication.translate("DRT_rawdata", u"y imag col", None))
    # retranslateUi

