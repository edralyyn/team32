import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QHBoxLayout, QWidget, QTextEdit
from functions import collect_data, forecast

class ButtonCustomizer:
    @staticmethod
    def customize_button(button):
        button.setStyleSheet(
            "background-color: #3c7c6e; color: white; border-style: solid; border-width: 0px; font: bold; padding: 10px 10px;"
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
        self.nav_bar.setGeometry(0, 0, self.width(), 70)

        collect_button = QPushButton("Collect", self)
        collect_button.clicked.connect(self.on_collect_click)
        ButtonCustomizer.customize_button(collect_button)

        forecast_button = QPushButton("Forecast", self)
        forecast_button.clicked.connect(self.on_forecast_click)
        ButtonCustomizer.customize_button(forecast_button)

        self.nav_bar_layout.addWidget(collect_button)
        self.nav_bar_layout.addWidget(forecast_button)

        self.frame1 = QWidget(self)
        self.frame1.setStyleSheet("background-color: " + self.background_color + ";")
        self.frame1.setGeometry(0, 70, self.width() // 4, self.height() - 70)

        # Replace QWidget with QTextEdit for canvas1 and canvas2
        self.canvas1 = QTextEdit(self.frame1)
        self.canvas1.setStyleSheet("background-color: white;")
        self.canvas1.setGeometry(10, 10, self.frame1.width() - 20, self.frame1.height() - 20)

        self.frame2 = QWidget(self)
        self.frame2.setStyleSheet("background-color: " + self.background_color + ";")
        self.frame2.setGeometry(self.width() // 4, 70, self.width() * 3 // 4, self.height() - 70)

        self.canvas2 = QTextEdit(self.frame2)
        self.canvas2.setStyleSheet("background-color: white;")
        self.canvas2.setGeometry(10, 10, self.frame2.width() - 20, self.frame2.height() - 20)
        
        self.resizeEvent = self.resize_frames

    def resize_frames(self, event):
        width = event.size().width()

        frame1_width = width // 4
        frame2_width = width - frame1_width

        self.frame1.setGeometry(0, 70, frame1_width, self.height() - 70)
        self.canvas1.setGeometry(10, 10, self.frame1.width() - 20, self.frame1.height() - 20)

        self.frame2.setGeometry(frame1_width, 70, frame2_width, self.height() - 70)
        self.canvas2.setGeometry(10, 10, self.frame2.width() - 20, self.frame2.height() - 20)

    def on_collect_click(self):
        collect_data(self.canvas1)

    def on_forecast_click(self):
        forecast()

def main():
    app = QApplication(sys.argv)
    gui = GUI()
    gui.setGeometry(100, 100, 1200, 700)
    gui.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
