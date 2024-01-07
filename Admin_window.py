from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QLabel, QPushButton, QTableWidgetItem
from Main_window import  MainWindow
import csv


class Admin(QtWidgets.QDialog): # класс окна админа
    def __init__(self, name_user=None): # основная настройка окна, принимает именованный аргумент name_user - имя человека который зашел в это окно
        super(Admin, self).__init__()
        self.setStyleSheet("background-color: rgb(210, 210, 210);")
        self.setGeometry(400, 200, 1125, 800)
        self.setMinimumSize(1125, 800)
        self.setWindowTitle('Окно администратора')

        self.name_user = name_user
        self.greetings = QLabel(f'Добро пожаловать, {self.name_user}!', self)
        self.greetings.setFont(QtGui.QFont('Arial', 27))
        self.greetings.setGeometry(250, 70, 450, 150)
        self.greetings.adjustSize()

        self.button_to_home()
        self.create_table_users()
        self.users_data_to_table()


    def decorator(func): # проверка функций на ошибки, принимает аргмент func - функцию, дальше обрабатывает ее на наличие ошибкм
        def inner(self, *args):
            try:
                func(self)
            except Exception as e:
                print(e)
        return inner

    def button_to_home(self): # кнопка вернуться назад на главную страницу
        self.button_exit_admin = QtWidgets.QPushButton('Назад', self)
        self.button_exit_admin.setGeometry(50, 650, 120, 60)
        self.button_exit_admin.setStyleSheet("background-color: rgb(120, 120, 120);")
        self.button_exit_admin.clicked.connect(self.admin_to_home)
        self.button_exit_admin.setFont(QtGui.QFont('Arial', 13))

    def create_table_users(self): # создание таблицы в окне администратора
        self.users_table = QtWidgets.QTableWidget(self)
        self.users_table.setColumnCount(4)
        self.users_table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.users_table.setHorizontalHeaderLabels(['Имя пользователя', 'Логин', 'Пароль', 'Роль'])
        self.users_table.setGeometry(150, 220, 830, 350)
        self.users_table.setColumnWidth(0, 200)
        self.users_table.setColumnWidth(1, 200)
        self.users_table.setColumnWidth(2, 200)
        self.users_table.setColumnWidth(3, 200)
        self.users_table.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.users_table.verticalHeader().setVisible(False)

        massive = ['Имя пользователя', 'Логин', 'Пароль', 'Роль']
        count = 0
        for items in massive:
            item = QtWidgets.QTableWidgetItem(items)
            item.setBackground(QtGui.QColor(120, 120, 120))
            self.users_table.setHorizontalHeaderItem(count, item)
            count += 1

        self.users_table.horizontalHeader().setFixedHeight(60)
        self.users_table.setFont(QtGui.QFont('Arial', 12))
        self.users_table.horizontalHeaderItem(0).setFont(QtGui.QFont('Arial', 12))
        self.users_table.horizontalHeaderItem(1).setFont(QtGui.QFont('Arial', 12))
        self.users_table.horizontalHeaderItem(2).setFont(QtGui.QFont('Arial', 12))
        self.users_table.horizontalHeaderItem(3).setFont(QtGui.QFont('Arial', 12))


    @decorator
    def users_data_to_table(self): # добавление данных пользователей в таблицу
        with open('scv_users.csv', 'r', encoding='utf-8') as file:
            file_reader = csv.reader(file)

            count_row = -1
            for users in file_reader:
                users = ''.join(users).split(';')
                self.users_table.setRowCount(count_row + 1)
                self.users_table.setItem(count_row, 0, QTableWidgetItem(users[0]))
                self.users_table.setItem(count_row, 1, QTableWidgetItem(users[1]))
                self.users_table.setItem(count_row, 2, QTableWidgetItem(users[2]))
                self.users_table.setItem(count_row, 3, QTableWidgetItem(users[3]))
                count_row += 1

    def admin_to_home(self): # переход на главную страницу если нажата кнопка назад
        self.home = MainWindow()
        self.home.show()
        self.close()
