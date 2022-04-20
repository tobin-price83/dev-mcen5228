label = QLabel(self)
pixmap = QPixmap('image.jpeg')
label.setPixmap(pixmap)

# Optional, resize window to image size
self.resize(pixmap.width(),pixmap.height())