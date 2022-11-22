import sqlite3
import sys

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem, QMessageBox


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("main.ui", self)
        self.con = sqlite3.connect("coffee.sqlite")
        self.titles = None

    def update_result(self):
        cur = self.con.cursor()
        result = cur.execute("SELECT * FROM films WHERE id=?",
                             (item_id := self.spinBox.text(),)).fetchall()
        self.tableWidget.setRowCount(len(result))
        if not result:
            self.statusBar().showMessage('Ничего не нашлось')
            self.filmID = None
            return
        else:
            self.statusBar().showMessage(f"Нашлась запись с id = {item_id}")
            self.filmID = int(item_id)
        self.tableWidget.setColumnCount(len(result[0]))
        self.titles = [description[0] for description in cur.description]
        for i, elem in enumerate(result):
            for j, val in enumerate(elem):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(val)))

    def save_results(self):
        if self.filmID is not None:
            button = QMessageBox.question(self, 'Изменение', f'Изменить фильм с id = {self.filmID}',
                                 QMessageBox.Yes, QMessageBox.No)
            if button == QMessageBox.No:
                return
            cur = self.con.cursor()
            que = """
                UPDATE films SET title = strrev(title),
                    year = year + 1000,
                    duration = duration * 2
                WHERE id = ?
            """
            cur.execute(que, (self.filmID,))
            self.con.commit()
            self.update_result()


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    sys.excepthook = except_hook
    ex.show()
    sys.exit(app.exec())
