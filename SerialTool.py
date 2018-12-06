#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
PyQt5 Serial Tool
Author: Hesuping 
date: 2018.12
"""
import threading
import time
import serial 
import serial.tools.list_ports 
import sys
from UI import SERIAL_UI
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import (QMainWindow,QApplication)
class SerialTool(QMainWindow,SERIAL_UI):
	def __init__(self):
		super().__init__() 
		self.serial_list = list() 
		self.avaliable_com()
		self.UI_init()
		self.Activated()
		self.initCOM()
		
		#创建定时发送定时器
		self.timer_send= QTimer(self)
		self.timer_send.timeout.connect(self.UartSend)
	def avaliable_com(self):
		self.serial_list = []
		port_list = list(serial.tools.list_ports.comports()) 
		if len(port_list) > 0: 
			for port_com in port_list:
				port_list_0 =list(port_com) 
				port_serial = port_list_0[0] 
				self.serial_list.append(port_serial)

	def Activated(self):      
		self.com.activated[str].connect(self.ComActivated)
		self.RefreshCom.clicked.connect(self.RefreshComActivated)
		self.baudrate.activated[str].connect(self.BaudActivated)
		self.parity_bit.activated[str].connect(self.ParityBitActivated)
		self.data_bit.activated[str].connect(self.DataBitActivated)
		self.stop_bit.activated[str].connect(self.StopBitActivated)
		self.StartCom.clicked[bool].connect(self.StartComActivated)
		self.ClearSend.clicked.connect(self.ClearSendActivated)
		self.ClearReceive.clicked.connect(self.ClearReceiveActivated)
		self.InputSend.clicked.connect(self.UartSend)
		self.TimerSendCheck.stateChanged.connect(lambda: self.CheckActivated(self.TimerSendCheck))
#		self.HexSend.stateChanged.connect(lambda: self.CheckActivated(self.HexSend))
#		self.HexReceive.stateChanged.connect(lambda: self.CheckActivated(self.HexReceive))
		
	def initCOM(self):
		self.l_serial = serial.Serial()
		self.l_serial.port = "COM1"
		self.l_serial.baudrate = 9600
		self.l_serial.bytesize = 8
		self.l_serial.stopbits = 1
		self.l_serial.parity = serial.PARITY_EVEN
		self.l_serial.timeout = 2
	def closeEvent(self,event):
		if self.l_serial.isOpen():
			self.l_serial.close()
			
	def ComActivated(self,text):
		self.l_serial.port = text
	def RefreshComActivated(self):
		self.avaliable_com()
		self.ComRelist()
	def BaudActivated(self,text):
		self.l_serial.baudrate = int(text)

	def ParityBitActivated(self,text):
		if(text == 'NONE'):
			self.l_serial.parity = serial.PARITY_NONE
		elif(text == 'ODD'):
			self.l_serial.parity = serial.PARITY_ODD
		elif(text == 'EVEN'):
			self.l_serial.parity = serial.PARITY_EVEN
			
	def DataBitActivated(self,text):
		self.l_serial.bytesize = int(text)
		
	def StopBitActivated(self,text):
		self.l_serial.stopbits = int(text)

	def StartComActivated(self,pressed):
		source = self.sender()

		if self.l_serial.isOpen():
			self.timer_send.stop()
			self.l_serial.close()
			
			self.thread_read.join()
			self.StartCom.setText("打开串口") 
#			self.square.setStyleSheet("QFrame { background-color: red}") 
		else:
			self.l_serial.open()
			self.StartCom.setText("关闭串口") 
#			self.square.setStyleSheet("QFrame { background-color: green}") 
#			self.col.setGreen(255) 

			self.thread_read = None
			self.thread_read = threading.Thread(target=self.UartRead)
			self.thread_read.setDaemon(1)
			self.thread_read.start()

	def UartRead(self):
		while self.l_serial.isOpen():
			time.sleep(0.2)
			data = ''
			data = data.encode('utf-8')
			n = self.l_serial.inWaiting()
			if n:
				data = data + self.l_serial.read(n)
				if self.HexReceive.checkState():        # 16进制接收
					hex_data=''
					for i in range(0, len(data)):
						hex_data = hex_data + '{:02X}'.format(data[i]) + ' '
					self.OutputText.append(hex_data.strip())
				else :
					self.OutputText.append(data.decode().strip())
					
	def ClearSendActivated(self):
		self.InputText.setPlainText('')
	
	def ClearReceiveActivated(self):
		self.OutputText.setPlainText('')
		
	def UartSend(self):
		InputStr = self.InputText.toPlainText()
		if InputStr != "": 
			if self.HexSend.checkState():
				#发送十六进制数据
				InputStr = InputStr.strip() #删除前后的空格
				send_list=[]
				while InputStr != '':
					try:
						num = int(InputStr[0:2], 16)
						
					except ValueError:
						print('input hex data!')
						QMessageBox.critical(self, 'pycom','请输入十六进制数据，以空格分开!')
						return None
					
					InputStr = InputStr[2:]
					InputStr = InputStr.strip()
					
					#添加到发送列表中
					send_list.append(num)
				InputStr = bytes(send_list)
				self.l_serial.write(InputStr)
			else :
				self.l_serial.write(InputStr.encode())

	def CheckActivated(self,BtnCheck):
		if BtnCheck == self.TimerSendCheck:
			if self.TimerSendCheck.checkState():
				time = self.TimerSendValue.text()
				time_val = int(time, 10)
				if time_val>0 :
					self.timer_send.start(time_val)
			else:
				self.timer_send.stop()
if __name__ == '__main__':

	app = QApplication(sys.argv)
	ex = SerialTool()
	sys.exit(app.exec_())