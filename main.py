import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from play_page import PlayPage
from story_page import StoryPage
from config_page import ConfigPage

WIDTH = 800
HEIGHT = 480
BUTTON_WIDTH = 200
BUTTON_HEIGHT = 75
BUTTON_FONT_SIZE = 30
INSET = 20
ATI = 10  # additional title inset

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Main Page')
        self.setGeometry(0, 0, WIDTH, HEIGHT)
        self.setStyleSheet("background-color: black; color: white;")

        self.title_label = QLabel('Quantum Quest Arena', self)
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setGeometry(int(WIDTH/2 - 350), INSET, 700, BUTTON_HEIGHT)
        self.title_label.setFont(QFont('Arial', 40))
        self.title_label.setStyleSheet("background-color: #F61A1A; color: white; border-radius: 10px;")
        
        self.play_button = QPushButton('PLAY', self)
        self.play_button.setGeometry(int(WIDTH/2 - BUTTON_WIDTH/2), INSET * 2 + BUTTON_HEIGHT + ATI, BUTTON_WIDTH, BUTTON_HEIGHT)
        self.play_button.setStyleSheet("background-color: #47FF43; color: black; border-radius: 10px;")
        self.play_button.setFont(QFont('Arial', BUTTON_FONT_SIZE))
        self.play_button.clicked.connect(self.show_play_page)
        
        self.story_button = QPushButton('STORY', self)
        self.story_button.setGeometry(int(WIDTH/2 -  BUTTON_WIDTH/2), INSET * 3 + 2 * BUTTON_HEIGHT + ATI, BUTTON_WIDTH, BUTTON_HEIGHT)
        self.story_button.setStyleSheet("background-color: #43DDFF; color: black; border-radius: 10px;")
        self.story_button.setFont(QFont('Arial', BUTTON_FONT_SIZE))
        self.story_button.clicked.connect(self.show_story_page)
        
        self.config_button = QPushButton('CONFIG', self)
        self.config_button.setGeometry(int(WIDTH/2 -  BUTTON_WIDTH/2), INSET * 4 + 3 * BUTTON_HEIGHT + ATI, BUTTON_WIDTH, BUTTON_HEIGHT)
        self.config_button.setStyleSheet("background-color: #FFCC47; color: black; border-radius: 10px;")
        self.config_button.setFont(QFont('Arial', BUTTON_FONT_SIZE))
        self.config_button.clicked.connect(self.show_config_page)
    
    def show_play_page(self):
        self.play_page = PlayPage(self)
        self.play_page.show()
        self.hide()
    
    def show_story_page(self):
        self.story_page = StoryPage(self)
        self.story_page.show()
        self.hide()
    
    def show_config_page(self):
        self.config_page = ConfigPage(self)
        self.config_page.show()
        self.hide()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
