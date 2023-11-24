from PyQt5.QtWidgets import QWidget, QPushButton, QLabel, QVBoxLayout, QHBoxLayout
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt, QTimer, pyqtSignal, QThread
from PyQt5.QtGui import QFont
import time
from configparser import ConfigParser
import serial
import player_variables
from player_variables import pretty_print, get_scores, get_lives, get_total_score, get_kdr, pretty_print_float

BUTTON_FONT_SIZE = 30
TOTAL_TIME = 600 # 10 minutes
PLAYER_FONT_SIZE = 20

class EndPage(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.setWindowTitle('End Page')
        self.setGeometry(0, 0, 800, 480)
        self.setStyleSheet("background-color: black; color: white;")
        
        layout = QVBoxLayout()

        # Top row with team rectangles
        top_row_layout = QHBoxLayout()
        team1_label = QLabel('TEAM 1', self)
        team1_label.setFont(QFont('Arial', BUTTON_FONT_SIZE))
        team1_label.setAlignment(Qt.AlignCenter)
        team1_label.setStyleSheet("background-color: #4356FF; color: white; border-radius: 10px;")
        top_row_layout.addWidget(team1_label)
        team1_label.adjustSize()

        spacer_label_team = QLabel(' ', self)
        top_row_layout.addWidget(spacer_label_team)
        
        team2_label = QLabel('TEAM 2', self)
        team2_label.setFont(QFont('Arial', BUTTON_FONT_SIZE))
        team2_label.setAlignment(Qt.AlignCenter)
        team2_label.setStyleSheet("background-color: #FF4343; color: white; border-radius: 10px;")
        top_row_layout.addWidget(team2_label)
        
        layout.addLayout(top_row_layout)

        # Score labels
        t1_score = get_total_score(1)
        t2_score = get_total_score(2)
        win_color = '#43FF78' 
        lose_color = '#FF4343'

        score_layout = QHBoxLayout()
        self.score1_label = QLabel(str(t1_score), self)
        self.score1_label.setFont(QFont('Courier', PLAYER_FONT_SIZE))
        self.score1_label.setAlignment(Qt.AlignCenter)
        self.score1_label.setStyleSheet(f"background-color: {win_color if t1_score >= t2_score else lose_color}; color: black; border-radius: 10px;")
        score_layout.addWidget(self.score1_label)

        spacer_label_2 = QLabel('POINTS', self)
        spacer_label_2.setFont(QFont('Courier', PLAYER_FONT_SIZE))
        spacer_label_2.setAlignment(Qt.AlignCenter)
        spacer_label_2.setStyleSheet("background-color: #B9B8A9; color: black; border-radius: 10px;")
        score_layout.addWidget(spacer_label_2)

        self.score2_label = QLabel(str(t2_score), self) 
        self.score2_label.setFont(QFont('Courier', PLAYER_FONT_SIZE))
        self.score2_label.setAlignment(Qt.AlignCenter)
        self.score2_label.setStyleSheet(f"background-color: {win_color if t2_score >= t1_score else lose_color}; color: black; border-radius: 10px;")
        score_layout.addWidget(self.score2_label)

        layout.addLayout(score_layout)

        # Player labels
        player_layout = QHBoxLayout()
        player1_label = QLabel('P1          P2', self) # todo: replace with actual players, zfill for spacing
        player1_label.setFont(QFont('Arial', PLAYER_FONT_SIZE))
        player1_label.setAlignment(Qt.AlignCenter | Qt.AlignTop)
        # player1_label.setStyleSheet("background-color: green; color: white; border-radius: 10px;")
        player_layout.addWidget(player1_label)

        spacer_label = QLabel(' ', self)
        player_layout.addWidget(spacer_label)
        
        player2_label = QLabel('P3          P4', self) # todo: replace with actual players
        player2_label.setFont(QFont('Arial', PLAYER_FONT_SIZE))
        player2_label.setAlignment(Qt.AlignCenter | Qt.AlignTop)
        player_layout.addWidget(player2_label)
        
        layout.addLayout(player_layout)

        # KDR labels
        kdr_layout = QHBoxLayout()
        kdr1_label = QLabel(pretty_print_float(get_kdr(1), dp=2), self)
        kdr1_label.setFont(QFont('Courier', PLAYER_FONT_SIZE))
        kdr1_label.setAlignment(Qt.AlignCenter)
        kdr1_label.setStyleSheet("background-color: #B9B8A9; color: black; border-radius: 10px;")
        kdr_layout.addWidget(kdr1_label)

        spacer_label_3 = QLabel('KDR', self)
        spacer_label_3.setFont(QFont('Courier', PLAYER_FONT_SIZE))
        spacer_label_3.setAlignment(Qt.AlignCenter)
        spacer_label_3.setStyleSheet("background-color: #B9B8A9; color: black; border-radius: 10px;")
        kdr_layout.addWidget(spacer_label_3)


        kdr2_label = QLabel(pretty_print_float(get_kdr(2), dp=2), self)  # TODO: look into pretty print with decimals
        kdr2_label.setFont(QFont('Courier', PLAYER_FONT_SIZE))
        kdr2_label.setAlignment(Qt.AlignCenter)
        kdr2_label.setStyleSheet("background-color: #B9B8A9; color: black; border-radius: 10px;")
        kdr_layout.addWidget(kdr2_label)

        layout.addLayout(kdr_layout)

        # Points label
        points_layout = QHBoxLayout()
        points1_label = QLabel(pretty_print(get_scores(1)), self)
        points1_label.setFont(QFont('Courier', PLAYER_FONT_SIZE))
        points1_label.setAlignment(Qt.AlignCenter)
        points1_label.setStyleSheet("background-color: #B9B8A9; color: black; border-radius: 10px;")
        points_layout.addWidget(points1_label)

        spacer_label_4 = QLabel('POINTS', self)
        spacer_label_4.setFont(QFont('Courier', PLAYER_FONT_SIZE))
        spacer_label_4.setAlignment(Qt.AlignCenter)
        spacer_label_4.setStyleSheet("background-color: #B9B8A9; color: black; border-radius: 10px;")
        points_layout.addWidget(spacer_label_4)


        points2_label = QLabel(pretty_print(get_scores(2)), self)
        points2_label.setFont(QFont('Courier', PLAYER_FONT_SIZE))
        points2_label.setAlignment(Qt.AlignCenter)
        points2_label.setStyleSheet("background-color: #B9B8A9; color: black; border-radius: 10px;")
        points_layout.addWidget(points2_label)

        layout.addLayout(points_layout)

        # Finish button
        finish_layout = QHBoxLayout()

        finish_space_1 = QLabel(' ', self)
        finish_layout.addWidget(finish_space_1)

        finish_button = QPushButton('Finish', self)
        finish_button.setFont(QFont('Arial', PLAYER_FONT_SIZE*2))
        finish_button.setStyleSheet("background-color: orange; color: black; border-radius: 10px;")
        finish_button.clicked.connect(self.show_main_page)
        finish_layout.addWidget(finish_button)

        finish_space_2 = QLabel(' ', self)
        finish_layout.addWidget(finish_space_2)

        layout.addLayout(finish_layout)

        self.setLayout(layout)

        config = ConfigParser()
        config.read('config.ini')
        fullscreen = config.getboolean('General', 'fullscreen')
        
        if fullscreen:
            self.showFullScreen()

    def show_main_page(self):
        self.parent.parent.show()
        self.hide()