import Main_window
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QLineEdit, QLabel, QTableWidgetItem, QMessageBox, QTableWidget
from csv import writer
import csv


class Director(QtWidgets.QDialog): # класс окна директора
    def __init__(self, name_user=None): # основная настройка окна, принимает именованный аргумент name_user - имя человека который зашел в это окно
        super(Director, self).__init__()
        self.setStyleSheet("background-color: rgb(210, 210, 210);")
        self.setGeometry(210, 200, 1500, 800)
        self.setMinimumSize(1500, 800)
        self.setWindowTitle('Окно директора')

        self.name_user = name_user
        self.greetings = QLabel(f'Добро пожаловать, {self.name_user}!', self)
        self.greetings.setFont(QtGui.QFont('Arial', 30))

        self.greetings.setGeometry(350, 70, 450, 150)
        self.greetings.adjustSize()

        self.create_table()
        self.table_buttons()
        self.button_to_home()
        self.open_data()

    def decorator(func): # проверка функций на ошибки, принимает аргмент func - функцию, дальше обрабатывает ее на наличие ошибкм
        def inner(self, *args):
            try:
                func(self)
            except Exception as e:
                print(e)
        return inner

    @decorator
    def create_table(self): #создание таблицы
        self.tableWidget = QtWidgets.QTableWidget(self)
        self.tableWidget.setColumnCount(5)
        self.tableWidget.setGeometry(200, 200, 1130, 350)
        self.tableWidget.setColumnWidth(0, 200)
        self.tableWidget.setColumnWidth(1, 200)
        self.tableWidget.setColumnWidth(2, 200)
        self.tableWidget.setColumnWidth(3, 250)
        self.tableWidget.setColumnWidth(4, 250)
        self.tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tableWidget.setHorizontalHeaderLabels(['Номер заказа', 'Имя клиента', 'Название товара', 'Количество изделий', 'Срок до выполнения'])
        self.tableWidget.setStyleSheet("background-color: rgb(255, 255, 255);")

        massive = ['Номер заказа', 'Имя клиента', 'Название товара', 'Количество изделий', 'Срок до выполнения']
        count = 0
        for items in massive:
            item = QtWidgets.QTableWidgetItem(items)
            item.setBackground(QtGui.QColor(120, 120, 120))
            self.tableWidget.setHorizontalHeaderItem(count, item)
            count += 1

        self.tableWidget.verticalHeader().setVisible(False)
        self.tableWidget.horizontalHeader().setFixedHeight(60)
        self.tableWidget.setFont(QtGui.QFont('Arial', 12))
        self.tableWidget.horizontalHeaderItem(0).setFont(QtGui.QFont('Arial', 12))
        self.tableWidget.horizontalHeaderItem(1).setFont(QtGui.QFont('Arial', 12))
        self.tableWidget.horizontalHeaderItem(2).setFont(QtGui.QFont('Arial', 12))
        self.tableWidget.horizontalHeaderItem(3).setFont(QtGui.QFont('Arial', 12))
        self.tableWidget.horizontalHeaderItem(4).setFont(QtGui.QFont('Arial', 12))

    def table_buttons(self): #кнопка добавить в таблицу
        self.add_button = QtWidgets.QPushButton('Добавить', self)
        self.add_button.setGeometry(200, 560, 120, 60)
        self.add_button.setStyleSheet("background-color: rgb(120, 120, 120);")
        self.add_button.clicked.connect(self.add_to_table)
        self.add_button.setFont(QtGui.QFont('Arial', 12))

        self.button_change = QtWidgets.QPushButton('Изменить', self)
        self.button_change.setGeometry(330, 560, 120, 60)
        self.button_change.setStyleSheet("background-color: rgb(120, 120, 120);")
        self.button_change.setFont(QtGui.QFont('Arial', 12))

        self.button_remove = QtWidgets.QPushButton('Удалить', self)
        self.button_remove.setGeometry(460, 560, 120, 60)
        self.button_remove.clicked.connect(self.remove_row)
        self.button_remove.setStyleSheet("background-color: rgb(120, 120, 120);")
        self.button_remove.setFont(QtGui.QFont('Arial', 12))

    def add_to_table(self): # переход к форме, если нажата кнопка добавить
        self.add_table_form = AddTableForm()
        self.add_table_form.show()
        self.close()

    def button_to_home(self): # кнопка вернуться назад
        self.button_exit_from_director = QtWidgets.QPushButton('Назад', self)
        self.button_exit_from_director.setGeometry(60, 675, 120, 60)
        self.button_exit_from_director.clicked.connect(self.exit_from_director_to_home)
        self.button_exit_from_director.setStyleSheet("background-color: rgb(120, 120, 120);")
        self.button_exit_from_director.setFont(QtGui.QFont('Arial', 13))

    def deadline_date(self): # подсчет времени до отгрузки товара
        time_now = self.date.split('-')
        year, month, day = time_now[0], time_now[1], time_now[2]

        import datetime

        delta = datetime.datetime(int(year), int(month), int(day)) - datetime.datetime.now()

        self.date = str(delta.days) + ' ' + str(delta.seconds // 3600) + ':' + str((delta.seconds // 60) % 60) + ':' + str(delta.seconds % 60)

    @decorator
    def open_data(self): # создание таблицы из csv файла
        with open('csv_dem_exam.csv', 'r', encoding='utf-8') as second_file:
            read_file = csv.reader(second_file)

            count_row = -1

            for values in read_file:
                values = ''.join(values).split(';')
                self.tableWidget.setRowCount(count_row + 1)
                self.tableWidget.setItem(count_row, 0, QTableWidgetItem(values[0]))
                self.tableWidget.setItem(count_row, 1, QTableWidgetItem(values[1]))
                self.tableWidget.setItem(count_row, 2, QTableWidgetItem(values[2]))
                self.tableWidget.setItem(count_row, 3, QTableWidgetItem(values[3]))
                self.date = values[4]
                if self.date[1] not in '0123456789':
                    self.tableWidget.setItem(count_row, 4, QTableWidgetItem(values[4]))
                else:
                    self.deadline_date()
                    self.tableWidget.setItem(count_row, 4, QTableWidgetItem(self.date))
                count_row += 1

    def remove_row(self): # удаление из таблицы выбранного элемента, если нажать на кнопку удалить
        if self.tableWidget.selectedIndexes():
            self.row = self.tableWidget.currentIndex().row()
            if self.row >= 0:
                self.tableWidget.removeRow(self.row)
                self.remove_row_csv()

    @decorator
    def remove_row_csv(self): # удаление из csv выбранного элемента в таблице, если нажать на кнопку удалить
        with open('csv_dem_exam.csv', 'r', encoding='utf-8') as file:
            file_reader = csv.reader(file)
            count = 0
            self.massive = []
            for i in file_reader:
                if count == self.row + 1:
                    result = i
                else:
                    self.massive.append(i)
                count += 1

        file_delete = open('csv_dem_exam.csv', 'w', encoding='utf-8')
        file_delete.truncate()

        with open('csv_dem_exam.csv', 'a', newline='', encoding='utf-8') as file_2:
            write_to_file = writer(file_2)
            for values in self.massive:
                write_to_file.writerow(values)
            file_2.close()



    def exit_from_director_to_home(self): # переход на главную страницу при нажатии кнопки назад
        from Main_window import MainWindow
        self.close()
        self.home = MainWindow()
        self.home.show()



class AddTableForm(QtWidgets.QDialog): # класс формы для добавления в таблицу
    def __init__(self): # основная настройка окна
        super(AddTableForm, self).__init__()
        self.setStyleSheet("background-color: rgb(210, 210, 210);")
        self.setGeometry(500, 300, 1000, 800)
        self.setMinimumSize(1000, 800)

        self.form_values()
        self.form_inputs()
        self.form_buttons()

    def decorator(func): # проверка функций на ошибки, принимает аргмент func - функцию, дальше обрабатывает ее на наличие ошибкм
        def inner(self):
            try:
                func(self)
            except Exception as e:
                print(e)
        return inner

    def form_values(self): # названия полей для ввода
        self.order_number_value = QLabel('Номер заказа:', self)
        self.order_number_value.setGeometry(250, 100, 250, 50)
        self.order_number_value.setFont(QtGui.QFont('Arial', 20))

        self.cilent_name_value = QLabel('Имя клиента:', self)
        self.cilent_name_value.setGeometry(260, 200, 250, 50)
        self.cilent_name_value.setFont(QtGui.QFont('Arial', 20))

        self.product_name_value = QLabel('Название товара:', self)
        self.product_name_value.setGeometry(200, 300, 300, 50)
        self.product_name_value.setFont(QtGui.QFont('Arial', 20))

        self.product_amount_value = QLabel('Количество товара:', self)
        self.product_amount_value.setGeometry(170, 400, 300, 50)
        self.product_amount_value.setFont(QtGui.QFont('Arial', 20))

        self.deadline_value = QLabel('Дата отгрузки:', self)
        self.deadline_value.setGeometry(250, 500, 500, 50)
        self.deadline_value.setFont(QtGui.QFont('Arial', 20))

    def form_inputs(self): # поля для ввода в форме
        self.order_number_input = QLineEdit(self)
        self.order_number_input.setGeometry(500, 100, 400, 50)
        self.order_number_input.setStyleSheet("background-color: rgb(255, 255, 255);")

        self.size_inputs = self.order_number_input.font()
        self.size_inputs.setPointSize(12)
        self.order_number_input.setFont(self.size_inputs)


        self.cilent_name_input = QLineEdit(self)
        self.cilent_name_input.setGeometry(500, 200, 400, 50)
        self.cilent_name_input.setFont(self.size_inputs)
        self.cilent_name_input.setStyleSheet("background-color: rgb(255, 255, 255);")

        self.product_name_input = QLineEdit(self)
        self.product_name_input.setGeometry(500, 300, 400, 50)
        self.product_name_input.setFont(self.size_inputs)
        self.product_name_input.setStyleSheet("background-color: rgb(255, 255, 255);")

        self.product_amount_input = QLineEdit(self)
        self.product_amount_input.setGeometry(500, 400, 400, 50)
        self.product_amount_input.setFont(self.size_inputs)
        self.product_amount_input.setStyleSheet("background-color: rgb(255, 255, 255);")

        self.deadline_input = QLineEdit(self)
        self.deadline_input.setGeometry(500, 500, 400, 50)
        self.deadline_input.setFont(self.size_inputs)
        self.deadline_input.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.deadline_input.setPlaceholderText("Пример: 2024-6-17")

    def form_buttons(self): # кнопки выход и принять в форме
        self.button_exit_from_form = QtWidgets.QPushButton('Выход', self)
        self.button_exit_from_form.setGeometry(60, 675, 120, 60)
        self.button_exit_from_form.clicked.connect(self.exit_from_form_to_director)
        self.button_exit_from_form.setStyleSheet("background-color: rgb(120, 120, 120);")
        self.button_exit_from_form.setFont(QtGui.QFont('Arial', 13))

        self.button_accept = QtWidgets.QPushButton('Принять', self)
        self.button_accept.setGeometry(640, 570, 120, 60)
        self.button_accept.setStyleSheet("background-color: rgb(120, 120, 120);")
        self.button_accept.clicked.connect(self.get_data_form)
        self.button_accept.setFont(QtGui.QFont('Arial', 13))

    def get_data_form(self): # обработка введенных значений в форму после нажатия кнопки принять
        self.order_number = self.order_number_input.text()
        self.cilent_name = self.cilent_name_input.text()
        self.product_name = self.product_name_input.text()
        self.product_amount = self.product_amount_input.text()
        self.deadline = self.deadline_input.text()

        if self.order_number == '' or self.cilent_name == '' or self.product_name == '' or self.product_amount == '' or self.deadline == '':
            self.form_error()
        else:
            try:
                self.data_form_to_table()
            except Exception as e:
                print(e)

    def form_error(self): # ошибка, если какие-то поля в форме не заполнены
        self.error = QMessageBox()
        self.error.setText('Заполните все поля')
        self.error.setGeometry(1000, 700, 1000, 700)
        self.error.setIcon(QMessageBox.Warning)
        self.error.setWindowTitle('Ошибка')
        self.error.setStandardButtons(QMessageBox.Ok | QMessageBox.No)

        self.error.exec_()

    @decorator
    def data_form_to_table(self): # вписывание в csv файл отправленных данных из формы
        with open('csv_dem_exam.csv', 'a', newline='', encoding='utf-8') as first_file:
            write_to_file = writer(first_file, delimiter=';')
            content = [self.order_number, self.cilent_name, self.product_name, self.product_amount, self.deadline]
            write_to_file.writerow(content)
            first_file.close()
        self.exit_from_form_to_director()

        # f = open("csv_dem_exam.csv", "w")
        # f.truncate()

    def exit_from_form_to_director(self): # переход из формы в окно директора
        self.close()
        self.Director_window = Director()
        self.Director_window.show()
