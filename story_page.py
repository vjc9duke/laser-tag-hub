from PyQt5.QtWidgets import QWidget, QPushButton, QLabel
from PyQt5.QtGui import QFont
from configparser import ConfigParser
from PyQt5.QtCore import Qt
from constants import *
import functools

class StoryPage(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.setWindowTitle('Story Page')
        self.setGeometry(0, 0, 800, 480)
        self.setStyleSheet("background-color: black; color: white;")
        
        self.title_label = QLabel('STORY SELECT', self)
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setGeometry(int(WIDTH/2 - 350), INSET, 700, BUTTON_HEIGHT)
        self.title_label.setFont(QFont('Arial', 40))
        self.title_label.setStyleSheet("background-color: #F61A1A; color: white; border-radius: 10px;")
        
        self.options = self.get_options()
        for index, option in enumerate(self.options):
            button = QPushButton(self.options.get(option), self)
            button.setGeometry(int(WIDTH/2 - BUTTON_WIDTH/2), INSET * (index+2) + (index+1) * BUTTON_HEIGHT + ATI, BUTTON_WIDTH, BUTTON_HEIGHT)
            button.setStyleSheet("background-color: #47FF43; color: black; border-radius: 10px;")
            button.setFont(QFont('Arial', BUTTON_FONT_SIZE))
            button.clicked.connect(functools.partial(self.show_main_page, index))

        # self.play_button = QPushButton('PLAY', self)
        # self.play_button.setGeometry(int(WIDTH/2 - BUTTON_WIDTH/2), INSET * 2 + BUTTON_HEIGHT + ATI, BUTTON_WIDTH, BUTTON_HEIGHT)
        # self.play_button.setStyleSheet("background-color: #47FF43; color: black; border-radius: 10px;")
        # self.play_button.setFont(QFont('Arial', BUTTON_FONT_SIZE))
        # self.play_button.clicked.connect(self.show_play_page)
        
        # self.story_button = QPushButton('STORY', self)
        # self.story_button.setGeometry(int(WIDTH/2 -  BUTTON_WIDTH/2), INSET * 3 + 2 * BUTTON_HEIGHT + ATI, BUTTON_WIDTH, BUTTON_HEIGHT)
        # self.story_button.setStyleSheet("background-color: #43DDFF; color: black; border-radius: 10px;")
        # self.story_button.setFont(QFont('Arial', BUTTON_FONT_SIZE))
        # self.story_button.clicked.connect(self.show_story_page)
        
        # self.config_button = QPushButton('CONFIG', self)
        # self.config_button.setGeometry(int(WIDTH/2 -  BUTTON_WIDTH/2), INSET * 4 + 3 * BUTTON_HEIGHT + ATI, BUTTON_WIDTH, BUTTON_HEIGHT)
        # self.config_button.setStyleSheet("background-color: #FFCC47; color: black; border-radius: 10px;")
        # self.config_button.setFont(QFont('Arial', BUTTON_FONT_SIZE))
        # self.config_button.clicked.connect(self.show_config_page)
        config = ConfigParser()
        config.read('config.ini')
        fullscreen = config.getboolean('General', 'fullscreen')
        
        if fullscreen:
            self.showFullScreen()

    def get_options(self):
        config = ConfigParser()
        config.read('story_config.ini')

        if 'options' in config:
            return config['options']
        else:
            return {'op1': 'Story Unavailable'}
    
    def show_main_page(self, index):
        config = ConfigParser()
        config.read('story_config.ini')
        config['selection']['select'] = str(index)

        with open('story_config.ini', 'w') as configfile:
            config.write(configfile)

        self.parent.show()
        self.hide()
