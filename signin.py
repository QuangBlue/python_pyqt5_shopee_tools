#!/usr/bin/python

'''
QNetworkAccessManager in PyQt

In this example we post data to a web page.

Author: Jan Bodnar
Website: zetcode.com
'''

from PyQt5 import QtNetwork
from PyQt5 import QtCore
import sys, json

class Example:

    def __init__(self):

        self.doRequest()


    def doRequest(self):

        data = QtCore.QByteArray()
        data.append('username=quangblue1603&')
        data.append('password=Thangkhung123!@#')
        print(data)

        url = 'http://fastaz.vn/wp-json/jwt-auth/v1/token'
        req = QtNetwork.QNetworkRequest(QtCore.QUrl(url))
        req.setHeader(QtNetwork.QNetworkRequest.ContentTypeHeader,
            'application/x-www-form-urlencoded')

        self.nam = QtNetwork.QNetworkAccessManager()
        self.nam.finished.connect(self.handleResponse)
        self.nam.post(req, data)


    def handleResponse(self, reply):
        er = reply.error()
        if er == QtNetwork.QNetworkReply.NoError:
            bytes_string = reply.readAll()
            json_ar = json.loads(str(bytes_string, 'utf-8'))
            print(json_ar)

        else:
            print('Error occurred: ', er)
            print(reply.errorString())

        QtCore.QCoreApplication.quit()


def main():

    app = QtCore.QCoreApplication([])
    ex = Example()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()