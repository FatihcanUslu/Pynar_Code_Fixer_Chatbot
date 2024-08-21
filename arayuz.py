import sys
from PyQt5.QtWidgets import QApplication, QWidget, QMenuBar, QMenu, QMainWindow
from PyQt5.QtWidgets import QTextEdit, QHBoxLayout, QVBoxLayout, QPushButton, QPlainTextEdit
from PyQt5 import QtWidgets, QtCore
import anvil.server

#connect to anvil server
anvil.server.connect("put your api key")

class ModelThread(QtCore.QThread):
    result_ready = QtCore.pyqtSignal(str)

    def __init__(self, user_input):
        super().__init__()
        self.user_input = user_input

    def run(self):
        # call the model function and emit the result
        model_answer = anvil.server.call("module_input_yolla1", self.user_input)
        model_answer = f"**Model is not yet implemented.** \nPlease replace this placeholder with your model call."
        self.result_ready.emit(model_answer)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("PyNar Editörü")
        self.setFixedSize(1300, 800)

        # Code editor (using QPlainTextEdit for better code formatting)
        self.code_editor = QPlainTextEdit()
        self.code_editor.setFixedSize(700, 700)  # Adjust size as needed

        # Yapay zeka editor
        self.yapay_zeka_editor = QPlainTextEdit()
        self.yapay_zeka_editor.setFixedSize(300, 700)  # Adjust size as needed
        yapay_zeka_layout = QVBoxLayout(self.yapay_zeka_editor)

        # Yapay zeka çıktısı
        self.yapay_zeka_text_area = QPlainTextEdit()
        self.yapay_zeka_text_area.setPlaceholderText("nasıl yardımcı olabilirim ?")
        self.yapay_zeka_text_area.setFixedSize(280, int(0.75*700))  # Adjust size as needed
        yapay_zeka_layout.addWidget(self.yapay_zeka_text_area)

        #soru satırı yeri ve gönder butonu
        self.the_line = QPlainTextEdit(self)
        self.the_line.setPlaceholderText("sorunuzu girin")
        self.the_line.setFixedSize(280, 200)
        yapay_zeka_layout.addWidget(self.the_line)
        
        #gonder butonu
        self.gonder_butonu = QPushButton("Gönder",self)
        self.gonder_butonu.clicked.connect(self.display_text)

        # self.gonder_butonu.clicked.connect(self.gonder_fonksiyonu)
        
        soru_layout = QVBoxLayout() #soru satırı ve buton düzeni
        soru_layout.addWidget(self.the_line)
        soru_layout.addWidget(self.gonder_butonu, alignment=QtCore.Qt.AlignRight)
        soru_layout.addWidget(self.gonder_butonu)
        yapay_zeka_layout.addLayout(soru_layout)

        # Left panel
        self.left_panel = QWidget()
        left_layout = QVBoxLayout(self.left_panel)

        # Buttons for left panel
        buttons = ["Temel Komutlar", "Değişkenler", "Veri Tipleri",
                   "Operatörler", "Koşullu ve Mantıksal İfadeler"]
        for button_text in buttons:
            button = QPushButton(button_text)
            button.setFixedSize(150, 100)
            left_layout.addWidget(button)

        # Main layout (horizontal) for overall structure
        main_layout = QHBoxLayout()

        # Left part (vertical) containing left panel and code editor
        left_part = QVBoxLayout()
        left_part.addWidget(self.left_panel)
        left_part.addWidget(self.code_editor)

        # Central part (vertical) containing code editor
        central_part = QVBoxLayout()
        central_part.addWidget(self.code_editor)
    
        # Yapay zeka editor (placed on the right)
        main_layout.addWidget(self.left_panel, stretch=1)
        main_layout.addLayout(central_part, stretch=5)
        main_layout.addWidget(self.yapay_zeka_editor, stretch=3)

        
        # Central widget with main layout
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)
        
        
        # Menu bar (implementation can be added later)
        menubar = QMenuBar()
        self.setMenuBar(menubar)

        # File, Settings, Cloud, and Help menus (add functionality as needed)
        file_menu = QMenu("&Dosya", menubar)
        menubar.addMenu(file_menu)

        settings_menu = QMenu("&Ayarlar", menubar)
        menubar.addMenu(settings_menu)

        cloud_menu = QMenu("&Bulut", menubar)
        menubar.addMenu(cloud_menu)

        help_menu = QMenu("&Yardım", menubar)
        menubar.addMenu(help_menu)
    
    def display_text(self):
        # get the text from the QPlainTextEdit
        user_input = self.the_line.toPlainText()

        #clear the input field after appending
        self.the_line.clear()
        print("user_input:",user_input)

        #create and start the model thread
        self.model_thread = ModelThread(user_input)
        self.model_thread.result_ready.connect(lambda result: self.update_text(user_input,result))
        self.model_thread.start()
    
    def update_text(self,user_input,model_answer):
        #append the result to the QTextEdit
        formatted_text = f"""
        <div style="margin-bottom: 15px;">
            <div style="font-weight: bold; color: blue;">User:</div>
            <div style="margin-left: 10px; color: black; white-space: pre-wrap; word-wrap: break-word;">{user_input}</div>
            <div style="font-weight: bold; color: green; margin-top: 5px;">Model:</div>
            <div style="margin-left: 10px; color: black; white-space: pre-wrap; word-wrap: break-word;">{model_answer}</div>
        </div>
        """
        self.yapay_zeka_text_area.append(formatted_text)

def window():
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    window()