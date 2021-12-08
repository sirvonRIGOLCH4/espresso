import sqlite3
import sys

from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5 import QtWidgets, QtCore
from main_ui import Ui_MainWindow
from addEditCoffeeForm_ui import Ui_Form

class SecondWindow(QtWidgets.QWidget, Ui_Form):

    def __init__(self, parent):
        super().__init__(parent, QtCore.Qt.Window)
        self.setupUi(self)
        self.parents = parent
        self.con = sqlite3.connect('data\coffee.sqlite')
        cur = self.con.cursor()
        self.result = cur.execute('SELECT * FROM cofa').fetchall()
        self.comboBox.addItems(["Новый элемент БД"] + list(map(lambda x: str(x[0]), self.result)))
        self.comboBox_2.addItems(["молотый", "в зернах"])
        self.comboBox.currentIndexChanged[int].connect(self.loadItems)
        self.pushButton_2.clicked.connect(self.update2)

    def loadItems(self, index):
        if index:
            self.data = self.result[index - 1]
            self.lineEditName.setText(str(self.data[1]))
            self.lineEditDegree.setText(str(self.data[2]))
            self.comboBox_2.setCurrentIndex(self.data[3] == "в зернах")
            self.lineEditTaste.setText(str(self.data[4]))
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

    def update2(self):
        self.con = sqlite3.connect('data\coffee.sqlite')
        cur = self.con.cursor()
        self.id = self.comboBox.currentText()
        self.name = self.lineEditName.text()
        self.degree = self.lineEditDegree.text()
        self.type = self.comboBox_2.currentText()
        self.taste = self.lineEditTaste.text()
        self.cost = self.lineEditCost.text()
        self.value = self.lineEditValue.text()
        if self.comboBox.currentIndex():
            request = f"""UPDATE cofa SET name = '{self.name}', degree = '{self.degree}', type = '{self.type}',
            taste = '{self.taste}', cost = '{self.cost}', value = '{self.value}' WHERE id = '{self.id}'"""
            result = cur.execute(request).fetchone()
        else:
            request = f"""INSERT INTO cofa (name, degree, type, taste, cost, value) VALUES ('{self.name}', '{self.degree}', '{self.type}', '{self.taste}', '{self.cost}', '{self.value}')"""
            result = cur.execute(request).fetchone()
        self.con.commit()
        self.clearbox()
        self.con.close()
        self.close()
        self.parents.showcoffe()

class Main(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.pushButton.clicked.connect(self.showcoffe)
        self.pushButton_2.clicked.connect(self.openWin2)
        self.showcoffe()

    def openWin2(self):
        self.secondWin = SecondWindow(self)
        self.secondWin.show()

    def showcoffe(self):
        self.con = sqlite3.connect('data\coffee.sqlite')
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
