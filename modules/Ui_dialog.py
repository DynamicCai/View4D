from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *
from . resources_rc import *

class Ui_pdl(object):
    def setupUi(self, plotDialog):
        if not plotDialog.objectName():
            plotDialog.setObjectName(u"plotDialog")
        plotDialog.resize(400, 300)
        self.gridLayout = QGridLayout(plotDialog)
        self.gridLayout.setObjectName(u"gridLayout")
        self.label_2 = QLabel(plotDialog)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout.addWidget(self.label_2, 0, 1, 1, 1)

        self.label_3 = QLabel(plotDialog)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout.addWidget(self.label_3, 0, 2, 1, 1)

        self.label = QLabel(plotDialog)
        self.label.setObjectName(u"label")

        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)

        self.buttonBox = QDialogButtonBox(plotDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.gridLayout.addWidget(self.buttonBox, 2, 0, 1, 3)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.plotlistWidget = QListWidget(plotDialog)
        self.plotlistWidget.setObjectName(u"plotlistWidget")

        self.horizontalLayout.addWidget(self.plotlistWidget)

        self.xlistWidget = QListWidget(plotDialog)
        self.xlistWidget.setObjectName(u"xlistWidget")

        self.horizontalLayout.addWidget(self.xlistWidget)

        self.listWidget_3 = QListWidget(plotDialog)
        self.listWidget_3.setObjectName(u"listWidget_3")

        self.horizontalLayout.addWidget(self.listWidget_3)


        self.gridLayout.addLayout(self.horizontalLayout, 1, 0, 1, 3)


        self.retranslateUi(plotDialog)
        self.buttonBox.accepted.connect(plotDialog.accept)
        self.buttonBox.rejected.connect(plotDialog.reject)

        QMetaObject.connectSlotsByName(plotDialog)
    # setupUi

    def retranslateUi(self, plotDialog):
        plotDialog.setWindowTitle(QCoreApplication.translate("plotDialog", u"Dialog", None))
        self.label_2.setText(QCoreApplication.translate("plotDialog", u"x Column", None))
        self.label_3.setText(QCoreApplication.translate("plotDialog", u"y Column", None))
        self.label.setText(QCoreApplication.translate("plotDialog", u"Sheet", None))
    # retranslateUi