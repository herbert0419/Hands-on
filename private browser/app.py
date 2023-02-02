import sys
from PyQt5.QtCore import QUrl
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import QApplication, QHBoxLayout, QPushButton, QVBoxLayout, QWidget

class Browser(QWidget):
    def __init__(self):
        super().__init__()
        self.view = QWebEngineView()
        self.back_button = QPushButton('Back')
        self.forward_button = QPushButton('Forward')
        self.back_button.setEnabled(False)
        self.forward_button.setEnabled(False)
        self.back_button.clicked.connect(self.view.back)
        self.forward_button.clicked.connect(self.view.forward)
        self.view.urlChanged.connect(self.update_buttons)

        layout = QVBoxLayout()
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.back_button)
        button_layout.addWidget(self.forward_button)
        layout.addLayout(button_layout)
        layout.addWidget(self.view)
        self.setLayout(layout)
        
    def update_buttons(self, url):
        self.back_button.setEnabled(self.view.history().canGoBack())
        self.forward_button.setEnabled(self.view.history().canGoForward())

app = QApplication(sys.argv)
browser = Browser()
browser.view.load(QUrl('https://www.google.com'))
browser.show()
sys.exit(app.exec_())

# import sys
# from PyQt5.QtCore import Qt
# from PyQt5.QtWebEngineWidgets  import QApplication, QMainWindow, QLineEdit, QToolBar, QAction, QWebEngineView

# class Browser(QMainWindow):
#     def __init__(self):
#         super().__init__()

#         # Create URL insert place
#         self.url_bar = QLineEdit()
#         self.url_bar.returnPressed.connect(self.navigate)

#         # Create Toolbar
#         self.toolbar = QToolBar()
#         self.addToolBar(self.toolbar)

#         # Create back button
#         self.back_button = QAction("<")
#         self.back_button.triggered.connect(self.web_view.back)
#         self.toolbar.addAction(self.back_button)

#         # Create forward button
#         self.forward_button = QAction(">")
#         self.forward_button.triggered.connect(self.web_view.forward)
#         self.toolbar.addAction(self.forward_button)

#         # Create zoom in button
#         self.zoom_in_button = QAction("+")
#         self.zoom_in_button.triggered.connect(self.web_view.zoomIn)
#         self.toolbar.addAction(self.zoom_in_button)

#         # Create zoom out button
#         self.zoom_out_button = QAction("-")
#         self.zoom_out_button.triggered.connect(self.web_view.zoomOut)
#         self.toolbar.addAction(self.zoom_out_button)

#         # Add URL bar to toolbar
#         self.toolbar.addWidget(self.url_bar)

#         # Create web view
#         self.web_view = QWebEngineView()
#         self.setCentralWidget(self.web_view)

#     def navigate(self):
#         url = self.url_bar.text()
#         self.web_view.load(url)

# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     browser = Browser()
#     browser.show()
#     sys.exit(app.exec_())
