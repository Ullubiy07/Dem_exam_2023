import Director_window
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow, QLineEdit, QLabel, QMessageBox
import sys

import csv


class MainWindow(QMainWindow): # класс главного окна
    def __init__(self): # основная настройка окна
        super(MainWindow, self).__init__()
        self.setStyleSheet("background-color: rgb(210, 210, 210);")
        self.setGeometry(400, 200, 1125, 800)
        self.setMinimumSize(1125, 800)
        self.setWindowTitle("Окно авторизации")

        self.password_values()
        self.exit_from()
        self.join_to()


    def decorator(func): # проверка функций на ошибки, принимает аргмент func - функцию, дальше обрабатывает ее на наличие ошибкм
        def inner(self, *args):
            try:
                func(self)
            except Exception as e:
                print(e)
        return inner

    def password_values(self): #ввод логина и пароля
        self.password_input = QLineEdit(self)
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setGeometry(450, 350, 400, 50)
        self.password_input.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.password_input.setFont(QtGui.QFont('Arial', 15))

        self.password_value = QLabel('Пароль:', self)
        self.password_value.setGeometry(220, 340, 200, 60)
        self.password_value.setFont(QtGui.QFont('Arial', 30))


        self.login_input = QLineEdit(self)
        self.login_input.setGeometry(450, 200, 400, 50)
        self.login_input.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.login_input.setPlaceholderText("Пример: 9164119009")
        self.login_input.setFont(QtGui.QFont('Arial', 15))

        self.login_value = QLabel('Логин:', self)
        self.login_value.setGeometry(250, 191, 200, 60)
        self.login_value.setFont(QtGui.QFont('Arial', 30))

    def exit_from(self): #выход из программы
        self.button_exit = QtWidgets.QPushButton('Выход', self)
        self.button_exit.setGeometry(50, 650, 120, 60)
        self.button_exit.setStyleSheet("background-color: rgb(120, 120, 120);")
        self.button_exit.clicked.connect(lambda: self.close())
        self.button_exit.setFont(QtGui.QFont('Arial', 13))

    def join_to(self): #войти под своим логином и паролем
        self.button_join = QtWidgets.QPushButton('Войти', self)
        self.button_join.setGeometry(550, 525, 120, 60)
        self.button_join.setStyleSheet("background-color: rgb(120, 120, 120);")
        self.button_join.clicked.connect(self.get_password_and_login)
        self.button_join.setFont(QtGui.QFont('Arial', 13))

    @decorator
    def check_permission(self): # проверка роли пользователя
        with open('scv_users.csv', 'r', encoding='utf-8') as file:
            file_reader = csv.reader(file)

            for users in file_reader:
                users = ''.join(users).split(';')
                if self.login == users[1] and self.password == users[2]:
                    self.access = True
                    self.user_name = users[0]
                    self.user_password = users[2]
                    self.user_permission = users[3]

    def get_password_and_login(self): #сохранить пароль и логин, обработать и перевести на соответствующую страницу
        self.password = self.password_input.text()
        self.login = self.login_input.text()
        digits = '0123456789'

        self.errors = True
        self.errors_empty()
        self.access = False
        self.check_permission()

        if len(self.login) == 10 and not self.errors:
            count = 0
            for dig in self.login:
                if dig in digits:
                    count += 1
            if count == 10:
                if self.access:
                    from Director_window import Director
                    from Admin_window import Admin
                    if self.user_permission == 'директор':
                        self.Director_window = Director(self.user_name)
                        self.Director_window.show()
                    elif self.user_permission == 'администратор':
                        self.Admin_window = Admin(self.user_name)
                        self.Admin_window.show()
                    self.close()

        if self.password != '' and self.login != '' and not self.access:
            self.error()


    def errors_empty(self): #ошибки при входе в аккаунт
        if self.login == '':
            self.error_login = QMessageBox()
            self.error_login.setWindowTitle('Ошибка')
            self.error_login.setText('Вы не ввели логин')
            self.error_login.setIcon(QMessageBox.Warning)
            self.error_login.setStandardButtons(QMessageBox.Ok)

            self.error_login.exec_()

        elif self.password == '':
            self.error_password = QMessageBox()
            self.error_password.setWindowTitle('Ошибка')
            self.error_password.setText('Вы не ввели пароль')
            self.error_password.setIcon(QMessageBox.Warning)
            self.error_password.setStandardButtons(QMessageBox.Ok)

            self.error_password.exec_()
        else:
            self.errors = False

    def error(self): # ошибка, если такого пароля и логина нету
        self.error_join = QMessageBox()
        self.error_join.setWindowTitle('Ошибка')
        self.error_join.setText('Неверный логин или пароль')
        self.error_join.setIcon(QMessageBox.Information)
        self.error_join.setStandardButtons(QMessageBox.Ok)

        self.error_join.exec_()

def aplication(): # запуск программы
    app = QApplication(sys.argv)
    app.setStyle(QtWidgets.QStyleFactory.create('Fusion'))
    Main_window = MainWindow()
    Main_window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    aplication()
