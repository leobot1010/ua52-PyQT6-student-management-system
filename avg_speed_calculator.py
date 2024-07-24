from PyQt6.QtWidgets import QApplication, QLabel, QWidget, QGridLayout, QLineEdit, QComboBox, QPushButton
import sys


class SpeedCalculator(QWidget):
    def __init__(self):

        # CORE SET-UP
        super().__init__()
        self.setWindowTitle("Age calculator")  # window title
        grid = QGridLayout()  # creates an invisible grid

        # ADD WIDGETS
        distance_label = QLabel("Distance:")
        self.user_distance = QLineEdit()

        time_label = QLabel("Time(hours):")
        self.user_time = QLineEdit()

        self.user_km_or_miles = QComboBox()
        self.user_km_or_miles.addItems(['  Metric (km)', '  Imperial (miles)'])

        calculate_button = QPushButton("Calculate")
        calculate_button.clicked.connect(self.calculate_speed)  # calls calculate_speed method
        self.output_label = QLabel("")

        # ADD WIDGETS TO GRID
        grid.addWidget(self.user_km_or_miles, 0, 2)
        grid.addWidget(distance_label, 0, 0)
        grid.addWidget(self.user_distance, 0, 1)
        grid.addWidget(time_label, 1, 0)
        grid.addWidget(self.user_time, 1, 1)
        grid.addWidget(calculate_button, 2, 1)
        grid.addWidget(self.output_label, 3, 1)

        self.setLayout(grid)

    def calculate_speed(self):
        distance = self.user_distance.text()
        time = self.user_time.text()
        avg_speed = round(int(distance) / int(time))
        avg_speed = str(avg_speed)

        if self.user_km_or_miles.currentText() == '  Metric (km)':
            self.output_label.setText(f"Average speed was {avg_speed}kph")

        if self.user_km_or_miles.currentText() == '  Imperial (miles)':
            self.output_label.setText(f"Average speed was {avg_speed}mph")


app = QApplication(sys.argv)
speed_calculator = SpeedCalculator()
speed_calculator.show()
sys.exit(app.exec())



# combo = QComboBox()
# combo.addItems(['Metric (km)', 'Imperial (miles)'])
#
# if combo.currentText() == 'Metric (km)':
#     "do something"
# if combo.currentText() == 'Imperial (miles)':
#     "do something else"