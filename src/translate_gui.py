from PyQt5.QtWidgets import * 
from PyQt5 import QtCore, QtGui 
from PyQt5.QtGui import * 
from PyQt5.QtCore import *
import math,sys,os,glob,time
#from translate import translate

from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from time import sleep
import concurrent.futures

import configparser


class translate():

    def __init__(self, text, box):
        self.text = text
        self.driver_path = 'C:\\Program Files\\chromedriver_win32\\chromedriver.exe'
        self.Box = box
        self.result = ['']*4
        self.max_workers = 2 

        self.set_options()

    def read_config(self):
        # 
        # get config setting
        #
        dpath = os.path.dirname(sys.argv[0])
        CONFIG_PATH = dpath + '/config.ini'

        config_ini = configparser.ConfigParser()
        config_ini.read(CONFIG_PATH, encoding='utf-8')

        self.driver_path = config_ini.get('DEFAULT', 'Driver_path')
        self.max_workers = int(config_ini.get('DEFAULT', 'Max_Core'))

        # google 
        self.google_xpath1 = config_ini.get('Google', 'English_choice')
        self.google_xpath2 = config_ini.get('Google', 'Text_Box')
        self.google_xpath3 = config_ini.get('Google', 'Text_Out')

        # DeepL
        self.deepl_xpath1 = config_ini.get('DeepL', 'Text_Box')
        self.deepl_xpath2 = config_ini.get('DeepL', 'Finish_Btn')
        self.deepl_xpath3 = config_ini.get('DeepL', 'Text_Out')

        # エキサイト
        self.excite_xpath1 = config_ini.get('Excite', 'English_choice')
        self.excite_xpath2 = config_ini.get('Excite', 'Text_Box')
        self.excite_xpath3 = config_ini.get('Excite', 'Run_Btn')
        self.excite_xpath4 = config_ini.get('Excite', 'Text_Out')

        # Weblio
        self.weblio_xpath1 = config_ini.get('Weblio', 'Text_Box')
        self.weblio_xpath2 = config_ini.get('Weblio', 'Run_Btn')
        self.weblio_xpath3 = config_ini.get('Weblio', 'Text_Out')


    def set_options(self):
        # chromedriver settings

        self.options = Options()
        self.options.add_argument('--headless')

        self.options.add_argument('--disable-gpu')
        # エラーの許容
        self.options.add_argument('--ignore-certificate-errors')
        self.options.add_argument('--allow-running-insecure-content')
        self.options.add_argument('--disable-web-security')
        # headlessでは不要そうな機能
        self.options.add_argument('--disable-desktop-notifications')
        self.options.add_argument("--disable-extensions")
        # UA
        self.options.add_argument('--user-agent=hogehoge')
        # 画像を読み込まないで軽くする
        self.options.add_argument('--blink-settings=imagesEnabled=false')
        self.options.add_argument('--single-process')
        self.options.add_argument('--disable-application-cache')
        self.options.add_argument('--start-maximized')

    def driverfunc1(self, text):
        # ===================================
        #
        #  Google 翻訳
        #
        # ===================================

        driver = webdriver.Chrome(executable_path = self.driver_path, options=self.options)
        driver.get('https://translate.google.com/?source=gtx')
        
        # 英語を選択
        elem_1 = WebDriverWait(driver,10).until(
            EC.presence_of_element_located((By.XPATH, self.google_xpath1))
        )
        elem_1.click()

        # 英語を入力
        elem_2 = WebDriverWait(driver,5).until(
            EC.presence_of_element_located((By.XPATH, self.google_xpath2))
        )
        elem_2.send_keys(self.text)

        # 翻訳を獲得
        elem_3 = WebDriverWait(driver,25).until(
            EC.presence_of_element_located((By.XPATH, self.google_xpath3))
        )
        trans_text = elem_3.text
        
        #print( "\n+++++++++++++++++++++++++++++++++++++++++++++++++++")
        #print('Google Translate \n\n' + trans_text)

        self.result[0] += trans_text
        sleep(0.3)
        driver.close()
        driver.quit()

    def driverfunc2(self, text):
        # ===================================
        #
        #  DeepL
        #
        # ===================================

        driver = webdriver.Chrome(executable_path = self.driver_path)#, options=self.options)
        
        #driver = webdriver.Chrome(executable_path = self.driver_path)
        driver.get('https://www.deepl.com/ja/translator')
        
        # 英語を入力
        elem_1 = WebDriverWait(driver,15).until(
            EC.presence_of_element_located((By.XPATH, self.deepl_xpath1))
        )
        elem_1.send_keys(self.text)
        
        # 翻訳を獲得
        sleep(0.5)
        WebDriverWait(driver,25).until(
            EC.element_to_be_clickable((By.XPATH, self.deepl_xpath2))
        )
        
        sleep(0.5)
        trans_text = driver.find_element_by_xpath(self.deepl_xpath3).get_attribute("textContent")
        
        #print( "+++++++++++++++++++++++++++++++++++++++++++++++++++")
        #print('DeepL \n\n' + trans_text)
        
        self.result[1] += trans_text
        sleep(0.3)
        driver.close()
        driver.quit()

    def driverfunc3(self, text):
        # ===================================
        #
        #  エキサイト翻訳
        #
        # ===================================

        driver = webdriver.Chrome(executable_path = self.driver_path, options=self.options)
        driver.get('https://www.excite.co.jp/world/english/')
        
        # 英語を選択
        elem_1 = WebDriverWait(driver,10).until(
            EC.presence_of_element_located((By.XPATH, self.excite_xpath1))
        )
        elem_1.click()

        # 英語を入力
        elem_2 = WebDriverWait(driver,2).until(
            EC.presence_of_element_located((By.XPATH, self.excite_xpath2))
        )
        elem_2.send_keys(self.text)

        # 翻訳を実行
        elem_3 = WebDriverWait(driver,5).until(
            EC.presence_of_element_located((By.XPATH, self.excite_xpath3))
        )
        elem_3.click()

        # 翻訳を獲得
        elem_4 = WebDriverWait(driver,25).until(
            EC.presence_of_element_located((By.XPATH, self.excite_xpath4))
        )
        trans_text = elem_4.text
        #print( "+++++++++++++++++++++++++++++++++++++++++++++++++++")
        #print('エキサイト Translate \n\n' + trans_text)
        
        self.result[2] += trans_text
        sleep(0.3)
        driver.close()
        driver.quit()

    def driverfunc4(self, text):
        # ===================================
        #
        #  Weblio 翻訳
        #
        # ===================================

        driver = webdriver.Chrome(executable_path = self.driver_path, options=self.options)
        driver.get('https://translate.weblio.jp/')
        
        # 英語を入力
        elem_1 = WebDriverWait(driver,2).until(
            EC.presence_of_element_located((By.XPATH, self.weblio_xpath1))
        )
        elem_1.send_keys(self.text)

        # 翻訳を実行
        driver.execute_script("window.scrollTo(20 ,document.body.scrollHeight)")
        elem_2 = WebDriverWait(driver,30).until(
            EC.presence_of_element_located((By.XPATH, self.weblio_xpath2))
        )
        elem_2.click()

        # 翻訳を獲得
        elem_3 = WebDriverWait(driver,20).until(
            EC.presence_of_element_located((By.XPATH, self.weblio_xpath3))
        )
        trans_text = elem_3.text
        
        #print( "\n+++++++++++++++++++++++++++++++++++++++++++++++++++")
        #print('Weblio Translate \n\n' + trans_text)
        #print( "\n+++++++++++++++++++++++++++++++++++++++++++++++++++")
        
        self.result[3] += trans_text
        sleep(0.3)
        driver.close()
        driver.quit()


    def Run(self):
        # 並列実行するexecutorを用意する。
        # max_workers が最大の並列実行数
        # 並列処理
        text = self.text

        with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_workers) as self.executor:
            for i in range(4):
                if self.Box[i] == False:
                    continue 
                elif i == 0:
                    self.executor.submit(self.driverfunc1, text)
                elif i == 1:
                    self.executor.submit(self.driverfunc2, text)
                elif i == 2:
                    self.executor.submit(self.driverfunc3, text)
                else:
                    self.executor.submit(self.driverfunc4, text)

    def output(self):
        ls = ['Google Translate','DeepL','エキサイト Translate','Weblio Translate']

        for trans_text, l, check in zip(self.result, ls, self.Box):
            if check:
                print( "\n+++++++++++++++++++++++++++++++++++++++++++++++++++")
                print(l +'\n\n' + trans_text)            
        print( "\n+++++++++++++++++++++++++++++++++++++++++++++++++++")

    def return_para(self):
        return self.result


# =====================================
#
# 以下GUIアプリ
#
# =====================================


class App(QWidget):

    def __init__(self, parent=None):
        super().__init__()

        self.initUI()

    def resource_path(self, relative_path):
        if getattr(sys, 'frozen', False): 
            base_path = sys._MEIPASS
        else:
            base_path = os.path.abspath(".")
        return os.path.join(base_path, relative_path)

    # UI settings
    def initUI(self):
        self.resize(450, 350)
        self.move(300, 100) 

        self.widget_layout()

        filename = self.resource_path(os.path.join('trans.ico'))
        icon = QIcon(filename)
        icon.addPixmap(QtGui.QPixmap(filename), QtGui.QIcon.Normal, QtGui.QIcon.Off)

        self.setWindowIcon(icon)
        
        self.setWindowTitle('Translate')
        self.show()


    def widget_layout(self):
        font_j = QtGui.QFont()
        font_j.Bold
        font_j.setPointSize(10)

        text = QLabel(' 使用する翻訳サイトを選んでください ')
        text.setFont(font_j)

        self.cb_1 = QCheckBox(' Google 翻訳 ')
        self.cb_2 = QCheckBox(' DeepL ')
        self.cb_3 = QCheckBox(' エキサイト 翻訳 ')
        self.cb_4 = QCheckBox(' Weblio 翻訳 ')
        
        self.cb_1.setFont(font_j)
        self.cb_2.setFont(font_j)
        self.cb_3.setFont(font_j)
        self.cb_4.setFont(font_j)

        self.cb_1.toggle()
        self.cb_2.toggle()
        self.cb_3.toggle()
        self.cb_4.toggle()

        Btn = QPushButton("&実行")
        Btn.setFont(font_j)
        Btn.clicked.connect(self.make_sub)

        # Setting layout
        layout = QGridLayout()
        layout.setSpacing(15)

        # ラベルの位置設定
        layout.addWidget(text, 1, 0)

        layout.addWidget(self.cb_1, 2, 0)
        layout.addWidget(self.cb_2, 3, 0)
        layout.addWidget(self.cb_3, 4, 0)
        layout.addWidget(self.cb_4, 5, 0)

        layout.addWidget(Btn, 6, 0)
        self.setLayout(layout)

    def make_sub(self):
        # チェックボックスの反映
        Box = [False]*4
        if self.cb_1.checkState(): Box[0] = True
        if self.cb_2.checkState(): Box[1] = True
        if self.cb_3.checkState(): Box[2] = True
        if self.cb_4.checkState(): Box[3] = True
        
        #print(Box)
        self.subwindow = SubApp(self)
        self.subwindow.get_data(Box)
        self.subwindow.show()
        self.close()



class SubApp(QWidget):

    def __init__(self, parent=None):
        super().__init__()

        self.initUI()
        QApplication.setAttribute(Qt.AA_DisableHighDpiScaling, True) 

    def resource_path(self, relative_path):
        if getattr(sys, 'frozen', False): 
            base_path = sys._MEIPASS
        else:
            base_path = os.path.abspath(".")
        return os.path.join(base_path, relative_path)


    def initUI(self):
        self.resize(550, 500)
        self.move(300, 100)
        
        filename = self.resource_path(os.path.join('trans.ico'))
        icon = QIcon()
        icon.addPixmap(QPixmap(filename), QIcon.Normal)
        self.setWindowIcon(icon)
        
    def get_data(self, Box):
        self.Box = Box
        self.n = sum(Box)
        #print(Box)

        self.widget_layout()
        self.setWindowTitle('Translate')
        self.show()

    def widget_layout(self):
        font_e = QtGui.QFont()
        font_e.setFamily("BatangChe")
        font_e.setPointSize(10)

        font_j = QtGui.QFont()
        #font_j.setFamily("游ゴシック")
        font_j.Bold
        font_j.setPointSize(10)

        text_1 = QLabel(' 英文を入力 ')
        text_1.setFont(font_j)

        self.lineEdit_1 = QTextEdit()
        self.lineEdit_1.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.lineEdit_1.setStyleSheet("""QPlainTextEdit {background-color: rgb(255, 255, 255);
                           color: #000000;
                           text-decoration: underline;
                           font-family: Courier;}""")
        self.lineEdit_1.setFont(font_e)

        Btn_1 = QPushButton("&クリア")
        Btn_1.setFont(font_j)
        Btn_1.clicked.connect(self.text_clc)

        Btn_2 = QPushButton("&翻訳")
        Btn_2.setFont(font_j)
        Btn_2.clicked.connect(self.translate)

        text_2 = QLabel(' Google 翻訳 ')
        text_2.setFont(font_j)
        self.lineEdit_2 = QTextEdit()
        self.lineEdit_2.setFont(font_j)
        self.lineEdit_2.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Expanding)

        text_3 = QLabel(' DeepL ')
        text_3.setFont(font_j)
        self.lineEdit_3 = QTextEdit()
        self.lineEdit_3.setFont(font_j)
        self.lineEdit_3.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Expanding)

        text_4 = QLabel(' エキサイト 翻訳 ')
        text_4.setFont(font_j)
        self.lineEdit_4 = QTextEdit()
        self.lineEdit_4.setFont(font_j)
        self.lineEdit_4.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Expanding)

        text_5 = QLabel(' Weblio 翻訳 ')
        text_5.setFont(font_j)
        self.lineEdit_5 = QTextEdit()
        self.lineEdit_5.setFont(font_j)
        self.lineEdit_5.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Expanding)

        texts = [text_2,text_3,text_4,text_5]
        self.lines = [self.lineEdit_2,self.lineEdit_3,self.lineEdit_4,self.lineEdit_5]

        # Setting layout
        layout = QGridLayout()
        layout.setSpacing(5)

        # ラベルの位置設定
        layout.addWidget(text_1, 0, 0)
        layout.addWidget(self.lineEdit_1, 1, 0, 1, -1)
        
        layout.addWidget(Btn_1, 2, 0)
        layout.addWidget(Btn_2, 2, 2)

        cnt = 0
        for i in range(4):
            if not self.Box[i]:
                continue
            text = texts[i]
            line = self.lines[i]

            layout.addWidget(text, 3+2*cnt, 0)
            layout.addWidget(line, 4+2*cnt, 0, 1, -1)

            cnt += 1

        self.setLayout(layout)

    def translate(self):
        text = self.lineEdit_1.toPlainText()
        Box = self.Box

        ts = time.time()
        trans = translate(text, Box)
        trans.read_config()
        trans.Run()
        trans_texts = trans.return_para()

        #print(trans_texts)
        for i in range(4):
            line = self.lines[i]
            line.setText(trans_texts[i])

        tf = time.time()
        print('runtime = {} [s]'.format(tf-ts))

    def text_clc(self):
        for line in (self.lines + [self.lineEdit_1]):
            line.setText('')




def main():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    app = QApplication(sys.argv)
    ew = App()
    sys.exit(app.exec_())

    

if __name__ == '__main__':
    main()
