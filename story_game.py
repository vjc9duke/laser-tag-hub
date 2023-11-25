import sys
from PyQt5.QtCore import Qt, QTimer
import time
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit, QLabel
from end_page import EndPage
from play_page import SerialReader

BUTTON_FONT_SIZE = 30
TOTAL_TIME = 90

class KeypadApp(QWidget):
    def __init__(self, parent):
        super().__init__()

        self.parent = parent
        self.setGeometry(0, 0, 800, 480)
        self.setStyleSheet("background-color: black; color: white;")

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Keypad App')

        # Timer
        self.timer_label = QLabel('{:02}:{:02}'.format((TOTAL_TIME-1) // 60, (TOTAL_TIME-1) % 60), self) 
        self.timer_label.setFont(QFont('Arial', BUTTON_FONT_SIZE))
        self.timer_label.setAlignment(Qt.AlignCenter)
        self.timer_label.setStyleSheet("background-color: #FFF969; color: black; border-radius: 10px;")

        # Input box
        self.top_input_box = QLineEdit(self)
        self.top_input_box.setReadOnly(True)
        self.top_input_box.setFont(QFont('Arial', 20))
        self.top_input_box.setAlignment(Qt.AlignCenter)
        self.top_input_box.setStyleSheet("background-color: #333333; color: white; border-radius: 10px;")
        self.top_input_box.setFixedHeight(60)  # Set the desired height
        self.top_input_box.setMaxLength(4)

        # Keypad buttons
        keypad_layout = QVBoxLayout()
        keypad_layout.addWidget(self.create_keypad_row('123'))
        keypad_layout.addWidget(self.create_keypad_row('456'))
        keypad_layout.addWidget(self.create_keypad_row('789'))
        keypad_layout.addWidget(self.create_keypad_row('*0<'))

        # Main layout
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.timer_label)
        main_layout.addWidget(self.top_input_box)
        main_layout.addLayout(keypad_layout)

        self.setLayout(main_layout)

        # Set up timer
        self.start_time = time.time()
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_timer)
        self.timer.start(1000)

        #Serial
        self.serial_thread = SerialReader()
        self.serial_thread.message_received.connect(self.updateLabel)

        config = ConfigParser()
        config.read('config.ini')
        fullscreen = config.getboolean('General', 'fullscreen')
        
        if fullscreen:
            self.showFullScreen()

    def apply_button_style(self, button, color="4356FF"):
        button.setFont(QFont('Arial', BUTTON_FONT_SIZE))
        button.setStyleSheet(f"background-color: #{color}; color: white; border-radius: 10px;")
        button.setFixedHeight(60)

    def create_keypad_row(self, buttons_text):
        widget = QWidget()
        layout = QHBoxLayout(widget)

        for button_text in buttons_text:
            button = QPushButton(button_text, self)
            if(button_text == "<"):
                self.apply_button_style(button, color="FF4343")
                button.clicked.connect(self.on_backspace_clicked)
            else:
                button.clicked.connect(lambda _, text=button_text: self.on_digit_clicked(text))
                self.apply_button_style(button)
            layout.addWidget(button)

        return widget

    def on_digit_clicked(self, digit):
        current_text = self.top_input_box.text()
        new_text = current_text + digit

        if len(new_text) <= 5:
            self.top_input_box.setText(new_text)

        if len(new_text) == 5 and new_text == '1234*':
            self.go_to_end_page(0)  # Replace with your function call

    def on_backspace_clicked(self):
        current_text = self.top_input_box.text()
        new_text = current_text[:-1]
        self.top_input_box.setText(new_text)

    def update_timer(self):
        time_left = int(TOTAL_TIME - (time.time() - self.start_time))
        if time_left > 0:  
            minutes = time_left // 60
            seconds = time_left % 60
            timer_text = '{:02}:{:02}'.format(minutes, seconds)
        else:
            timer_text = '00:00'  # Timer expired
            self.timer.stop()
            self.go_to_end_page(1)
        
        self.timer_label.setText(timer_text)

    def go_to_end_page(self, won):
        # temp: show that send message works
        # self.sendMessage('AT+IPR=115200\r\n')
        self.end_page = EndPage(self, won)
        self.end_page.show()
        self.hide()



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
    
    def parseMessage(self, message):
        # message format for now: +RCV=shot,1,shooter
        parameters = re.findall(r'\d+', input_string)
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


if __name__ == '__main__':
    app = QApplication(sys.argv)
    keypad_app = KeypadApp()
    keypad_app.show()
    sys.exit(app.exec_())
