from PyQt5.QtWidgets import QWidget, QPushButton, QLabel, QVBoxLayout, QHBoxLayout
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt, QTimer, pyqtSignal, QThread
from PyQt5.QtGui import QFont
import time
from configparser import ConfigParser
import serial
import player_variables
from player_variables import pretty_print, get_scores, get_lives
from end_page import EndPage
import re

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
        player1_label = QLabel('P1         P2', self) # todo: replace with actual players
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

        # Score labels
        score_layout = QHBoxLayout()
        self.score1_label = QLabel(pretty_print(get_scores(1), sp=5), self)
        self.score1_label.setFont(QFont('Courier', PLAYER_FONT_SIZE))
        self.score1_label.setAlignment(Qt.AlignCenter)
        self.score1_label.setStyleSheet("background-color: #43FF78; color: black; border-radius: 10px;")
        score_layout.addWidget(self.score1_label)

        # Serial receive
        self.serial_thread = SerialReader()
        self.serial_thread.message_received.connect(self.updateLabel)

        spacer_label_2 = QLabel('POINTS', self)
        spacer_label_2.setFont(QFont('Courier', PLAYER_FONT_SIZE))
        spacer_label_2.setAlignment(Qt.AlignCenter)
        spacer_label_2.setStyleSheet("background-color: #43FF78; color: black; border-radius: 10px;")
        score_layout.addWidget(spacer_label_2)

        self.score2_label = QLabel(pretty_print(get_scores(2)), self)
        self.score2_label.setFont(QFont('Courier', PLAYER_FONT_SIZE))
        self.score2_label.setAlignment(Qt.AlignCenter)
        self.score2_label.setStyleSheet("background-color: #43FF78; color: black; border-radius: 10px;")
        score_layout.addWidget(self.score2_label)

        layout.addLayout(score_layout)

        # Lives labels
        kdr_layout = QHBoxLayout()
        kdr1_label = QLabel(pretty_print(get_lives(1)), self)
        kdr1_label.setFont(QFont('Courier', PLAYER_FONT_SIZE))
        kdr1_label.setAlignment(Qt.AlignCenter)
        kdr1_label.setStyleSheet("background-color: #43FF78; color: black; border-radius: 10px;")
        kdr_layout.addWidget(kdr1_label)

        spacer_label_3 = QLabel('LIVES', self)
        spacer_label_3.setFont(QFont('Courier', PLAYER_FONT_SIZE))
        spacer_label_3.setAlignment(Qt.AlignCenter)
        spacer_label_3.setStyleSheet("background-color: #43FF78; color: black; border-radius: 10px;")
        kdr_layout.addWidget(spacer_label_3)


        kdr2_label = QLabel(pretty_print(get_lives(2)), self)
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
        finish_button.clicked.connect(self.go_to_end_page)
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
            self.timer.stop()
            self.go_to_end_page()
        
        self.timer_label.setText(timer_text)
        # self.timer_label.repaint()

    def updateLabel(self, message):
        # message format for now: +RCV=shot,1,shooter
        print(f'Received message: {message}')
        (shot, shooter) = self.parseMessage(message)
        if shot not in player_variables.LORA_id_map:
            print(f"Invalid shot: {shot}")
            return
        player_variables.scores[shooter] += 1
        player_variables.lives[player_variables.LORA_id_map.get(shot)] -= 1
        print(f'Updating score for player {player}')
        
        self.score1_label.setText(pretty_print(get_scores(1)))
        self.score2_label.setText(pretty_print(get_scores(2)))

    def parseMessage(self, message):
        # message format for now: +RCV=shot,1,shooter
        parameters = re.findall(r'\d+', message)
        print(f'Parameters: {parameters}')
        if len(parameters) >= 3:
            return (int(parameters[0]), int(parameters[2]))  # shot, shooter
        else:
            return -1

    def sendMessage(self, message):
        if not self.serial_thread.running:
            return 
        message_bytes = message.encode('utf-8')
        self.serial_thread.serial_port.write(message_bytes)

    def go_to_end_page(self):
        # temp: show that send message works
        # self.sendMessage('AT+IPR=115200\r\n')
        self.end_page = EndPage(self)
        self.end_page.show()
        self.hide()


class SerialReader(QThread):
    _instance = None
    message_received = pyqtSignal(str)
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.initialize()
            cls._instance.start()
        return cls._instance

    def initialize(self):
        try:
            self.serial_port = serial.Serial('/dev/serial0', 115200)  # Default serial port and baud rate
            self.running = True
        except Exception as e: # no serial port, UI mode only
            print("Serial not found, UI mode only")
            self.running = False
        super(SerialReader, self).__init__()
        
    def run(self):
        while self.running:
            received_data = self.serial_port.readline().decode('utf-8').strip()
            print(f'Received data: {received_data}')
            self.message_received.emit(received_data)
