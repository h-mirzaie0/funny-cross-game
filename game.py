
from PyQt5 import QtCore, QtGui, QtWidgets
import random

class Ui_Form(object):
    def setupUi(self, Form):
        self.buttons = []
        self.labels = []  
        self.reset()
        Form.setObjectName("Form")
        p1_size = len(self.players)*50
        Form.resize(600, 800+p1_size)
        
        
        font = QtGui.QFont()
        font.setPointSize(40)  # Set the point size here
        self.label_0 = QtWidgets.QLabel(Form)
        self.label_0.setGeometry(QtCore.QRect(250, 0, 200, 100))
        self.label_0.setFont(font)
        self.label_0.setObjectName("label_0")
        
        font.setPointSize(20)
        for i in range(len(self.players)):
            label = QtWidgets.QLabel(Form)
            label.setObjectName(f"label_{i}")
            label.setGeometry(QtCore.QRect(20, i*50+10, 80, 60))
            label.setFont(font)
            self.labels.append(label)
            
        container = QtWidgets.QWidget(Form)
        container.setGeometry(QtCore.QRect(20, p1_size + 20, 500, 750))  # Adjust the position and size
        self.layout = QtWidgets.QGridLayout(container)        
        self.layout.setSpacing(10)  
        self.buttons = []  
        positions = [
            (6, 1), (6, 2), (6, 3),
            (5, 1), (5, 2), (5, 3),
            (4, 1), (4, 2), (4, 3),
            (3, 1), (3, 2), (3, 3),
            (2, 1), (2, 2), (2, 3),
            (1, 1), (1, 2), (1, 3),
            (0, 1), (0, 2), (0, 3)
        ]

        button_size = (90, 70) 
        
        for i, (row, col) in enumerate(positions, start=1):
            button = QtWidgets.QPushButton(Form)
            button.setObjectName(f"pushButton_{i}")
            button.setFixedSize(*button_size)
            button.clicked.connect(lambda checked, btn=button: self.select(btn))
            self.layout.addWidget(button, row, col)
            self.buttons.append(button)
            
            
        

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate                
        Form.setWindowTitle(_translate("Form", "Form"))
        
        self.reset()
        
        for i in range(len(self.players)):
            self.labels[i].setText(_translate("Form", self.players[i]))
            

        self.label_0.setText(_translate("Form", self.players[0]))
    
    
    def randomRoad(self):
        return [random.randint(1,3) for  i in range(7)]
               
    
    def select(self,btn):

        
        # reset game
        if len(self.road) == 0:
            self.reset()
            
        palteNumb = int(btn.objectName().split('_')[-1])
        condition = (len(self.road))*3 + palteNumb 
        if condition>len(self.buttons) and condition<len(self.buttons)+4:
            if palteNumb%3+1 == self.road[0]:
                self.result(True,btn)
            else:
                self.result(False,btn)
        else:
            print('out of order')
                        
    def result(self,S,btn):
        
        # eliminate position
        for button in self.buttons:
            button.setText("")

        # show position
        btn.setText("O")
        
        if S:
            self.road = self.road[1:]
            if len(self.road) == 0:
                self.label_0.setText(f'{self.label_0.text()} Win!')
                self.label_0.setStyleSheet("color: green;")
                
                       
        else:    
            self.road = self.MainRoad
            self.players = self.players[1:] + [self.players[0]]
            self.label_0.setText(self.players[0])
            btn.setVisible(False) 

    def reset(self):
        self.players = []
        self.MainRoad = self.randomRoad()
        self.road = self.MainRoad
        
        for button in self.buttons:
            button.setVisible(True)
            button.setText("")
            self.label_0.setStyleSheet("color: black;")
            
        with open('players.txt','r') as f:
            for line in f:
                self.players = line.strip().split(',') if not line.startswith("#") else self.players

            
        
        
        
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())