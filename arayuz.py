import sys
from PyQt5.QtWidgets import QApplication, QWidget, QMenuBar, QMenu, QMainWindow, QPlainTextEdit
from PyQt5.QtWidgets import QTextEdit, QHBoxLayout, QVBoxLayout, QPushButton , QSizeGrip
from PyQt5.QtCore import Qt
from PyQt5 import QtCore
import anvil.server

#connect to anvil server
anvil.server.connect("put your api key")

class ModelThread(QtCore.QThread):
    result_ready = QtCore.pyqtSignal(list)

    def __init__(self, user_input):
        super().__init__()
        self.user_input = user_input

    def run(self):
        # call the model function and emit the result
        model_answer = anvil.server.call("modele_input_yolla1", self.user_input)
        self.result_ready.emit(model_answer)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.duzeltilmis_kod = None
        self.setWindowTitle("PyNar Editörü")
        self.setGeometry(550, 250, 800, 600)
        #self.setFixedSize(1300, 800) # bu fixedsize arayüzü mause ile
        #küçültüp büyütülmesini engelliyor.

        
        # Code editor (using QPlainTextEdit for better code formatting)
        self.code_editor = QPlainTextEdit()
        #self.code_editor.setFixedSize(700, 700)  # Adjust size as needed

        #kopyala yapıştır butonu editördeki
        self.kopyala_yapistir_butonu = QPushButton("Kopyala-Yapıştır",self)
        self.kopyala_yapistir_butonu.setParent(self.code_editor)#butonu editörün içine koyduk.
        self.kopyala_yapistir_butonu.move(300,0)
        self.kopyala_yapistir_butonu.clicked.connect(self.kodu_kopyala_yapistir_fonksiyonu)

        #editör kodu çalıştır butonu
        self.kodu_calistir_butonu = QPushButton("kodu çalıştır",self)
        self.kodu_calistir_butonu.setParent(self.code_editor) # butonu editörün içine al.
        self.kodu_calistir_butonu.move(300, 450) # butonun taşınıp konumlandırılması

        #bu kısma bak. ekranı genişlet düzen bozulmasın 
        # Use QSizeGrip to position the button
        #self.size_grip = QSizeGrip(self.kodu_calistir_butonu)
        #self.size_grip.setFixedSize(self.kodu_calistir_butonu.size())

        
        
        # Yapay zeka çıktısı
        self.yapay_zeka_text_area = QTextEdit(self)
        self.yapay_zeka_text_area.setPlaceholderText("nasıl yardımcı olabilirim ?")
        #self.yapay_zeka_text_area.setFixedSize(280, 400)  # Adjust size as needed
        self.yapay_zeka_text_area.setLineWrapMode(QTextEdit.LineWrapMode.WidgetWidth)
        self.yapay_zeka_text_area.setReadOnly(True)  # kullanıcı buraya bir şey yazamaz sadece okur.

        #yapaya zekadan dönen sonucu kopyalayıp editöre yapıştıran buton
        self.geri_kopyala_yapistir_butonu = QPushButton("Düzelt Butonu",self)
        self.geri_kopyala_yapistir_butonu.setParent(self.yapay_zeka_text_area) #butonu yapayzekaçıktısı içine al
        self.geri_kopyala_yapistir_butonu.clicked.connect(self.geri_kopyala_yapistir_fonksiyonu)
        self.geri_kopyala_yapistir_butonu.move(50,200) #butonun konumu

        # Soru satırı yeri ve gönder butonu
        self.the_line = QPlainTextEdit(self)
        self.the_line.setPlaceholderText("sorunuzu girin")
        #self.the_line.setFixedSize(280, 100)
        
        # Gönder butonu
        self.gonder_butonu = QPushButton("Gönder", self)
        self.gonder_butonu.clicked.connect(self.display_text)

        # Right layout (vertical) for yapay zeka output and input area
        right_layout = QVBoxLayout()
        right_layout.addWidget(self.yapay_zeka_text_area)
        right_layout.addWidget(self.the_line)
        right_layout.addWidget(self.gonder_butonu, alignment=Qt.AlignRight)

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

        # Adding layouts to the main layout
        main_layout.addWidget(self.left_panel, stretch=1)   # Left panel with buttons
        main_layout.addWidget(self.code_editor, stretch=3)  # Code editor in the center
        main_layout.addLayout(right_layout, stretch=1)      # Right panel with yapay zeka output and input

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
    
    def kodu_kopyala_yapistir_fonksiyonu(self):
        code_text = self.code_editor.toPlainText() #code editörü code text değişkenine plain text formatında ata
        self.the_line.setPlainText(code_text) #sonra theline kısmına bunu yapıştır

    def geri_kopyala_yapistir_fonksiyonu(self):
        if self.duzeltilmis_kod != None:
            code_text2 = self.duzeltilmis_kod #yapay zeka çıktısını codetext2 ye ata.
            self.code_editor.setPlainText(code_text2) #sonra bunu code_editöre yapıştır.

    def display_text(self):
        # get the text from the QPlainTextEdit
        user_input = self.the_line.toPlainText()

        #clear the input field after appending
        self.the_line.clear()
        print("user_input:", user_input)

        #create and start the model thread
        self.model_thread = ModelThread(user_input)
        self.model_thread.result_ready.connect(lambda result: self.update_text(user_input, result))
        self.model_thread.start()
    
    def update_text(self, user_input, model_answer):
        #append the result to the QTextEdit
        
        turkce_sonuc_str = "\n".join(model_answer)# model_answer birleştirilerek türkçe sonuç haline getirildi.
        if len(model_answer) > 1:
            temp = model_answer[1]
            index = temp.find("python\n")
            # Alt string bulunursa, onu sil
            if index != -1:
                temp = temp[:index] + temp[index + len("python\n"):]
            self.duzeltilmis_kod = temp
        
        formatted_text = f"""
        <div style="margin-bottom: 15px;">
            <div style="font-weight: bold; color: blue;">User:</div>
            <div style="margin-left: 10px; color: black; white-space: pre-wrap; word-wrap: break-word;">{user_input}</div>
            <div style="font-weight: bold; color: green; margin-top: 5px;">Model:</div>
            <div style="margin-left: 10px; color: black; white-space: pre-wrap; word-wrap: break-word;">{turkce_sonuc_str}</div>
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
