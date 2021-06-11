from main import *

from . ui_functions import *

class ChatBot(MainWindow):

    def setupChatBotScreen(self):

        self.ui.btnChatBotSwitch = CustomToggle()
        self.ui.btnChatBotSwitch.setObjectName('chatBotSwitch')
        self.ui.activeChatBotLayout.addWidget(self.ui.btnChatBotSwitch)
        self.ui.btnChatBotSwitch.setFocusPolicy(Qt.NoFocus)
        self.ui.btnChatBotSwitch.clicked.connect(lambda: UIFunctions.checkSwitch(self))

        self.ui.addTextOrderNew.clicked.connect(lambda : UIFunctions.countFrameText(self,self.ui.frameOrderNew_obj,self.ui.frameOrderNew))
        self.ui.addTextOrderCancel.clicked.connect(lambda : UIFunctions.countFrameText(self,self.ui.frameOrderCancel_obj,self.ui.frameOrderCancel))
        self.ui.addTextOrderReady.clicked.connect(lambda : UIFunctions.countFrameText(self,self.ui.frameOrderReady_obj,self.ui.frameOrderReady))
        self.ui.addTextOrderSuccess.clicked.connect(lambda : UIFunctions.countFrameText(self,self.ui.frameOrderSuccess_obj,self.ui.frameOrderSuccess))
        self.ui.addTextOrderShipping.clicked.connect(lambda : UIFunctions.countFrameText(self,self.ui.frameOrderShipping_obj,self.ui.frameOrderShipping))
        
        self.ui.btnOrderNew.clicked.connect(lambda: ChatBot.btnChatBot(self))
        self.ui.btnOrderReady.clicked.connect(lambda: ChatBot.btnChatBot(self))
        self.ui.btnOrderShipping.clicked.connect(lambda: ChatBot.btnChatBot(self))
        self.ui.btnOrderSuccess.clicked.connect(lambda: ChatBot.btnChatBot(self))
        self.ui.btnOrderCancel.clicked.connect(lambda: ChatBot.btnChatBot(self))

        self.ui.stackedWidgetChatBot.setCurrentIndex(0)        

    def setStyleButtonChatBot(self,objectName):
        for w in self.ui.frameButtonChatBot.findChildren(QPushButton):
            if w.objectName() != objectName:
                w.setStyleSheet('')
            if w.objectName() == objectName:
                w.setStyleSheet('background-color: rgb(38, 166, 154);')

    def btnChatBot(self):
        btn = self.sender()

        if btn.objectName() == 'btnOrderNew':
            self.ui.stackedWidgetChatBot.setCurrentIndex(0)
            ChatBot.setStyleButtonChatBot(self,btn.objectName())

        elif btn.objectName() == 'btnOrderReady':
            self.ui.stackedWidgetChatBot.setCurrentIndex(4)
            ChatBot.setStyleButtonChatBot(self,btn.objectName())

        elif btn.objectName() == 'btnOrderShipping':
            self.ui.stackedWidgetChatBot.setCurrentIndex(3)
            ChatBot.setStyleButtonChatBot(self,btn.objectName())

        elif btn.objectName() == 'btnOrderSuccess':
            self.ui.stackedWidgetChatBot.setCurrentIndex(2)
            ChatBot.setStyleButtonChatBot(self,btn.objectName())

        elif btn.objectName() == 'btnOrderCancel':
            self.ui.stackedWidgetChatBot.setCurrentIndex(1)
            ChatBot.setStyleButtonChatBot(self,btn.objectName())