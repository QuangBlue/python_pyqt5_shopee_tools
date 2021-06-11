from main import *

from . ui_functions import *

class PushProduct(MainWindow):

    def setupPushProductScreen(self):
        self.ui.btnPushProductSwitch = CustomToggle()
        self.ui.btnPushProductSwitch.setObjectName('pushProductSwitch')
        self.ui.activePushProductLayout.addWidget(self.ui.btnPushProductSwitch)
        self.ui.btnPushProductSwitch.setFocusPolicy(Qt.NoFocus)
        self.ui.btnPushProductSwitch.clicked.connect(lambda: UIFunctions.checkSwitch(self))

    def setDataProductPushTable(self,shopTarget,data):
        self.ui.tableWidget_product_push.setRowCount(24)
        for k in range(self.ui.tableWidget_product_push.rowCount()):
            self.ui.tableWidget_product_push.setRowHeight(k, 90)

        self.ui.tableWidget_product_push.setColumnWidth(0, 50)
        self.ui.tableWidget_product_push.setColumnWidth(1, 100)
        self.ui.tableWidget_product_push.setColumnWidth(2, 800)
        self.ui.tableWidget_product_push.setColumnWidth(3, 150)
        self.ui.tableWidget_product_push.setColumnWidth(4, 150)
        self.ui.tableWidget_product_push.setColumnWidth(5, 150)
        self.ui.tableWidget_product_push.setColumnWidth(6, 150)