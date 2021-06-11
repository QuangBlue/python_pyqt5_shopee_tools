from main import *

from . ui_functions import *

from . app_requests import *

class ReplyRating(MainWindow):

    def setupReplyRatingScreen(self):
        self.ui.btnReplyRatingSwitch = CustomToggle()
        self.ui.btnReplyRatingSwitch.setObjectName('replyRatingSwitch')
        self.ui.activeReplyRatingLayout.addWidget(self.ui.btnReplyRatingSwitch)
        self.ui.btnReplyRatingSwitch.setFocusPolicy(Qt.NoFocus)
        self.ui.btnReplyRatingSwitch.clicked.connect(lambda: UIFunctions.checkSwitch(self))

        self.ui.addTextOneStar.clicked.connect(lambda : UIFunctions.countFrameText(self,self.ui.frameOneStar_obj,self.ui.frameOneStar))
        self.ui.addTextTwoStar.clicked.connect(lambda : UIFunctions.countFrameText(self,self.ui.frameTwoStar_obj,self.ui.frameTwoStar))
        self.ui.addTextThreeStar.clicked.connect(lambda : UIFunctions.countFrameText(self,self.ui.frameThreeStar_obj,self.ui.frameThreeStar))
        self.ui.addTextFourStar.clicked.connect(lambda : UIFunctions.countFrameText(self,self.ui.frameFourStar_obj,self.ui.frameFourStar))
        self.ui.addTextFiveStar.clicked.connect(lambda : UIFunctions.countFrameText(self,self.ui.frameFiveStar_obj,self.ui.frameFiveStar))

        self.ui.addTextOneStar.clicked.connect(lambda : ReplyRating.unSaveReplyRating(self))
        self.ui.addTextTwoStar.clicked.connect(lambda : ReplyRating.unSaveReplyRating(self))
        self.ui.addTextThreeStar.clicked.connect(lambda : ReplyRating.unSaveReplyRating(self))
        self.ui.addTextFourStar.clicked.connect(lambda : ReplyRating.unSaveReplyRating(self))
        self.ui.addTextFiveStar.clicked.connect(lambda : ReplyRating.unSaveReplyRating(self)) 


        self.ui.btnOneStar.clicked.connect(lambda: ReplyRating.btnReplyRating(self))
        self.ui.btnTwoStar.clicked.connect(lambda: ReplyRating.btnReplyRating(self))
        self.ui.btnThreeStar.clicked.connect(lambda: ReplyRating.btnReplyRating(self))
        self.ui.btnFourStar.clicked.connect(lambda: ReplyRating.btnReplyRating(self))
        self.ui.btnFiveStar.clicked.connect(lambda: ReplyRating.btnReplyRating(self))

        self.ui.stackedWidgetReplyRating.setCurrentIndex(0)

    def setStyleButtonReplyRating(self,objectName):
        for w in self.ui.frameButtonReplyRating.findChildren(QPushButton):
            if w.objectName() != objectName:
                w.setStyleSheet('')
            if w.objectName() == objectName:
                w.setStyleSheet('background-color: rgb(38, 166, 154);')


    def btnReplyRating(self):
        btn = self.sender()

        if btn.objectName() == 'btnOneStar':
            self.ui.stackedWidgetReplyRating.setCurrentIndex(0)
            ReplyRating.setStyleButtonReplyRating(self,btn.objectName())

        elif btn.objectName() == 'btnTwoStar':
            self.ui.stackedWidgetReplyRating.setCurrentIndex(1)
            ReplyRating.setStyleButtonReplyRating(self,btn.objectName())

        elif btn.objectName() == 'btnThreeStar':
            self.ui.stackedWidgetReplyRating.setCurrentIndex(2)
            ReplyRating.setStyleButtonReplyRating(self,btn.objectName())

        elif btn.objectName() == 'btnFourStar':
            self.ui.stackedWidgetReplyRating.setCurrentIndex(3)
            ReplyRating.setStyleButtonReplyRating(self,btn.objectName())

        elif btn.objectName() == 'btnFiveStar':
            self.ui.stackedWidgetReplyRating.setCurrentIndex(4)
            ReplyRating.setStyleButtonReplyRating(self,btn.objectName())

    def btnSaveReplyRating(self,usernameGlobal,usernameShop):

        textOneStar = []
        textTwoStar = []
        textThreeStar = []
        textFourStar = []
        textFiveStar = []

        obj = [
            self.ui.frameOneStar_obj,
            self.ui.frameTwoStar_obj,
            self.ui.frameThreeStar_obj,
            self.ui.frameFourStar_obj,
            self.ui.frameFiveStar_obj,
        ]
        countError = 0
        for frame in obj:
            for textData in frame.findChildren(QPlainTextEdit):
                if len(textData.toPlainText()) != 0 and len(textData.toPlainText()) <= 400:
                    if frame == self.ui.frameOneStar_obj:
                        textOneStar.append(textData.toPlainText())
                    elif frame == self.ui.frameTwoStar_obj:
                        textTwoStar.append(textData.toPlainText())
                    elif frame == self.ui.frameThreeStar_obj:
                        textThreeStar.append(textData.toPlainText())
                    elif frame == self.ui.frameFourStar_obj:
                        textFourStar.append(textData.toPlainText())
                    elif frame == self.ui.frameFiveStar_obj:
                        textFiveStar.append(textData.toPlainText())

                elif len(textData.toPlainText()) > 400:
                    countError +=1

        data = {
            'textOneStar' : textOneStar,
            'textTwoStar' : textTwoStar,
            'textThreeStar' : textThreeStar,
            'textFourStar' : textFourStar,
            'textFiveStar' : textFiveStar}
  
        re = SaveReplyRating.saveReplyRating(self, usernameGlobal, usernameShop, data)
            
        if re['updated'] == True:
            ReplyRating.savedReplyRating(self)
            if countError != 0 :
                self.showPopup("Cảnh báo","Có nội dung không lưu được",f"Có {countError} nội dung có hơn 400 ký tự nên không lưu được\nTất cả nội dung trả lời hợp lệ đã được lưu Thành Công",False)
            else:
                self.showPopup("Thành Công","Nội dung đã lưu thành cồng","Tất cả nội dung trả lời đã được lưu Thành Công",True)
        else:
            self.showPopup("Không Thành Công","Không lưu được nội dung","Vui lòng liên hệ fanpage để được trợ giúp",False)

    def setReplyRatingPlainText(self,shopTarget,data):
            obj = [
            self.ui.frameOneStar_obj,
            self.ui.frameTwoStar_obj,
            self.ui.frameThreeStar_obj,
            self.ui.frameFourStar_obj,
            self.ui.frameFiveStar_obj,
            ]
            layout = [
            self.ui.frameOneStar,
            self.ui.frameTwoStar,
            self.ui.frameThreeStar,
            self.ui.frameFourStar,
            self.ui.frameFiveStar,
            ]      

            oneStar = data['data']['shopee'][shopTarget]['reply_rating']['1']
            twoStar = data['data']['shopee'][shopTarget]['reply_rating']['2']
            threeStar = data['data']['shopee'][shopTarget]['reply_rating']['3']
            fourStar = data['data']['shopee'][shopTarget]['reply_rating']['4']
            fiveStar = data['data']['shopee'][shopTarget]['reply_rating']['5']
            dataText = [oneStar,twoStar,threeStar,fourStar,fiveStar]
            for o , l , d in zip(obj,layout,dataText):
                count = 1
                for i in d:
                    lenText = len(i)
                    UIFunctions.addFrameText(self,count,o,l,i,lenText)
                    count += 1
  
    def unSaveReplyRating(self):
        self.ui.saveReplyRating.setStyleSheet('background-color: rgb(217, 38, 0);')

    def savedReplyRating(self):
        self.ui.saveReplyRating.setStyleSheet('')

    