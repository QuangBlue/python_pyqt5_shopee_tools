from main import *

class SignInAz(QWidget):
    signInComplete = pyqtSignal(dict)
    def signIn(self,username,password,rememberPass):
        self.rememberPass = rememberPass

        data = QByteArray()
        data.append(f'username={username}&')
        data.append(f'password={password}')
        url = 'http://fastaz.vn/wp-json/jwt-auth/v1/token'
        req = QNetworkRequest(QUrl(url))
        req.setHeader(QNetworkRequest.ContentTypeHeader,
            'application/x-www-form-urlencoded')
        self.signIn = QNetworkAccessManager()
        self.signIn.finished.connect(self.handleResponse)
        self.signIn.post(req, data)

    def handleResponse(self,reply):
        er = reply.error()
        if er == QNetworkReply.NoError:
            bytes_string = reply.readAll()
            json_ar = json.loads(str(bytes_string, 'utf-8'))
            if json_ar['statusCode'] == 200:
                dictSignIn = {}
                dictSignIn['_id'] = json_ar['data']['id']
                dictSignIn['usernameAz'] = json_ar['data']['nicename']
                dictSignIn['tokenWeb'] = json_ar['data']['token']
                dictSignIn['email'] = json_ar['data']['email']
                dictSignIn['rememberPass'] = self.rememberPass
                self.signInComplete.emit(dictSignIn)
            else:
                print (json_ar['message'])
        else:
            print('Error occurred: ', er)
            print(reply.errorString())


class SignInAuto(QWidget):
    signInAutoComplete = pyqtSignal(dict)
    def signInAutoAz(self,token):  
        url = 'http://fastaz.vn/wp-json/jwt-auth/v1/token/validate'
        req = QNetworkRequest(QUrl(url))
        token_ = f"Bearer{token}"

        data = QByteArray()
        data.append(f'{token_}')

        req.setHeader(QNetworkRequest.ContentTypeHeader,
            'application/x-www-form-urlencoded')
        req.setRawHeader(b"Authorization", data)
        self.signInAu = QNetworkAccessManager()
        self.signInAu.finished.connect(self.handleResponse)
        self.signInAu.post(req, data)

    def handleResponse(self,reply):
        er = reply.error()
        if er == QNetworkReply.NoError:
            bytes_string = reply.readAll()
            json_ar = json.loads(str(bytes_string, 'utf-8'))
            self.signInAutoComplete.emit(json_ar)
        else:
            print('Error occurred: ', er)
            print(reply.errorString())

class LoginAz(QWidget):

    def login(self,_id,usernameAz,tokenWeb,email):
        data = QByteArray()
        data.append(f'_id={_id}&')
        data.append(f'usernameAz={usernameAz}&')
        data.append(f'tokenWeb={tokenWeb}&')
        data.append(f'email={email}')

        url = 'http://127.0.0.1:5000/login'
        req = QNetworkRequest(QUrl(url))
        req.setHeader(QNetworkRequest.ContentTypeHeader,
            'application/x-www-form-urlencoded')
        self.nam = QNetworkAccessManager()
        self.nam.finished.connect(self.handleResponse)
        self.nam.post(req, data)

    def handleResponse(self,reply):
        er = reply.error()
        if er == QNetworkReply.NoError:
            bytes_string = reply.readAll()
            json_ar = json.loads(str(bytes_string, 'utf-8'))      
        else:
            print('Error occurred: ', er)
            print(reply.errorString())

class GetDataUserShopee(QWidget):
    def getDataUser(self,usernameAz):
        data = QByteArray()
        data.append(f'usernameAz={usernameAz}')
        url = 'http://127.0.0.1:5000/get_data_user_shopee'
        req = QNetworkRequest(QUrl(url))
        req.setHeader(QNetworkRequest.ContentTypeHeader,
            'application/x-www-form-urlencoded')
        self.nam = QNetworkAccessManager()
        reply = self.nam.post(req, data)
        loop = QEventLoop()
        reply.finished.connect(loop.quit)
        loop.exec_()
        bytes_string = reply.readAll()
        json_ar = json.loads(str(bytes_string, 'utf-8'))

        return json_ar
        if reply.error() != QNetworkReply.NoError:
            QCoreApplication.quit()
    
class GetDataShopee(QWidget):
    getDataShopeeComplete = pyqtSignal(dict)
    
    def __init__(self,usernameAz):
        super().__init__()
        data = QByteArray()
        data.append(f'usernameAz={usernameAz}')

        url = 'http://127.0.0.1:5000/get_data_shopee'
        req = QNetworkRequest(QUrl(url))
        req.setHeader(QNetworkRequest.ContentTypeHeader,
            'application/x-www-form-urlencoded')
        self.getDataShopee = QNetworkAccessManager()
        self.getDataShopee.finished.connect(self.handleResponse)
        self.getDataShopee.post(req, data)

    def handleResponse(self,reply):
        er = reply.error()
        if er == QNetworkReply.NoError:
            bytes_string = reply.readAll()
            json_ar = json.loads(str(bytes_string, 'utf-8'))
            self.getDataShopeeComplete.emit(json_ar)      
        else:
            print('Error occurred: ', er)
            print(reply.errorString())

class DelUserShopee(QWidget):
    def delUserShope(self,usernameAz,usernameShop):
        data = QByteArray()
        data.append(f'usernameAz={usernameAz}&')
        data.append(f'usernameShop={usernameShop}')

        url = 'http://127.0.0.1:5000/del_user_shopee'
        req = QNetworkRequest(QUrl(url))
        req.setHeader(QNetworkRequest.ContentTypeHeader,
            'application/x-www-form-urlencoded')
        self.delUserShopee = QNetworkAccessManager()
        reply = self.delUserShopee.post(req, data)
        loop = QEventLoop()
        reply.finished.connect(loop.quit)
        loop.exec_()
        bytes_string = reply.readAll()
        json_ar = json.loads(str(bytes_string, 'utf-8'))

        return json_ar
        if reply.error() != QNetworkReply.NoError:
            QCoreApplication.quit()
    
class SaveReplyRating(QWidget):
    def saveReplyRating(self,usernameAz,usernameShop,dataUpadte):
        data = QByteArray()
        data.append(f'usernameAz={usernameAz}&')
        data.append(f'usernameShop={usernameShop}&')
        data.append(f'dataUpadte={dataUpadte}')

        url = 'http://127.0.0.1:5000/save_reply_rating'
        req = QNetworkRequest(QUrl(url))
        req.setHeader(QNetworkRequest.ContentTypeHeader,
            'application/x-www-form-urlencoded')
        self.saveReplyRating = QNetworkAccessManager()
        reply = self.saveReplyRating.post(req, data)
        loop = QEventLoop()
        reply.finished.connect(loop.quit)
        loop.exec_()
        bytes_string = reply.readAll()
        json_ar = json.loads(str(bytes_string, 'utf-8'))

        return json_ar
        # if reply.error() != QNetworkReply.NoError:
        #     print('quit')
        #     QCoreApplication.quit()
