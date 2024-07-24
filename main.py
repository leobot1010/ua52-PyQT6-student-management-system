from PyQt6.QtWidgets import QApplication, QLabel, QWidget, QGridLayout, QLineEdit, QPushButton, QMainWindow, \
        QTableWidget, QTableWidgetItem, QDialog, QVBoxLayout, QComboBox
from PyQt6.QtGui import QAction
import sys
import sqlite3


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()  # runs the init of the parent class ie QMainWindow
        self.setWindowTitle("Student Management System")

        # ------ MENU ITEMS ------- #
        file_menu_item = self.menuBar().addMenu("&File")
        help_menu_item = self.menuBar().addMenu("&Help")

        # sub items
        add_student_action = QAction("Add Student", self)
        add_student_action.triggered.connect(self.insert)
        file_menu_item.addAction(add_student_action)

        about_action = QAction("About", self)
        help_menu_item.addAction(about_action)

        # -------- TABLE -------- #
        self.table = QTableWidget()
        self.table.setColumnCount(4)        # no of columns
        self.table.setHorizontalHeaderLabels(("Id", "Name", "Course", "Mobile"))      # column headings
        self.table.verticalHeader().setVisible(False)    # hides the default index column
        self.setCentralWidget(self.table)    # specify the table as the central/main widget

    def load_data(self):
        """ loads the student data to the program """
        connection = sqlite3.connect("database.db")   # connect to the .db file
        query = connection.execute("SELECT * FROM students")     # run a query

        self.table.setRowCount(0)

        for row_number, row_data in enumerate(query):       # row_data is each tuple record
            self.table.insertRow(row_number)     # create empty row: row 0, row 1, row 2 etc...
            for column_number, data in enumerate(row_data):
                self.table.setItem(row_number, column_number, QTableWidgetItem(str(data)))

        connection.close()

    def insert(self):
        dialog = InsertDialog()     # instantiate an InsertDialog Class
        dialog.exec()


class InsertDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Insert Student Data")
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        layout = QVBoxLayout()

        # Add student name widget
        self.student_name = QLineEdit()
        self.student_name.setPlaceholderText("Name")
        layout.addWidget(self.student_name)

        # Add course combo box
        self.subject = QComboBox()
        courses = ['Astronomy', 'Biology', 'Math', 'Physics']
        self.subject.addItems(courses)
        layout.addWidget(self.subject)

        # Add mobile number widget
        self.mobile_no = QLineEdit()
        self.mobile_no.setPlaceholderText("Phone")
        layout.addWidget(self.mobile_no)

        # Add submit button
        submit = QPushButton("Submit")
        submit.clicked.connect(self.add_student)
        layout.addWidget(submit)

        self.setLayout(layout)

    def add_student(self):
        name = self.student_name.text()         # get text from QlineEdit
        course = self.subject.itemText(self.subject.currentIndex())     # get text from selection in ComboBox
        mobile = self.mobile_no.text()      # get text from mobile QLineEdit
        connection = sqlite3.connect("database.db")     # connect to the database
        cursor = connection.cursor()     # we need a cursor object to insert data
        cursor.execute("INSERT INTO STUDENTS (name, course, mobile) VALUES (?, ?, ?)",
                       (name, course, mobile))
        connection.commit()
        cursor.close()
        connection.close()

        MainWindow_instance.load_data()


app = QApplication(sys.argv)

MainWindow_instance = MainWindow()    # initializes an instance of the main window
MainWindow_instance.show()            # opens the main windows with an empty table
MainWindow_instance.load_data()       # populates empty table with the data from the .sql file

sys.exit(app.exec())

