from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QPlainTextEdit, QPushButton, QTextEdit
import sys
import anvil.server
from viztracer import VizTracer

tracer = VizTracer()
tracer.start()
# Connect to the Anvil server
anvil.server.connect("put your own api key")
class ModelThread(QtCore.QThread):
    result_ready = QtCore.pyqtSignal(str)

    def __init__(self, user_input):
        super().__init__()
        self.user_input = user_input

    def run(self):
        # Call the model function and emit the result
        model_answer = anvil.server.call("modele_input_yolla1", self.user_input)
        self.result_ready.emit(model_answer)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("chatbot")
        self.setFixedSize(500, 568)

        # soru satırı ve yeri
        self.the_line = QPlainTextEdit(self)
        self.the_line.setPlaceholderText("sorunuzu giriniz")
        self.the_line.setFixedSize(400, 50)
        self.the_line.move(20, 500)

        # arama butonu ve yeri
        self.v2 = QPushButton("arama", self)
        self.v2.resize(60, 25)
        self.v2.move(425, 500)
        self.v2.clicked.connect(self.display_text)

        # cevap satırı ve yeri
        self.s1 = QTextEdit(self)
        self.s1.setPlaceholderText("cevap yükleniyor...")
        self.s1.move(48, 60)
        self.s1.setFixedSize(400, 400)
        self.s1.setReadOnly(True)

    def display_text(self):
        # Get the text from the QPlainTextEdit
        user_input = self.the_line.toPlainText()
        # Clear the input field after appending
        self.the_line.clear()
        print("user_input:", user_input)

        # Create and start the model thread
        self.model_thread = ModelThread(user_input)
        # fuckyeahhhh = anvil.server.call("modele_input_yolla1", "self.user_yeahhhinput")
        self.model_thread.result_ready.connect(lambda result: self.update_text(user_input, result))
        self.model_thread.start()

    def update_text(self, user_input, model_answer):
        # Append the result to the QTextEdit
        formatted_text = f"""
        <div style="margin-bottom: 15px;">
            <div style="font-weight: bold; color: blue;">User:</div>
            <div style="margin-left: 10px; color: black; white-space: pre-wrap; word-wrap: break-word;">{user_input}</div>
            <div style="font-weight: bold; color: green; margin-top: 5px;">Model:</div>
            <div style="margin-left: 10px; color: black; white-space: pre-wrap; word-wrap: break-word;">{model_answer}</div>
        </div>
        """
        self.s1.append(formatted_text)

def window():
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    app.exec_()
    # Stop the tracer and save the trace
    tracer.stop()
    tracer.save()
    #break program 
    sys.exit()
window()


