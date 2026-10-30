import sys
import asyncio
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtCore import QUrl, QThread, pyqtSignal
from PyQt6.QtWebEngineCore import QWebEnginePage
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWidgets import (QHBoxLayout,QPushButton,QVBoxLayout,QWidget)
import src.ai_page.my_agents as my_agents
import src.database_page.database as database2

#Class for threading
class AgentWorker(QThread):
    finished = pyqtSignal(str)

    def __init__(self, query: str):
        super().__init__()
        self.query = query

    def run(self):
        # Run the async agent_runner inside the background thread's event loop
        response = asyncio.run(my_agents.agent_runner(self.query))
        self.finished.emit(str(response))

#Class for window popup
class CustomWebEnginePage(QWebEnginePage):
    """Intercepts new window/popup requests and opens them in a separate window."""

    def createWindow(self, _type):
        self.popup = QWidget()
        self.popup.setWindowTitle("Popup Window")
        self.popup.resize(900, 650)

        layout = QVBoxLayout(self.popup)
        layout.setContentsMargins(0, 0, 0, 0)

        popup_view = QWebEngineView(self.popup)
        layout.addWidget(popup_view)

        self.popup.show()
        return popup_view.page()

#Class for the main UI
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):

        #################################################
        # UI SETUP
        #################################################

        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1692, 798)
        MainWindow.setMinimumSize(QtCore.QSize(0, 0))
        MainWindow.setStyleSheet("")
        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setMinimumSize(QtCore.QSize(1280, 720))
        self.centralwidget.setStyleSheet("")
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_5.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.splitter = QtWidgets.QSplitter(parent=self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.splitter.setFont(font)
        self.splitter.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.splitter.setOpaqueResize(True)
        self.splitter.setHandleWidth(0)
        self.splitter.setObjectName("splitter")
        self.SideMenu = QtWidgets.QWidget(parent=self.splitter)
        self.SideMenu.setMinimumSize(QtCore.QSize(250, 0))
        self.SideMenu.setMaximumSize(QtCore.QSize(230, 16777215))
        font = QtGui.QFont()
        font.setFamily("Berlin Sans FB Demi")
        font.setPointSize(15)
        self.SideMenu.setFont(font)
        self.SideMenu.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        self.SideMenu.setToolTipDuration(0)
        self.SideMenu.setStyleSheet("QWidget\n"
"{\n"
"background-color: rgb(22, 31, 53);\n"
"color : #fff\n"
"}\n"
"#toolBox {\n"
"    font-weight: bold;\n"
"}\n"
"#toolBox::tab {\n"
"    padding-left:5px;\n"
"    text-align:left;\n"
"    border-radius: 10px;\n"
"}\n"
"#toolBox::tab:selected {\n"
"    background-color: rgb(66, 83, 102);\n"
"    font-weight: bold;\n"
"}\n"
"#toolBox QPushButton {\n"
"    padding:5px 0px 5px 20px;\n"
"    text-align:left;\n"
"    border-radius: 3px;\n"
"}\n"
"#toolBox QPushButton:hover {\n"
"    background-color: rgb(121, 193, 185);\n"
"}\n"
"#toolBox QPushButton:checked {\n"
"    background-color: #3498DB;\n"
"}\n"
"")
        self.SideMenu.setObjectName("SideMenu")
        self.gridLayout = QtWidgets.QGridLayout(self.SideMenu)
        self.gridLayout.setContentsMargins(4, 4, 4, 15)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName("gridLayout")
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Fixed)
        self.gridLayout.addItem(spacerItem, 1, 0, 1, 1)
        self.toolBox = QtWidgets.QToolBox(parent=self.SideMenu)
        font = QtGui.QFont()
        font.setFamily("Berlin Sans FB Demi")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.toolBox.setFont(font)
        self.toolBox.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.toolBox.setObjectName("toolBox")
        self.Menu = QtWidgets.QWidget()
        self.Menu.setGeometry(QtCore.QRect(0, 0, 242, 577))
        self.Menu.setObjectName("Menu")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.Menu)
        self.verticalLayout.setContentsMargins(0, -1, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.PropertyManagementAssistant_Button = QtWidgets.QPushButton(parent=self.Menu)
        font = QtGui.QFont()
        font.setFamily("Arial Black")
        font.setPointSize(8)

        self.PropertyManagementAssistant_Button.setFont(font)
        self.PropertyManagementAssistant_Button.setStyleSheet("QPushButton\n"
"{\n"
"border-radius : 10px;\n"
"padding-left: 20px;\n"
"padding-right: 20px;\n"
"}\n"
"QPushButton:hover {\n"
"    background-color: rgb(79, 74, 134);\n"
"}\n"
"")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("images/icons8-chatbot-30.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.PropertyManagementAssistant_Button.setIcon(icon)
        self.PropertyManagementAssistant_Button.setObjectName("PropertyManagementAssistant_Button")
        self.verticalLayout.addWidget(self.PropertyManagementAssistant_Button)

        self.Database_Button = QtWidgets.QPushButton(parent=self.Menu)
        font = QtGui.QFont()
        font.setFamily("Arial Black")
        font.setPointSize(8)
        self.Database_Button.setFont(font)
        self.Database_Button.setStyleSheet("QPushButton\n"
"{\n"
"border-radius : 10px;\n"
"padding-left: 20px;\n"
"padding-right: 20px;\n"
"}\n"
"QPushButton:hover {\n"
"    background-color: rgb(79, 74, 134);\n"
"}\n"
"")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("images/icons8-database-32.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.Database_Button.setIcon(icon1)
        self.Database_Button.setObjectName("Database_Button")
        self.verticalLayout.addWidget(self.Database_Button)

        self.Analytics_Button = QtWidgets.QPushButton(parent=self.Menu)
        self.Analytics_Button.hide()
        font = QtGui.QFont()
        font.setFamily("Arial Black")
        font.setPointSize(8)
        self.Analytics_Button.setFont(font)
        self.Analytics_Button.setStyleSheet("QPushButton\n"
"{\n"
"border-radius : 10px;\n"
"padding-left: 20px;\n"
"padding-right: 20px;\n"
"}\n"
"QPushButton:hover {\n"
"    background-color: rgb(79, 74, 134);\n"
"}\n"
"")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("images/icons8-analytics-30.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.Analytics_Button.setIcon(icon2)
        self.Analytics_Button.setObjectName("Analytics_Button")
        self.verticalLayout.addWidget(self.Analytics_Button)
        self.Email_Button = QtWidgets.QPushButton(parent=self.Menu)
        font = QtGui.QFont()
        font.setFamily("Arial Black")
        font.setPointSize(8)

        self.Email_Button.setFont(font)
        self.Email_Button.setStyleSheet("QPushButton\n"
"{\n"
"border-radius : 10px;\n"
"padding-left: 20px;\n"
"padding-right: 20px;\n"
"}\n"
"QPushButton:hover {\n"
"    background-color: rgb(79, 74, 134);\n"
"}\n"
"")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("images/icons8-email-30.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.Email_Button.setIcon(icon3)
        self.Email_Button.setObjectName("Email_Button")
        self.verticalLayout.addWidget(self.Email_Button)
        spacerItem1 = QtWidgets.QSpacerItem(20, 365, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.verticalLayout.addItem(spacerItem1)
        icon_menu = QtGui.QIcon()
        icon_menu.addPixmap(QtGui.QPixmap("../../../../.designer/icon/White Icons/icons8-menu-30.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.toolBox.addItem(self.Menu, icon_menu, "")
        self.Help = QtWidgets.QWidget()
        self.Help.setGeometry(QtCore.QRect(0, 0, 242, 577))
        font = QtGui.QFont()
        font.setFamily("Arial Black")
        font.setPointSize(12)
        self.Help.setFont(font)
        self.Help.setObjectName("Help")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.Help)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.verticalLayout_4.addItem(spacerItem2)
        icon_help = QtGui.QIcon()
        icon_help.addPixmap(QtGui.QPixmap("../../../../.designer/icon/White Icons/icons8-help-50.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.toolBox.addItem(self.Help, icon_help, "")
        self.gridLayout.addWidget(self.toolBox, 2, 0, 1, 1)
        self.lsg_logo = QtWidgets.QLabel(parent=self.SideMenu)
        self.lsg_logo.setMinimumSize(QtCore.QSize(0, 100))
        self.lsg_logo.setMaximumSize(QtCore.QSize(1000, 100))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.lsg_logo.setFont(font)
        self.lsg_logo.setStyleSheet("QFrame\n"
"{\n"
"padding-left: 20px;\n"
"padding-right: 20px;\n"
"}\n"
"")
        self.lsg_logo.setText("")
        self.lsg_logo.setPixmap(QtGui.QPixmap("images/company_logo.jpg"))
        self.lsg_logo.setScaledContents(True)
        self.lsg_logo.setWordWrap(False)
        self.lsg_logo.setObjectName("lsg_logo")
        self.gridLayout.addWidget(self.lsg_logo, 0, 0, 1, 1)
        self.layoutWidget = QtWidgets.QWidget(parent=self.splitter)
        self.layoutWidget.setObjectName("layoutWidget")
        self.Main_Screen = QtWidgets.QGridLayout(self.layoutWidget)
        self.Main_Screen.setContentsMargins(0, 0, 0, 0)
        self.Main_Screen.setSpacing(0)
        self.Main_Screen.setObjectName("Main_Screen")
        self.Bottom = QtWidgets.QFrame(parent=self.layoutWidget)
        self.Bottom.setStyleSheet("")
        self.Bottom.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.Bottom.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.Bottom.setObjectName("Bottom")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.Bottom)
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_3.setSpacing(0)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.Main_Window = QtWidgets.QStackedWidget(parent=self.Bottom)
        font = QtGui.QFont()
        font.setPointSize(17)
        self.Main_Window.setFont(font)
        self.Main_Window.setStyleSheet("background-color: rgb(225, 225, 225);")
        self.Main_Window.setObjectName("Main_Window")
        self.AI_Assistant_QWidget = QtWidgets.QWidget()
        self.AI_Assistant_QWidget.setObjectName("AI_Assistant_QWidget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.AI_Assistant_QWidget)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.ChatHistory_QFrame = QtWidgets.QFrame(parent=self.AI_Assistant_QWidget)
        self.ChatHistory_QFrame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.ChatHistory_QFrame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.ChatHistory_QFrame.setObjectName("ChatHistory_QFrame")
        self.gridLayout_6 = QtWidgets.QGridLayout(self.ChatHistory_QFrame)
        self.gridLayout_6.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_6.setSpacing(0)
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.ChatHistory_QtextBrowser = QtWidgets.QTextBrowser(parent=self.ChatHistory_QFrame)
        self.ChatHistory_QtextBrowser.setStyleSheet("/* Crisp Light SaaS */\n"
"QTextBrowser {\n"
"    background-color: #F8FAFC;\n"
"    color: #0F172A;\n"
"    font-family: \'Segoe UI\', system-ui, -apple-system, sans-serif;\n"
"    font-size: 13px;\n"
"    border: 1px solid #CBD5E1;\n"
"    border-radius: 8px;\n"
"    padding: 12px;\n"
"    selection-background-color: #2563EB;\n"
"    selection-color: #FFFFFF;\n"
"}\n"
"QTextBrowser QScrollBar:vertical {\n"
"    background: transparent;\n"
"    width: 6px;\n"
"    margin: 4px 2px 4px 0px;\n"
"}\n"
"QTextBrowser QScrollBar::handle:vertical {\n"
"    background: #CBD5E1;\n"
"    min-height: 25px;\n"
"    border-radius: 3px;\n"
"}\n"
"QTextBrowser QScrollBar::handle:vertical:hover {\n"
"    background: #94A3B8;\n"
"}\n"
"QTextBrowser QScrollBar::add-line:vertical,\n"
"QTextBrowser QScrollBar::sub-line:vertical,\n"
"QTextBrowser QScrollBar::add-page:vertical,\n"
"QTextBrowser QScrollBar::sub-page:vertical {\n"
"    background: none;\n"
"    border: none;\n"
"    height: 0px;\n"
"}")
        self.ChatHistory_QtextBrowser.setOpenExternalLinks(True)
        self.ChatHistory_QtextBrowser.setObjectName("ChatHistory_QtextBrowser")
        self.gridLayout_6.addWidget(self.ChatHistory_QtextBrowser, 0, 0, 1, 1)
        self.gridLayout_2.addWidget(self.ChatHistory_QFrame, 0, 0, 1, 1)
        self.Chat_QFrame = QtWidgets.QFrame(parent=self.AI_Assistant_QWidget)
        self.Chat_QFrame.setMinimumSize(QtCore.QSize(0, 0))
        self.Chat_QFrame.setStyleSheet("QFrame {\n"
"    background-color: #FFFFFF;\n"
"    border-radius: 6px;\n"
"}")
        self.Chat_QFrame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.Chat_QFrame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.Chat_QFrame.setObjectName("Chat_QFrame")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.Chat_QFrame)
        self.gridLayout_4.setContentsMargins(6, 6, 6, 6)
        self.gridLayout_4.setSpacing(5)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.Chat_QtextBrowser = QtWidgets.QLineEdit(parent=self.Chat_QFrame)
        self.Chat_QtextBrowser.setMinimumSize(QtCore.QSize(0, 60))
        self.Chat_QtextBrowser.setStyleSheet("QLineEdit {\n"
"    background-color: #FFFFFF;\n"
"    color: #0F172A;\n"
"    font-family: \'Segoe UI\', system-ui, -apple-system, sans-serif;\n"
"    font-size: 13px;\n"
"    border-radius: 6px;\n"
"    padding: 9px 12px;\n"
"    selection-background-color: #2563EB;\n"
"    selection-color: #FFFFFF;\n"
"}\n"
"QLineEdit:hover {\n"
"    border-color: #94A3B8;\n"
"}\n"
"QLineEdit:focus {\n"
"    background-color: #FFFFFF;\n"
"}\n"
"QLineEdit:disabled {\n"
"    background-color: #F1F5F9;\n"
"    color: #94A3B8;\n"
"    border-color: #E2E8F0;\n"
"}")
        self.Chat_QtextBrowser.setObjectName("Chat_QtextBrowser")
        self.gridLayout_4.addWidget(self.Chat_QtextBrowser, 0, 0, 1, 1)
        self.Send_Button = QtWidgets.QPushButton(parent=self.Chat_QFrame)
        self.Send_Button.setMinimumSize(QtCore.QSize(0, 60))
        self.Send_Button.setStyleSheet("QPushButton {\n"
"    background-color: #3B82F6;\n"
"    color: #FFFFFF;\n"
"    font-family: \'Segoe UI\', system-ui, -apple-system, sans-serif;\n"
"    font-size: 13px;\n"
"    font-weight: 600;\n"
"    border: none;\n"
"    border-radius: 6px;\n"
"    padding: 9px 18px;\n"
"}\n"
"QPushButton:hover {\n"
"    background-color: #2563EB;\n"
"}\n"
"QPushButton:pressed {\n"
"    background-color: #1D4ED8;\n"
"    padding-top: 10px;\n"
"    padding-bottom: 8px;\n"
"}\n"
"QPushButton:disabled {\n"
"    background-color: #4A5568;\n"
"    color: #A0AEC0;\n"
"}")
        self.Send_Button.setObjectName("pushButton")
        self.gridLayout_4.addWidget(self.Send_Button, 0, 1, 1, 1)
        self.gridLayout_2.addWidget(self.Chat_QFrame, 1, 0, 1, 1)
        self.Main_Window.addWidget(self.AI_Assistant_QWidget)


        self.Database_QWidget = QtWidgets.QWidget()
        self.Database_QWidget.setObjectName("Database_QWidget")
        self.gridLayout_7 = QtWidgets.QGridLayout(self.Database_QWidget)
        self.gridLayout_7.setObjectName("gridLayout_7")
        self.tableView = QtWidgets.QTableView(parent=self.Database_QWidget)
        self.tableView.setStyleSheet("QTableView {\n"
"    background-color: #FFFFFF;\n"
"    alternate-background-color: #F8FAFC;\n"
"    color: #0F172A;\n"
"    font-family: 'Segoe UI', system-ui, sans-serif;\n"
"    font-size: 13px;\n"
"    border: 1px solid #CBD5E1;\n"
"    border-radius: 8px;\n"
"    gridline-color: #F1F5F9;\n"
"    selection-background-color: #EFF6FF;\n"
"    selection-color: #1E40AF;\n"
"    outline: none;\n"
"}\n"
"QTableView::item {\n"
"    padding: 8px 12px;\n"
"    border: none;\n"
"}\n"
"QTableView::item:hover {\n"
"    background-color: #F1F5F9;\n"
"}\n"
"QTableView::item:selected {\n"
"    background-color: #DBEAFE;\n"
"    color: #1E3A8A;\n"
"    font-weight: 600;\n"
"}\n"
"QHeaderView::section {\n"
"    background-color: #F8FAFC;\n"
"    color: #475569;\n"
"    font-size: 11px;\n"
"    font-weight: 700;\n"
"    text-transform: uppercase;\n"
"    border: none;\n"
"    border-bottom: 2px solid #E2E8F0;\n"
"    border-right: 1px solid #F1F5F9;\n"
"    padding: 10px 12px;\n"
"}\n"
"QHeaderView::section:vertical {\n"
"    background-color: #FFFFFF;\n"
"    color: #94A3B8;\n"
"    border-right: 1px solid #E2E8F0;\n"
"    border-bottom: none;\n"
"    padding: 0px 8px;\n"
"}\n"
"QTableCornerButton::section {\n"
"    background-color: #F8FAFC;\n"
"    border: none;\n"
"    border-bottom: 2px solid #E2E8F0;\n"
"    border-right: 1px solid #E2E8F0;\n"
"}\n"
"QTableView QScrollBar:vertical {\n"
"    background: transparent;\n"
"    width: 6px;\n"
"    margin: 4px 2px 4px 0px;\n"
"}\n"
"QTableView QScrollBar::handle:vertical {\n"
"    background: #CBD5E1;\n"
"    min-height: 25px;\n"
"    border-radius: 3px;\n"
"}\n"
"QTableView QScrollBar::handle:vertical:hover {\n"
"    background: #94A3B8;\n"
"}\n"
"QTableView QScrollBar::add-line:vertical,\n"
"QTableView QScrollBar::sub-line:vertical,\n"
"QTableView QScrollBar::add-page:vertical,\n"
"QTableView QScrollBar::sub-page:vertical {\n"
"    background: none;\n"
"    border: none;\n"
"    height: 0px;\n"
"}\n"
"QTableView QScrollBar:horizontal {\n"
"    background: transparent;\n"
"    height: 6px;\n"
"    margin: 0px 4px 2px 4px;\n"
"}\n"
"QTableView QScrollBar::handle:horizontal {\n"
"    background: #CBD5E1;\n"
"    min-width: 25px;\n"
"    border-radius: 3px;\n"
"}\n"
"QTableView QScrollBar::add-line:horizontal,\n"
"QTableView QScrollBar::sub-line:horizontal {\n"
"    background: none;\n"
"    border: none;\n"
"    width: 0px;\n"
"}")
        self.tableView.setObjectName("tableView")
        self.gridLayout_7.addWidget(self.tableView, 0, 0, 1, 1)

        # Bottom-right button action bar
        self.db_action_layout = QtWidgets.QHBoxLayout()
        self.db_action_layout.setObjectName("db_action_layout")
        
        # Spacer pushes the button flush to the right
        self.db_spacer = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.db_action_layout.addItem(self.db_spacer)

        self.btn_connect_db = QtWidgets.QPushButton(parent=self.Database_QWidget)
        self.btn_connect_db.setObjectName("btn_connect_db")
        self.btn_connect_db.setText("Connect to Database")
        self.btn_connect_db.setStyleSheet("""
            QPushButton#btn_connect_db {
                background-color: #2563EB;
                color: #FFFFFF;
                font-family: 'Segoe UI', system-ui, sans-serif;
                font-size: 13px;
                font-weight: 600;
                padding: 8px 16px;
                border: none;
                border-radius: 6px;
            }
            QPushButton#btn_connect_db:hover {
                background-color: #1D4ED8;
            }
            QPushButton#btn_connect_db:pressed {
                background-color: #1E40AF;
            }
            QPushButton#btn_connect_db:disabled {
                background-color: #94A3B8;
                color: #E2E8F0;
            }
        """)
        self.db_action_layout.addWidget(self.btn_connect_db)
        
        # Add the action layout below the table in gridLayout_7
        self.gridLayout_7.addLayout(self.db_action_layout, 1, 0, 1, 1)

        self.Main_Window.addWidget(self.Database_QWidget)




        self.Analytics_QWidget = QtWidgets.QWidget()
        self.Analytics_QWidget.setObjectName("Analytics_QWidget")
        self.gridLayout_8 = QtWidgets.QGridLayout(self.Analytics_QWidget)
        self.gridLayout_8.setObjectName("gridLayout_8")
        self.Analytics_WebEngineView = QWebEngineView(parent=self.Analytics_QWidget)
        self.Analytics_WebEngineView.setObjectName("Analytics_WebEngineView")
        self.Analytics_WebEngineView.load(QUrl("https://www.google.com"))
        self.gridLayout_8.addWidget(self.Analytics_WebEngineView, 0, 0, 1, 1)
        self.Main_Window.addWidget(self.Analytics_QWidget)
        self.Email_QWidget = QtWidgets.QWidget()
        self.Email_QWidget.setObjectName("Email_QWidget")
        self.gridLayout_9 = QtWidgets.QGridLayout(self.Email_QWidget)
        self.gridLayout_9.setObjectName("gridLayout_9")
        nav_layout = QHBoxLayout()
        self.btn_back = QPushButton("◀ Back", parent=self.Email_QWidget)
        self.btn_forward = QPushButton("Forward ▶", parent=self.Email_QWidget)
        nav_layout.addWidget(self.btn_back)
        nav_layout.addWidget(self.btn_forward)
        nav_layout.addStretch()
        self.Email_WebEngineView = QWebEngineView(parent=self.Email_QWidget)
        self.Email_WebEngineView.setObjectName("Email_WebEngineView")
        self.custom_page = CustomWebEnginePage(self.Email_WebEngineView)
        self.Email_WebEngineView.setPage(self.custom_page)
        self.btn_back.clicked.connect(self.Email_WebEngineView.back)
        self.btn_forward.clicked.connect(self.Email_WebEngineView.forward)
        page = self.Email_WebEngineView.page()
        page.action(QWebEnginePage.WebAction.Back).changed.connect(
            lambda: self.btn_back.setEnabled(
                page.action(QWebEnginePage.WebAction.Back).isEnabled()
            )
        )
        page.action(QWebEnginePage.WebAction.Forward).changed.connect(
            lambda: self.btn_forward.setEnabled(
                page.action(QWebEnginePage.WebAction.Forward).isEnabled()
            )
        )
        self.btn_back.setEnabled(False)
        self.btn_forward.setEnabled(False)
        self.gridLayout_9.addLayout(nav_layout, 0, 0, 1, 1)
        self.gridLayout_9.addWidget(self.Email_WebEngineView, 1, 0, 1, 1)
        self.Email_WebEngineView.load(QUrl("https://www.gmail.com"))

        self.Main_Window.addWidget(self.Email_QWidget)
        self.gridLayout_3.addWidget(self.Main_Window, 1, 0, 1, 1)
        self.Main_Screen.addWidget(self.Bottom, 0, 0, 1, 1)
        self.gridLayout_5.addWidget(self.splitter, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        self.toolBox.setCurrentIndex(0)
        self.toolBox.layout().setSpacing(0)
        self.Main_Window.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        MainWindow.setTabOrder(self.Database_Button, self.PropertyManagementAssistant_Button)
        MainWindow.setTabOrder(self.PropertyManagementAssistant_Button, self.Analytics_Button)

        #################################################
        # BUTTON CONNECTIONS
        #################################################
        self.PropertyManagementAssistant_Button.clicked.connect(lambda: self.Main_Window.setCurrentWidget(self.AI_Assistant_QWidget))
        self.Database_Button.clicked.connect(lambda: self.Main_Window.setCurrentWidget(self.Database_QWidget))
        self.Email_Button.clicked.connect(lambda: self.Main_Window.setCurrentWidget(self.Email_QWidget))
        self.Analytics_Button.clicked.connect(lambda: self.Main_Window.setCurrentWidget(self.Analytics_QWidget))
        self.btn_connect_db.clicked.connect(lambda:database2.btn_connect_db_button_clicked(self,self))


        self.Send_Button.clicked.connect(self.send_query)
        self.Chat_QtextBrowser.returnPressed.connect(self.send_query)

    #Function for sending a query
    def send_query(self):
        # Support both QLineEdit (.text) and QTextEdit/QTextBrowser (.toPlainText)
        if hasattr(self.Chat_QtextBrowser, "toPlainText"):
            query = self.Chat_QtextBrowser.toPlainText().strip()
        else:
            query = self.Chat_QtextBrowser.text().strip()

        if not query:
            return

        # Display user query
        self.ChatHistory_QtextBrowser.append(f"<b>You:</b> {query}")
        self.Chat_QtextBrowser.clear()
        self.Send_Button.setEnabled(False)

        # Append temporary status
        self.ChatHistory_QtextBrowser.append("<i>Assistant is thinking...</i>")

        # Launch background runner thread
        self.worker = AgentWorker(query)
        self.worker.finished.connect(self.handle_agent_response)
        self.worker.start()

    #Function for displaying the output from the agent
    def handle_agent_response(self, response: str):
        # Remove the "Assistant is thinking..." line
        cursor = self.ChatHistory_QtextBrowser.textCursor()
        cursor.movePosition(cursor.MoveOperation.End)
        cursor.select(cursor.SelectionType.BlockUnderCursor)
        cursor.removeSelectedText()
        cursor.deletePreviousChar()  # Cleans up the newline

        # Append actual assistant response
        self.ChatHistory_QtextBrowser.append(f"<b>Assistant:</b> {response}\n")
        self.Send_Button.setEnabled(True)


    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "SatteliteInc"))
        self.PropertyManagementAssistant_Button.setText(_translate("MainWindow", "Sattelite Assistant"))
        self.Database_Button.setText(_translate("MainWindow", "Database"))
        self.Analytics_Button.setText(_translate("MainWindow", "Analytics"))
        self.Email_Button.setText(_translate("MainWindow", "Google Email"))
        self.toolBox.setItemText(self.toolBox.indexOf(self.Menu), _translate("MainWindow", "Menu"))
        self.toolBox.setItemText(self.toolBox.indexOf(self.Help), _translate("MainWindow", "Help"))
        self.ChatHistory_QtextBrowser.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Segoe UI,system-ui,-apple-system,sans-serif\'; font-size:13px; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
        self.Chat_QtextBrowser.setPlaceholderText(_translate("MainWindow", "Ask Sattelite Assistant"))
        self.Send_Button.setText(_translate("MainWindow", "Send"))


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())