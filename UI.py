#! /usr/bin/env python
# -*- coding: utf-8 -*-
from pic import logo 
from PyQt5.QtCore import Qt,pyqtSlot
from PyQt5.QtWidgets import (QWidget, QCheckBox,QLabel,QMainWindow,QDesktopWidget,QPushButton,QHBoxLayout, QVBoxLayout,QTextEdit,
    QLineEdit,QComboBox,QFrame,QMessageBox,QToolTip)
from PyQt5.QtGui import QFont,QIcon,QColor
import sys
import base64

class SERIAL_UI(object):
	def __init__(self):
		super().__init__() 
		self.resize(850, 600)
		self.center()
	def UI_init(self):
		lbl = QLabel("端口", self)
		lbl.move(20, 45)
		self.com = QComboBox(self)
		self.ComRelist()
		self.com.move(70, 45)
		self.com.resize(80,25)

		self.RefreshCom = QPushButton("刷新串口", self)
		self.RefreshCom.move(30, 10)
		self.RefreshCom.resize(80,25)
		
		lbl = QLabel("波特率", self)
		lbl.setFont(QFont("Microsoft YaHei"))
		lbl.move(20, 75)
		self.baudrate = QComboBox(self)
		self.baudrate.addItem("1200")
		self.baudrate.addItem("2400")
		self.baudrate.addItem("4800")
		self.baudrate.addItem("9600")
		self.baudrate.addItem("19200")
		self.baudrate.addItem("38400")
		self.baudrate.addItem("57600")
		self.baudrate.addItem("115200")
		self.baudrate.move(70, 75)
		self.baudrate.setCurrentIndex(3)  # 设置默认的下拉选项
#		self.formLayout.setWidget(5, QtWidgets.QFormLayout.FieldRole, self.s1__box_5)
		self.baudrate.resize(80,25)

		self.lbl = QLabel("校验位", self)
		self.lbl.move(20, 105)
		self.parity_bit = QComboBox(self)
		self.parity_bit.addItem("NONE")
		self.parity_bit.addItem("ODD")
		self.parity_bit.addItem("EVEN")
		self.parity_bit.move(70, 105)
		self.parity_bit.setCurrentIndex(2)
		self.parity_bit.resize(80,25)

		lbl = QLabel("数据位", self)
		lbl.move(20, 135)
		self.data_bit = QComboBox(self)
		self.data_bit.addItem("5")
		self.data_bit.addItem("6")
		self.data_bit.addItem("7")
		self.data_bit.addItem("8")
		self.data_bit.move(70, 135)
		self.data_bit.setCurrentIndex(3)
		self.data_bit.resize(80,25)

		lbl = QLabel("停止位", self)
		lbl.move(20, 165)
		self.stop_bit = QComboBox(self)
		self.stop_bit.addItem("1")
		self.stop_bit.addItem("2")
		self.stop_bit.move(70, 165)
		self.stop_bit.resize(80,25)

#		self.col = QColor(0, 0, 0) 
		self.StartCom = QPushButton("打开串口", self)
#		StartCom.setStyleSheet(''' text-align : center;
#                                            background-color : NavajoWhite;
#                                            height : 30px;
#                                            border-style: outset;
#                                           font : 13px  ''')

		self.StartCom.setCheckable(True)
		self.StartCom.move(40, 200)
		self.StartCom.resize(80,30)

#		self.square = QFrame(self)
#		self.square.setGeometry(140, 245, 20, 20)
#		self.square.setStyleSheet("QWidget { background-color:red}")

		self.OutputText=QTextEdit(self)
		self.OutputText.move(180, 20)
		self.OutputText.resize(650, 400)
#		self.OutputText.setPlainText('Hello PyQt5!\n单击按钮')
#		self.OutputText.append("close")
		self.InputText=QTextEdit(self)
		self.InputText.move(180, 470)
		self.InputText.resize(650, 60)

		self.HexSend = QCheckBox('Hex发送',self)
		self.HexSend.move(550, 540)
		self.HexSend.resize(100,30)
		
		self.ClearSend = QPushButton("清发送区", self)
		self.ClearSend.move(650,540)
		self.ClearSend.resize(80,30)

		self.HexReceive = QCheckBox('Hex接收',self)
		self.HexReceive.move(550, 430)
		self.HexReceive.resize(100,30)
		
		self.ClearReceive = QPushButton("清接收区", self)
		self.ClearReceive.move(650, 430)
		self.ClearReceive.resize(80,30)
		
		self.TimerSendCheck = QCheckBox('定时发送',self)
		self.TimerSendCheck.move(350, 540)
		self.TimerSendCheck.resize(100,30)
		self.TimerSendValue = QLineEdit(self)
		self.TimerSendValue.move(420, 540)
		self.TimerSendValue.resize(50, 30)
		self.TimerSendValue.setText("")
		lbl = QLabel("ms/次", self)
		lbl.move(470, 540)
		
#		ClearReceive.setStyleSheet(''' text-align : center;
#                                            background-color : NavajoWhite;
#                                            height : 30px;
#                                            border-style: outset;
#                                           font : 13px  ''')
		self.InputSend = QPushButton("发送", self)
		self.InputSend.move(200, 540)
		self.InputSend.resize(80,30)
		

		tmp = open('logo.png', 'wb')
		tmp.write(base64.b64decode(logo))
		tmp.close()
		
		self.statusBar()
		self.setWindowIcon(QIcon('logo.png'))
		self.setWindowTitle('Python串口调试助手     作者: 何苏平 QQ:398002463')
		self.show()

	def center(self):
		qr = self.frameGeometry()
		cp = QDesktopWidget().availableGeometry().center()
		qr.moveCenter(cp)
		self.move(qr.topLeft())
	
	def ComRelist(self):
		self.com.clear()
		for i in self.serial_list:
			self.com.addItem(i)
		
		