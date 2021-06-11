# ///////////////////////////////////////////////////////////////
#
# BY: WANDERSON M.PIMENTA
# PROJECT MADE WITH: Qt Designer and PySide6
# V: 1.0.0
#
# This project can be used freely for all uses, as long as they maintain the
# respective credits only in the Python scripts, any information in the visual
# interface (GUI) can be modified without any implication.
#
# There are limitations on Qt licenses if you want to use your products
# commercially, I recommend reading them on the official website:
# https://doc.qt.io/qtforpython/licenses.html
#
# ///////////////////////////////////////////////////////////////

# MAIN FILE
# ///////////////////////////////////////////////////////////////
from main import *


# GLOBALS
# ///////////////////////////////////////////////////////////////
GLOBAL_STATE = False
GLOBAL_TITLE_BAR = True

class UIFunctions(MainWindow):
    # MAXIMIZE/RESTORE
    # ///////////////////////////////////////////////////////////////
    def maximize_restore(self):
        global GLOBAL_STATE
        status = GLOBAL_STATE
        if status == False:
            self.showMaximized()
            GLOBAL_STATE = True
            self.ui.appMargins.setContentsMargins(0, 0, 0, 0)
            self.ui.maximizeRestoreAppBtn.setToolTip("Restore")
            self.ui.maximizeRestoreAppBtn.setIcon(QIcon(u":/icons/images/icons/icon_restore.png"))
            self.ui.frame_size_grip.hide()
            self.left_grip.hide()
            self.right_grip.hide()
            self.top_grip.hide()
            self.bottom_grip.hide()
        else:
            GLOBAL_STATE = False
            self.showNormal()
            self.resize(self.width()+1, self.height()+1)
            self.ui.appMargins.setContentsMargins(10, 10, 10, 10)
            self.ui.maximizeRestoreAppBtn.setToolTip("Maximize")
            self.ui.maximizeRestoreAppBtn.setIcon(QIcon(u":/icons/images/icons/icon_maximize.png"))
            self.ui.frame_size_grip.show()
            self.left_grip.show()
            self.right_grip.show()
            self.top_grip.show()
            self.bottom_grip.show()

    # RETURN STATUS
    # ///////////////////////////////////////////////////////////////
    def returStatus(self):
        return GLOBAL_STATE

    # SET STATUS
    # ///////////////////////////////////////////////////////////////
    def setStatus(self, status):
        global GLOBAL_STATE
        GLOBAL_STATE = status

    # TOGGLE MENU
    # ///////////////////////////////////////////////////////////////
    def toggleMenu(self, enable):
        if enable:
            # GET WIDTH
            width = self.ui.leftMenuBg.width()
            maxExtend = Settings.MENU_WIDTH
            standard = 60

            # SET MAX WIDTH
            if width == 60:
                widthExtended = maxExtend
            else:
                widthExtended = standard

            # ANIMATION
            self.animation = QPropertyAnimation(self.ui.leftMenuBg, b"minimumWidth")
            self.animation.setDuration(Settings.TIME_ANIMATION)
            self.animation.setStartValue(width)
            self.animation.setEndValue(widthExtended)
            self.animation.setEasingCurve(QEasingCurve.InOutQuart)
            self.animation.start()

    # TOGGLE LEFT BOX
    # ///////////////////////////////////////////////////////////////
    def toggleLeftBox(self, enable):
        if enable:
            # GET WIDTH
            width = self.ui.extraLeftBox.width()
            widthRightBox = self.ui.extraRightBox.width()
            maxExtend = Settings.LEFT_BOX_WIDTH
            color = Settings.BTN_LEFT_BOX_COLOR
            standard = 0

            # GET BTN STYLE
            style = self.ui.toggleLeftBox.styleSheet()

            # SET MAX WIDTH
            if width == 0:
                widthExtended = maxExtend
                # SELECT BTN
                self.ui.toggleLeftBox.setStyleSheet(style + color)
                if widthRightBox != 0:
                    style = self.ui.settingsTopBtn.styleSheet()
                    self.ui.settingsTopBtn.setStyleSheet(style.replace(Settings.BTN_RIGHT_BOX_COLOR, ''))
            else:
                widthExtended = standard
                # RESET BTN
                self.ui.toggleLeftBox.setStyleSheet(style.replace(color, ''))
                
        UIFunctions.start_box_animation(self, width, widthRightBox, "left")

    # TOGGLE RIGHT BOX
    # ///////////////////////////////////////////////////////////////
    def toggleRightBox(self, enable):
        if enable:
            # GET WIDTH
            width = self.ui.extraRightBox.width()
            widthLeftBox = self.ui.extraLeftBox.width()
            maxExtend = Settings.RIGHT_BOX_WIDTH
            color = Settings.BTN_RIGHT_BOX_COLOR
            standard = 0

            # GET BTN STYLE
            style = self.ui.settingsTopBtn.styleSheet()

            # SET MAX WIDTH
            if width == 0:
                widthExtended = maxExtend
                # SELECT BTN
                self.ui.settingsTopBtn.setStyleSheet(style + color)
                if widthLeftBox != 0:
                    style = self.ui.toggleLeftBox.styleSheet()
                    self.ui.toggleLeftBox.setStyleSheet(style.replace(Settings.BTN_LEFT_BOX_COLOR, ''))
            else:
                widthExtended = standard
                # RESET BTN
                self.ui.settingsTopBtn.setStyleSheet(style.replace(color, ''))

            UIFunctions.start_box_animation(self, widthLeftBox, width, "right")

    def start_box_animation(self, left_box_width, right_box_width, direction):
        right_width = 0
        left_width = 0 

        # Check values
        if left_box_width == 0 and direction == "left":
            left_width = Settings.LEFT_BOX_WIDTH
        else:
            left_width = 0
        # Check values
        if right_box_width == 0 and direction == "right":
            right_width = Settings.RIGHT_BOX_WIDTH
        else:
            right_width = 0       

        # ANIMATION LEFT BOX        
        self.left_box = QPropertyAnimation(self.ui.extraLeftBox, b"minimumWidth")
        self.left_box.setDuration(Settings.TIME_ANIMATION)
        self.left_box.setStartValue(left_box_width)
        self.left_box.setEndValue(left_width)
        self.left_box.setEasingCurve(QEasingCurve.InOutQuart)

        # ANIMATION RIGHT BOX        
        self.right_box = QPropertyAnimation(self.ui.extraRightBox, b"minimumWidth")
        self.right_box.setDuration(Settings.TIME_ANIMATION)
        self.right_box.setStartValue(right_box_width)
        self.right_box.setEndValue(right_width)
        self.right_box.setEasingCurve(QEasingCurve.InOutQuart)

        # GROUP ANIMATION
        self.group = QParallelAnimationGroup()
        self.group.addAnimation(self.left_box)
        self.group.addAnimation(self.right_box)
        self.group.start()

    # SELECT/DESELECT MENU
    # ///////////////////////////////////////////////////////////////
    # SELECT
    def selectMenu(getStyle):
        select = getStyle + Settings.MENU_SELECTED_STYLESHEET
        return select

    # DESELECT
    def deselectMenu(getStyle):
        deselect = getStyle.replace(Settings.MENU_SELECTED_STYLESHEET, "")
        return deselect

    # START SELECTION
    def selectStandardMenu(self, widget):
        for w in self.ui.topMenu.findChildren(QPushButton):
            if w.objectName() == widget:
                w.setStyleSheet(UIFunctions.selectMenu(w.styleSheet()))

    # RESET SELECTION
    def resetStyle(self, widget):
        for w in self.ui.topMenu.findChildren(QPushButton):
            if w.objectName() != widget:
                w.setStyleSheet(UIFunctions.deselectMenu(w.styleSheet()))

    # IMPORT THEMES FILES QSS/CSS
    # ///////////////////////////////////////////////////////////////
    def theme(self, file, useCustomTheme):
        if useCustomTheme:
            str = open(file, 'r').read()
            self.ui.styleSheet.setStyleSheet(str)

    # START - GUI DEFINITIONS
    # ///////////////////////////////////////////////////////////////
    def uiDefinitions(self):
        def dobleClickMaximizeRestore(event):
            # IF DOUBLE CLICK CHANGE STATUS
            if event.type() == QEvent.MouseButtonDblClick:
                QTimer.singleShot(250, lambda: UIFunctions.maximize_restore(self))
        self.ui.titleRightInfo.mouseDoubleClickEvent = dobleClickMaximizeRestore

        if Settings.ENABLE_CUSTOM_TITLE_BAR:
            #STANDARD TITLE BAR
            self.setWindowFlags(Qt.FramelessWindowHint)
            self.setAttribute(Qt.WA_TranslucentBackground)

            # MOVE WINDOW / MAXIMIZE / RESTORE
            def moveWindow(event):
                # IF MAXIMIZED CHANGE TO NORMAL
                if UIFunctions.returStatus(self):
                    UIFunctions.maximize_restore(self)
                # MOVE WINDOW
                if event.buttons() == Qt.LeftButton:
                    self.move(self.pos() + event.globalPos() - self.dragPos)
                    self.dragPos = event.globalPos()
                    event.accept()
            self.ui.titleRightInfo.mouseMoveEvent = moveWindow

            # CUSTOM GRIPS
            self.left_grip = CustomGrip(self, Qt.LeftEdge, True)
            self.right_grip = CustomGrip(self, Qt.RightEdge, True)
            self.top_grip = CustomGrip(self, Qt.TopEdge, True)
            self.bottom_grip = CustomGrip(self, Qt.BottomEdge, True)

        else:
            self.ui.appMargins.setContentsMargins(0, 0, 0, 0)
            self.ui.minimizeAppBtn.hide()
            self.ui.maximizeRestoreAppBtn.hide()
            self.ui.closeAppBtn.hide()
            self.ui.frame_size_grip.hide()

        # DROP SHADOW
        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(17)
        self.shadow.setXOffset(0)
        self.shadow.setYOffset(0)
        self.shadow.setColor(QColor(0, 0, 0, 150))
        self.ui.bgApp.setGraphicsEffect(self.shadow)

        # RESIZE WINDOW
        self.sizegrip = QSizeGrip(self.ui.frame_size_grip)
        self.sizegrip.setStyleSheet("width: 20px; height: 20px; margin 0px; padding: 0px;")

        # MINIMIZE
        self.ui.minimizeAppBtn.clicked.connect(lambda: self.showMinimized())

        # MAXIMIZE/RESTORE
        self.ui.maximizeRestoreAppBtn.clicked.connect(lambda: UIFunctions.maximize_restore(self))

        # CLOSE APPLICATION
        self.ui.closeAppBtn.clicked.connect(lambda: self.close())

    def resize_grips(self):
        if Settings.ENABLE_CUSTOM_TITLE_BAR:
            self.left_grip.setGeometry(0, 10, 10, self.height())
            self.right_grip.setGeometry(self.width() - 10, 10, 10, self.height())
            self.top_grip.setGeometry(0, 0, self.width(), 10)
            self.bottom_grip.setGeometry(0, self.height() - 10, self.width(), 10)

    def addUserShopee(self):
        self.btn = QPushButton(self)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn.sizePolicy().hasHeightForWidth())
        self.btn.setSizePolicy(sizePolicy)
        self.btn.setMinimumSize(QSize(0, 45))
        self.btn.setCursor(QCursor(Qt.PointingHandCursor))
        self.btn.setLayoutDirection(Qt.LeftToRight)
        self.btn.setStyleSheet(u"background-image: url(:/icons/images/icons/cil-share-boxed.png);")
        self.btn.setText(QCoreApplication.translate("MainWindow", u"Share", None))
        self.verticalLayout_11.addWidget(self.btn)

    def countFrameText(self,obj,layout):
    
        r = obj.findChildren(QPlainTextEdit)
        UIFunctions.addFrameText(self,len(r)+1,obj,layout)

    def addFrameText(self,count,obj,layout,text='',lenText=0):
        font = QFont()
        font.setFamily(u"Nunito")
        font.setPointSize(16)
        frameT = QHBoxLayout()
        plainText = QPlainTextEdit()
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        plainText.setSizePolicy(sizePolicy)
        plainText.setMinimumSize(QSize(0,200))
        plainText.setLayoutDirection(Qt.LeftToRight)
        plainText.setObjectName(f"plainText_{count}")
        plainText.setFont(font)
        plainText.setPlaceholderText('Nội dung sẽ gửi cho khách hàng.')
        plainText.setFocus()
        plainText.setPlainText(text)

        sizePolicy2 = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)

        label = QLabel(f"{count}#")
        label.setObjectName(f"label_{count}")
        label.setFont(font)
        label.setSizePolicy(sizePolicy2)

        font1 = QFont()
        font1.setFamily(u"Nunito")
        font1.setPointSize(14)


        labelCount = QLabel(f"{lenText}/400")
        labelCount.setObjectName(f"count_{count}")
        labelCount.setFont(font1)
        labelCount.setStyleSheet("color : #A6A6A6")
        
        plainText.textChanged.connect(lambda : UIFunctions.countPlainTextEdit(self,obj,layout))

        btn = QPushButton('')
        btn.setObjectName(f"_{count}")
        btn.setStyleSheet('QPushButton { background: transparent;}')
        sizePolicy1 = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        btn.setSizePolicy(sizePolicy1)
        btn.setIcon(QIcon('images/images/clear.png')) 
        btn.clicked.connect(lambda : UIFunctions.delPlainTextEdit(self,obj,layout))       
        frameT.addWidget(label)
        frameT.addWidget(labelCount)
        frameT.addWidget(btn)
        layout.addLayout(frameT)
        layout.addWidget(plainText)

    def countPlainTextEdit(self,obj,layout):
        widget = self.sender()
        objNameCountText = widget.objectName()
        objNameCountLabel = objNameCountText.replace("plainText","count")
        plainTextCount = obj.findChildren(QPlainTextEdit,objNameCountText)[0]
        labelCountText = obj.findChildren(QLabel,objNameCountLabel)[0]
        countText = len(plainTextCount.toPlainText())
        labelCountText.setText(f"{countText}/400")

        if countText > 400:
            labelCountText.setStyleSheet("color : red")
            plainTextCount.setStyleSheet("border: 1px solid red;")     
        else:
            labelCountText.setStyleSheet("color : #A6A6A6")
            plainTextCount.setStyleSheet("border: 1px solid rgb(127, 126, 128);")

    def delPlainTextEdit(self,obj,layout):
        btnWidget = self.sender()
        objName = btnWidget.objectName()
        layout.removeWidget(obj.findChildren(QLabel , f'label{objName}')[0]) 
        layout.removeWidget(obj.findChildren(QPushButton, f'{objName}')[0])
        layout.removeWidget(obj.findChildren(QPlainTextEdit, f'plainText{objName}')[0])
        layout.removeWidget(obj.findChildren(QLabel, f'count{objName}')[0])

        if layout in [self.ui.frameOrderNew,
            self.ui.frameOrderReady,
            self.ui.frameOrderShipping,
            self.ui.frameOrderSuccess,
            self.ui.frameOrderCancel]:
            self.ui.btnSaveOrderNew.setStyleSheet('background-color: rgb(217, 38, 0);')
            self.ui.btnSaveOrderReady.setStyleSheet('background-color: rgb(217, 38, 0);')
            self.ui.btnSaveOrderShipping.setStyleSheet('background-color: rgb(217, 38, 0);')
            self.ui.btnSaveOrderSuccess.setStyleSheet('background-color: rgb(217, 38, 0);')
            self.ui.btnSaveOrderCancel.setStyleSheet('background-color: rgb(217, 38, 0);')
        elif layout in [self.ui.frameOneStar,
            self.ui.frameTwoStar,
            self.ui.frameThreeStar,
            self.ui.frameFourStar,
            self.ui.frameFiveStar]:
            self.ui.saveReplyRating.setStyleSheet('background-color: rgb(217, 38, 0);')


    def logout(self):
        print('Logout')    

    def checkSwitch(self):

        btn = self.sender()
        objName = btn.objectName()
        
        if objName == 'pushProductSwitch':

            if self.ui.btnPushProductSwitch.isChecked() == True:
                print ('Mở đẩy sản phẩm')
            else:
                print ('Tắt đẩy sản phẩm')

        elif objName == "replyRatingSwitch":

            if self.ui.btnReplyRatingSwitch.isChecked() == True:
                print ('Mở trả lời tin nhắn')
            else:
                print ('Tắt trả lời tin nhắn')

        elif objName == "chatBotSwitch":

            if self.ui.btnChatBotSwitch.isChecked() == True:
                print ('Mở Chat Bot')
            else:
                print ('Tắt Chat Bot')
            

    # ///////////////////////////////////////////////////////////////
    # END - GUI DEFINITIONS
