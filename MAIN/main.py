import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QHBoxLayout, QWidget, QLabel
from PyQt5.QtCore import Qt
from functions import collect_data, forecast

class ButtonCustomizer:
    @staticmethod
    def customize_button(button):
        button.setStyleSheet(
        "background-color: #00563B; border-radius: 10px; color: white; border-style: solid; font: bold Arial; padding: 10px 10px;"
        )

class GUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.background_color = "#88a5cd"
        self.setWindowTitle("Predictive Maintenance System")
        self.setStyleSheet("background-color: " + self.background_color + ";")
        self.initUI()

    def initUI(self):
        self.nav_bar = QWidget(self)
        self.nav_bar_layout = QHBoxLayout()
        self.nav_bar.setLayout(self.nav_bar_layout)
        self.nav_bar.setGeometry(0, 0, self.width(), 50)
        self.nav_bar_layout.setAlignment(Qt.AlignLeft)

        collect_button = QPushButton("COLLECT", self)
        collect_button.clicked.connect(self.on_collect_click)
        ButtonCustomizer.customize_button(collect_button)

        forecast_button = QPushButton("FORECAST", self)
        forecast_button.clicked.connect(self.on_forecast_click)
        ButtonCustomizer.customize_button(forecast_button)

        self.nav_bar_layout.addWidget(collect_button)
        self.nav_bar_layout.addWidget(forecast_button)

        self.frame1 = QWidget(self)
        self.frame1.setStyleSheet("background-color: " + self.background_color + ";")

        self.canvas1 = QLabel(self.frame1)
        self.canvas1.setStyleSheet("background-color: white; border-radius: 10px;")
        self.canvas1.setAlignment(Qt.AlignTop)

        self.frame2 = QWidget(self)
        self.frame2.setStyleSheet("background-color: " + self.background_color + ";")

        self.canvas2 = QLabel(self.frame2)
        self.canvas2.setStyleSheet("background-color: white; border-radius: 10px;")


        self.resizeEvent = self.resize_frames

    def resize_frames(self, event):
        width = self.width()
        height = self.height()

        self.nav_bar.setGeometry(0, 0, width, 50)
        self.frame1.setGeometry(0, 50, width // 3, height - 50)
        self.canvas1.setGeometry(10, 0, self.frame1.width() - 20, self.frame1.height() - 20)
        self.frame2.setGeometry(width // 3, 50, width * 2 // 3, height - 50)
        self.canvas2.setGeometry(10, 0, self.frame2.width() - 20, self.frame2.height() - 20)

    def on_collect_click(self):
        collect_data(self.canvas1)

    def on_forecast_click(self):
        forecast()

def main():
    app = QApplication(sys.argv)
    gui = GUI()
    gui.setGeometry(100, 100, 1500, 700)
    gui.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
