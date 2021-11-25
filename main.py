import sqlite3
import sys

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5 import QtWidgets, QtCore


class SecondWindow(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent, QtCore.Qt.Window)
        self.build2()

    def build2(self):
        self.spisokItems = []
        uic.loadUi('addEditCoffeeForm.ui', self)
        self.con = sqlite3.connect('coffee.sqlite')
        cur = self.con.cursor()
        self.result = cur.execute('SELECT * FROM cofa').fetchall()
        self.spisokItems = list(map(lambda x: str(x[0]), self.result))
        self.comboBox.addItems(["Новый элемент БД"] + self.spisokItems)
        self.comboBox_2.addItems(["Молотый", "В зернах"])
        self.comboBox.currentIndexChanged[int].connect(self.loadItems)

    def loadItems(self, index):
        if index:
            self.data = self.result[index - 1]
            self.lineEditName.setText(self.data[1])
            self.lineEditDegree.setText(self.data[2])
            self.comboBox_2.setCurrentIndex(self.data[3] == "Молотый")
            self.lineEditTaste.setText(self.data[4])
            self.lineEditCost.setText(str(self.data[5]))
            self.lineEditValue.setText(str(self.data[6]))
            self.update()
        else:
            self.clearbox()

    def clearbox(self):
        self.lineEditName.clear()
        self.lineEditDegree.clear()
        self.comboBox_2.setCurrentIndex(0)
        self.lineEditTaste.clear()
        self.lineEditCost.clear()
        self.lineEditValue.clear()
        self.update()


class Main(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.secondWin = None
        self.build()

    def build(self):
        uic.loadUi('main.ui', self)
        self.pushButton.clicked.connect(self.showcoffe)
        self.pushButton_2.clicked.connect(self.openWin2)

    def openWin2(self):
        if not self.secondWin:
            self.secondWin = SecondWindow(self)
        self.secondWin.show()

    def showcoffe(self):
        self.con = sqlite3.connect('coffee.sqlite')
        cur = self.con.cursor()
        result = cur.execute('SELECT * FROM cofa').fetchall()
        self.tableWidget.setRowCount(len(result))
        self.tableWidget.setColumnCount(7)
        self.tableWidget.setHorizontalHeaderLabels(["ID", "Название", "Степень обжарки", "Молотый/Зерновой", "Описание вкуса", "Цена", "Объём"])
        for i, elem in enumerate(result):
            for j, val in enumerate(elem):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(val)))
        self.tableWidget.resizeColumnsToContents()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Main()
    ex.show()
    sys.exit(app.exec())
