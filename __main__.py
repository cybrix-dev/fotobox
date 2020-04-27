import sys

from PyQt5.Qt import QApplication
from PyQt5.QtCore import Qt
from box import MainWindowB, Box


app = QApplication(sys.argv)

# disable mouse-cursor
app.setOverrideCursor(Qt.BlankCursor)

MainWindow = MainWindowB()
test = Box(MainWindow)
MainWindow.show()
sys.exit(app.exec_())
