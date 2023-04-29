import sys
import random
from PyQt5 import uic, QtGui
from PyQt5.QtWidgets import QApplication, QAbstractItemView
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QInputDialog
import sqlite3
import time

ns = [1, 2, 3, 4]
random_val = [2, 2, 2, 2, 2, 2, 2, 4, 4, 4]


def reverse(matrix):
    new_matrix = []
    for i in range(4):
        new_matrix.append([])
        for j in range(4):
            new_matrix[i].append(matrix[i][3 - j])
    return new_matrix


def transp(matrix):
    new_matrix = [[0 for i in range(4)] for i in range(4)]
    for i in range(4):
        for j in range(4):
            new_matrix[i][j] = matrix[j][i]
    return new_matrix


def merge(matrix):
    for i in range(4):
        for j in range(3):
            if matrix[i][j] == matrix[i][j + 1] and matrix[i][j] != 0:
                matrix[i][j] += matrix[i][j]
                matrix[i][j + 1] = 0
    return matrix


def compress(matrix):
    new_matrix = [[0 for i in range(4)] for i in range(4)]
    for i in range(4):
        pos = 0
        for j in range(4):
            if matrix[i][j] != 0:
                new_matrix[i][pos] = matrix[i][j]
                pos += 1
    return new_matrix


def moveLeft(arr):  # left
    step1 = compress(arr)
    step2 = merge(step1)
    step3 = compress(step2)
    return step3


def moveRight(arr):  # right
    step1 = reverse(arr)
    step2 = compress(step1)
    step3 = merge(step2)
    step4 = compress(step3)
    step5 = reverse(step4)
    return step5


def moveUp(arr):  # up
    step1 = transp(arr)
    step2 = compress(step1)
    step3 = merge(step2)
    step4 = compress(step3)
    step5 = transp(step4)
    return step5


def moveDown(arr):  # down
    step1 = transp(arr)
    step2 = reverse(step1)
    step3 = compress(step2)
    step4 = merge(step3)
    step5 = compress(step4)
    step6 = reverse(step5)
    step7 = transp(step6)
    return step7


class MyWidget(QMainWindow):  # Графический интерфейс
    def __init__(self):
        super().__init__()
        self.nap = None
        uic.loadUi('2048.ui', self)
        self.setWindowIcon(QtGui.QIcon('2048.png'))
        self.f = False
        self.new_game()
        self.pushButton_3.clicked.connect(self.new_game)
        self.pushButton_9.clicked.connect(self.game)
        self.pushButton_8.clicked.connect(self.game)
        self.pushButton_7.clicked.connect(self.game)
        self.pushButton_6.clicked.connect(self.game)
        self.pushButton_2.clicked.connect(self.exs)
        self.flag2048 = True
        bd = sqlite3.connect('2048.sqlite')  # Подключение к базе данных
        curs = bd.cursor()
        curs.execute("""CREATE TABLE IF NOT EXISTS records(
                       userid INT PRIMARY KEY,
                       score INT,
                       steps INT);
                    """)
        curs.execute('''
                    SELECT score , steps from RECORDS
                    ORDER BY score DESC
                    limit 3
                    ''')
        res = curs.fetchall()  # Получение данных
        if len(res) > 0:
            self.label_5.setText(f'1   {res[0][0]} шаги {res[0][1]}')
        if len(res) > 1:
            self.label_8.setText(f'2   {res[1][0]} шаги {res[1][1]}')  # Рекорды
        if len(res) > 2:
            self.label_9.setText(f'3   {res[2][0]} шаги {res[2][1]}')
        curs.close()

    def exs(self):  # Функция выхода
        exit()

    def color_row(self, row1, row2, color):  # Функция для изменений цветов
        self.tableWidget.item(row1, row2).setBackground(color)

    def new_game(self):  # Работа с новой игрой
        bd = sqlite3.connect('2048.sqlite')  # Обновление рекордов
        curs = bd.cursor()
        curs.execute('''
                    SELECT score , steps from RECORDS
                    ORDER BY score DESC
                    limit 3
                    ''')
        res = curs.fetchall()
        if len(res) > 0:
            self.label_5.setText(f'1   {res[0][0]} шаги {res[0][1]}')
        if len(res) > 1:
            self.label_8.setText(f'2   {res[1][0]} шаги {res[1][1]}')
        if len(res) > 2:
            self.label_9.setText(f'3   {res[2][0]} шаги {res[2][1]}')
        curs.close()
        x_1 = random.choice(ns)  # Создание 2 клеток
        y_1 = random.choice(ns)
        val_1 = random.choice(random_val)
        x_2 = random.choice(ns)
        y_2 = random.choice(ns)
        val_2 = random.choice(random_val)
        while x_1 == x_2 or y_1 == y_2:
            x_1 = random.choice(ns)
            y_1 = random.choice(ns)
        self.count = 0
        self.score = 0
        self.matrx = [[0, 0, 0, 0],
                      [0, 0, 0, 0],
                      [0, 0, 0, 0],
                      [0, 0, 0, 0]]  # Создание матрицы
        self.void = ' '
        self.matrx[x_1 - 1][y_1 - 1] = val_1
        self.matrx[x_2 - 1][y_2 - 1] = val_2  # Добавление 2 клеток в матрицу
        for i in range(4):
            for j in range(4):
                self.element = str(self.matrx[i][j])
                self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
                if self.element != '0':
                    self.tableWidget.setItem(i, j, QTableWidgetItem(self.element))  # Вывод матрицы и цветокор
                    if self.element == '2':
                        color = QColor(238, 228, 218)
                    if self.element == '4':
                        color = QColor(237, 224, 200)
                    self.color_row(i, j, color)
                else:
                    self.tableWidget.setItem(i, j, QTableWidgetItem(self.void))
                self.f = True
                self.label_4.setText(f'0')  # Вывод очков и ходов
                self.label_3.setText(f'0')

    def game(self):
        self.label_7.setText('')
        global colored
        if self.f:
            name = (self.sender().text())
            flag2 = True
            if name == 'D':  # Ходы
                self.n_matrx = moveDown(self.matrx)
            if name == 'L':
                self.n_matrx = moveLeft(self.matrx)
            if name == 'R':
                self.n_matrx = moveRight(self.matrx)
            if name == 'U':
                self.n_matrx = moveUp(self.matrx)
            self.matrx_l = moveLeft(self.matrx)
            self.matrx_d = moveDown(self.matrx)
            self.matrx_r = moveRight(self.matrx)
            self.matrx_u = moveUp(self.matrx)
            if self.matrx_u == self.matrx_d == self.matrx_r == self.matrx_l:  # Проверка на возможность ходов
                self.label_7.setText('Game over')
                time.sleep(0.5)
                self.save()
                self.update()
            if self.n_matrx != self.matrx:  # Проверка на правильность хода
                self.count += 1
                while flag2:
                    self.matrx = self.n_matrx
                    x = random.choice(ns)
                    y = random.choice(ns)
                    if self.matrx[x - 1][y - 1] == 0:  # Добавление элемента
                        val = random.choice(random_val)
                        self.matrx[x - 1][y - 1] = val
                        flag2 = False
                self.tableWidget.clear()
                for i in range(4):
                    for j in range(4):
                        self.element = str(self.matrx[i][j])
                        if self.element != '0':
                            self.score += int(self.element)
                            self.tableWidget.setItem(i, j, QTableWidgetItem(self.element))  # Вывод матрицы и цветокор
                            if self.element == '2':
                                color = QColor(238, 228, 218)
                            if self.element == '4':
                                color = QColor(237, 224, 200)
                            if self.element == '8':
                                color = QColor(242, 177, 121)
                            if self.element == '16':
                                color = QColor(245, 149, 99)
                            if self.element == '32':
                                color = QColor(246, 124, 95)
                            if self.element == '64':
                                color = QColor(247, 101, 63)
                            if self.element == '128':
                                color = QColor(237, 206, 114)
                            if self.element == '256':
                                color = QColor(237, 204, 97)
                            if self.element == '512':
                                color = QColor(237, 200, 80)
                            if self.element == '1024':
                                color = QColor(237, 200, 70)
                            if self.element == '2048':
                                color = QColor(237, 194, 47)
                                if self.flag2048:  # Проверка на 'победу'
                                    self.flag2048 = False
                                    self.label_7.setText(
                                        'Вы собрали 2048, не остонавливайтесь!')
                            if self.element == '4096':
                                color = QColor(158, 41, 207)
                            if self.element == '8192':
                                color = QColor(97, 25, 128)
                            if self.element == '16384':
                                color = QColor(58, 15, 75)
                            if self.element == '32768':
                                color = QColor(100, 100, 100)
                            self.color_row(i, j, color)
                        else:
                            self.tableWidget.setItem(i, j, QTableWidgetItem(self.void))
        else:
            self.new_game()
        self.label_4.setText(f'{self.count}')  # Счёт
        self.label_3.setText(f'{self.score}')

    def save(self):  # Сохранение при проигрыше
        if self.f:
            self.f = False
            sc = int(self.score)
            st = int(self.count)
            bd = sqlite3.connect('2048.sqlite')
            cur = bd.cursor()
            cur.execute(f"""INSERT INTO records( score, steps) 
               VALUES('{sc}', '{st}');""")
            bd.commit()
            cur.close()


class Example(MyWidget):  # Графический интерфейс диалогового окна
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(300, 300, 150, 150)
        self.pushButton.clicked.connect(self.run)

    def run(self):
        text, ok_pressed = QInputDialog.getText(self, "Вы уверены?",
                                                "'Да'/'Нет'")  # 1/3 удаление счета
        if ok_pressed:  # 2/3 удаление счета 'ВЫ ТОЧНО ВЕРЕНЫ??'
            if text == 'Да' or text == 'да' or text == 'ДА':  # удаление счета
                bd = sqlite3.connect('2048.sqlite')
                cur = bd.cursor()
                cur.execute(f"""DELETE from records;""")
                bd.commit()
                cur.close()
                self.update()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec_())
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())
