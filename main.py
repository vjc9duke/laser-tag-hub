import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel
from PyQt5.QtCore import Qt, QPropertyAnimation, QEasingCurve
from PyQt5.QtGui import QFont
from play_page import PlayPage
from story_page import StoryPage
from config_page import ConfigPage
from configparser import ConfigParser
from constants import *

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

        self.current_play = QLabel(f'Playing {self.get_current_game()}', self)
        self.current_play.setAlignment(Qt.AlignCenter)
        self.current_play.setFont(QFont('Arial', int(BUTTON_FONT_SIZE * 0.8)))
        self.current_play.setStyleSheet("background-color: #43DDFF; color: black; border-radius: 10px;")
        self.current_play.setGeometry(int(WIDTH/2 -  BUTTON_WIDTH/2) + BUTTON_WIDTH + INSET, INSET * 3 + 2 * BUTTON_HEIGHT + ATI, BUTTON_WIDTH, BUTTON_HEIGHT)
        
        self.config_button = QPushButton('CONFIG', self)
        self.config_button.setGeometry(int(WIDTH/2 -  BUTTON_WIDTH/2), INSET * 4 + 3 * BUTTON_HEIGHT + ATI, BUTTON_WIDTH, BUTTON_HEIGHT)
        self.config_button.setStyleSheet("background-color: #FFCC47; color: black; border-radius: 10px;")
        self.config_button.setFont(QFont('Arial', BUTTON_FONT_SIZE))
        self.config_button.clicked.connect(self.show_config_page)

        config = ConfigParser()
        config.read('config.ini')
        fullscreen = config.getboolean('General', 'fullscreen')
        
        if fullscreen:
            self.showFullScreen()

    def get_current_game(self):
        config = ConfigParser()
        config.read('story_config.ini')

        index = 0
        if 'selection' in config:
            index = config['selection']['select']

        return config['options'][f'op{index}']
    
    def show_play_page(self):
        self.play_page = PlayPage(self)
        # self.animate_change_page(self.play_page)
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
    
    def showEvent(self, event):
        self.current_play.setText(f'Playing {self.get_current_game()}')

    # def animate_change_page(self, page):
    #     page.setWindowOpacity(0.0)  # Set initial opacity to 0

    #     # Set up animation for fade-in effect
    #     fade_in_animation = QPropertyAnimation(page, b"windowOpacity")
    #     fade_in_animation.setDuration(500)  # Set duration in milliseconds
    #     fade_in_animation.setStartValue(0.0)
    #     fade_in_animation.setEndValue(1.0)
    #     fade_in_animation.setEasingCurve(QEasingCurve.InOutQuad)

    #     # Set up animation for fade-out effect for the main window
    #     fade_out_animation = QPropertyAnimation(self, b"windowOpacity")
    #     fade_out_animation.setDuration(500)  # Set duration in milliseconds
    #     fade_out_animation.setStartValue(1.0)
    #     fade_out_animation.setEndValue(0.0)
    #     fade_out_animation.setEasingCurve(QEasingCurve.InOutQuad)

    #     # Hide the main window after fade-out animation
    #     fade_out_animation.finished.connect(self.hide)

    #     # Start animations
    #     fade_in_animation.start()
    #     fade_out_animation.start()

    #     # Show the play page widget after fade-in animation
    #     self.hide()
    #     page.show()
    #     fade_in_animation.finished.connect(page.show)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
