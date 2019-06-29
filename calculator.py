import sys
# Импортируем наш интерфейс из файла
from kalkulator import *
from PyQt5 import QtCore, QtGui, QtWidgets

sys.path.append('D:\PyPrograms\Kalkulator\kalkulator.py')

#создаём класс наследующий от класса QtWidgets.QMainWindow
class MyWin(QtWidgets.QMainWindow):

    #Значение firstNum оставляем неопределённым в начале выполнения программы.
    firstNum = None
    UserIsTypingSecondNum = False
    Zero = False

    def __init__(self, parent=None):
        """Основная функция программы которая присоединяет кнопки и переменные."""
        QtWidgets.QWidget.__init__(self, parent)
        #Назначаем классу Ui_window краткое название ui для быстрого доступа к ней, то же делаем с функцией setupUi.
        self.ui = Ui_window()
        self.ui.setupUi(self)

        # Инициализация кнопок цифр на калькуляторе и события происходящих при их нажатии.      
        self.ui.num0.clicked.connect(self.widget_pressed)
        self.ui.num1.clicked.connect(self.widget_pressed)
        self.ui.num2.clicked.connect(self.widget_pressed)
        self.ui.num3.clicked.connect(self.widget_pressed)
        self.ui.num4.clicked.connect(self.widget_pressed)
        self.ui.num5.clicked.connect(self.widget_pressed)
        self.ui.num6.clicked.connect(self.widget_pressed)
        self.ui.num7.clicked.connect(self.widget_pressed)
        self.ui.num8.clicked.connect(self.widget_pressed)
        self.ui.num9.clicked.connect(self.widget_pressed)

        #Инициализация кнопки точки на калькуляторе и её события при нажатии.
        self.ui.comma.clicked.connect(self.comma_pressed)

        #Инициализация кнопок % и +/-
        self.ui.plus_minus.clicked.connect(self.pocent_PM_press)
        self.ui.procent.clicked.connect(self.pocent_PM_press)

        #Инициализация кнопок действий(кроме равно)
        self.ui.plus.clicked.connect(self.binary_operations)
        self.ui.minus.clicked.connect(self.binary_operations)
        self.ui.multiply.clicked.connect(self.binary_operations)
        self.ui.divide.clicked.connect(self.binary_operations)

        #Инициализация кнопок равно и стереть.
        self.ui.equally.clicked.connect(self.equals_pressed)
        self.ui.clear_all.clicked.connect(self.clear_pressed)

        #Даём возможность проверять кнопки операций на доступность.
        self.ui.plus.setCheckable(True)
        self.ui.minus.setCheckable(True)
        self.ui.divide.setCheckable(True)
        self.ui.multiply.setCheckable(True)
        self.text_size_check()
        self.set_font(15)

    def set_font(self,size):
        font = QtGui.QFont()
        font.setPointSize(size)
        self.ui.label.setFont(font)

    def text_size_check(self):
        if (len(self.ui.label.text()) >= 15):
            self.set_font(13)
        else:
            self.set_font(15)


    def widget_pressed(self):
        """Функция, срабатывает при нажатии на одну из цифр"""
        if not self.Zero:
            #sender() - определяет какая именно кнопка была нажата и записывает её имя в переменную button
            button = self.sender()
            #Проверка, активна ли какая либо из вычислительных операций.
            if ((self.ui.plus.isChecked() or self.ui.minus.isChecked() or self.ui.multiply.isChecked() or self.ui.divide.isChecked()) 
                    and (not self.UserIsTypingSecondNum)):
                #Переменная newLabel берёт значиние кнопки, нажатой после вычислительной операции.
                newLabel = format(float(button.text()), '.15g')
                self.UserIsTypingSecondNum = True
            else:
                #Если в введённом числе уже есть точка, и нажата кнопка 0, то программа добавит его к числу.
                if (('.' in self.ui.label.text()) and (button.text() == '0')):
                    newLabel = format(self.ui.label.text() + button.text(), '.15')
                #Иначе программа просто прибавит значение нажатой кнопки к уже введённым числам и запишет всё это в переменную newLabel.
                else:
                    if (len(self.ui.label.text()) > 14):
                        newLabel = format(self.ui.label.text())
                    else:
                        newLabel = format(float(self.ui.label.text() + button.text()), '.15g')
            #В конечном счете окно ввода чисел запишет в себя значение переменной newLabel
            self.ui.label.setText(newLabel)
 
    def comma_pressed(self):
        """Функция обрабатывает нажатие на кнопку сточкой для десятичного деления"""
        #Прибавление точки к уже введённым данным.
        #Если точка уже есть, то ничего не происходит.
        if not self.Zero:
            if('.' in self.ui.label.text()):
                self.ui.label.setText(self.ui.label.text())
            else:
                self.ui.label.setText(self.ui.label.text() + '.')

    def pocent_PM_press(self):
        """Функция обрабатывает нажатие на кнопку процента и смены знака"""
        if not self.Zero:
            button = self.sender()

            #Запись в переменную labelNumber текстового значения окна.
            labelNumber = float(self.ui.label.text())
            if button.text() == '+/-':
                labelNumber*=-1
            else: #если будет нажата клавиша %
                labelNumber*=0.01
        
            newLabel = format(labelNumber, '.15g')
            self.ui.label.setText(newLabel)

    def binary_operations(self):
        """Функция обрабатывает нажатие кнопок вычислительных операций"""

        if not self.Zero:
            button = self.sender()
            self.firstNum = float(self.ui.label.text())
            #Нажатая кнопка становится активной.
            button.setChecked(True)

    def equals_pressed(self):
        """Функция обрабатывает нажатие кнопки равенства"""
        #В переменную secondNum помещается значение текстового поля.
        if not self.Zero:
            secondNum = float(self.ui.label.text())

            #Условия проверяющие, активна какая либо из вычислительных операций.
            if self.ui.plus.isChecked():
                #В переменную labelNumber записывается вычислительное действие между переменными firstNum и secondNum.
                labelNumber = self.firstNum + secondNum
                newLabel = format(labelNumber, '.15g')
                #Окно берёт текстовое знаение сделанных выше вычислений.
                self.ui.label.setText(newLabel)
                self.text_size_check()
                #Происходит дизактивация нажатой ранее кнопки орифметического действия.
                self.ui.plus.setChecked(False)
            if self.ui.minus.isChecked():
                labelNumber = self.firstNum - secondNum
                newLabel = format(labelNumber, '.15g')
                self.ui.label.setText(newLabel)
                self.text_size_check()
                self.ui.minus.setChecked(False)
            if self.ui.multiply.isChecked():
                labelNumber = self.firstNum * secondNum
                newLabel = format(labelNumber, '.15g')
                self.ui.label.setText(newLabel)
                self.text_size_check()
                self.ui.multiply.setChecked(False)
            if self.ui.divide.isChecked():
                try:
                    labelNumber = self.firstNum / secondNum
                    newLabel = format(labelNumber, '.15g')
                    self.ui.label.setText(newLabel)
                    self.text_size_check()
                    self.ui.divide.setChecked(False)

                except ZeroDivisionError:
                    self.set_font(12)
                    self.ui.label.setText('Нельзя делить на ноль!')
                    self.ui.plus.setChecked(False)
                    self.ui.minus.setChecked(False)
                    self.ui.divide.setChecked(False)
                    self.ui.multiply.setChecked(False)
                    self.UserIsTypingSecondNum = False
                    self.Zero = True

            #Переменная ниже, берёт ложное значение.
            self.UserIsTypingSecondNum = False

    def clear_pressed(self):
        """Функция обрабатывает нажатие на кнопку стереть"""
        #Дизактивация всех орифметических действий 
        self.ui.plus.setChecked(False)
        self.ui.minus.setChecked(False)
        self.ui.divide.setChecked(False)
        self.ui.multiply.setChecked(False)
        self.UserIsTypingSecondNum = False
        self.set_font(15)
        #Поле принимает значение 0.
        self.ui.label.setText('0')
        self.Zero = False

#Запуск окна и самой апликации.
if __name__=="__main__":
    app = QtWidgets.QApplication(sys.argv)
    myapp = MyWin()
    myapp.show()
    sys.exit(app.exec_())