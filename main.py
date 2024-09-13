# ///////////////////////////////////////////////////////////////
#
# BY: DYNAMIC_CAI
# PROJECT MADE WITH: Qt Designer and PySide6
# V: 1.0.0
#
# This project can be used freely for all uses, as long as they maintain the
# respective credits only in the Python scripts, any information in the visual
# interface (GUI) can be modified without any implication.
#
# There are limitations on Qt licenses if you want to use your products
# commercially, I recommend reading them on the official website:
# https://doc.qt.io/qtforpython/licenses.html
#
# ///////////////////////////////////////////////////////////////

import sys
import os
import re
from typing import Any, Dict, Optional
from PySide6.QtCore import QModelIndex, QPersistentModelIndex, Qt
from PySide6.QtGui import QCloseEvent
from PySide6.QtWidgets import QWidget
import numpy as np
from typing import Union
from lmfit import Parameters, minimize

# IMPORT / GUI AND MODULES AND WIDGETS
# ///////////////////////////////////////////////////////////////
from modules import *
from widgets import *
import pyqtgraph as pg

# os.environ["QT_FONT_DPI"] = "96" # FIX Problem for High DPI and Scale above 100%
os.environ["QT_ENABLE_HIGHDPI_SCALING"] = "1"
QApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
## Switch to using white background and black foreground
pg.setConfigOption('background', 'w')
pg.setConfigOption('foreground', 'k')
## The following plot has inverted colors

# IMPORT / GUI AND MODULES AND WIDGETS
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# SET AS GLOBAL WIDGETS
# ///////////////////////////////////////////////////////////////
widgets = None

class MainWindow(QMainWindow):
    sheetcount = 0
    graphcount = 0
    DRTcount = 0
    activatesheetwindow = Signal(object)
    listdict = dict()
    def __init__(self):
        QMainWindow.__init__(self)
        # SET AS GLOBAL WIDGETS
        # ///////////////////////////////////////////////////////////////
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        global widgets
        widgets = self.ui
        self.DRTwidget = DRTwindow(self)
        self.TIDRT = transform_window(self)
        global FITwidget
        FITwidget = CurveFitWindow(self)
        widgets.mdiArea.subWindowActivated.connect(self.toolshowornot)
        # USE CUSTOM TITLE BAR | USE AS "False" FOR MAC OR LINUX
        # ///////////////////////////////////////////////////////////////
        Settings.ENABLE_CUSTOM_TITLE_BAR = True

        # TOGGLE MENU
        # ///////////////////////////////////////////////////////////////
        widgets.toggleButton.clicked.connect(lambda: UIFunctions.toggleMenu(self, True))

        # SET UI DEFINITIONS
        # ///////////////////////////////////////////////////////////////
        UIFunctions.uiDefinitions(self)

        # QListWidget PARAMETERS
        # ///////////////////////////////////////////////////////////////

        # BUTTONS CLICK
        # ///////////////////////////////////////////////////////////////

        # LEFT MENUS
        widgets.btn_home.clicked.connect(self.buttonClick)
        widgets.btn_widgets.clicked.connect(self.buttonClick)
        widgets.btn_import.clicked.connect(self.buttonClick)
        widgets.btn_save.clicked.connect(self.buttonClick)
        widgets.btn_fit.clicked.connect(self.buttonClick)
        widgets.btn_transform.clicked.connect(self.buttonClick)

        # EXTRA LEFT BOX
        widgets.btn_sheet.clicked.connect(self.buttonClick)
        widgets.btn_graph.clicked.connect(self.buttonClick)
        widgets.btn_plot.clicked.connect(self.buttonClick)
        def openCloseLeftBox():
            UIFunctions.toggleLeftBox(self, True)
        widgets.toggleLeftBox.clicked.connect(openCloseLeftBox)
        widgets.extraCloseColumnBtn.clicked.connect(openCloseLeftBox)
        widgets.listWidget.itemDoubleClicked.connect(self.listitemclick)
        # EXTRA RIGHT BOX
        def openCloseRightBox():
            UIFunctions.toggleRightBox(self, True)
        widgets.settingsTopBtn.clicked.connect(openCloseRightBox)

        # SHOW APP
        # ///////////////////////////////////////////////////////////////
        self.show()

        # SET CUSTOM THEME
        # ///////////////////////////////////////////////////////////////
        useCustomTheme = True
        themeFile = "themes\py_dracula_light.qss"

        # SET THEME AND HACKS
        if useCustomTheme:
            # LOAD AND APPLY STYLE
            UIFunctions.theme(self, themeFile, True)

            # SET HACKS
            AppFunctions.setThemeHack(self)

    # SHEET ACTION
    # ///////////////////////////////////////////////////////////////
    def subwindowaction(self,text):
        if text.text() == 'Cascade':
            self.mdi.cascadeSubWindows()
        if text.text() == 'Tile':
            self.mdi.tileSubWindow()

    def generatesheet(self,model,name):
        # GENERATE NEW LISTITEM
        item = CustomListWidgetItem(name)
        widgets.listWidget.addItem(item)
        icon = QIcon(u":/icons2/images/icons2/table--pencil.png")
        item.setIcon(icon)
        # GENERATE NEW SHEET
        sub = SubWindow('Sheet')
        item.setData(11,1)
        item.setData(Qt.UserRole,sub)
        sub.setWindowTitle(name)
        widgets.mdiArea.addSubWindow(sub)
        # GENERATE VIEW LAYER
        sub.model = model
        sub.table = QTableView()
        sub.table.setModel(sub.model)
        sub.setWidget(sub.table)
        # MainWindow.listdict[name] = ['Sheet',sub, sub.model]
        sub.show()
        widgets.listWidget.sortItems()

    # QListWidget ACTION
    # ///////////////////////////////////////////////////////////////
        
    def toolshowornot(self, sub):
        if not sub == None:
            if sub._windowtype != 'Graph':
                FITwidget.hide()
            else:
                self.DRTwidget.hide()

    def listitemclick(self,item: QListWidgetItem):
        sub: QMdiSubWindow = item.data(Qt.UserRole)
        if not sub.isVisible():
            sub.show()
        widgets.mdiArea.setActiveSubWindow(sub)
        """
        widgets.mdiArea.setActiveSubWindow(MainWindow.listdict[item.text()][1])
        MainWindow.listdict[item.text()][1].show()
        """
    
    # GRAPH ACTIONS
    # ///////////////////////////////////////////////////////////////

    def createDRTpanel(self,data=None,data_type=None):
        MainWindow.DRTcount +=1
        item = CustomListWidgetItem('DRT'+str(MainWindow.DRTcount))
        widgets.listWidget.addItem(item)
        icon = QIcon(u":/icons2/images/icons2/robot.png")
        item.setIcon(icon)
        # GENERATE NEW GRAPH
        sub = SubWindow('DRT')
        item.setData(11,3)
        item.setData(Qt.UserRole,sub)
        sub.setWindowTitle('DRT'+str(MainWindow.DRTcount))
        widgets.mdiArea.addSubWindow(sub)
        widgets.listWidget.sortItems()

        sub.tab1 = QWidget()
        sub.tab1layout = QVBoxLayout()
        sub.graphwidget1 = pg.PlotWidget()
        sub.graphwidget1.showGrid(x=True, y=True, alpha=0.5)
        sub.tab1layout.addWidget(sub.graphwidget1)
        sub.tab1.setLayout(sub.tab1layout)

        sub.tab2 = QWidget()
        sub.tab2layout = QVBoxLayout()
        sub.graphwidget2 = pg.PlotWidget()
        sub.graphwidget2.showGrid(x=True, y=True, alpha=0.5)
        sub.graphwidget2.setLogMode(x=True,y=False)
        sub.tab2layout.addWidget(sub.graphwidget2)
        sub.tab2.setLayout(sub.tab2layout)
        
        sub.tab3 = QWidget()
        sub.tab3layout = QVBoxLayout()
        sub.graphwidget3 = pg.PlotWidget()
        sub.graphwidget3.showGrid(x=True, y=True, alpha=0.5)
        sub.graphwidget3.setLogMode(x=True,y=False)
        sub.tab3layout.addWidget(sub.graphwidget3)
        sub.tab3.setLayout(sub.tab3layout)

        sub.tab4 = QWidget()
        sub.tab4layout = QVBoxLayout()
        sub.graphwidget4 = pg.PlotWidget()
        sub.graphwidget4.showGrid(x=True, y=True, alpha=0.5)
        sub.graphwidget4.setLogMode(x=True,y=False)
        sub.tab4layout.addWidget(sub.graphwidget4)
        sub.tab4.setLayout(sub.tab4layout)

        sub.tab5 = QWidget()
        sub.tab5layout = QVBoxLayout()
        sub.graphwidget5 = pg.PlotWidget()
        sub.graphwidget5.showGrid(x=True, y=True, alpha=0.5)
        sub.tab5layout.addWidget(sub.graphwidget5)
        sub.tab5.setLayout(sub.tab5layout)

        sub.tab6 = QWidget()
        sub.tab6layout = QVBoxLayout()
        sub.graphwidget6 = pg.PlotWidget()
        sub.graphwidget6.showGrid(x=True, y=True, alpha=0.5)
        sub.tab6layout.addWidget(sub.graphwidget6)
        sub.tab6.setLayout(sub.tab6layout)

        tab = QTabWidget()
        tab.addTab(sub.tab1,'Nyquist')
        tab.addTab(sub.tab2,'Re Part')
        tab.addTab(sub.tab3,'Im Part')
        tab.addTab(sub.tab4,'DRT')
        tab.addTab(sub.tab5,'Re Res')
        tab.addTab(sub.tab6,'Im Res')

        sub.setWidget(tab)
        sub.show()
        # MainWindow.listdict['DRT'+str(MainWindow.DRTcount)] = ['DRT',sub,data]
        self.DRTwidget.sub.append(sub)

        self.DRTwidget.label_show.setText(item.text())
        self.DRTwidget.label_show.setStyleSheet('color: green')

        pen=pg.mkPen(color=(255,0,0),width=6)
        if data_type == 'Impedance' or data_type == 'Dielectric Permittivity':
            sub.graphwidget1.plot(data.Z_prime,-data.Z_double_prime,pen=pen,symbolBrush=(255,0,0))
            sub.graphwidget2.plot(data.freq,data.Z_prime,pen=pen,symbolBrush=(255,0,0))
            sub.graphwidget3.plot(data.freq,-data.Z_double_prime,pen=pen,symbolBrush=(255,0,0))
        elif data_type == 'Electric Modulus':
            sub.graphwidget1.plot(data.Z_prime,data.Z_double_prime,pen=pen,symbolBrush=(255,0,0))
            sub.graphwidget2.plot(data.freq,data.Z_prime,pen=pen,symbolBrush=(255,0,0))
            sub.graphwidget3.plot(data.freq,data.Z_double_prime,pen=pen,symbolBrush=(255,0,0))

    def generategraph(self,model,xcol,ycol):
        MainWindow.graphcount += 1
        item = CustomListWidgetItem('Graph'+str(MainWindow.graphcount))
        widgets.listWidget.addItem(item)
        icon = QIcon(u":/icons2/images/icons2/chart--pencil.png")
        item.setIcon(icon)
        # GENERATE NEW GRAPH
        sub = SubWindow('Graph')
        item.setData(11,2)
        item.setData(Qt.UserRole,sub)
        sub.setWindowTitle('Graph'+str(MainWindow.graphcount))
        widgets.mdiArea.addSubWindow(sub)
        # Set layout
        sub.show()
        widgets.listWidget.sortItems()

    # BUTTONS CLICK
    # Post here your functions for clicked buttons
    # ///////////////////////////////////////////////////////////////    

    def buttonClick(self):
        # GET BUTTON CLICKED
        btn = self.sender()
        btnName = btn.objectName()

        # SHOW HOME PAGE
        if btnName == "btn_home":
            pass

        # SHOW WIDGETS PAGE
        if btnName == "btn_widgets":
            if not self.DRTwidget.isVisible():
                self.DRTwidget.show()
            if FITwidget.isVisible():
                FITwidget.hide()
 
        if btnName == "btn_import":
            filename = QFileDialog.getOpenFileNames(None, 'import file', '.', 'ASCII file(*.txt *.csv *.dat)')
            for name in filename[0]:
                data = self.readdata(name)
                model = TableModel(data)
                # model.setHorizontalHeaderLabels(['a','b','c'])
                dirStr, ext = os.path.splitext(name)
                file = dirStr.split('/')[-1]
                for row in range(widgets.listWidget.count()):
                    item = widgets.listWidget.item(row)
                    if item.text() == file:
                        return None
                # 获取文件名
                self.generatesheet(model,file)

        if btnName == "btn_sheet":
            MainWindow.sheetcount += 1
            name = 'Sheet'+str(MainWindow.sheetcount)
            # GENERATE MODEL LAYER
            data = np.full([10,3],np.nan)
            model = TableModel(data)
            self.generatesheet(model,name)
        
        if btnName == "btn_graph":
            # GENERATE NEW LISTITEM
            self.generategraph(model=None,xcol=None,ycol=None)

        if btnName == "btn_plot":
            #if MainWindow.listdict[widgets.mdiArea.activeSubWindow().windowTitle()][0] == "Graph":
            sub = widgets.mdiArea.activeSubWindow()
            if sub != None:
                if sub._windowtype == 'Graph':
                    pdlgwidget = plotDialog(sub,self)
                    items = [widgets.listWidget.item(x) for x in range(widgets.listWidget.count())]
                    for item in items:
                        if item.data(11) == 1:  #if MainWindow.listdict[item][0] == "Sheet":
                            pdlgwidget.plotlistWidget.addItem(item.text())
                    pdlgwidget.exec()

        if btnName == "btn_save":
            print("Save BTN clicked!")

        if btnName == "btn_fit":
            if not FITwidget.isVisible():
                sub = widgets.mdiArea.activeSubWindow()
                if sub != None:
                    if sub._windowtype == 'Graph':
                        FITwidget.show()
                        for s in widgets.mdiArea.subWindowList():
                            if s._windowtype == 'Graph':
                                s.refreshplotwidget(s.graph)
            if self.DRTwidget.isVisible():
                self.DRTwidget.hide()

        if btnName == "btn_transform":
            self.TIDRT.show()

    def readdata(self, name):
        datalist = list()
        with open(name, 'r') as f:
            for line in f:
                line = line.strip()
                if re.match(r'\s*\d',line) is not None: # 检查每一行开头是否为“空格+数字”
                    splitline = re.split(r'[;,\s]\s*',line)
                    if splitline[0] == '':
                        splitline.remove('')
                    splitline = [float(i) for i in splitline]
                    datalist.append(splitline)
        data = np.array(datalist)
        return data

    # RESIZE EVENTS
    # ///////////////////////////////////////////////////////////////
    def resizeEvent(self, event):
        # Update Size Grips
        UIFunctions.resize_grips(self)

    # MOUSE CLICK EVENTS
    # ///////////////////////////////////////////////////////////////

    def mousePressEvent(self, event):
        # SET DRAG POS WINDOW
        self.dragPos = event.globalPos()

        # PRINT MOUSE EVENTS
        if event.buttons() == Qt.LeftButton:
            print('Mouse click: LEFT CLICK')
        if event.buttons() == Qt.RightButton:
            print('Mouse click: RIGHT CLICK')

    def closeEvent(self, event):
        msgBox = QMessageBox()
        msgBox.setWindowTitle('提示')
        msgBox.setText('是否要关闭所有窗口？')
        msgBox.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        reply = msgBox.exec()
        if reply == QMessageBox.Yes:
            event.accept()
            sys.exit(0)
        else:
            event.ignore()

class CustomPlotDataItem(pg.PlotDataItem):
    def __init__(self, title=None, key=None, params=None, parentgraph=None, document=None, 
                 model=None, *args, **kargs):
        super().__init__(*args, **kargs)
        self.dragIndex = -1
        self.parentgraph = parentgraph
        self.document = document
        self.model:ParameterModel = model
        self.key = key
        self.title = title
        self.x = None
        self.y = None
        self.parvals = None

    def boundingRect(self):
        return self.scatter.boundingRect()

    def mouseDragEvent(self, ev):
        if ev.button() != Qt.LeftButton:
            ev.ignore()
            return

        if ev.isStart():

            self.parvals = self.model.modeldict[self.title].copy()
            pos = ev.buttonDownPos()
            pts = self.scatter.pointsAt(pos)

            if len(pts) > 0:
                self.dragIndex = self.scatter.points().tolist().index(pts[0])
                self.dragOffset = pts[0].pos() - pos
                # self.startPosition = pts[0].pos()
                ev.accept()
                self.x, self.y = self.getData()
                vb = self.getViewBox()
                if vb.state['logMode'][0] == True:
                    self.x = 10 ** self.x
                if vb.state['logMode'][1] == True:
                    self.y = 10 ** self.y

        elif ev.isFinish():
            # record changed params
            self.model.update_params()
            self.parvals = None
            self.dragIndex = -1
            self.dragOffset = 0
            self.x = None
            self.y = None
            # self.enableAutoRange(axis='x')
            # self.parentgraph.enableAutoRange(axis='x')
            return
        
        else:
            # update the curve
            newpos = ev.pos() + self.dragOffset
            xn, yn = newpos.x(), newpos.y()
            x0, y0 = self.x[self.dragIndex], self.y[self.dragIndex]

            vb = self.getViewBox()
            if vb.state['logMode'][0] == True:
                xn = 10 ** xn
            if vb.state['logMode'][1] == True:
                yn = 10 ** yn

            # get params
            kwargs = {}
            kwargs['x'], kwargs['y'], kwargs['xn'], kwargs['yn'] = x0, y0, xn, yn
            for index in range(len(self.parvals['pars'])):
                kwargs[self.parvals['pars'][index]] = float(self.parvals['values'][index])

            # compute move
            move = getattr(FITwidget, self.key+'_move')(**kwargs)
            self.model.modeldict[self.title]['values'] = move
            self.model.setselfmodel()

            # compute curve
            # y1 = getattr(FITwidget, self.key)(self.x,move,'imag')
            # self.setData(self.x,y1)
            y_sum = np.zeros(np.shape(self.x))
            for title,key,curve in zip(self.model.titlelist, self.model.keylist, self.model.curves):
                pars = self.model.modeldict[title]['values']
                pars = [float(p) for p in pars]
                y = getattr(FITwidget, key)(self.x,pars,comp=self.model.parentsub.comp)
                y_sum = y + y_sum
                curve.setData(self.x,y)
            self.model.sumcurve.setData(self.x,y_sum)

class CustomListWidgetItem(QListWidgetItem):
    def __lt__(self, other):
        try:
            return self.data(11) < other.data(11)
        except Exception:
            return QListWidgetItem.__lt__(self, other)

class SubWindow(QMdiSubWindow):
    def __init__(self, _windowtype: str):
        super().__init__()
        self._windowtype = _windowtype
        self.setgraphwindow()
        self.windowStateChanged.connect(self.refreshfitmodel)

    def closeEvent(self, event):
        event.ignore()
        self.hide()

    def setgraphwindow(self):
        if self._windowtype == 'Graph':
            self.datalist = QListWidget()
            self.datalist.itemChanged.connect(self.refreshdatalist)
            self.graph = pg.PlotWidget()
            self.graph.disableAutoRange(axis='x')
            self.graph.showGrid(x=True, y=True, alpha=0.5)
            self.graph.setLabel('left','Y Axis')
            self.graph.setLabel('bottom','X Axis')
            self.graphlayout = QHBoxLayout()
            self.graphlayout.addWidget(self.graph)
            self.graphlayout.addWidget(self.datalist)
            self.g = QWidget()
            self.g.setLayout(self.graphlayout)
            self.setWidget(self.g)
            self.comp = 'imag'
            self.fitmodel = ParameterModel(self)
            self.graph.sigRangeChanged.connect(self.refreshplotwidget)
    """
    def refreshdatalist(self):
        self.FitWidget.datawidget.clear()
        for index in range(self.datalist.count()): 
            item = self.datalist.item(index)
            if item.checkState() == Qt.Checked:
                newitem = QListWidgetItem(item.text())
                self.FitWidget.datawidget.addItem(newitem)
                newitem.setData(Qt.UserRole, item)
    """
    def refreshdatalist(self):
        FITwidget.datatree.clear()
        for index in range(self.datalist.count()):
            item = self.datalist.item(index)
            if item.checkState() == Qt.Checked:
                newchild = QTreeWidgetItem(FITwidget.datatree)
                newchild.setText(0,item.text())
                newchild.setText(1,'')
                newchild.setCheckState(1,Qt.Checked)
                newchild.setData(1, Qt.UserRole, item.data(Qt.UserRole))

    def refreshfitmodel(self, oldstate, newstate):
        if self._windowtype == 'Graph':
            if newstate == Qt.WindowActive:
                FITwidget.refreshfitwindow(self.fitmodel)
                FITwidget.sub = self
                self.refreshdatalist()

    def refreshplotwidget(self, g):
        g.disableAutoRange(axis='x')
        xRange = g.viewRange()[0]
        vb = g.getViewBox()

        if FITwidget.isVisible():
            if vb.state['logMode'][0] == True:
                x = np.logspace(xRange[0],xRange[1],num=250)
            else:
                x = np.linspace(xRange[0],xRange[1],num=500)
            y_sum = np.zeros(np.shape(x))
            for title,key,curve in zip(self.fitmodel.titlelist, self.fitmodel.keylist, self.fitmodel.curves):
                pars = self.fitmodel.modeldict[title]['values']
                pars = [float(p) for p in pars]
                y = getattr(FITwidget, key)(x,pars,comp=self.comp)
                y_sum = y + y_sum
                curve.setData(x,y)
            self.fitmodel.sumcurve.setData(x,y_sum)

class plotDialog(Ui_pdl,QDialog):
    def __init__(self, sub, parent=None):
        super().__init__(parent)
        self.sub = sub                                          
        self.setupUi(self)
        self.parent = parent
        self.items = []
        self.xitem = []
        self.yitems = []
        self.mincount = int()
        self.minmodel = []
        self.plotlistWidget.setSelectionMode(QAbstractItemView.MultiSelection)
        self.plotlistWidget.itemSelectionChanged.connect(self.index_selected)
        self.listWidget_3.setSelectionMode(QAbstractItemView.MultiSelection)
        self.listWidget_3.itemSelectionChanged.connect(self.yindex_selected)
    def index_selected(self):
        self.xlistWidget.clear()
        self.listWidget_3.clear()
        self.items = self.plotlistWidget.selectedItems()
        if self.items != []:
            count = []
            for item in self.items:
                model = widgets.listWidget.findItems(item.text(), Qt.MatchFlag.MatchExactly)[0].data(Qt.UserRole).model
                #MainWindow.listdict[item.text()][2]
                count.append(model.columnCount(1))
            self.mincount = min(count)
            self.minmodel = widgets.listWidget.findItems(self.items[0].text(), Qt.MatchFlag.MatchExactly)[0].data(Qt.UserRole).model
            #MainWindow.listdict[self.items[0].text()][2]
            for c in range(self.mincount):
                self.xlistWidget.addItem(self.minmodel.columns[c])
                self.listWidget_3.addItem(self.minmodel.columns[c])
    def yindex_selected(self):
        self.yitems = self.listWidget_3.selectedItems()
        self.sequence = []
        if self.yitems != []:
            for c in range(self.mincount):
                for item in self.yitems:
                    if self.minmodel.columns[c] == item.text():
                        self.sequence.append(c)
    def accept(self):
        xcol = self.xlistWidget.currentRow()
        ycol = self.sequence

        if (self.items != []) and (self.yitems != []):
            if xcol != -1:
                for item in self.items:
                    model: TableModel = widgets.listWidget.findItems(item.text(), Qt.MatchFlag.MatchExactly)[0].data(Qt.UserRole).model
                    #MainWindow.listdict[item.text()][2]
                    #self.plotdata(model=model,xcol=xcol,ycol=ycol,sub=self.sub)
                    pen=pg.mkPen(color=(255,0,0),width=3)
                    self.sub.graph.setLogMode(x=True, y=False)
                    self.sub.graph.disableAutoRange(axis='x')
                    data = model._data
                    x = data[:,xcol]
                    for yi in ycol:
                        y = data[:,yi]
                        newplot = self.sub.graph.plot(x,y,pen=pen, symbolSize=6, symbolBrush=(255,0,0))
                        model.plotted_data.append((newplot,xcol,yi))
                        newitem = QListWidgetItem(f'{model.columns[yi]}({model.columns[xcol]}) - {item.text()}')
                        self.sub.datalist.addItem(newitem)
                        newitem.setData(Qt.UserRole,(model,xcol,yi))
                        newitem.setCheckState(Qt.Unchecked)
        self.close()
    '''
    def plotdata(self,model,xcol,ycol,sub):
        pen=pg.mkPen(color=(255,0,0),width=6)
        sub.graph.setLogMode(x=True, y=False)
        sub.graph.disableAutoRange(axis='x')
        if model is not None:
            data = model._data
            x = data[:,xcol]
            for i in ycol:
                y = data[:,i]
                sub.graph.plot(x,y,pen=pen, symbolSize=10, symbolBrush=(255,0,0))
    '''

class DRTrawdataDialog(Ui_DRTrawdata,QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.parent = parent
        self.items = []
        self.xitem = []
        self.model = []
        self.realcol = None
        self.imagcol = None
        self.mincount = int()
        self.minmodel = []
        self.plotlistWidget.setSelectionMode(QAbstractItemView.MultiSelection)
        self.plotlistWidget.itemSelectionChanged.connect(self.index_selected)
        self.listWidget_3.currentItemChanged.connect(self.y1index_selected)
        self.listWidget.currentItemChanged.connect(self.y2index_selected)
    def index_selected(self):
        self.xlistWidget.clear()
        self.listWidget_3.clear()
        self.listWidget.clear()
        self.model = []
        self.items = self.plotlistWidget.selectedItems()
        if self.items != []:
            count = []
            for item in self.items:
                model = widgets.listWidget.findItems(item.text(), Qt.MatchFlag.MatchExactly)[0].data(Qt.UserRole).model
                #MainWindow.listdict[item.text()][2]
                count.append(model.columnCount(1))
                self.model.append(model)
            self.mincount = min(count)
            self.minmodel = self.minmodel = widgets.listWidget.findItems(self.items[0].text(), Qt.MatchFlag.MatchExactly)[0].data(Qt.UserRole).model
            for c in range(self.mincount):
                self.xlistWidget.addItem(self.minmodel.columns[c])
                self.listWidget_3.addItem(self.minmodel.columns[c])
                self.listWidget.addItem(self.minmodel.columns[c])
    def y1index_selected(self,item):
        for c in range(self.mincount):
            if self.minmodel.columns[c] == item.text():
                self.realcol = c
    def y2index_selected(self,item):
        for c in range(self.mincount):
            if self.minmodel.columns[c] == item.text():
                self.imagcol = c
    def accept(self):
        xcol = self.xlistWidget.currentRow()
        if ((self.imagcol is not None)&(self.realcol is not None)):
            if xcol != -1:
                self.parent.model = self.model
                self.parent.xcol = xcol
                self.parent.realcol = self.realcol
                self.parent.imagcol = self.imagcol
                self.parent.initiate_data(model=self.model,xcol=xcol,realcol=self.realcol,imagcol=self.imagcol)
                #for model in self.model:
                    #self.parent.parent.generategraph(model=model,xcol=xcol,ycol=[self.realcol,self.imagcol])
        self.close()

class transform_window(Ui_Transform,QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.parent = parent
        self.setWindowFlag(Qt.Tool)

class DRTwindow(Ui_DRT,QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.parent = parent
        self.model = None
        self.data = []
        self.sub = []
        self.mark_data.clicked.connect(self.mark_data_callback)
        self.simple_run.clicked.connect(self.simple_run_callback)
        self.removeButton.clicked.connect(self.remove_negatives_callback)
        self.setWindowFlag(Qt.Tool)

    def mark_data_callback(self):
        self.label_show.setText('------')
        self.label_show.setStyleSheet('color: black')
        self.data = []
        self.realcol = -1
        self.imagcol = -1
        self.xcol = -1
        self.sub = []
        pdlgwidget = DRTrawdataDialog(self)
        items = [widgets.listWidget.item(x) for x in range(widgets.listWidget.count())]
        for item in items:
            if item.data(11) == 1:  #if MainWindow.listdict[item][0] == "Sheet":
                pdlgwidget.plotlistWidget.addItem(item.text())
        pdlgwidget.exec()

    def remove_negatives_callback(self):
        # read the option
        data_type = str(self.data_type.currentText())
        if self.data == []:
            return
        elif data_type == 'Impedance' or data_type == 'Dielectric Permittivity':
            for data in self.data:
                data.freq = data.freq[data.Z_double_prime>0]
                data.Z_prime = data.Z_prime[-data.Z_double_prime>0]
                data.Z_double_prime = data.Z_double_prime[-data.Z_double_prime>0]
                data.Z_exp = data.Z_double_prime*1j + data.Z_prime
        elif data_type == 'Electric Modulus':
            for data in self.data:
                data.freq = data.freq_0
                data.Z_prime = data.Z_prime_0
                data.Z_double_prime = data.Z_double_prime_0
                data.Z_exp = data.Z_exp_0               

    def initiate_data(self,model,xcol,realcol,imagcol):
        # read the option
        data_type = str(self.data_type.currentText())
        for m in model:
            data = m._data
            freq = data[:,xcol]
            if data_type == 'Impedance':
                Data_exp = data[:,realcol] + 1j*data[:,imagcol]
            if data_type == 'Dielectric Permittivity':
                Data_exp = data[:,realcol] - 1j*data[:,imagcol]
            if data_type == 'Electric Modulus':
                Data_exp = data[:,realcol] + 1j*data[:,imagcol]
            if data_type == 'Admittance':
                Data_exp = data[:,realcol] - 1j*data[:,imagcol]
            Data_prime = np.real(Data_exp)
            Data_double_prime = np.imag(Data_exp)
            eis_data = EIS_object(freq,Data_prime,Data_double_prime)
            self.data.append(eis_data)
            self.parent.createDRTpanel(eis_data,data_type)

    def simple_run_callback(self):
        if self.data is None:
            return
        # read the options
        data_type = str(self.data_type.currentText())
        data_used = str(self.data_used.currentText())
        ind_cap = int(self.ind_cap.currentIndex())
        discre_method = str(self.discre_method.currentText())
        reg_deriv = str(self.reg_deriv.currentText())
        rbf_shape = str(self.rbf_shape.currentText())
        coeff = float(self.coeff_edit.text())
        reg_par = float(self.reg_par.text())

        for data,sub in zip(self.data,self.sub):
            output = simple_run(data, rbf_type=discre_method, data_used=data_used, induct_used=ind_cap, lambda_0=reg_par,
                                  der_used=reg_deriv, shape_control=rbf_shape, coeff=coeff, data_type=data_type)
            pen=pg.mkPen(color=(0,255,0),width=3)
            if data_type == 'Impedance' or data_type == 'Dielectric Permittivity':
                sub.graphwidget1.plot(output.mu_Z_re,-output.mu_Z_im,pen=pen)
                sub.graphwidget2.plot(output.freq,output.mu_Z_re,pen=pen)
                sub.graphwidget3.plot(output.freq,-output.mu_Z_im,pen=pen)

            elif data_type == 'Electric Modulus' or data_type == 'Admittance':
                sub.graphwidget1.plot(output.mu_Z_re,output.mu_Z_im,pen=pen)
                sub.graphwidget2.plot(output.freq,output.mu_Z_re,pen=pen)
                sub.graphwidget3.plot(output.freq,output.mu_Z_im,pen=pen)
            sub.graphwidget4.plot(output.out_tau_vec,output.gamma,pen=pen)
            forsave = np.stack((output.out_tau_vec,output.gamma),axis=1)
            np.savetxt('DRT.txt', forsave)
            """
            computed = np.column_stack((output.out_tau_vec,output.gamma))
            DRT_model = TableModel(computed)
            self.parent.generategraph(model=DRT_model,xcol=0,ycol=[1])
            """

class TableModel(QAbstractTableModel):
    sigdatachanged = Signal(object)
    def __init__(self, data):
        super(TableModel, self).__init__()
        self._data = data
        self.columns = ['col'+str(i) for i in range(data.shape[1])]
        self.row = [str(i) for i in range(data.shape[0])]
        self.plotted_data = []
        self.sigdatachanged.connect(self.changeplotdata)

    def changeplotdata(self,col):
        for r in self.plotted_data:
            if col == r[1] or col == r[2]:
                data_line = r[0]
                data_line.setData(self._data[:,r[1]], self._data[:,r[2]])

    def data(self, index, role):
        if role == Qt.DisplayRole or role == Qt.EditRole:
            # Note: self._data[index.row()][index.column()] will also work
            value = self._data[index.row(), index.column()]
            if str(value) == 'nan':
                return None
            return str(value)
        if role == Qt.ForegroundRole:
            value = self._data[index.row()][index.column()]

            if (
                (isinstance(value, int) or isinstance(value, float))
                and value < 0
            ):
                return QColor('red')

    def rowCount(self, index):
        return self._data.shape[0]

    def columnCount(self, index):
        return self._data.shape[1]
    
    def setData(self, index, value, role):
        if role == Qt.EditRole:
            try:
                value = float(value)
                self._data[index.row(), index.column()] = value
                print(value)
                self.sigdatachanged.emit(index.column())
            except ValueError:
                return False                # self._data[index.row(), index.column()] = np.nan return True
        return False
    
    def flags(self, index):
        return Qt.ItemIsSelectable | Qt.ItemIsEnabled | Qt.ItemIsEditable
    
    def headerData(self, section, orientation, role):
        # section is the index of the column/row.
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return self.columns[section]
            if orientation == Qt.Vertical:
                return self.row[section]

class CurveFitWindow(QMainWindow):
    def __init__(self,parent=None):
        super().__init__(parent)
        self.sub = None
        self.setWindowTitle('Complex Nonlinear Least Squares Fitting')
        self.resize(520,600)
        self.setWindowFlag(Qt.Tool)
        self.setMouseTracking(True)
        menu = self.menuBar()
        functions_menu = menu.addMenu('Add Terms')
        
        settings_menu = QAction('Settings',self)
        menu.addAction(settings_menu)
        settings_menu.triggered.connect(self.MenuButtonClick)

        fit_menu = QAction('Fit',self)
        menu.addAction(fit_menu)
        fit_menu.triggered.connect(self.fitcallback)

        params_menu = QAction('Params',self)
        menu.addAction(params_menu)
        params_menu.triggered.connect(self.MenuButtonClick)

        curves_menu = QAction('Curves',self)
        menu.addAction(curves_menu)
        curves_menu.triggered.connect(self.printfittedcurves)

        close_menu = QAction('Clear',self)
        menu.addAction(close_menu)
        close_menu.triggered.connect(self.MenuButtonClick)
        
        button_action1 = QAction('HN Permittivity',self)
        functions_menu.addAction(button_action1)
        button_action1.triggered.connect(self.AddFunctionsbtnclicked)
        button_action2 = QAction('HN Modulus',self)
        functions_menu.addAction(button_action2)
        button_action2.triggered.connect(self.AddFunctionsbtnclicked)
        button_action3 = QAction('RBM Conductivity',self)
        functions_menu.addAction(button_action3)
        button_action3.triggered.connect(self.AddFunctionsbtnclicked)
        button_action4 = QAction('KWW freq',self)
        functions_menu.addAction(button_action4)
        button_action4.triggered.connect(self.AddFunctionsbtnclicked)
        button_action5 = QAction('Arrhenius',self)
        functions_menu.addAction(button_action5)
        button_action5.triggered.connect(self.AddFunctionsbtnclicked)
        button_action6 = QAction('VFT',self)
        functions_menu.addAction(button_action6)
        button_action6.triggered.connect(self.AddFunctionsbtnclicked)
        button_action7 = QAction('WLF',self)
        functions_menu.addAction(button_action7)
        button_action7.triggered.connect(self.AddFunctionsbtnclicked)
        self.modelview = QTreeView()
        self.modelview.setAlternatingRowColors(True)

        # DATATREE showing marked data
        self.datatree = QTreeWidget()
        self.datatree.setColumnCount(2)
        self.datatree.setHeaderLabels(['Data for Fit','imag?'])
        self.datatree.setMaximumHeight(80)
        self.datatree.header().setSectionResizeMode(0, QHeaderView.Stretch)
        self.datatree.currentItemChanged.connect(self.updatecurves)
        self.datatree.itemChanged.connect(self.checkstatechanged)
        """
        self.datawidget = QListWidget()
        self.datawidget.currentItemChanged.connect(self.checkrealstate)
        self.datawidget.setMaximumHeight(50)
        """
        self.fitlayout = QVBoxLayout()
        self.fitlayout.addWidget(self.modelview)
        self.fitlayout.addWidget(self.datatree)
        self.FITWidgets = QWidget()
        self.FITWidgets.setLayout(self.fitlayout)
        self.setCentralWidget(self.FITWidgets)

        # Functions
        self.HNP = havriliak_negami_permittivity
        self.HNP_move = HNP_move # for move
        self.HNM = havriliak_negami_modulus
        self.HNM_move = HNM_move
        self.VFT = VFT
        self.VFT_move = VFT_move
        self.WLF = WLF
        self.WLF_move = WLF_move

    def MenuButtonClick(self, s):
        print('click', s)

    def printfittedcurves(self):
        sub: SubWindow = widgets.mdiArea.activeSubWindow()
       
        sumx, sumy = sub.fitmodel.sumcurve.xData, sub.fitmodel.sumcurve.yData
        forsave = [sumx, sumy]

        for curve in sub.fitmodel.curves:
            forsave.append(curve.xData)
            forsave.append(curve.yData)

        forsave = np.stack(forsave, axis=1)
        np.savetxt('curves.txt', forsave)

    def checkstatechanged(self, item, col):
        if col == 1 and self.datatree.currentItem() == item:
            sub: SubWindow = widgets.mdiArea.activeSubWindow()
            if item.checkState(1) == Qt.Checked:
                sub.comp = 'imag'
                print('imag')
                sub.refreshplotwidget(sub.graph)
            else:
                sub.comp = 'real'
                print('real')
                sub.refreshplotwidget(sub.graph)

    def updatecurves(self,current):
        sub: SubWindow = widgets.mdiArea.activeSubWindow()
        if current is not None and sub is not None:
            if current.checkState(1) == Qt.Checked:
                sub.comp = 'imag'
                print('imag')
                sub.refreshplotwidget(sub.graph)
            else:
                sub.comp = 'real'
                print('real')
                sub.refreshplotwidget(sub.graph)

    def residual(self, params, model, x, y, ifimag):
        parvals = params.valuesdict()

        n = len(y)
        resid = [0] * n

        for i in range(n):
            comp = ifimag[i]
            final = np.zeros(x[i].size)
            for title,key in zip(model.titlelist,model.keylist):
                pars = []
                modeldict = model.modeldict[title]
                for j in range(len(modeldict['pars'])):
                    pars.append(parvals[title+'_'+modeldict['pars'][j]])
                output = getattr(self, key)(x[i],pars,comp)
                final = final + output

            resid[i] = final - y[i]
        resid = tuple(resid)

        return np.concatenate(resid)

    def fitcallback(self):
        sub: SubWindow = widgets.mdiArea.activeSubWindow()
        model, rootitem = sub.fitmodel, self.datatree.invisibleRootItem()
        ifimag, x, y = [], [], []
        for index in range(rootitem.childCount()):
            item = rootitem.child(index)
            r = item.data(1, Qt.UserRole)
            table, xcol, ycol = r[0], r[1], r[2]
            xi, yi = table._data[:,xcol], table._data[:,ycol]
            x.append(xi)
            y.append(yi)
            if item.checkState(1) == Qt.Checked:
                comp = 'imag'
            else:
                comp = 'real'
            ifimag.append(comp)
        params = model.params
        output = minimize(self.residual, params, args=(model,x,y,ifimag))
        print(output.params)
        print('-------------------------------')
        print('Parameter    Value       Stderr')
        for name, param in output.params.items():
            print(f'{name} {param.value} {param.stderr}')
        
        # update ParameterModel
        child_item = []
        for item in model.titleitem:
            for child in item._children:
                child_item.append(child)
        
        for child, param in zip(child_item, output.params.values()):
            child.set_data(1, param, role=Qt.EditRole)
        
        model.update_params()
        sub.refreshplotwidget(sub.graph)

    def refreshfitwindow(self, fitmodel):
        self.modelview.setModel(fitmodel)
        self.modelview.expandAll()

    def AddFunctionsbtnclicked(self):
        btn = self.sender()
        btnName = btn.text()
        sub = widgets.mdiArea.activeSubWindow()

        if btnName == 'HN Permittivity':
            sub.fitmodel.addafunction('HNP', functions['HNP'])
            
        if btnName == 'HN Modulus':
            sub.fitmodel.addafunction('HNM', functions['HNM'])

        if btnName == 'WLF':
            sub.fitmodel.addafunction('WLF', functions['WLF'])

        if btnName == 'VFT':
            sub.fitmodel.addafunction('VFT', functions['VFT'])
        self.modelview.expandAll()
    
    def hideEvent(self, event: QHideEvent) -> None:
        for sub in widgets.mdiArea.subWindowList():
            if sub._windowtype == 'Graph':
                for curve in sub.fitmodel.curves:
                    curve.setData()
                sub.fitmodel.sumcurve.setData()
        return super().hideEvent(event)
    
class TreeItem:
    def __init__(self, data: list, parent: 'TreeItem' = None):
        self._parent = parent
        self._children = []
        self.item_data = data
        self.checked = 2  
        # self.ifreal = False
    
    def data(self, column: int):
        if column < 0 or column >= len(self.item_data):
            return None
        return self.item_data[column]
    
    def set_data(self, column:int, value, role):
        if column < 0 or column >= len(self.item_data):
            return False
        if role == Qt.EditRole:
            try:
                value = float(value)
                self.item_data[column] = value
            except ValueError:
                return False
        self.item_data[column] = str(value)
        return True

    """
        def setData(self, index, value, role):
        if role == Qt.EditRole:
            try:
                value = float(value)
                self._data[index.row(), index.column()] = value
            except ValueError:
                self._data[index.row(), index.column()] = np.nan
            return True
        return False
    """

    def set_checked(self, value):
        self.checked = value
        return self.checked

    def appendChild(self, item: "TreeItem"):
        """Add item as a child"""
        self._children.append(item)

    def child(self, number: int) -> 'TreeItem':
        if number < 0 or number >= len(self._children):
            return None
        return self._children[number]
    
    def child_count(self) -> int:
        return len(self._children)
    
    def last_child(self):
        return self._children[-1] if self._children else None

    def child_number(self) -> int:
        if self._parent:
            return self._parent._children.index(self)
        return 0
    
    def parent(self):
        return self._parent
    
    def column_count(self) -> int:
        return len(self.column_count)
    
    def insert_children(self, count: int, column: int) -> bool:
        for row in range(count):
            data = [None] * column
            item = TreeItem(data,self)
            self._children.append(item)
        return True

class ParameterModel(QAbstractItemModel):
    def __init__(self, parent):
        super(ParameterModel,self).__init__()
        self.parentsub = parent
        self.headers = ['Name', 'Value', 'Limits','Errors','Vary']
        self._rootItem = TreeItem(self.headers.copy())
        self.titleitem = []
        self.titlelist = []
        self.keylist = []
        self.curves = []
        # modeldict
        """
        self.values = {}
        self.vary = {}
        self.errors = {}
        """
        self.params = Parameters()
        self.modeldict = {}
        self.sumcurve = pg.PlotDataItem(pen=pg.mkPen(color='k',width=5))
        self.sumcurve.setZValue(1)
        # self.sumcurve.tag = 'SUM'
        self.parentsub.graph.addItem(self.sumcurve)

    def update_params(self):
        self.titlelist = []
        for title in self.titleitem:
            pars = []
            values = []
            varys = []
            errors = []
            key = title.data(0)
            for index in range(len(title._children)):
                pars.append(title._children[index].data(0))
                values.append(title._children[index].data(1))
                errors.append(title._children[index].data(3))
                parname = title._children[index].data(0)
                # update self.params
                self.params[key+'_'+parname].value = float(title._children[index].data(1))
                if title._children[index].checked == 2:
                    vary=True
                else:
                    vary=False
                varys.append(vary)
                self.params[key+'_'+parname].vary = vary

            """
            self.values[title.data(0)] = values
            self.vary[title.data(0)] = vary
            self.errors[title.data(0)] = errors
            """
            self.modeldict[key]['pars'] = pars
            self.modeldict[key]['values'] = values
            self.modeldict[key]['vary'] = varys
            self.modeldict[key]['errors'] = errors
            self.titlelist.append(key)

    def setselfmodel(self):
        self.beginResetModel()
        for item in self.titleitem:
            title = item.data(0)
            for kid in range(len(item._children)):
                child_item: TreeItem = item._children[kid]
                child_item.set_data(1, self.modeldict[title]['values'][kid], role=Qt.EditRole)
        self.endResetModel()
        FITwidget.modelview.expandAll()

    def addafunction(self, key:str, document: dict):
        """
        if parent == None:
            self._rootItem = TreeItem.addafunction(key,document,self._rootItem)
        else:
            self._rootItem = TreeItem.addafunction(key,document,parent)
        """
        self.beginResetModel()
        parent = self._rootItem
        parent.insert_children(1,2)
        parent_title: TreeItem = parent.last_child()
        self.titleitem.append(parent_title)
        parent_title.set_data(1, document['name'], role=Qt.DisplayRole)
        self.keylist.append(key)
        index = 0
        for t,k in zip(self.titleitem,self.keylist):
            t.set_data(0, k + f"{index}", role=Qt.DisplayRole)
            self.modeldict.setdefault(k + f"{index}", {})
            index += 1

        rowcount = len(document['pars'])
        parent_title.insert_children(rowcount,5)
        # set children values
        for kid in range(len(parent_title._children)):
            child_item: TreeItem = parent_title._children[kid]
            child_item.set_data(0, document['pars'][kid], role=Qt.DisplayRole)
            child_item.set_data(1, document['value'][kid], role=Qt.EditRole)
            child_item.set_data(2, document['limits'][kid], role=Qt.DisplayRole)
            child_item.set_data(3, '', role=Qt.DisplayRole)
            self.params.add(parent_title.data(0) +'_'+ document['pars'][kid],value=document['value'][kid],
                            min=document['limits'][kid][0], max=document['limits'][kid][1], vary=True)

        """
        if document['real?'] == True:
            parent_title.insert_children(1,2)
            child: TreeItem = parent_title.last_child()
            child.ifreal = True
            child.set_data(0, 'real?', role=Qt.DisplayRole)
        """
        self.endResetModel()
        curve = CustomPlotDataItem(title=parent_title.data(0),key=key,parentgraph=self.parentsub.graph,
                                   document=document,model=self,
                                   pen=pg.mkPen(width=5),symbolPen=None,symbolBrush=None,symbloSize=5)
        # curve.tag = 'SPLIT'
        self.parentsub.graph.disableAutoRange()
        self.parentsub.graph.addItem(curve)
        self.curves.append(curve)
        self.update_params()
        self.parentsub.refreshplotwidget(self.parentsub.graph)

    def columnCount(self, parent: QModelIndex = None) -> int:
        return 5

    def headerData(self, section: int, orientation: Qt.Orientation, role: int = ...) -> Any:
        if role != Qt.DisplayRole:
            return None

        if orientation == Qt.Horizontal:
            return self.headers[section]
        
    def flags(self, index: QModelIndex) -> Qt.ItemFlags:
        """Override from QAbstractItemModel

        Return flags of index
        """
        if not index.isValid()  :
            return Qt.NoItemFlags

        flags = super(ParameterModel, self).flags(index)
        item: TreeItem = index.internalPointer()

        if index.column() == 1 and item._parent != self._rootItem: # and index.row() != item._parent.child_count()-1:
            return Qt.ItemIsEditable | flags
        elif index.column() == 4: # or index.column() == 0:
            return Qt.ItemIsUserCheckable | flags
        else:
            return flags
        
    def data(self, index: QModelIndex, role: Qt.ItemDataRole) -> Any:
        """Override from QAbstractItemModel

        Return data from a item according index and role

        """
        if not index.isValid():
            return None
        
        item: TreeItem = index.internalPointer()

        if role == Qt.DisplayRole or role == Qt.EditRole:
            return item.data(index.column())
        elif item._parent != self._rootItem:
            """
            if item.ifreal == True:
                if index.row() == item._parent.child_count()-1:
                    if index.column() == 0:
                        if role == Qt.CheckStateRole:
                            return item.checked
                elif index.column() == 4:
                    if role == Qt.CheckStateRole:
                        return item.checked
            """
            if index.column() == 4:
                if role == Qt.CheckStateRole:
                    return item.checked
        
        return None
    
    def itemData(self, index) -> Dict[int, Any]:
        return super().itemData(index)

    def setData(self, index: QModelIndex, value: Any, role: Qt.ItemDataRole):
        """Override from QAbstractItemModel

        Set json item according index and role

        Args:
            index (QModelIndex)
            value (Any)
            role (Qt.ItemDataRole)

        """
        if role == Qt.EditRole:
            if index.column() == 1:
                item: TreeItem = index.internalPointer()
                result: bool = item.set_data(index.column(), value, role)
                if result:
                    self.dataChanged.emit(index, index, [Qt.EditRole])
                    self.update_params()
                    self.parentsub.refreshplotwidget(self.parentsub.graph)
                return result
        if role == Qt.CheckStateRole:
            item: TreeItem = index.internalPointer()
            item.set_checked(value)
            self.dataChanged.emit(index, index, [Qt.CheckStateRole])
            self.update_params()
        return False
    
    def index(self, row: int, column: int, parent=QModelIndex()) -> QModelIndex:
        """Override from QAbstractItemModel

        Return index according row, column and parent

        """
        if not self.hasIndex(row, column, parent):
            return QModelIndex()

        if not parent.isValid():
            parentItem = self._rootItem
        else:
            parentItem = parent.internalPointer()

        childItem = parentItem.child(row)
        if childItem:
            return self.createIndex(row, column, childItem)
        else:
            return QModelIndex()
    
    def parent(self, index: QModelIndex) -> QModelIndex:
        """Override from QAbstractItemModel

        Return parent index of index

        """

        if not index.isValid():
            return QModelIndex()

        childItem: TreeItem = index.internalPointer()
        if childItem:
            parentItem = childItem.parent()
        else:
            parentItem = None

        if parentItem == self._rootItem or not parentItem:
            return QModelIndex()

        return self.createIndex(parentItem.child_number(), 0, parentItem)
    
    def rowCount(self, parent=QModelIndex()):
        """Override from QAbstractItemModel

        Return row count from parent index
        """
        if parent.column() > 0:
            return 0

        if not parent.isValid():
            parentItem = self._rootItem
        else:
            parentItem = parent.internalPointer()

        return parentItem.child_count()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("icon.ico"))
    window = MainWindow()
    sys.exit(app.exec())
