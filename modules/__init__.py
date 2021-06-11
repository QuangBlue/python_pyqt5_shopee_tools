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
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtNetwork import *
from PyQt5.uic import loadUi

# GUI FILE
from . ui_signin import Ui_SignInScreen

# GUI FILE
from . ui_splash_screen import Ui_SplashScreen

# GUI FILE
from . ui_main import Ui_MainWindow

# APP SETTINGS
from . app_settings import Settings

# IMPORT FUNCTIONS
from . ui_functions import UIFunctions

# APP FUNCTIONS
from . app_functions import *

# APP REQUESTS
from . app_requests import *

# CHAT BOT
from . chat_bot import *

# REPLY RATING
from . reply_rating import *

# REPLY RATING
from . push_product import *

# BROWSER
from . browser import *

# POPUP PUSH PRODUCT
from . popup_push_product import *