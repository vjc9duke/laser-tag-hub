from PyQt5.QtWidgets import QWidget, QPushButton, QLabel, QVBoxLayout, QHBoxLayout
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt, QTimer, pyqtSignal, QThread
from PyQt5.QtGui import QFont
import time
from configparser import ConfigParser
import serial

BUTTON_FONT_SIZE = 30
TOTAL_TIME = 600 # 10 minutes
PLAYER_FONT_SIZE = 20

class PlayPage(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.setWindowTitle('Play Page')
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
        
        self.timer_label = QLabel('{:02}:{:02}'.format((TOTAL_TIME-1) // 60, (TOTAL_TIME-1) % 60), self) 
        self.timer_label.setFont(QFont('Arial', BUTTON_FONT_SIZE))
        self.timer_label.setAlignment(Qt.AlignCenter)
        self.timer_label.setStyleSheet("background-color: #FFF969; color: black; border-radius: 10px;")
        top_row_layout.addWidget(self.timer_label)
        
        team2_label = QLabel('TEAM 2', self)
        team2_label.setFont(QFont('Arial', BUTTON_FONT_SIZE))
        team2_label.setAlignment(Qt.AlignCenter)
        team2_label.setStyleSheet("background-color: #FF4343; color: white; border-radius: 10px;")
        top_row_layout.addWidget(team2_label)
        
        layout.addLayout(top_row_layout)

        # Player labels
        player_layout = QHBoxLayout()
        player1_label = QLabel('P1 P4 P5', self) # todo: replace with actual players
        player1_label.setFont(QFont('Arial', PLAYER_FONT_SIZE))
        player1_label.setAlignment(Qt.AlignCenter | Qt.AlignTop)
        # player1_label.setStyleSheet("background-color: green; color: white; border-radius: 10px;")
        player_layout.addWidget(player1_label)

        spacer_label = QLabel(' ', self)
        player_layout.addWidget(spacer_label)
        
        player2_label = QLabel('P2 P3 P6', self) # todo: replace with actual players
        player2_label.setFont(QFont('Arial', PLAYER_FONT_SIZE))
        player2_label.setAlignment(Qt.AlignCenter | Qt.AlignTop)
        player_layout.addWidget(player2_label)
        
        layout.addLayout(player_layout)

        # Score labels
        self.test_score = 0

        score_layout = QHBoxLayout()
        self.score1_label = QLabel(f'{test_score} 00 00', self)
        self.score1_label.setFont(QFont('Courier', PLAYER_FONT_SIZE))
        self.score1_label.setAlignment(Qt.AlignCenter)
        self.score1_label.setStyleSheet("background-color: #43FF78; color: black; border-radius: 10px;")
        score_layout.addWidget(self.score1_label)

        # Serial receive
        self.serial_thread = SerialReader()
        self.serial_thread.message_received.connect(self.updateLabel)
        self.serial_thread.start()

        spacer_label_2 = QLabel('POINTS', self)
        spacer_label_2.setFont(QFont('Courier', PLAYER_FONT_SIZE))
        spacer_label_2.setAlignment(Qt.AlignCenter)
        spacer_label_2.setStyleSheet("background-color: #43FF78; color: black; border-radius: 10px;")
        score_layout.addWidget(spacer_label_2)

        score2_label = QLabel('00 00 00', self)
        score2_label.setFont(QFont('Courier', PLAYER_FONT_SIZE))
        score2_label.setAlignment(Qt.AlignCenter)
        score2_label.setStyleSheet("background-color: #43FF78; color: black; border-radius: 10px;")
        score_layout.addWidget(score2_label)

        layout.addLayout(score_layout)

        # Lives labels
        kdr_layout = QHBoxLayout()
        kdr1_label = QLabel('05 05 05', self)
        kdr1_label.setFont(QFont('Courier', PLAYER_FONT_SIZE))
        kdr1_label.setAlignment(Qt.AlignCenter)
        kdr1_label.setStyleSheet("background-color: #43FF78; color: black; border-radius: 10px;")
        kdr_layout.addWidget(kdr1_label)

        spacer_label_3 = QLabel('LIVES', self)
        spacer_label_3.setFont(QFont('Courier', PLAYER_FONT_SIZE))
        spacer_label_3.setAlignment(Qt.AlignCenter)
        spacer_label_3.setStyleSheet("background-color: #43FF78; color: black; border-radius: 10px;")
        kdr_layout.addWidget(spacer_label_3)


        kdr2_label = QLabel('05 05 05', self)
        kdr2_label.setFont(QFont('Courier', PLAYER_FONT_SIZE))
        kdr2_label.setAlignment(Qt.AlignCenter)
        kdr2_label.setStyleSheet("background-color: #43FF78; color: black; border-radius: 10px;")
        kdr_layout.addWidget(kdr2_label)

        layout.addLayout(kdr_layout)

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

        # Set up timer
        self.start_time = time.time()
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_timer)
        self.timer.start(1000)

        self.setLayout(layout)

        config = ConfigParser()
        config.read('config.ini')
        fullscreen = config.getboolean('General', 'fullscreen')
        
        if fullscreen:
            self.showFullScreen()

    def update_timer(self):
        time_left = int(TOTAL_TIME - (time.time() - self.start_time))
        if time_left > 0:  
            minutes = time_left // 60
            seconds = time_left % 60
            timer_text = '{:02}:{:02}'.format(minutes, seconds)
        else:
            timer_text = '00:00'  # Timer expired
        
        self.timer_label.setText(timer_text)
        # self.timer_label.repaint()

    def updateLabel(self, message):
        self.test_score += 1
        self.score1_label = QLabel(f'{test_score} 00 00', self)


    def show_main_page(self):
        self.parent.show()
        self.hide()


class SerialReader(QThread):
    message_received = pyqtSignal(str)
    
    def __init__(self, port='/dev/serial0', baud_rate=9600, parent=None):
        super().__init__(parent)
        self.serial_port = serial.Serial(port, baud_rate)
        
    def run(self):
        while True:
            received_data = self.serial_port.readline().decode('utf-8').strip()
            self.message_received.emit(received_data)
