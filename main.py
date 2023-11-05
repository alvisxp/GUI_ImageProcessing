from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog
from PyQt5.QtGui import QPixmap, QImage
from ImgProcess_ui import Ui_MainWindow 
from docs import HelpDialog
import cv2
import numpy as np

class MyMainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.actionOpen.triggered.connect(self.import_image)
        self.toGrayscale.clicked.connect(self.convert_to_grayscale)
        self.toBGR.clicked.connect(self.convert_to_BGR)
        self.toRGB.clicked.connect(self.convert_to_RGB)
        self.toHSV.clicked.connect(self.convert_to_HSV)
        self.actionSave_Image.triggered.connect(self.save_image)
        self.toSmoothen.clicked.connect(self.smoothing)
        self.actionDocumentation.triggered.connect(self.docs)
        self.file_name = ""
        self.latest_processed_image = None

    def import_image(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        self.file_name, _ = QFileDialog.getOpenFileName(self, "Open Image File", "", "Image Files (*.png *.jpg *.jpeg *.bmp);;All Files (*)", options=options)
        if self.file_name:
            pixmap = QPixmap(self.file_name)
            self.imported_image.setPixmap(pixmap)
            self.latest_processed_image = pixmap
    
    def convert_to_grayscale(self):
        if self.file_name:
            grayscale_image = cv2.imread(self.file_name, cv2.IMREAD_GRAYSCALE)
            height, width = grayscale_image.shape
            bytes_per_line = width
            grayscale_qimage = QImage(grayscale_image.data, width, height, bytes_per_line, QImage.Format_Grayscale8)
            pixmap = QPixmap.fromImage(grayscale_qimage)
            self.processed_image.setPixmap(pixmap)
            self.latest_processed_image = pixmap


    def convert_to_BGR(self):
        if self.file_name:
            bgr_image = cv2.imread(self.file_name)
            self.update_and_display(bgr_image)
   
    def convert_to_RGB(self):
        if self.file_name:
            image = cv2.imread(self.file_name)
            rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            self.update_and_display(rgb_image)
    
    def convert_to_HSV(self):
        if self.file_name:
            image = cv2.imread(self.file_name)
            hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV_FULL)
            self.update_and_display(hsv_image)
    
    def smoothing(self):
        if self.file_name:
            image = cv2.imread(self.file_name)
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            smoother_img = cv2.blur(image, (10,10))
            self.update_and_display(smoother_img)
   
    def update_and_display(self, image):
        pixmap = self.cvimage_to_pixmap(image)
        self.latest_processed_image = pixmap
        self.processed_image.setPixmap(pixmap)


    def pixmap_to_cvimage(self, pixmap):
        qimage = pixmap.toImage()
        width, height = qimage.width(), qimage.height()
        ptr = qimage.bits()
        ptr.setsize(qimage.byteCount())
        image = np.array(ptr).reshape(height, width, -1) 
        return image


    def cvimage_to_pixmap(self, image):
        height, width, _ = image.shape
        bytes_per_line = 3 * width
        qimage = QImage(image.data, width, height, bytes_per_line, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(qimage)
        return pixmap
    
    def save_image(self):
        if self.latest_processed_image:
            options = QFileDialog.Options()
            options |= QFileDialog.ReadOnly
            file_name, _ = QFileDialog.getSaveFileName(self, "Save Image File", "", "Image Files (*.png);;All Files (*)", options=options)
            if file_name:
                pixmap = self.latest_processed_image
                pixmap.save(file_name, "PNG")
    
    def docs(self):
        help_dialog = HelpDialog()
        help_dialog.exec_()
    

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    main_window = MyMainWindow()
    main_window.show()
    sys.exit(app.exec_())
