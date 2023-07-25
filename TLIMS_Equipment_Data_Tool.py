import sys
import os
import time
import random
import pandas as pd
import numpy as np
import re
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import chicon  # 引用图标
from TLIMS_Equipment_Data_Tool import *
from TLIMS_Equipment_Data_Tool_UI import *
from Table_Ui import *


class MyMainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MyMainWindow, self).__init__(parent)
        self.setupUi(self)

        # self.pushButton_23.clicked.connect(self.aasBatch)
        # self.pushButton_39.clicked.connect(self.tabWidget.close)
        # self.pushButton_15.clicked.connect(self.clearContent)
        # self.pushButton_18.clicked.connect(lambda: self.getBatch('Auto'))
        self.actionExport.triggered.connect(self.exportConfig)
        self.actionImport.triggered.connect(self.importConfig)
        self.actionExit.triggered.connect(MyMainWindow.close)
        self.actionEdit.triggered.connect(self.showTable)
        self.actionImport.triggered.connect(self.lineEdit.clear)
        self.actionHelp.triggered.connect(self.showVersion)
        self.actionAuthor.triggered.connect(self.showAuthorMessage)

    # self.pushButton_51.clicked.connect(self.lineEdit_5.clear)
    # self.pushButton_51.clicked.connect(self.textBrowser_2.clear)

    def getConfig(self):
        # 初始化，获取或生成配置文件
        global configFileUrl
        global desktopUrl
        global now
        global last_time
        global today
        now = int(time.strftime('%Y'))
        last_time = now - 1
        today = time.strftime('%Y%m%d')
        desktopUrl = os.path.join(os.path.expanduser("~"), 'Desktop')
        configFileUrl = '%s/config' % desktopUrl
        configFile = os.path.exists('%s/config_tlims.csv' % configFileUrl)
        # print(desktopUrl,configFileUrl,configFile)
        if not configFile:  # 判断是否存在文件夹如果不存在则创建为文件夹
            reply = QMessageBox.question(self, '信息', '确认是否要创建配置文件', QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
            if reply == QMessageBox.Yes:
                if not os.path.exists(configFileUrl):
                    os.makedirs(configFileUrl)
                MyMainWindow.createConfigContent(self)
                MyMainWindow.getConfigContent(self)
                self.textBrowser.append("配置获取成功")
            else:
                exit()
        else:
            MyMainWindow.getConfigContent(self)

    def getConfigContent(self):
        csvFile = pd.read_csv('%s/config_tlims.csv' % configFileUrl, names=['A', 'B', 'C'])
        global configContent
        configContent = {}
        content = list(csvFile['A'])
        rul = list(csvFile['B'])
        use = list(csvFile['C'])
        for i in range(len(content)):
            configContent['%s' % content[i]] = rul[i]
        a = len(configContent)
        if (int(configContent['config_num']) != len(configContent)) or (len(configContent) != 4):
            reply = QMessageBox.question(self, '信息', 'config文件配置缺少一些参数，是否重新创建并获取新的config文件',
                                         QMessageBox.Yes | QMessageBox.No,
                                         QMessageBox.Yes)
            if reply == QMessageBox.Yes:
                MyMainWindow.createConfigContent(self)
                MyMainWindow.getConfigContent(self)
        try:
            self.textBrowser.append("配置获取成功")
        except AttributeError:
            QMessageBox.information(self, "提示信息", "已获取配置文件内容", QMessageBox.Yes)
        else:
            pass

    def createConfigContent(self):
        months = "JanFebMarAprMayJunJulAugSepOctNovDec"
        n = time.strftime('%m')
        pos = (int(n) - 1) * 3
        monthAbbrev = months[pos:pos + 3]

        configContent = [
            ['config_num', '4', 'config文件条目数量,不能更改数值'],  # getConfigContent()中需要更改配置文件数量
            ['输入路径和输出路径', '默认，可更改为自己需要的', '备注'],
            ['Import_URL', 'Z:\\Data\\2023\\66-01-2013-009 HPLC-MS\\AP&APEO\\%s' % monthAbbrev, '输入路径'],
            ['Export_URL', 'Z:\\Data\\2023\\66-01-2013-009 HPLC-MS\\AP&APEO\\result', '输出路径'],
        ]
        config = np.array(configContent)
        df = pd.DataFrame(config)
        df.to_csv('%s/config_tlims.csv' % configFileUrl, index=0, header=0, encoding='utf_8_sig')
        self.textBrowser.append("配置文件创建成功")
        QMessageBox.information(self, "提示信息",
                                "默认配置文件已经创建好，\n如需修改请在用户桌面查找config文件夹中config_tlims.csv，\n将相应的文件内容替换成用户需求即可，修改后记得重新导入配置文件。",
                                QMessageBox.Yes)

    def exportConfig(self):
        # 重新导出默认配置文件
        reply = QMessageBox.question(self, '信息', '确认是否要创建默认配置文件', QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
        if reply == QMessageBox.Yes:
            MyMainWindow.createConfigContent(self)
        else:
            QMessageBox.information(self, "提示信息", "没有创建默认配置文件，保留原有的配置文件", QMessageBox.Yes)

    def importConfig(self):
        # 重新导入配置文件
        reply = QMessageBox.question(self, '信息', '确认是否要导入配置文件', QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
        if reply == QMessageBox.Yes:
            MyMainWindow.getConfigContent(self)
        else:
            QMessageBox.information(self, "提示信息", "没有重新导入配置文件，将按照原有的配置文件操作", QMessageBox.Yes)

    def showAuthorMessage(self):
        # 关于作者
        QMessageBox.about(self, "关于",
                          "人生苦短，码上行乐。\n\n\n        ----Frank Chen")

    def showVersion(self):
        # 关于作者
        QMessageBox.about(self, "版本",
                          "V 1.00.00\n\n\n     2023-07-25")

    def showTable(self):
        # myTable = MyTableWindow()
        # myTable.show()
        myTable.createTable()
        myTable.showMaximized()

    def test(self):
        return 'test'


class MyTableWindow(QMainWindow, Ui_TableWindow):
    def __init__(self, parent=None):
        super(MyTableWindow, self).__init__(parent)
        self.setupUi(self)
        self.pushButton.clicked.connect(self.saveTable)
        self.pushButton_2.clicked.connect(self.createTable)

    # self.QtWidgets.QDialogButtonBox.Save

    def createTable(self):
        self.df = pd.read_csv('%s/config_tlims.csv' % configFileUrl, names=['A', 'B', 'C'])
        self.df_rows = self.df.shape[0]
        self.df_cols = self.df.shape[1]
        self.tableWidget.setRowCount(self.df_rows)
        self.tableWidget.setColumnCount(self.df_cols)

        # self.tabletWidget.
        for i in range(self.df_rows):
            for j in range(self.df_cols):
                self.tableWidget.setItem(i, j, QTableWidgetItem(self.df.iloc[i, j]))
        # 第1列不允许编辑
        self.tableWidget.setItemDelegateForColumn(0, EmptyDelegate(self))
        # 行颜色
        self.tableWidget.setAlternatingRowColors(True)
        # 显示所有内容
        self.tableWidget.resizeColumnsToContents()
        # 平均分配
        self.tableWidget.horizontalHeader().setSectionResizeMode(True)

    @pyqtSlot()
    def print_my_df(self):
        print(self.df)

    @pyqtSlot()
    def saveTable(self):
        col = self.tableWidget.columnCount()
        row = self.tableWidget.rowCount()
        # for currentQTableWidgetItem in self.tableWidget.selectedItems():
        # 	print((currentQTableWidgetItem.row(), currentQTableWidgetItem.column()))
        data = []
        for i in range(col):
            data.append(i)
            data[i] = []
            for j in range(row):
                itemData = self.tableWidget.item(j, i).text()
                data[i].append(itemData)
        configFile = pd.DataFrame({'a': data[0], 'b': data[1], 'c': data[2]})
        configFile.to_csv('%s/config_tlims.csv' % configFileUrl, encoding="utf_8_sig", index=0, header=0)
        reply = QMessageBox.question(self, '信息', '配置文件已修改成功，是否重新获取新的config文件内容',
                                     QMessageBox.Yes | QMessageBox.No,
                                     QMessageBox.Yes)
        if reply == QMessageBox.Yes:
            MyMainWindow.getConfigContent(self)


# table不可编辑
class EmptyDelegate(QItemDelegate):
    def __init__(self, parent):
        super(EmptyDelegate, self).__init__(parent)

    def createEditor(self, QWidget, QStyleOptionViewItem, QModelIndex):
        return None


if __name__ == "__main__":
    import sys
    import os
    import time
    import random
    import pandas as pd
    import numpy as np
    import re

    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    app = QApplication(sys.argv)
    myWin = MyMainWindow()
    myTable = MyTableWindow()
    myWin.show()
    myWin.getConfig()
    sys.exit(app.exec_())
