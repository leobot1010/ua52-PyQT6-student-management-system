from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QLabel, QWidget, QGridLayout, QLineEdit, QPushButton, QMainWindow, \
        QTableWidget, QTableWidgetItem, QDialog, QVBoxLayout, QComboBox, QToolBar, QStatusBar, QMessageBox
from PyQt6.QtGui import QAction, QIcon
import sys
import sqlite3


class DatabaseConnection:
    def __init__(self, database_file="database.db"):
        self.database_file = database_file

    def connect(self):
        connection = sqlite3.connect(self.database_file)             # connect to the .db file
        return connection



"""  >>>>>>>>>>>>>>>>>>>>>>>>>    MAIN WINDOW   >>>>>>>>>>>>>>>>>>>>>>>>>>    """


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()  # runs the init of the parent class ie QMainWindow
        self.setWindowTitle("Student Management System")
        self.setMinimumSize(800, 600)

        # ------ MENU ITEMS ------- #

        file_menu_item = self.menuBar().addMenu("&File")
        edit_menu_item = self.menuBar().addMenu("&Edit")
        help_menu_item = self.menuBar().addMenu("&Help")

        # sub items
        add_student_action = QAction(QIcon("icons/add.png"), "Add Student", self)
        file_menu_item.addAction(add_student_action)
        add_student_action.triggered.connect(self.insert_student)          # triggers the insert student window

        search_student_action = QAction(QIcon("icons/search.png"), "Search", self)
        edit_menu_item.addAction(search_student_action)
        search_student_action.triggered.connect(self.search_student)       # triggers the search student window

        about_action = QAction("About", self)
        help_menu_item.addAction(about_action)
        about_action.triggered.connect(self.about)

        # -------- TOOLBAR ------ #

        toolbar = QToolBar()       # create to toolbar instance
        toolbar.setMovable(True)   # allow the toolbar to be moveable
        self.addToolBar(toolbar)   # add the toolbar to self, self is the main window instance

        toolbar.addAction(add_student_action)
        toolbar.addAction(search_student_action)

        # -------- TABLE -------- #

        self.table = QTableWidget()
        self.table.setColumnCount(4)        # sets no of columns
        self.table.setHorizontalHeaderLabels(("Id", "Name", "Course", "Mobile"))      # column headings
        self.table.verticalHeader().setVisible(False)    # hides the default index column
        self.setCentralWidget(self.table)    # specify the table as the central/main widget

        # ------ STATUS BAR ------ #    To def(cell_clicked)

        self.status_bar = QStatusBar()       # create a status bar instance
        self.setStatusBar(self.status_bar)   # add the status bar to self, self is the main window

        # calls the cell_clicked method every time a cell is highlighted by user
        self.table.cellClicked.connect(self.cell_clicked)

    def cell_clicked(self):
        """ called everytime that a cell in the table is clicked"""
        # From Status Bar
        # create edit button
        edit_button = QPushButton("Edit Record")
        edit_button.clicked.connect(self.edit)

        # create delete button
        delete_button = QPushButton("Delete Record")
        delete_button.clicked.connect(self.delete)

        # deletes the buttons to prevent added successive buttons
        children = self.findChildren(QPushButton)
        if children:
            for child in children:
                self.status_bar.removeWidget(child)

        # add buttons to status bar
        self.status_bar.addWidget(edit_button)
        self.status_bar.addWidget(delete_button)




    def load_data(self):
        """ loads the student data to the program """
        connection = DatabaseConnection().connect()
        query = connection.execute("SELECT * FROM students")     # run a query

        self.table.setRowCount(0)

        for row_number, row_data in enumerate(query):       # row_data is each tuple record
            self.table.insertRow(row_number)     # create empty row: row 0, row 1, row 2 etc...
            for column_number, data in enumerate(row_data):
                self.table.setItem(row_number, column_number, QTableWidgetItem(str(data)))

        connection.close()

    # CALL THE ADD STUDENT WINDOW, THE SEARCH STUDENT WINDOW
    def insert_student(self):
        dialog = InsertDialog()     # instantiate the InsertDialog Class
        dialog.exec()

    def search_student(self):
        dialog = SearchDialog()     # instantiate the InsertDialog Class
        dialog.exec()

    def edit(self):
        dialog = EditDialog()
        dialog.exec()

    def delete(self):
        dialog = DeleteDialog()
        dialog.exec()

    def about(self):
        dialog = AboutDialog()
        dialog.exec()


"""  >>>>>>>>>>>>>>>>>>>>>>>>>    DIALOG WINDOWS   >>>>>>>>>>>>>>>>>>>>>>>>>>    """


class AboutDialog(QMessageBox):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("About")
        content = """
        This app was created in the Udemy Python Course by Ardit.
        """
        self.setText(content)


class EditDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Update Student Data")
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        layout = QVBoxLayout()

        # Get student name from selected row
        index = MainWindow_instance.table.currentRow()   # the index of the row that is clicked on
        student_name = MainWindow_instance.table.item(index, 1).text()

        # Add student name widget
        self.student_name = QLineEdit(student_name)
        self.student_name.setPlaceholderText("Name")
        layout.addWidget(self.student_name)

        # Get subject from Combo Box
        course_name = MainWindow_instance.table.item(index, 2).text()

        # Add Combo box widget
        self.subject = QComboBox()
        courses = ['Astronomy', 'Biology', 'Math', 'Physics']
        self.subject.addItems(courses)
        self.subject.setCurrentText(course_name)
        layout.addWidget(self.subject)

        # Get mobile from selected row
        # index = MainWindow_instance.table.currentRow()
        mobile = MainWindow_instance.table.item(index, 3).text()

        # Add mobile number widget
        self.mobile_no = QLineEdit(mobile)
        self.mobile_no.setPlaceholderText("Phone")
        layout.addWidget(self.mobile_no)

        # Get student_id of selected row/student
        self.student_id = MainWindow_instance.table.item(index, 0).text()

        # Add submit button
        submit = QPushButton("Update")
        submit.clicked.connect(self.update_student)     # calls update_student method below
        layout.addWidget(submit)

        self.setLayout(layout)

    def update_student(self):
        name = self.student_name.text()
        course = self.subject.itemText(self.subject.currentIndex())    # combobox has different extraction method
        mobile = self.mobile_no.text()
        id = self.student_id

        connection = DatabaseConnection().connect()
        cursor = connection.cursor()
        cursor.execute("UPDATE students SET name = ?, course = ?, mobile = ? WHERE id = ?",
                       (name, course, mobile, id))

        connection.commit()
        cursor.close()
        connection.close()

        #Refresh the table
        MainWindow_instance.load_data()


class DeleteDialog(QDialog, QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Delete Student Data")

        layout = QGridLayout()    # We use grid layout because there are more than 1 grid columns

        index = MainWindow_instance.table.currentRow()
        student_name = MainWindow_instance.table.item(index, 1).text()

        confirmation = QLabel(f"WARNING: This will delete ALL the data of {student_name}"
                              f"Are you sure you want to continue?")
        yes = QPushButton("Yes")
        no = QPushButton("no")

        # arranges the widgets to the grid
        layout.addWidget(confirmation, 0, 0, 1, 2)
        layout.addWidget(yes, 1, 0)
        layout.addWidget(no, 1, 1)
        self.setLayout(layout)

        yes.clicked.connect(self.delete_student)    # calls delete_student method, below
        no.clicked.connect(self.close)

    # def close_wi

    def delete_student(self):
        index = MainWindow_instance.table.currentRow()   # get the index of the row that is clicked on
        id = MainWindow_instance.table.item(index, 0).text()   # 0 is the id column
        student_name = MainWindow_instance.table.item(index, 1).text()
        # print(f"Name: {name}")

        # connect to the database
        connection = DatabaseConnection().connect()
        cursor = connection.cursor()
        cursor.execute(f"DELETE FROM students WHERE id = {id}")

        # commit changes and close connection to database
        connection.commit()
        cursor.close()
        connection.close()

        # refresh the table
        MainWindow_instance.load_data()

        self.close()  # close window

        confirmation_window = QMessageBox()
        confirmation_window.setWindowTitle("Completed")
        confirmation_window.setText(f"{student_name}'s record has been deleted")
        confirmation_window.exec()


"""  >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>   ADD STUDENT WINDOW   >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>    """

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
        name = self.student_name.text()                          # get text from QlineEdit
        course = self.subject.itemText(self.subject.currentIndex())     # get text from selection in ComboBox
        mobile = self.mobile_no.text()                           # get text from mobile QLineEdit

        connection = DatabaseConnection().connect()
        cursor = connection.cursor()                             # we need a cursor object to insert data
        cursor.execute("INSERT INTO STUDENTS (name, course, mobile) VALUES (?, ?, ?)",
                       (name, course, mobile))
        connection.commit()
        cursor.close()
        connection.close()

        MainWindow_instance.load_data()      # Refresh: reloads the data from the database


"""  >>>>>>>>>>>>>>>>>>>>>>>>>    SEARCH STUDENT WINDOW   >>>>>>>>>>>>>>>>>>>>>>>>>>    """

class SearchDialog(QDialog):
    def __init__(self):
        super().__init__()

        # Set window title and size
        self.setWindowTitle("Search Student")
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        layout = QVBoxLayout()

        # Search student name widget
        self.student_name = QLineEdit()               # variable that contains user search name
        self.student_name.setPlaceholderText("Name")
        layout.addWidget(self.student_name)

        # Add search button
        submit = QPushButton("Search")
        submit.clicked.connect(self.search)   # call the search method
        layout.addWidget(submit)

        self.setLayout(layout)

    def search(self):
        name = self.student_name.text()             # grabs the name currently in the text box

        connection = DatabaseConnection().connect()
        cursor = connection.cursor()

        query = cursor.execute("SELECT * FROM students WHERE name = ?", (name,))
        rows = list(query)
        print(rows)
        items = MainWindow_instance.table.findItems(name, Qt.MatchFlag.MatchFixedString)
        for item in items:
            print(item)
            MainWindow_instance.table.item(item.row(), 1).setSelected(True)

        cursor.close()
        connection.close()


"""  >>>>>>>>>>>>>>>>>>>>>>>>>    EXECUTE   >>>>>>>>>>>>>>>>>>>>>>>>>>    """

app = QApplication(sys.argv)

MainWindow_instance = MainWindow()    # initializes an instance of the main window
MainWindow_instance.show()            # opens the main windows with an empty table
MainWindow_instance.load_data()       # populates empty table with the data from the .sql file

sys.exit(app.exec())

