import sys
from tkinter.font import Font
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QFont, QPixmap
from extracttextfn import extract_text_from_pdf
from splitpdffn import split_by_range

#initialize main window
class mainwindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.setAcceptDrops(True)

    def initUI(self):
        #set dimensions and title (main window)
        self.setGeometry(300,300,800,600)
        self.setWindowTitle('PDFile')
        self.setWindowIcon(QIcon('favicon.png'))
        #create central widget and set layout on it 
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        layout = QVBoxLayout(self.central_widget)
    #Inserting logo  
        #create label 
        self.logo_label = QLabel(self)
        #load main page image
        self.pixmap = QPixmap('mainimage.png')
        scale_pixmap = self.pixmap.scaled(800,600,Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.logo_label.setPixmap(scale_pixmap)
        self.logo_label.adjustSize()
        layout = QVBoxLayout()
        layout.addWidget(self.logo_label, alignment=Qt.AlignCenter)
        self.logo_label.move(100,0)
    #Enable drag and drop (create labels)
        self.dd_label = QLabel('Drag and drop your files here ', self)
        self.dd_label.setFont(QFont('Calibri',14))
        self.dd_label.setAlignment(Qt.AlignCenter)
        self.dd_label.setWordWrap(True)
        #self.dd_label.move(100,0)
        self.dd_label.setGeometry(200,-150,400,400)
        layout = QVBoxLayout()
        layout.addWidget(self.dd_label)
    #create buttons for functionalities 
        QToolTip.setFont(QFont('Calibri',15))
        btn1 = QPushButton('Merge', self)
        btn1.resize(btn1.sizeHint())
        btn1.move(240,430)

        btn2 = QPushButton('Split', self)
        btn2.resize(btn1.sizeHint())
        btn2.move(350,430)

        btn3 = QPushButton('Extract Text', self)
        btn3.resize(btn1.sizeHint())
        btn3.move(460,430)

        #add buttons to layout 
        layout.addWidget(btn1)
        layout.addWidget(btn2)
        layout.addWidget(btn3)   
        btn3.clicked.connect(self.extract_text_button)
        btn2.clicked.connect(self.split_pdf_button)

    #function for activating extract text button
    def extract_text_button(self):     
        if not hasattr(self, 'dropped_pdf_path') or not self.dropped_pdf_path:
            self.dd_label.setText('No PDF File dropped !!')
            return
        output_path = 'extracted_text.txt'
        try:
            extract_text_from_pdf(self.dropped_pdf_path,output_path)
            self.dd_label.setText(f'Text extracted and saved to : {output_path}')
        except Exception as e:
            self.dd_label.setText('Error extracting text')

    #function for activating split pdf button
    def split_pdf_button(self):
        if not hasattr(self, 'dropped_pdf_path') or not self.dropped_pdf_path:
            self.dd_label.setText('No PDF File dropped !!')
            return
        try:
            ranges_value = "2-6"  
            out_paths = split_by_range(
                self.dropped_pdf_path,
                output_template="split_{i}_{start}-{end}.pdf",
                ranges=ranges_value
        )
            if len(out_paths) == 1:
                self.dd_label.setText(f"Split saved: {out_paths}")
            else:
                self.dd_label.setText(f"Split created: {len(out_paths)} files (e.g., {out_paths})")
        except Exception as e:
            self.dd_label.setText(f"Error splitting PDF: {e}")


    
    #Define functions for drag and drop 
        #accept only if files are dragged 
    def dragEnterEvent(self,drag):
        if drag.mimeData().hasUrls():
            urls = drag.mimeData().urls()
            if all(url.toLocalFile().lower().endswith('.pdf') for url in urls):     
                drag.acceptProposedAction()
            else:
                drag.ignore()
        else:
            drag.ignore()
            
                

    def dropEvent(self, drop):
        files = [url.toLocalFile() for url in drop.mimeData().urls()]
        self.dropped_pdf_path = files[0] if files else None
        self.dd_label.setText('Dropped files:\n'.join(files))
        drop.acceptProposedAction()
        

    #options after clicking the close button
    def closeEvent(self, quit):
        reply = QMessageBox.question(self,'Message','Do you really want to quit?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            quit.accept()
        else:
            quit.ignore()
def main():
    #launching the window 
    app = QApplication(sys.argv)
    window = mainwindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
