import sys

from PyQt5.Qt import QApplication
from box import MainWindowB, Box


app = QApplication(sys.argv)
MainWindow = MainWindowB()
test = Box(MainWindow)
MainWindow.show()
sys.exit(app.exec_())
