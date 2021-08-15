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

# IMPORT PACKAGES AND MODULES
# ///////////////////////////////////////////////////////////////
from gui.uis.windows.main_window.functions_main_window import *
import sys
import os
import time
import queue
import json
import uuid

# IMPORT QT CORE
# ///////////////////////////////////////////////////////////////
from qt_core import *

# IMPORT SETTINGS
# ///////////////////////////////////////////////////////////////
from gui.core.json_settings import Settings

# IMPORT PY ONE DARK WINDOWS
# ///////////////////////////////////////////////////////////////
# MAIN WINDOW
from gui.uis.windows.main_window import *

# IMPORT PY ONE DARK WIDGETS
# ///////////////////////////////////////////////////////////////
from gui.widgets import *

# modules
from modules.sub_thread import *
import paho.mqtt.client as mqtt

# ADJUST QT FONT DPI FOR HIGHT SCALE AN 4K MONITOR
# ///////////////////////////////////////////////////////////////
os.environ["QT_FONT_DPI"] = "96"
# IF IS 4K MONITOR ENABLE 'os.environ["QT_SCALE_FACTOR"] = "2"'

server_ip = '159.75.74.72'

# MAIN WINDOW
# ///////////////////////////////////////////////////////////////
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # SETUP MAIN WINDOw
        # Load widgets from "gui\uis\main_window\ui_main.py"
        # ///////////////////////////////////////////////////////////////
        self.ui = UI_MainWindow()
        self.ui.setup_ui(self)

        # LOAD SETTINGS
        # ///////////////////////////////////////////////////////////////
        settings = Settings()
        self.settings = settings.items

        # sub thread init
        self.mqtt_thread_init()

        # SETUP MAIN WINDOW
        # ///////////////////////////////////////////////////////////////
        self.hide_grips = True # Show/Hide resize grips
        SetupMainWindow.setup_gui(self)

        # SHOW MAIN WINDOW
        # ///////////////////////////////////////////////////////////////
        self.show()

    # LEFT MENU BTN IS CLICKED
    # Run function when btn is clicked
    # Check funtion by object name / btn_id
    # ///////////////////////////////////////////////////////////////
    def btn_clicked(self):
        # GET BT CLICKED
        btn = SetupMainWindow.setup_btns(self)

        # Remove Selection If Clicked By "btn_close_left_column"
        if btn.objectName() != "btn_settings":
            self.ui.left_menu.deselect_all_tab()

        # Get Title Bar Btn And Reset Active         
        top_settings = MainFunctions.get_title_bar_btn(self, "btn_top_settings")
        top_settings.set_active(False)

        # LEFT MENU
        # ///////////////////////////////////////////////////////////////
        
        # HOME BTN
        if btn.objectName() == "btn_home":
            # Select Menu
            self.ui.left_menu.select_only_one(btn.objectName())

            # Load Page 1
            MainFunctions.set_page(self, self.ui.load_pages.page_1)

        # WIDGETS BTN
        if btn.objectName() == "btn_widgets":
            # Select Menu
            self.ui.left_menu.select_only_one(btn.objectName())

            # Load Page 2
            MainFunctions.set_page(self, self.ui.load_pages.page_2)

        # LOAD USER PAGE
        if btn.objectName() == "btn_add_user":
            # Select Menu
            self.ui.left_menu.select_only_one(btn.objectName())

            # Load Page 3 
            MainFunctions.set_page(self, self.ui.load_pages.page_3)

        # BOTTOM INFORMATION
        if btn.objectName() == "btn_info":
            # CHECK IF LEFT COLUMN IS VISIBLE
            if not MainFunctions.left_column_is_visible(self):
                self.ui.left_menu.select_only_one_tab(btn.objectName())

                # Show / Hide
                MainFunctions.toggle_left_column(self)
                self.ui.left_menu.select_only_one_tab(btn.objectName())
            else:
                if btn.objectName() == "btn_close_left_column":
                    self.ui.left_menu.deselect_all_tab()
                    # Show / Hide
                    MainFunctions.toggle_left_column(self)
                
                self.ui.left_menu.select_only_one_tab(btn.objectName())

            # Change Left Column Menu
            if btn.objectName() != "btn_close_left_column":
                MainFunctions.set_left_column_menu(
                    self, 
                    menu = self.ui.left_column.menus.menu_2,
                    title = "Info tab",
                    icon_path = Functions.set_svg_icon("icon_info.svg")
                )

        # SETTINGS LEFT
        if btn.objectName() == "btn_settings" or btn.objectName() == "btn_close_left_column":
            # CHECK IF LEFT COLUMN IS VISIBLE
            if not MainFunctions.left_column_is_visible(self):
                # Show / Hide
                MainFunctions.toggle_left_column(self)
                self.ui.left_menu.select_only_one_tab(btn.objectName())
            else:
                if btn.objectName() == "btn_close_left_column":
                    self.ui.left_menu.deselect_all_tab()
                    # Show / Hide
                    MainFunctions.toggle_left_column(self)
                self.ui.left_menu.select_only_one_tab(btn.objectName())

            # Change Left Column Menu
            if btn.objectName() != "btn_close_left_column":
                MainFunctions.set_left_column_menu(
                    self, 
                    menu = self.ui.left_column.menus.menu_1,
                    title = "Settings Left Column",
                    icon_path = Functions.set_svg_icon("icon_settings.svg")
                )
        
        # TITLE BAR MENU
        # ///////////////////////////////////////////////////////////////
        
        # SETTINGS TITLE BAR
        if btn.objectName() == "btn_top_settings":
            # Toogle Active
            if not MainFunctions.right_column_is_visible(self):
                btn.set_active(True)

                # Show / Hide
                MainFunctions.toggle_right_column(self)
            else:
                btn.set_active(False)

                # Show / Hide
                MainFunctions.toggle_right_column(self)

            # Get Left Menu Btn            
            top_settings = MainFunctions.get_left_menu_btn(self, "btn_settings")
            top_settings.set_active_tab(False)            

        # DEBUG
        print(f"Button {btn.objectName()}, clicked!")

    # LEFT MENU BTN IS RELEASED
    # Run function when btn is released
    # Check funtion by object name / btn_id
    # ///////////////////////////////////////////////////////////////
    def btn_released(self):
        # GET BT CLICKED
        btn = SetupMainWindow.setup_btns(self)

        # DEBUG
        print(f"Button {btn.objectName()}, released!")

    # RESIZE EVENT
    # ///////////////////////////////////////////////////////////////
    def resizeEvent(self, event):
        SetupMainWindow.resize_grips(self)

    # MOUSE CLICK EVENTS
    # ///////////////////////////////////////////////////////////////
    def mousePressEvent(self, event):
        # SET DRAG POS WINDOW
        self.dragPos = event.globalPos()

    # mqtt clear
    def mqtt_msg_clear(self):
        self.ui.load_pages.txb_mqtt.setText('')

    # mqtt send
    def mqtt_send(self):
        if self.mqtt_state:
            msg = {'user':self.le_name.text(), 'content':self.le_send_text.text(), 'target':'null', 'uuid':self.uuid}
            self.client.publish('mchat', payload=json.dumps(msg), qos=0) 
            self.le_send_text.setText('')
        else:
            self.ui.load_pages.txb_mqtt.append('mqtt disconnect, send fail')
            self.ui.load_pages.txb_mqtt.moveCursor(self.ui.load_pages.txb_mqtt.textCursor().End)  #文本框显示到底部

        # msg = {'usr':'timo', 'content':'hello', 'target':'null', 'uuid':self.uuid}
        # self.ui.load_pages.txb_mqtt.append('test')
        # self.ui.load_pages.txb_mqtt.moveCursor(self.ui.load_pages.txb_mqtt.textCursor().End)  #文本框显示到底部

    # sub thread init
    def mqtt_thread_init(self):
        self.uuid = get_mac_address()
        self.mqtt_state = False
        self.ui_to_mqtt_q = queue.Queue()
        thread_run(self.mqtt_run_func)
        post = {'msg':'client init'}
        self.ui_to_mqtt_q.put(post)

    # mqtt run func:
    def mqtt_run_func(self):
        while True:
            time.sleep(0.1)

            while not self.ui_to_mqtt_q.empty():
                recv = self.ui_to_mqtt_q.get()
                if recv['msg'] == 'client init':
                    self.mqtt_client_init()

    def mqtt_client_init(self):
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.connect(server_ip, 1883, 60) # 600为keepalive的时间间隔
        self.client.subscribe('mchat', qos=0)
        self.client.loop_start()

    def on_connect(self, client, userdata, flags, rc):
        print("Connected with result code: " + str(rc))
        if rc == 0:
            self.mqtt_state = True
            self.icon_2 = QIcon(Functions.set_svg_icon("icon_online.svg"))
            self.btn_name.setIcon(self.icon_2)
            self.ui.load_pages.txb_mqtt.append('mqtt server:'+server_ip+'connect sucess')
        else:
            self.mqtt_state = False
            self.icon_2 = QIcon(Functions.set_svg_icon("icon_close.svg"))
            self.btn_name.setIcon(self.icon_2)
            self.ui.load_pages.txb_mqtt.append('mqtt server:'+server_ip+' connect fail')


    def on_message(self, client, userdata, msg):
        print(msg.topic + " " + str(msg.payload))
        try:
            msg_dict = eval(msg.payload)
            # 判断方向
            head = '->recv:'
            if msg_dict['uuid'] == self.uuid:
                head = '<-send:'

            self.ui.load_pages.txb_mqtt.append(head + '<'+msg_dict['user']+'>'+ '['+str(msg.timestamp)+']'+msg_dict['content'])
            self.ui.load_pages.txb_mqtt.moveCursor(self.ui.load_pages.txb_mqtt.textCursor().End)  #文本框显示到底部
            # print(type(msg.timestamp))
            # timeArray = time.localtime(int(msg.timestamp))
            # otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
            # print(otherStyleTime)
            
        except Exception as e:
            print(e)
    
    def keyPressEvent(self, QKeyEvent):  # 键盘某个键被按下时调用
        #参数1  控件
        if QKeyEvent.key()== Qt.Key_Enter or QKeyEvent.key()== Qt.Key_Return: 
            if self.ui.load_pages.pages.currentIndex() == 2:
                self.mqtt_send()

def get_mac_address(): 
    mac=uuid.UUID(int = uuid.getnode()).hex[-12:] 
    return ":".join([mac[e:e+2] for e in range(0,11,2)])

# SETTINGS WHEN TO START
# Set the initial class and also additional parameters of the "QApplication" class
# ///////////////////////////////////////////////////////////////
if __name__ == "__main__":
    # APPLICATION
    # ///////////////////////////////////////////////////////////////
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("icon.ico"))
    window = MainWindow()

    # EXEC APP
    # ///////////////////////////////////////////////////////////////
    sys.exit(app.exec())