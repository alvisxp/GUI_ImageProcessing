from PyQt5.QtWidgets import QDialog, QLabel, QVBoxLayout

class HelpDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Docs")
        self.setGeometry(100, 100, 400, 300)  

        layout = QVBoxLayout(self)

        label = QLabel()
        label.setText("Click on File -> Open to import an image. Click on Edit -> Save Image to save the image.")
        label.setWordWrap(True)
        layout.addWidget(label)

        self.setLayout(layout)
