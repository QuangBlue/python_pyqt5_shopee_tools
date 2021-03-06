from main import *

from . ui_popup_product_push import *

numbers = 1

class PopupProduct(QMainWindow):
    def __init__(self):
        super(PopupProduct,self,).__init__()
        self.popupPushProduct = Ui_PopupPushProduct()
        self.popupPushProduct.setupUi(self)

        self.resize(1700, 1000)

        self.get_list_products_shopee()

        self.popupPushProduct.btn_forward.clicked.connect(lambda : self.next_page())
        self.popupPushProduct.btn_back.clicked.connect(lambda : self.back_page())

        self.popupPushProduct.btn_confirm.clicked.connect(lambda : self.add_to_product_push())
        self.popupPushProduct.btn_cancel.clicked.connect(lambda : self.close())

        self.popupPushProduct.btnSearch.clicked.connect(lambda: self.searchProduct())
        self.popupPushProduct.searchLineEdit.returnPressed.connect(lambda: self.searchProduct())

    def searchProduct(self):
        search = self.popupPushProduct.searchLineEdit.text()
        for i in reversed(range(self.popupPushProduct.tableWidget_product_push_shopee.rowCount())):
            self.popupPushProduct.tableWidget_product_push_shopee.removeRow(i)
        if search != "":
            self.get_list_products_shopee(self.popupPushProduct.searchLineEdit.text())           
        elif search == "":
            self.get_list_products_shopee()

    def get_list_products_shopee(self,keyword=""): 
        pass     
        # self.tableWidget_product_push_shopee.setRowCount(24)
        # for k in range(self.tableWidget_product_push_shopee.rowCount()):
        #     self.tableWidget_product_push_shopee.setRowHeight(k, 90)
        # self.tableWidget_product_push_shopee.setColumnWidth(0, 50)
        # self.tableWidget_product_push_shopee.setColumnWidth(1, 100)
        # self.tableWidget_product_push_shopee.setColumnWidth(2, 700)
        # self.tableWidget_product_push_shopee.setColumnWidth(3, 140)
        # self.tableWidget_product_push_shopee.setColumnWidth(4, 140)
        # self.tableWidget_product_push_shopee.setColumnWidth(5, 140)
        # self.tableWidget_product_push_shopee.setColumnWidth(6, 140)
        # self.tableWidget_product_push_shopee.setItem(0, 2,QTableWidgetItem("??ang t???i d??? li???u ...."))      
        # global numbers  
        # with open('temp//data.json') as f:
        #     data = json.load(f)
        #     self.id_wp = data['id_wp']          
        #     if len(data['shopee']) != 0:
        #         c = data['shopee'][self.cc]['cookie']             
        #         self.worker_product = ThreadGetListProduct(c,numbers,keyword)
        #         self.worker_product.start()
        #         self.worker_product.r_json.connect(self.update_list_products_shopee)
    
    def update_list_products_shopee(self, l):
        self.r = l[0]
        self.page_number = l[1]
        self.checkTheme()
        a = self.r['data']['page_info']['total']

        page_size = 1 if a <= 24 else (a // 24) +1
        self.popupPushProduct.btn_back.setEnabled(False) if self.popupPushProduct.page_number == 1 else self.btn_back.setEnabled(True)
        self.popupPushProduct.btn_forward.setEnabled(False) if self.popupPushProduct.page_number == page_size else self.btn_forward.setEnabled(True)

        if len(self.r['data']['list']) != 0:
            self.name = []
            self.img = []  
            self.ids = []  
            self.stock = []       
            self.normal_price = []
            self.promotion_price = []
            self.sold = []
            self.parent_sku = []
            for x in range(len(self.r['data']['list'])):
                self.name.append(self.r['data']['list'][x]['name'])
                self.img.append(self.r['data']['list'][x]['images'][0])
                self.ids.append(self.r['data']['list'][x]['id'])
                self.stock.append(self.r['data']['list'][x]['stock'])
                self.normal_price.append(self.r['data']['list'][x]['price_info']['normal_price'])
                self.promotion_price.append(self.r['data']['list'][x]['price_info']['promotion_price'])
                self.sold.append(self.r['data']['list'][x]['sold'])
                self.parent_sku.append(self.r['data']['list'][x]['parent_sku'])
            for row ,data_name in enumerate(self.name):                
                self.popupPushProduct.tableWidget_product_push_shopee.setItem(row, 2,QTableWidgetItem(data_name))

            for row ,parent_sku in enumerate(self.parent_sku):                
                self.popupPushProduct.tableWidget_product_push_shopee.setItem(row, 3,QTableWidgetItem(parent_sku))

            for row ,stock in enumerate(self.stock):                
                self.popupPushProduct.tableWidget_product_push_shopee.setItem(row, 4,QTableWidgetItem(str(stock)))

            for row ,normal_price in enumerate(self.normal_price):                
                self.popupPushProduct.tableWidget_product_push_shopee.setItem(row, 5,QTableWidgetItem(normal_price))

            for row ,promotion_price in enumerate(self.promotion_price):                
                self.popupPushProduct.tableWidget_product_push_shopee.setItem(row, 6,QTableWidgetItem(promotion_price))

            for row ,sold in enumerate(self.sold):                
                self.popupPushProduct.tableWidget_product_push_shopee.setItem(row, 7,QTableWidgetItem(str(sold)))

            # self.workerthread = WorkerThread(self.img,'product_list_shopee')
            # self.workerthread.start()
            # self.workerthread.img_complete.connect(self.update_img)

    def update_img(self,l):
        i = QImage()
        i.loadFromData(l[1]) 
        imgLabel = QLabel()
        imgLabel.setText('')
        imgLabel.setScaledContents(True)    
        imgLabel.setPixmap(QPixmap(i))

        self.popupPushProduct.tableWidget_product_push_shopee.setCellWidget(l[0],1,imgLabel)

    def next_page(self):
        global numbers
        numbers += 1
        for i in reversed(range(self.popupPushProduct.tableWidget_product_push_shopee.rowCount())):
            self.popupPushProduct.tableWidget_product_push_shopee.removeRow(i) 
        self.get_list_products_shopee()

    def back_page(self):
        global numbers
        if numbers <= 1:
            numbers = 1
        elif numbers > 1:
            numbers -= 1
            for i in reversed(range(self.popupPushProduct.tableWidget_product_push_shopee.rowCount())):
                self.popupPushProduct.tableWidget_product_push_shopee.removeRow(i) 
            self.get_list_products_shopee()

    def add_to_product_push(self):
        x = self.popupPushProduct.tableWidget_product_push_shopee.selectedItems()
        l = []
        data = []
        for i in x:
            l.append(i.row())
        for p in set(l):
            k ={}
            k['image'] = self.img[p]
            k['name'] = self.name[p]
            k['ids'] = self.ids[p]
            k['stock'] = self.stock[p] 
            k['parent_sku'] = self.parent_sku[p]
            k['normal_price'] = self.normal_price[p]
            k['promotion_price'] = self.promotion_price[p]
            k['sold'] = self.sold[p]
            k['done'] = 'False'
            data.append(k)
            
        # r , change , duplicate = Database_mongoDB.add_protuct_push(self,self.id_wp,self.cc,data)

        # if r['updatedExisting'] == True:
        #     self.tableWidget_product_push_shopee.clearSelection()
        #     if duplicate == 0 :
        #         self.showPopup("Th??nh C??ng","Th??m s???n ph???m th??nh c??ng",f"{change} s???n ph???m ???????c ch???n ???? th??m th??nh c??ng",True)
        #     else:
        #         self.showPopup("Th??nh C??ng","Th??m s???n ph???m th??nh c??ng",f"{change} s???n ph???m th??m th??nh c??ng v?? {duplicate} s???n ph???m b??? tr??ng ",True)    
        # else:
        #     self.showPopup("Kh??ng Th??nh C??ng","Th??m s???n ph???m kh??ng th??nh c??ng","Vui l??ng li??n h??? fanpage ????? ???????c tr??? gi??p",False)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.popupPushProduct.close()


    def showPopup(self,title,info,notification,c=True):   
        msg = QMessageBox()   
        msg.setWindowTitle(title)
        msg.setText(notification)
        msg.setInformativeText(info)
        if c == True:
            msg.setIconPixmap(QPixmap("img//success.png"))
        else:
            msg.setIconPixmap(QPixmap("img//warning.png"))
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = PopupProduct()
    w.show()
    sys.exit(app.exec_())