import sys
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
		self.pushButton_15.clicked.connect(self.clearContent)
		# self.pushButton_18.clicked.connect(lambda: self.getBatch('Auto'))
		self.actionExport.triggered.connect(self.exportConfig)
		self.actionImport.triggered.connect(self.importConfig)
		self.actionExit.triggered.connect(MyMainWindow.close)
		self.actionEdit.triggered.connect(self.showTable)
		self.actionImport.triggered.connect(self.lineEdit.clear)
		self.actionHelp.triggered.connect(self.showVersion)
		self.actionAuthor.triggered.connect(self.showAuthorMessage)
		self.pushButton_51.clicked.connect(self.lineEdit_5.clear)
		self.pushButton_51.clicked.connect(self.textBrowser_2.clear)

	def getConfig(self):
		# 初始化，获取或生成配置文件
		global configFileUrl
		global desktopUrl
		global now
		global last_time
		global today
		# getBatch里的
		global labNumber
		global qualityValue
		global volumeValue
		global analyteList
		global batchNum
		global selectBatchFile
		# getResult里的
		global selectResultFile
		# getReachMessage
		global reachLimsNo
		global reachEnglish
		global reachChinese
		global reachCas
		global reachPurpose
		now = int(time.strftime('%Y'))
		last_time = now - 1
		today = time.strftime('%Y%m%d')
		desktopUrl = os.path.join(os.path.expanduser("~"), 'Desktop')
		configFileUrl = '%s/config' % desktopUrl
		configFile = os.path.exists('%s/config_inorganic.csv' % configFileUrl)
		# print(desktopUrl,configFileUrl,configFile)
		if not configFile:  # 判断是否存在文件夹如果不存在则创建为文件夹
			reply = QMessageBox.question(self, '信息', '确认是否要创建配置文件', QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
			if reply == QMessageBox.Yes:
				if not os.path.exists(configFileUrl):
					os.makedirs(configFileUrl)
				MyMainWindow.createConfigContent(self)
				MyMainWindow.getConfigContent(self)
				self.lineEdit_6.setText("创建并导入配置成功")
			else:
				exit()
		else:
			MyMainWindow.getConfigContent(self)

	def getConfigContent(self):
		csvFile = pd.read_csv('%s/config_inorganic.csv' % configFileUrl, names=['A', 'B', 'C'])
		global configContent
		configContent = {}
		content = list(csvFile['A'])
		rul = list(csvFile['B'])
		use = list(csvFile['C'])
		for i in range(len(content)):
			configContent['%s' % content[i]] = rul[i]
		a = len(configContent)
		if (int(configContent['config_num']) != len(configContent)) or (len(configContent) != 43):
			reply = QMessageBox.question(self, '信息', 'config文件配置缺少一些参数，是否重新创建并获取新的config文件', QMessageBox.Yes | QMessageBox.No,
										 QMessageBox.Yes)
			if reply == QMessageBox.Yes:
				MyMainWindow.createConfigContent(self)
				MyMainWindow.getConfigContent(self)
		try:
			self.lineEdit_6.setText("配置获取成功")
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
			['config_num','43','config文件条目数量,不能更改数值'],# getConfigContent()中需要更改配置文件数量
			['选择ICP_Batch的输入路径和输出路径', '默认，可更改为自己需要的', '以下ICP组Batch相关'],
			['ICP_Batch_Import_URL', 'Z:\\Inorganic_batch\\Microwave\\Batch', 'ICP的Batch引入路径，所有ICP组batch均为次路径'],
			['ICP_Batch_Export_URL', '%s' % desktopUrl, 'ICP仪器使用，一般为本机电脑桌面'],
			['ECO_Batch_Export_URL','Z:\\Data\\%s\\Subcon\\厦门质检院\\%s' % (now,monthAbbrev),'ECO项目的导出路径(质检院或者中讯德)'],
			['ECO_Batch_Export_NB_URL','Z:\\Data\\%s\\Subcon\\NB CHM\\%s' % (now,monthAbbrev),'ECO项目的导出路径，质检院格式(宁波)'],
			['Nickel_Batch_Export_URL','Z:\\Inorganic_batch\\Microwave\\Result\\Nickel','镍释放项目的导出路径'],
			['Nickel_Model_Import_URL','Z:\\Inorganic\\Program\\1.Inorganic Operate\\1.New edition\\2.Model','镍释放项目的模板文件路径'],
			['Nickel_File_Name','TC_XMN_CHM_F_T.02E.xlsm','镍释放项目的模板文件名称'],
			['选择ICP_Result的输入路径和输出路径','默认，可更改为自己需要的','以下ICP组Result相关'],
			['ICP_Result_Import_URL','Z:\\Data\\%s\\66-01-2018-012-ICPOES 5110\\%s' % (now,monthAbbrev),'ICP OES组结果的引入路径，选择CSV结果文件'],
			['ICP_Result_Export_URL','Z:\\Data\\%s\\66-01-2018-012-ICPOES 5110\\%s' % (now,monthAbbrev),'ICP OES组结果的导出路径，转化为TXT保存路径'],
			['NB_Result_Import_URL','Z:\\Data\\%s\\Subcon\\NB CHM\\Raw Dada\\%s' % (now,monthAbbrev),'NB-ICP OES组结果的引入路径，选择CSV结果文件'],
			['NB_Result_Export_URL','Z:\\Data\\%s\\Subcon\\NB CHM\\NB Result\\%s' % (now,monthAbbrev),'NB-ICP OES组结果的导出路径，转化为TXT保存路径'],
			['AAS_Result_Import_URL','Z:\\Data\\%s\\66-01-2018-012-ICPOES 5110' % now,'AAS组结果的引入路径，选择CSV结果文件'],
			['AAS_Result_Export_URL','Z:\\Data\\%s\\66-01-2018-012-ICPOES 5110' % now,'AAS组结果的导出路径，转化为TXT保存路径'],
			['ECO_Result_Import_URL','Z:\\Data\\%s\\Subcon\\厦门质检院\\RawData' % now,'ECO项目结果的引入路径'],
			['ECO_Result_Export_URL','Z:\\Data\\%s\\Subcon\\厦门质检院\\ZJY-Resuls' % now,'ECO项目结果转化后的输出路径'],
			['ICP_QC_Chart_Import_URL','Z:\\QC Chart\\%s' % now,'ICP OES仪器的QC-Chart路径'],
			['ICP_QC_Chart_File_Name','QC_Chart_Heavy_Metal_66_01_2018_012.xlsx','ICP OES仪器的QC-Chart文件名'],
			['Reach_Model_Import_URL', 'Z:\\Inorganic\\Program\\1.Inorganic Operate\\1.New edition\\2.Model', 'Reach项目的模板路径'],
			['Reach_Result_File_Name', 'SVHC_DCU.xlsx', 'Reach项目的模板文件名'],
			['Reach_Result_Export_URL', 'Z:\\Data\\%s\\66-01-2018-012-ICPOES 5110\\SVHC'% now, 'Reach项目结果转化后的导出路径'],
			['Reach_Message_Import_URL', 'Z:\\Inorganic\\Program\\1.Inorganic Operate\\1.New edition\\2.Model', 'Reach-Message项目的模板路径'],
			['Reach_Message_File_Name', 'REACH_SVHC_Candidate_List.csv', 'Reach-Message项目的模板文件名'],
			['ICP_MS_Result_Import_URL', 'Z:\\Data\\%s\\66-01-2022-005-ICPMS 7850\\%s' % (now,monthAbbrev), 'ICP-MS结果导入路径，选择CSV结果文件'],
			['ICP_MS_QC_Chart_Import_URL', 'Z:\\QC Chart\\%s' % now, 'ICP MS仪器的QC-Chart路径'],
			['ICP_MS_QC_Chart_File_Name', 'QC_Chart_extractable Heavy Metal_2022_005V1.xlsx', 'ICP MS仪器的QC-Chart文件名'],
			['选择UV_Batch的输入路径和输出路径', '默认，可更改为自己需要的', '以下UV组Batch相关'],
			['UV_Batch_Import_URL', 'Z:\\Inorganic_batch\\Formaldehyde\\Batch', 'UV组的Batch引入路径'],
			['UV_Batch_Export_URL', 'Z:\\Inorganic_batch\\Formaldehyde\\Batch', 'UV组的Batch转化后的导出路径'],
			['UV_Rusult_Export_URL', 'Z:\\Inorganic_batch\\Formaldehyde\\Result', 'UV组的Batch转化为DCU结果格式后的导出路径，主要针对pH'],
			['选择UV_Result的输入路径和输出路径', '默认，可更改为自己需要的', '以下UV组Result相关'],
			['UV_QC_Chart_Import_URL', 'Z:\\QC Chart\\%s' % now, 'UV组仪器的QC-Chart路径'],
			['Formal_QC_Chart_File_Name', 'QC_Chart_HCHO_66_01_2016_051_CARY60.xlsx', '甲醛QC-Chart文件名'],
			['Cr_VI_QC_Chart_File_Name', 'QC_Chart_Cr_66_01_2013_011_CARY100.xlsx', '六价铬QC-Chart文件名'],
			['pH2014_QC_Chart_File_Name', 'QC_Chart_pH_66_01_2014_015.xlsx', 'pH2014-QC-Chart文件名'],
			['pH2018_QC_Chart_File_Name', 'QC_Chart_pH_66_01_2018_006.xlsx', 'pH2018-QC-Chart文件名'],
			['Formal_Result_Import_URL', 'Z:\\Data\\%s\\66-01-2016-051 UV-Vis (60)\\Formal' % now, '甲醛结果的导入路径'],
			['Cr_VI_Result_Import_URL', 'Z:\\Data\\%s\\66-01-2013-011 UV-Vis (100)\\Cr-VI\\Data' % now, '六价铬结果的导入路径'],
			['pH2014_Result_Import_URL', 'Z:\\Data\\%s\\66-01-2014-015 pH' % now, 'pH2014结果的导入路径'],
			['pH2018_Result_Import_URL', 'Z:\\Data\\%s\\66-01-2018-006 pH' % now, 'pH2018结果的导入路径'],
			['pH_Result_Import_URL', 'C:\Data\pH CSV', '原始pH结果路径']
		]
		config = np.array(configContent)
		df = pd.DataFrame(config)
		df.to_csv('%s/config_inorganic.csv' % configFileUrl, index=0, header=0, encoding='utf_8_sig')
		self.lineEdit_6.setText("配置文件创建成功")
		QMessageBox.information(self, "提示信息",
								"默认配置文件已经创建好，\n如需修改请在用户桌面查找config文件夹中config_inorganic.csv，\n将相应的文件内容替换成用户需求即可，修改后记得重新导入配置文件。",
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
						  "V 2.21.20\n\n\n     2021-11-26")

	def showTable(self):
		myTable.createTable()
		myTable.showMaximized()


class MyTableWindow(QMainWindow, Ui_TableWindow):
	def __init__(self, parent=None):
		super(MyTableWindow, self).__init__(parent)
		self.setupUi(self)
		self.pushButton.clicked.connect(self.saveTable)
		self.pushButton_2.clicked.connect(self.createTable)
		# self.QtWidgets.QDialogButtonBox.Save


	def createTable(self):
		self.df = pd.read_csv('%s/config_inorganic.csv' % configFileUrl, names=['A', 'B', 'C'])
		self.df_rows = self.df.shape[0]
		self.df_cols = self.df.shape[1]
		self.tableWidget.setRowCount(self.df_rows)
		self.tableWidget.setColumnCount(self.df_cols)

		# self.tabletWidget.
		for i in range(self.df_rows):
			for j in range(self.df_cols):
				self.tableWidget.setItem(i, j, QTableWidgetItem(self.df.iloc[i, j]))
		# 第1列不允许编辑
		self.tableWidget.setItemDelegateForColumn(0,EmptyDelegate(self))
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
		data =[]
		for i in range(col):
			data.append(i)
			data[i] = []
			for j in range(row):
				itemData = self.tableWidget.item(j,i).text()
				data[i].append(itemData)
		configFile = pd.DataFrame({'a': data[0], 'b': data[1], 'c': data[2]})
		configFile.to_csv('%s/config_inorganic.csv' % configFileUrl,encoding="utf_8_sig", index=0, header=0)
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





