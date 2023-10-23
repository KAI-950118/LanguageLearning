import sys

import pandas as pd
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QApplication, QMainWindow, QLineEdit, QTextEdit, QPushButton
from PySide6.QtCore import QTimer

import Azure_TTS as TTS
import BackEndMain as BE


class LoadMainUI(QMainWindow):
    def __init__(self):
        super().__init__()
        # 抓ExcelPath
        self.path = BE.GetExcelPath()
        # 抓VoicePath
        self.voicePath = TTS.GetVoicePath()
        # 抓Excel的CoverPageTestTime
        self.Sentence_df = pd.DataFrame()
        # 先確定有沒有抓到句子
        self.StartTest = False
        # 執行完一次測試就要開啟
        self.Over = False
        # 先定義空內容
        self.Sentence_df = pd.DataFrame()
        self.TestNow = 0
        self.TestTotal = 999
        # 跟當前測試句子有關
        self.TestId = 0
        self.TestSentence = ""
        self.TestTranslation = ""
        self.TestUsage = ""
        self.TestVoiceFile = ""
        # AutoRepeat
        self.is_running = False
        self.timer = QTimer(self)
        # 取出UI
        loader = QUiLoader()
        ui_file = loader.load('MainUI.ui', self)
        self.setCentralWidget(ui_file)
        self.setFixedSize(640, 480)

        # StartButton的任務
        StartButton = self.findChild(QPushButton, "StartButton")
        StartButton.clicked.connect(self.Startbutton_click)

        # Show Button的任務
        ShowButton = self.findChild(QPushButton, "ShowButton")
        ShowButton.clicked.connect(self.Showbutton_click)

        # PassButton的任務
        PassButton = self.findChild(QPushButton, "PassButton")
        PassButton.clicked.connect(self.Passbutton_click)

        # FailButton的任務
        FailButton = self.findChild(QPushButton, "FailButton")
        FailButton.clicked.connect(self.Failbutton_click)

        # NewWord的任務
        WordAddButton = self.findChild(QPushButton, "NewWordButton")
        WordAddButton.clicked.connect(self.WordAdd)

        # NewSentence的任務
        SentenceAddButton = self.findChild(QPushButton, "GenerateButton")
        SentenceAddButton.clicked.connect(self.SentenceAdd)

        # Repeat的任務
        RepeatButton = self.findChild(QPushButton, "RepeatButton")
        RepeatButton.clicked.connect(self.SentenceRepeat)

        # Auto Repeat的任務
        AutoRepeatButton = self.findChild(QPushButton, "AutoRepeatButton")
        AutoRepeatButton.clicked.connect(self.SentenceAutoRepeat)

        # ChangeVoice的任務
        ChangeVoiceButton = self.findChild(QPushButton, "ChangeVoiceButton")
        ChangeVoiceButton.clicked.connect(self.SentenceChangeVoice)


    def InitialSetting(self):
        CoverDf = BE.CoverRead(path=self.path)
        self.NewTestTime = int(CoverDf['TestTime']) + 1
        self.findChild(QLineEdit, "Main_TestTime_Show").setText(str(self.NewTestTime))

    def Startbutton_click(self):
        if self.Over == False:
            self.StartTest = True
            TestNumber = self.findChild(QLineEdit, "Main_TestNumber_Show").text()
            # 取得要測試的內容
            self.Sentence_df = BE.SentGetTest(TestTime=self.NewTestTime, TestNum=int(TestNumber),path=self.path)
            self.TestTotal = len(self.Sentence_df)
            # 如果今天沒有要測試的例外
            if self.TestTotal == 0:
                # 更新進度條
                Content = "本次無測試項目"
                self.findChild(QLineEdit, "Test_Progress_Show").setText(Content)
                # 更新測試次數回Excel
                data_dict = {'TestTime': self.NewTestTime}
                BE.CoverUpdate(data_dict, path=self.path)
                self.Over = True
            else:
                # 抓到測試項目
                self.TestNow = 1
                self.SentecneTestGo()

    def Showbutton_click(self):
        if self.StartTest == True and self.Over == False and self.TestTotal != 0:
            # 顯示提示
            self.findChild(QTextEdit, "Test_Sentence_Show").setText(self.TestSentence)
            self.findChild(QTextEdit, "Test_Translation_Show").setText(self.TestTranslation)
            self.findChild(QTextEdit, "Test_Usage_Show").setText(self.TestUsage)

    def Passbutton_click(self):
        if self.StartTest == True and self.Over == False and self.TestTotal != 0:
            if self.TestNow < self.TestTotal:
                # 測試項目+1
                self.TestNow = self.TestNow + 1
                self.SentecneTestGo()
                # 清空提示
                self.findChild(QTextEdit, "Test_Sentence_Show").setText("")
                self.findChild(QTextEdit, "Test_Translation_Show").setText("")
                self.findChild(QTextEdit, "Test_Usage_Show").setText("")
            else:
                # 將結果更新上資料庫
                BE.SentUpdateAftTest(TestTime=self.NewTestTime, MainDf=self.Sentence_df, path=self.path)
                self.Over = True
                self.TestVoiceFile = f'{self.voicePath}/Test_Over.wav'
                # 發出聲音
                TTS.Play_wav(self.TestVoiceFile)

    def Failbutton_click(self):
        if self.StartTest == True and self.Over == False and self.TestTotal != 0:
            # 顯示提示
            self.findChild(QTextEdit, "Test_Sentence_Show").setText(self.TestSentence)
            self.findChild(QTextEdit, "Test_Translation_Show").setText(self.TestTranslation)
            self.findChild(QTextEdit, "Test_Usage_Show").setText(self.TestUsage)

            # 標記失敗
            self.Sentence_df = BE.SentChangeCorrect(self.Sentence_df, self.TestId)

    def SentecneTestGo(self):  # Dataframe的Index會比Now-1,
        # 設定進度條
        Content = f"{self.TestNow}/{self.TestTotal}"
        self.findChild(QLineEdit, "Test_Progress_Show").setText(Content)
        # 抓出測試項目
        self.TestId = self.Sentence_df.loc[self.TestNow - 1, 'Id']
        self.TestSentence = self.Sentence_df.loc[self.TestNow - 1, 'Sentence']
        self.TestTranslation = self.Sentence_df.loc[self.TestNow - 1, 'Translation']
        self.TestUsage = self.Sentence_df.loc[self.TestNow - 1, 'Usage']
        self.TestVoiceFile = f'{self.voicePath}/{self.TestId}_voice.wav'

        # 發出聲音
        TTS.Play_wav(self.TestVoiceFile)

    def SentenceRepeat(self):
        # 發出聲音
        TTS.Play_wav(self.TestVoiceFile)

    def SentenceAutoRepeat(self):
        if not self.is_running:
            self.timer.timeout.connect(self.SentenceRepeat)
            self.timer.start(5000)
            self.is_running = True
            self.findChild(QPushButton, "AutoRepeatButton").setText("Auto Repeat: Stop")
        else:
            self.timer.stop()
            self.timer.timeout.disconnect(self.SentenceRepeat)
            self.is_running = False
            self.findChild(QPushButton, "AutoRepeatButton").setText("Auto Repeat: Start")
    def SentenceChangeVoice(self):
        # 更換音檔
        voice_name = TTS.Azure_VoiceName(DeleteList=[])
        TTS.Azure_TTS(self.voicePath, voice_name=voice_name, text=self.TestSentence, GetFile=True, FileName=f'{self.TestId}_voice')
        TTS.Play_wav(self.TestVoiceFile)

    def WordAdd(self):
        Word = self.findChild(QLineEdit, "Word_Text").text()
        if len(Word) >= 1:
            BE.VocaUpdate(Vocabulary=Word, path=self.path)
        self.findChild(QLineEdit, "Word_Text").setText("")

    def SentenceAdd(self):
        BE.SentUpdate(TestTime=self.NewTestTime, path=self.path)
        self.TestVoiceFile = f'{self.voicePath}/GPT_Done.wav'
        # 發出聲音
        TTS.Play_wav(self.TestVoiceFile)
        self.findChild(QLineEdit, "Word_Text").setText("OK")

if __name__ == "__main__":
    # 打開UI Window
    app = QApplication(sys.argv)
    main_window = LoadMainUI()
    main_window.show()
    main_window.InitialSetting()
    sys.exit(app.exec_())

    # TODO 需不需要刪除句子的功能?
