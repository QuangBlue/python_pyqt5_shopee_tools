import sys, json, requests
import platform

# IMPORT / GUI AND MODULES
# ///////////////////////////////////////////////////////////////
from modules import *
from widgets import *

# SET AS GLOBAL WIDGETS
# ///////////////////////////////////////////////////////////////
widgets = None

# GLOBALS
counter = 0

usernameGlobal = None
shopTarget = None

targetFunc = None
btnFunc = None
pageFunc = None

class SignInScreen(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = Ui_SignInScreen()
        self.ui.setupUi(self)
        global widgets
        widgets = self.ui

        widgets.signinBtn.clicked.connect(self.signIn)
        widgets.password.returnPressed.connect(self.signIn)
        try:
            with open("data/data.json") as f:
                self.data = json.load(f)
            if self.data['rememberPass'] == True and self.data['token']:
                self.signInAuto = SignInAuto()
                self.signInAuto.signInAutoAz(self.data['token'])
                self.signInAuto.signInAutoComplete.connect(self.signInAutoAz)
            else:
                self.show()
        except Exception as inst:
            print(inst)
            self.show()
            
    def signInAutoAz(self,dict_):
        global usernameGlobal
        if dict_['success'] == True:
            usernameGlobal = dict_['data']['nicename']
            dictSignIn = {
                '_id' : dict_['data']['id'],
                'usernameAz' : usernameGlobal,
                'tokenWeb' : dict_['data']['token'],
                'email' : dict_['data']['email'],
                'rememberPass' : True
            }
            self.signInSuccess(dictSignIn)

        elif dict_['success'] == False:
            self.show() 

    def signIn(self):
        global usernameGlobal
        self.signIn = SignInAz()
        self.signIn.signIn(widgets.username.text(),widgets.password.text(),widgets.savePassCheckBox.isChecked())
        self.signIn.signInComplete.connect(self.signInSuccess)

        usernameGlobal = widgets.username.text()

    def signInSuccess(self,dictSignIn):
        self.splash = SplashScreen(
            dictSignIn['_id'],
            dictSignIn['usernameAz'],
            dictSignIn['tokenWeb'],
            dictSignIn['email'],
            dictSignIn['rememberPass']
            )


        self.splash.show()
        self.close()        

class SplashScreen(QMainWindow):
    def __init__(self,_id,usernameAz,tokenWeb,email,rememberPass):
        QMainWindow.__init__(self)
        self.ui = Ui_SplashScreen()
        self.ui.setupUi(self)

        self._id  = _id
        self.usernameAz = usernameAz
        self.tokenWeb = tokenWeb
        self.email = email
        self.rememberPass = rememberPass


        # REMOVE TITLE BAR
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        # IMPORT CIRCULAR PROGRESS
        self.progress = CircularProgress()
        self.progress.width = 270
        self.progress.height = 270
        self.progress.value = 0
        self.progress.setFixedSize(self.progress.width, self.progress.height)
        self.progress.move(15, 15)
        self.progress.font_size = 40
        self.progress.add_shadow(True)
        self.progress.progress_width = 5
        self.progress.bg_color = QColor(68, 71, 90, 140)
        self.progress.setParent(self.ui.centralwidget)
        self.progress.show()

        # ADD DROP SHADOW
        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(15)
        self.shadow.setXOffset(0)
        self.shadow.setYOffset(0)
        self.shadow.setColor(QColor(0, 0, 0, 80))
        self.setGraphicsEffect(self.shadow)

        # QTIMER 
        self.timer = QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(25)

        self.show()

    # UPDATE PROGRESS BAR
    def update(self):
        global counter

        # SET VALUE TO PROGRESS BAR
        self.progress.set_value(counter)

        if counter == 50:

            self.loginAz = LoginAz()
            self.loginAz.login(self._id,self.usernameAz,self.tokenWeb,self.email)

        if counter == 60:
            data = {
                "rememberPass" : self.rememberPass,
                "token" : self.tokenWeb
            }
            with open('data//data.json', 'w') as f:
                    json.dump(data, f)

        # CLOSE SPLASH SCREEN AND OPEN MAIN APP
        if counter >= 100:
            # STOP TIMER
            self.timer.stop()

            # SHOW MAIN WINDOW
            self.main = MainWindow()
            self.main.show()

            # CLOSE SPLASH SCREEN
            self.close()

        # INCREASE COUNTER
        counter += 1

class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)

        # SET AS GLOBAL WIDGETS
        # ///////////////////////////////////////////////////////////////
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        global widgets
        widgets = self.ui

        # USE CUSTOM TITLE BAR | USE AS "False" FOR MAC OR LINUX
        # ///////////////////////////////////////////////////////////////
        Settings.ENABLE_CUSTOM_TITLE_BAR = False

        # APP NAME
        # ///////////////////////////////////////////////////////////////
        title = "FastAz - Phần mềm quản lý bán hàng"
        description = "FastAz - Phần mềm quản lý bán hàng."
        # APPLY TEXTS
        self.setWindowTitle(title)
        widgets.titleRightInfo.setText(description)

        # TOGGLE MENU
        # ///////////////////////////////////////////////////////////////
        widgets.toggleButton.clicked.connect(lambda: UIFunctions.toggleMenu(self, True))
        widgets.btn_logout.clicked.connect(lambda: UIFunctions.logout(self))
        # SET UI DEFINITIONS
        # ///////////////////////////////////////////////////////////////
        UIFunctions.uiDefinitions(self)

        # SET LIST USER SHOPEE
        # ///////////////////////////////////////////////////////////////

        self.setListUserShopee()

        # QTableWidget PARAMETERS
        # ///////////////////////////////////////////////////////////////
        # widgets.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        widgets.saveReplyRating.clicked.connect(lambda: ReplyRating.btnSaveReplyRating(self, usernameGlobal, shopTarget))

        # SETUP PUSH PRODUCT SCREEN
        # ///////////////////////////////////////////////////////////////

        PushProduct.setupPushProductScreen(self)

        # SETUP REPLY RATING SCREEN
        # ///////////////////////////////////////////////////////////////
        ReplyRating.setupReplyRatingScreen(self)

        # SETUP CHAT BOT SCREEN
        # ///////////////////////////////////////////////////////////////
        ChatBot.setupChatBotScreen(self)

        # BUTTONS CLICK
        # ///////////////////////////////////////////////////////////////

        # LEFT MENUS
        widgets.btnPushProduct.clicked.connect(self.buttonClick)
        widgets.btnReplyRating.clicked.connect(self.buttonClick)
        widgets.btnChatBot.clicked.connect(self.buttonClick)
        widgets.btn_save.clicked.connect(self.buttonClick)

        # EXTRA LEFT BOX
        def openCloseLeftBox():
            UIFunctions.toggleLeftBox(self, True)
        widgets.toggleLeftBox.clicked.connect(openCloseLeftBox)
        widgets.extraCloseColumnBtn.clicked.connect(openCloseLeftBox)

        # EXTRA RIGHT BOX
        def openCloseRightBox():
            UIFunctions.toggleRightBox(self, True)
        widgets.settingsTopBtn.clicked.connect(openCloseRightBox)

        # MANAGER USER SHOPEE - BUTTONS CLICK
        # ///////////////////////////////////////////////////////////////

        widgets.addUserShopeeBtn.clicked.connect(lambda: self.openBrowserAddUserShopee())

        widgets.btn_add_product_push.clicked.connect(lambda: self.openPopupPushProduct())

        # SHOW APP
        # ///////////////////////////////////////////////////////////////
        self.show()

        # SET CUSTOM THEME
        # ///////////////////////////////////////////////////////////////
        useCustomTheme = False
        themeFileLight = "themes\py_dracula_light.qss"

        # SET THEME AND HACKS
        if useCustomTheme:
            # LOAD AND APPLY STYLE
            UIFunctions.theme(self, themeFileLight, True)

            # SET HACKS
            AppFunctions.setThemeHack(self)


        # SET HOME PAGE AND SELECT MENU
        # ///////////////////////////////////////////////////////////////
        widgets.stackedWidget.setCurrentWidget(widgets.pageHome)
        # widgets.btnPushProduct.setStyleSheet(UIFunctions.selectMenu(widgets.btnPushProduct.styleSheet()))


    # BUTTONS CLICK
    # Post here your functions for clicked buttons
    # ///////////////////////////////////////////////////////////////
    def buttonClick(self):
        global targetFunc, btnFunc, pageFunc

        # GET BUTTON CLICKED
        btnFunc = self.sender()
        targetFunc = btnFunc.objectName()

        # SHOW HOME PAGE
        if targetFunc == "btnPushProduct":
            pageFunc = widgets.pagePushProduct
            # widgets.stackedWidget.setCurrentWidget(widgets.pagePushProduct)
            # UIFunctions.resetStyle(self, btnName)
            # btn.setStyleSheet(UIFunctions.selectMenu(btn.styleSheet()))
            self.checkStatusShop(pageFunc,targetFunc,btnFunc)

        # SHOW WIDGETS PAGE
        if targetFunc == "btnReplyRating":
            pageFunc = widgets.pageReplyRating
            # widgets.stackedWidget.setCurrentWidget(widgets.pageReplyRating)
            # UIFunctions.resetStyle(self, btnName)
            # btn.setStyleSheet(UIFunctions.selectMenu(btn.styleSheet()))
            self.checkStatusShop(pageFunc,targetFunc,btnFunc)
        # SHOW NEW PAGE
        if targetFunc == "btnChatBot":
            pageFunc = widgets.pageChatBot
            # widgets.stackedWidget.setCurrentWidget(widgets.pageChatBot) # SET PAGE
            # UIFunctions.resetStyle(self, btnName) # RESET ANOTHERS BUTTONS SELECTED
            # btn.setStyleSheet(UIFunctions.selectMenu(btn.styleSheet())) # SELECT MENU
            self.checkStatusShop(pageFunc,targetFunc,btnFunc)

        if targetFunc == "btn_save":
            print("Save BTN clicked!")

        # PRINT BTN NAME
        print(f'Button "{targetFunc}" pressed!')

    # RESIZE EVENTS
    # ///////////////////////////////////////////////////////////////
    def resizeEvent(self, event):
        # Update Size Grips
        UIFunctions.resize_grips(self)

    # MOUSE CLICK EVENTS
    # ///////////////////////////////////////////////////////////////
    def mousePressEvent(self, event):
        # SET DRAG POS WINDOW
        self.dragPos = event.globalPos()

        # PRINT MOUSE EVENTS
        if event.buttons() == Qt.LeftButton:
            print('Mouse click: LEFT CLICK')
        if event.buttons() == Qt.RightButton:
            print('Mouse click: RIGHT CLICK')

    def openBrowserAddUserShopee(self):
        self.browser = Browser(usernameGlobal)
        self.browser.msg.buttonClicked.connect(lambda: self.browser.close())
        self.browser.msg.buttonClicked.connect(lambda: self.setListUserShopee())
        self.browser.show()
        
    def openPopupPushProduct(self):
        self.popup = PopupProduct()
        self.popup.show()

    def setListUserShopee(self):
        getList = GetDataUserShopee()
        r = getList.getDataUser(usernameGlobal)

        self.clearLayout(widgets.verticalLayout_11)

        if r['success'] == True:
            for name in r['data']:
                self.addUserShopeeBtn(name)
        elif r['success'] == False:
            print('Lỗi không tài khoản shopee')

    def clearLayout(self, layout):
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
                else:
                    self.clearLayout(item.layout())


    def addUserShopeeBtn(self,nameShop):

        self.layout = QHBoxLayout()

        self.btn = QPushButton(self)
        self.btn.setObjectName(nameShop)
        self.btn.clicked.connect(self.buttonShopTarget)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn.sizePolicy().hasHeightForWidth())
        self.btn.setSizePolicy(sizePolicy)
        self.btn.setMinimumSize(QSize(0, 50))
        self.btn.setCursor(QCursor(Qt.PointingHandCursor))
        self.btn.setLayoutDirection(Qt.LeftToRight)
        self.btn.setText("      "+f"{nameShop}")
        icon = QIcon()
        icon.addFile("images//images//logo-shopee.png", QSize(), QIcon.Normal, QIcon.Off)
        self.btn.setIcon(icon)
        self.btn.setIconSize(QSize(25, 25))

        self.btnDel = QPushButton('x')
        self.btnDel.setObjectName(f'del_{nameShop}')
        self.btnDel.setStyleSheet('QPushButton {background : transparent} QPushButton:hover { color : rgb(255, 55, 44)}')
        self.btnDel.clicked.connect(self.buttonDelUserShopee)

        self.layout.addWidget(self.btn)
        self.layout.addWidget(self.btnDel)
        widgets.verticalLayout_11.addLayout(self.layout)

    def buttonDelUserShopee(self):
        btnWidget = self.sender()
        objName = btnWidget.objectName().split("_")[1]
        x = QMessageBox.warning(self, 'MessageBox', "TẤT CẢ DỮ LIỆU SẼ MẤT \nBạn có chắc chắn muốn xóa tài khoản này không ?", QMessageBox.Yes|QMessageBox.No, QMessageBox.Yes)
        if x == QMessageBox.Yes:
            r = DelUserShopee.delUserShope(self,usernameGlobal,objName)
            if r['updated'] == True:
                self.setListUserShopee()

    def buttonShopTarget(self):
        global shopTarget
        btnWidget = self.sender()

        btnName = btnWidget.objectName()

        if btnName != shopTarget:
            self.clearData()
            shopTarget = btnWidget.objectName()
            self.setupData()

            for w in widgets.extraTopMenu.findChildren(QPushButton):
                if w.objectName() != shopTarget and w.objectName().split("_")[0] != 'del':
                    w.setStyleSheet('')
                if w.objectName() == shopTarget:
                    w.setStyleSheet('	background-color: #4070f4; border-radius: 8px')
        
        self.checkStatusShop(pageFunc,targetFunc,btnFunc)

    def checkStatusShop(self,pageFunc,targetFunc,btnFunc):
        if not targetFunc:
            widgets.labelHomePage.setText('Vui lòng chọn chức năng')
        elif not shopTarget:
            widgets.labelHomePage.setText('Vui lòng chọn shop cần thao tác')
        else:
            widgets.stackedWidget.setCurrentWidget(pageFunc)
            UIFunctions.resetStyle(self, targetFunc)
            btnFunc.setStyleSheet(UIFunctions.selectMenu(btnFunc.styleSheet()))
            

    def clearData(self):
        l = [widgets.tableWidget_product_push]
        for x in l:
            for i in reversed(range(x.rowCount())):
                x.removeRow(i)

        obj = [
            widgets.frameOrderNew_obj,
            widgets.frameOrderReady_obj,
            widgets.frameOrderShipping_obj,
            widgets.frameOrderSuccess_obj,
            widgets.frameOrderCancel_obj,
            widgets.frameOneStar_obj,
            widgets.frameTwoStar_obj,
            widgets.frameThreeStar_obj,
            widgets.frameFourStar_obj,
            widgets.frameFiveStar_obj,
            ]

        layout = [
            widgets.frameOrderNew,
            widgets.frameOrderReady,
            widgets.frameOrderShipping,
            widgets.frameOrderSuccess,
            widgets.frameOrderCancel,
            widgets.frameOneStar,
            widgets.frameTwoStar,
            widgets.frameThreeStar,
            widgets.frameFourStar,
            widgets.frameFiveStar,
            ]    
        for o , l in zip(obj, layout):
            for i in range(len(o.findChildren(QPlainTextEdit))):
                l.removeWidget(o.findChildren(QPlainTextEdit)[0])
                l.removeWidget(o.findChildren(QLabel)[0])
                l.removeWidget(o.findChildren(QLabel)[0])
                l.removeWidget(o.findChildren(QPushButton)[0])

    def showPopup(self,title,info,notification,c=True):   
        msg = QMessageBox()   
        msg.setWindowTitle(title)
        msg.setText(notification)
        msg.setInformativeText(info)
        if c == True:
            msg.setIconPixmap(QPixmap("images//images//success.png"))
        else:
            msg.setIconPixmap(QPixmap("images//images//warning.png"))
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()

    def setupData(self):
        self.getData = GetDataShopee(usernameGlobal)
        self.getData.getDataShopeeComplete.connect(self.setDataReplyRating)
        self.getData.getDataShopeeComplete.connect(self.setDataProductPush)

        
    def setDataReplyRating(self,dictDataReplyRating):
        ReplyRating.setReplyRatingPlainText(self,shopTarget,dictDataReplyRating)
    
    def setDataProductPush(self,dictDataProductPush):
        PushProduct.setDataProductPushTable(self,shopTarget,dictDataProductPush)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("icon.ico"))
    window = SignInScreen()
    sys.exit(app.exec_())
