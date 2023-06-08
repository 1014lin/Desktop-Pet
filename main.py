# *_* coding : UTF-8 *_*
# 鼠标左键拖动 右键变向 双击发声
import random
import sys
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QThread
from PyQt5.QtMultimedia import QSound

class TablePet(QWidget):
    c=0
    # 初始化
    def __init__(self):
        super(TablePet, self).__init__()
        self.initUi()
        self.tray()
        self.is_follow_mouse = False
        self.is_flying = False
        self.mouse_drag_pos = self.pos()
        # 每隔一段时间做个动作
        self.timer = QTimer()
        self.timer.timeout.connect(self.doAction)
        self.timer.start(150)
        self.actTimer = QTimer()
        self.actTimer.timeout.connect(self.randomAct)
        self.actTimer.start(6000)

    # 初始化UI
    def initUi(self):
        self.pic =0
        self.w = 1850
        self.h = 910
        self.direction = 1
        self.action = 1
        self.setGeometry(self.w, self.h, 150, 150)
        self.lbl = QLabel(self)
        self.frame = 1
        self.pic_url = 'pet\Chicken\c'+str(self.pic)+ str(self.direction)+str(self.action)+str(self.frame) + '.png'
        self.pm = QPixmap(self.pic_url)
        self.lbl.setPixmap(self.pm)
        # 背景透明等效果
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.SubWindow)
        self.setAutoFillBackground(False)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.show()
        self.repaint()

    # 系统托盘
    def tray(self):
        tp = QSystemTrayIcon(self)
        tp.setIcon(QIcon('pet\Chicken\c0111.png'))
        ation_quit = QAction('退出', self, triggered=self.quit)
        action_change = QAction('更換角色',self, triggered=self.change)
        tpMenu = QMenu(self)
        tpMenu.addAction(ation_quit)
        tpMenu.addAction(action_change)
        tp.setContextMenu(tpMenu)
        tp.show()

    # 改变方向
    def changeDirection(self):
        if self.direction == 1:
            self.direction = 1
        else:
            self.direction = 1

    # 发出叫声
    def playSound(self):
        self.action = 2
        if self.pic==0:
            QSound.play("pet\Chicken\jier.wav")
        else :
            QSound.play("pet\Chicken\qiye.wav")
    # 随机动作
    def randomAct(self):
        temp = random.random()
        if temp > 0.9:
            self.changeDirection()
        else:
            self.changeDirection()

    def tuozhuai(self):
        self.action = 4

    # 窗口运动
    def doAction(self):
        # 读取图片不同的地址，实现动画效果
        if self.frame < 27:
            self.frame += 1
        else:
            self.frame = 1
        self.pic_url = 'pet\Chicken\c'+str(self.pic)+str(self.direction)+str(self.action)+str(self.frame) + '.png'
        self.pm = QPixmap(self.pic_url)
        # 检测是否飞行
        if self.h != 910:
            self.is_flying = True
        else:
            self.is_flying = False
            self.action = 1
        # 实现行进效果
        if not self.is_follow_mouse:
            # 飞行效果
            if self.is_flying:
                self.action = 3
                if self.h > 1100:
                    self.h = 0
                elif self.h > 900:
                    self.h += 1
                else:
                    self.h += 15
            # 行走效果
            
            self.move(self.w, self.h)
        self.lbl.setPixmap(self.pm)

    # 鼠标事件
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.is_follow_mouse = True
            self.mouse_drag_pos = event.globalPos() - self.pos()
            event.accept()
            self.setCursor(QCursor(Qt.OpenHandCursor))
        elif event.button() == Qt.RightButton:
           self.changeDirection()

    def mouseMoveEvent(self, event):
        if Qt.LeftButton and self.is_follow_mouse:
            self.move(event.globalPos() - self.mouse_drag_pos)
            xy = self.pos()
            self.tuozhuai()
            self.w, self.h = xy.x(), xy.y()
            event.accept()

    def mouseDoubleClickEvent(self, event):
        self.playSound()

    def mouseReleaseEvent(self, event):
        self.is_follow_mouse = False
        self.setCursor(QCursor(Qt.ArrowCursor))

    # 托盘退出
    def quit(self):
        self.close()
        sys.exit()
    #更換角色
    def change(self):
        if self.pic==0:
            self.pic=3
        else :
            self.pic=0

        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    myPet = TablePet()
    sys.exit(app.exec_())
