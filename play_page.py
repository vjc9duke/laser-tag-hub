from PyQt5.QtWidgets import QWidget, QPushButton, QLabel, QVBoxLayout, QHBoxLayout
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont
import time

BUTTON_FONT_SIZE = 30
TOTAL_TIME = 600 # 10 minutes

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
        team1_label.setStyleSheet("background-color: blue; color: white; border-radius: 10px;")
        top_row_layout.addWidget(team1_label)
        
        self.timer_label = QLabel('{:02}:{:02}'.format((TOTAL_TIME-1) // 60, (TOTAL_TIME-1) % 60), self) 
        self.timer_label.setFont(QFont('Arial', BUTTON_FONT_SIZE))
        self.timer_label.setAlignment(Qt.AlignCenter)
        self.timer_label.setStyleSheet("background-color: yellow; color: black; border-radius: 10px;")
        top_row_layout.addWidget(self.timer_label)
        
        team2_label = QLabel('TEAM 2', self)
        team2_label.setFont(QFont('Arial', BUTTON_FONT_SIZE))
        team2_label.setAlignment(Qt.AlignCenter)
        team2_label.setStyleSheet("background-color: red; color: white; border-radius: 10px;")
        top_row_layout.addWidget(team2_label)
        
        layout.addLayout(top_row_layout)

        # Player labels
        player_layout = QHBoxLayout()
        player1_label = QLabel('P1 P4 P5', self)
        player1_label.setFont(QFont('Arial', 18))
        player_layout.addWidget(player1_label)
        
        player2_label = QLabel('P2 P3 P6', self)
        player2_label.setFont(QFont('Arial', 18))
        player_layout.addWidget(player2_label)
        
        layout.addLayout(player_layout)

        # Green rounded text labels
        green_labels_layout = QHBoxLayout()
        for i in range(3):
            green_label = QLabel('Green Label {}'.format(i+1), self)
            green_label.setFont(QFont('Arial', 18))
            green_label.setStyleSheet("background-color: green; color: white; border-radius: 10px;")
            green_labels_layout.addWidget(green_label)

        layout.addLayout(green_labels_layout)

        # Finish button
        finish_button = QPushButton('Finish', self)
        finish_button.setFont(QFont('Arial', 18))
        finish_button.setStyleSheet("background-color: orange; color: white; border-radius: 10px;")
        finish_button.clicked.connect(self.show_main_page)
        layout.addWidget(finish_button, alignment=Qt.AlignCenter)

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

    def show_main_page(self):
        self.parent.show()
        self.hide()



