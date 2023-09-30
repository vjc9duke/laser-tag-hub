from PyQt5.QtWidgets import QWidget, QPushButton
from PyQt5.QtGui import QFont

class StoryPage(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.setWindowTitle('Story Page')
        self.setGeometry(0, 0, 800, 480)
        self.setStyleSheet("background-color: black; color: white;")
        
        back_button = QPushButton('Back', self)
        back_button.setGeometry(50, 50, 200, 100)
        back_button.setFont(QFont('Arial', 20))
        back_button.clicked.connect(self.show_main_page)
    
    def show_main_page(self):
        self.parent.show()
        self.hide()
