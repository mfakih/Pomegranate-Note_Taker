import sys
import os
import ctypes
from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from datetime import datetime
import codecs
import glob
import time
import stat


from iptcinfo import IPTCInfo

import copy 

import ctypes

class Notepad(QtGui.QMainWindow):

	global xcdPath
	global xcdPath2
	global scpPath

	xcdPath = 'x:/xcd/'
	scpPath = 'x:/scp/' + datetime.now().strftime('%y.%m.%d')

	def __init__(self):
		super(Notepad, self).__init__()
		self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
		self.initUI()

	def initUI(self):
		myappid = 'mycompany.myproduct.gte3.version' # arbitrary string
		ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

		self.central = QWidget(self)

		self.hbox = QVBoxLayout(self.central)



		newAction = QtGui.QAction('New', self)
		newAction.setShortcut('Ctrl+N')
		newAction.setStatusTip('Clear')
		newAction.triggered.connect(self.newFile)

		saveAction = QtGui.QAction('Save', self)
		saveAction.setShortcut('Ctrl+S')
		saveAction.setStatusTip('Save current text')
		saveAction.triggered.connect(self.saveFile)


		captureAction = QtGui.QAction('Capture', self)
		captureAction.setShortcut('Ctrl+R')
		captureAction.setStatusTip('Save current screen')
		captureAction.triggered.connect(self.captureScreen)


		closeAction = QtGui.QAction('Close', self)
		closeAction.setShortcut('Ctrl+Q')
		closeAction.setStatusTip('Close Notepad')
		closeAction.triggered.connect(self.close)

		menubar = self.menuBar()
		fileMenu = menubar.addMenu('&File')
		fileMenu.addAction(newAction)
		fileMenu.addAction(saveAction)
		fileMenu.addAction(captureAction)
		fileMenu.addAction(closeAction)

		self.label = QLabel("Enter [type] [your text], then press Ctrl+S...", self)

		self.stat = QLabel("", self)
		xcdCount = str(len(glob.glob1(xcdPath,"*_*.txt")))
		scpCount = str(len(glob.glob1(scpPath,"*.jpg")))
		self.stat.setText(xcdCount + ' xcd ' + scpCount + ' scp')

		self.text = QtGui.QTextEdit(self)

		self.timer = QTimer(self)
		self.timer.timeout.connect(self.timeout)
		self.timer.start(600000)

		#if not os.path.exists(path):
		 #       QMessageBox.critical(self, "Critical",
		  #    '''Directory does not exist''',
		   #   QMessageBox.Ok, QMessageBox.Cancel)


		self.timer2 = QTimer(self)
		self.timer2.timeout.connect(self.timeout2)
		self.timer2.start(600000)


		self.text.textChanged.connect(self.showEntity)

		self.hbox.addWidget(self.label)
		self.hbox.addWidget(self.text)
		self.hbox.addWidget(self.stat)
		self.setCentralWidget(self.central)



		#self.setCentralWidget(self.text)
		self.setGeometry(300,300,340,150)
		self.setWindowTitle('PKM Note Taker v3.4')
		self.setWindowIcon(QtGui.QIcon('favicon.jpg'))

		self.show()

	def newFile(self):
		self.text.clear()

	def getEntity(self):
		firstLine = self.text.toPlainText().split('\n')[0]
		entity = 'Enter [type] [text], then press Ctrl+S...'
		if (firstLine.count(' ') > 0):
			entity = firstLine.split(' ')[0]
		else:
			if (firstLine == ''):
				entity = 'note'
			else:
				entity = firstLine
		return entity

	def showEntity(self):
		if (len(self.getEntity()) >= 1):
			self.label.setStyleSheet("color: green;")
			self.label.setText(self.getEntity())
		else:
			#self.label.setStyleSheet("color: red;")
			self.label.setText(self.getEntity())



	def saveFile(self):
		'''filename = QtGui.QFileDialog.getSaveFileName(self, 'Save File', os.getenv('HOME'))'''
		filedata = self.text.toPlainText()
  

		entity = str(self.getEntity()).upper()
		if not os.path.exists(xcdPath):
			#QMessageBox.critical(self, "Critical",
			#'''Directory does not exist''',
			#QMessageBox.Ok, QMessageBox.Cancel)
			os.makedirs(xcdPath)

		# if (len(entity) == 1):
		# 	path = xcdPath + entity + '_' + \
		# 			datetime.now().strftime('%y.%m.%d') + '.txt'
		#
		# 	f = codecs.open(path, "a", "utf-8")
		# 	f.write(unicode(filedata) + '\n')
		# 	f.close()
		# 	self.text.clear() #['text'] = 'ok'
		# 	size = os.stat(path)[stat.ST_SIZE]
		# 	self.label.setText('Written to ' +  path + ' (' + str(size) + ' bytes)')
		# 	#_%H%M%S only date
		# else:
#			if (len(entity) > 1):

		path = xcdPath + entity + '_' + \
			 datetime.now().strftime('%y.%m.%d_%H-%M-%S') + \
			 '.txt'

		f = codecs.open(path, "w", "utf-8-sig")
		f.write(unicode(filedata) + '\n')
		f.close()


		self.text.clear() #['text'] = 'ok'
		size = os.stat(path)[stat.ST_SIZE]
		self.label.setStyleSheet("color: gray;")
		self.label.setText('Written to ' +  path + ' (' + str(size) + ' bytes)')
		#time.sleep(2)
		#self.label.setText('')

		xcdCount = str(len(glob.glob1(xcdPath,"*_*.txt")))
		scpCount = str(len(glob.glob1(scpPath,"*.jpg")))
		self.stat.setText(xcdCount + ' xcd ' + scpCount + ' scp')


	def restartTimer(self):
		if not self.hasFocus():
			self.captureScreen()


	def timeout(self):
		# Update the lcd
		self.timer.stop()
		self.setFocus(True)
		self.activateWindow()
		self.raise_()
		self.show()

		self.captureScreen()

		self.timer.start()



	#def countFiles(self):
	 #  len(glob.glob1(xcdPath,"*_*.txt"))
	def captureScreen (self):
		text, ok = QInputDialog.getText(self,
			'Current activity',
			'Current activity')

		if ok:
			if text:
				print('Text entered')
			else:
				text = "Untitled"

			#self.le.setText(str(text))
						#app = QApplication(sys.argv)

			lastCapture =  time.strftime("%Y.%m.%d_%H-%M-%S",
											 time.localtime())
			lastCaptureLcd =  time.strftime("%H:%M",
											time.localtime())


			self.lower()
			time.sleep(1)

			originalText =  copy.copy(text)

			illegal = '?"/\\*:<>' + '!$^&{}|'
			for s in illegal:
				text = text.replace(s, '_')

			path = scpPath
			if not os.path.exists(path):
				 #QMessageBox.critical(self, "Critical",
			  #'''Directory does not exist''',
			  #QMessageBox.Ok, QMessageBox.Cancel)
				  os.makedirs(path)
			if not os.path.exists(xcdPath):
				 #QMessageBox.critical(self, "Critical",
			  #'''Directory does not exist''',
			  #QMessageBox.Ok, QMessageBox.Cancel)
				  os.makedirs(xcdPath)

			QPixmap.grabWindow(QApplication.desktop().winId())\
			.save(path + '/scp-' +
			lastCapture + ' ' + text + '.jpg',
			'jpeg', 95)


			jpath = xcdPath + '/Jtrk' + '_' + \
				datetime.now().strftime('%y.%m.%d') + '.txt'
			jf = codecs.open(jpath, "a", "utf-8")
			jf.write(unicode(datetime.now().strftime('%y.%m.%d_%H-%M-%S') + ': ' + originalText) + '\n')
			jf.close()

			


				#self.lcd.display(lastCaptureLcd)

			xcdCount = str(len(glob.glob1(xcdPath,"*_*.txt")))
			scpCount = str(len(glob.glob1(scpPath,"*.jpg")))
			self.stat.setText(xcdCount + ' xcd ' + scpCount + ' scp')

			self.label.setText('Captured the screen at ' +
			lastCapture) # + ' doing ' + str(text))
			
			
			# Create new info object
			info = IPTCInfo(path + '/scp-' +
			lastCapture + ' ' + text + '.jpg',
			'jpeg')
			info.data['caption/abstract'] = originalText
			info.data['supplemental category'] = ['Screenshot']
			info.save()

	def timeout2(self):
		# Update the lcd
		self.setFocus(True)
		self.activateWindow()
		self.raise_()
		self.show()



	def closeEvent(self, event):
		quit_msg = "Are you sure you want to exit the program?"
		reply = QtGui.QMessageBox.question(self, 'Message', \
						 quit_msg, QtGui.QMessageBox.Yes, \
						 QtGui.QMessageBox.No)
		if reply == QtGui.QMessageBox.Yes:
			event.accept()
		else:
			event.ignore()

def main():
	app = QtGui.QApplication(sys.argv)
	app.setWindowIcon(QtGui.QIcon('favicon.png'))
	notepad = Notepad()
	notepad.setWindowIcon(QtGui.QIcon('favicon.png'))
	sys.exit(app.exec_())

if __name__ == '__main__':
	main()

