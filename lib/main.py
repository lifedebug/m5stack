from m5stack import lcd, speaker, buttonA, buttonB, buttonC
import utime
import uos


applist=[]
try :
    uos.mountsd()
    lcd.println("SD mount OK!")
    lcd.println("read file in sdcard!")
    filetemp=uos.listdir('/sd')

    for i in filetemp:
        if ".app" == i.lower()[-4:]:
            applist.append(['/sd',i])
    lcd.println('OK!')

    lcd.println("read file in flash!")
    filetemp = uos.listdir('/flash')
    for i in filetemp:
        if ".app.py" == i.lower()[-7:]:
            applist.append(['/flash', i])
    lcd.println('OK!')

except:
    lcd.println("SD mount fail!")
    lcd.println("read file in flash!")
    filetemp = uos.listdir('/flash')
    for i in filetemp:
        if ".app.py" == i.lower()[-7:]:
            applist.append(['/flash', i])
    lcd.println('OK!')

lcd.setColor(lcd.RED,lcd.BLACK)



for i in applist:
    if i[0] == "/sd":
        lcd.print(i[0]+"     ")
    else:
        lcd.print(i[0] + " ")
    lcd.println(i[1])


class List:
    def __init__(self,applist):
        # 第一次显示应该显示widget的当前索引
        self.x = 10
        self.y = 50
        self.length = 300
        self.width = 150

        self.applist = applist

        self.color_1 = [lcd.WHITE, lcd.DARKGREY]  # 未选中
        self.color_2 = [lcd.BLACK, lcd.WHITE]  # 选中

        self.font = lcd.FONT_DejaVu18
        lcd.font(self.font, fixedwidth=0)
        self.fontheight = lcd.fontSize()[1]  # 获取字符高度
        self.lines = int(200 / self.fontheight)  # 每页显示的行数
        self.index = 0
        self.previous_index = None
        self.draw(self.index)
    def clear(self):
        lcd.rect(self.x,self.y,self.length,self.width,self.color_1[1],self.color_1[1])
    def draw(self,index):
        a,b=divmod(len(self.applist),self.lines)
        A,B=divmod(index,self.lines)
        if A == a:
            frontlist=self.applist[A*self.lines:]
        else:
            frontlist=self.applist[A*self.lines:(A+1)*self.lines]
        if self.previous_index is None:
            self.clear()
            lcd.font(self.font, fixedwidth=0)
            for i in range(len(frontlist)):
                print(i,frontlist[i],end=" ")
                if i == B:
                    lcd.setColor(self.color_2[0],self.color_2[1])
                    lcd.rect(self.x,self.y+B*self.fontheight,self.length,self.fontheight,self.color_2[1],self.color_2[1])
                    if frontlist[i][0]=="/sd":
                        lcd.text(self.x,self.y+i*self.fontheight,"SD-"+frontlist[i][1][:-4])
                    else:
                        lcd.text(self.x, self.y + i * self.fontheight, "FLASH-" + frontlist[i][1][:-7])
                else:
                    lcd.setColor(self.color_1[0], self.color_1[1])
                    lcd.rect(self.x, self.y + i * self.fontheight, self.length,self.fontheight,self.color_1[1], self.color_1[1])
                    if frontlist[i][0]=="/sd":
                        lcd.text(self.x,self.y+i*self.fontheight,"SD-"+frontlist[i][1][:-4])
                    else:
                        lcd.text(self.x, self.y + i * self.fontheight, "FLASH-" + frontlist[i][1][:-7])
            self.previous_index=index
        else:
            if A != divmod(self.previous_index, self.lines)[0]:
                self.previous_index = None
                self.draw(index)
            else:
                pb = divmod(self.previous_index, self.lines)[1]
                lcd.setColor(self.color_1[0], self.color_1[1])
                lcd.rect(self.x, self.y + pb * self.fontheight,self.length,self.fontheight,self.color_1[1], self.color_1[1])
                if frontlist[pb][0] == "/sd":
                    lcd.text(self.x, self.y + pb * self.fontheight, "SD-" + frontlist[pb][1][:-4])
                else:
                    lcd.text(self.x, self.y + pb * self.fontheight, "FLASH-" + frontlist[pb][1][:-7])
                lcd.setColor(self.color_2[0], self.color_2[1])
                lcd.rect(self.x, self.y + B * self.fontheight, self.length,self.fontheight,self.color_2[1], self.color_2[1])
                if frontlist[B][0] == "/sd":
                    lcd.text(self.x, self.y + B * self.fontheight, "SD-" + frontlist[B][1][:-4])
                else:
                    lcd.text(self.x, self.y + B * self.fontheight, "FLASH-" + frontlist[B][1][:-7])
            self.previous_index=index
    def event(self,argument):
        if argument == 1:
            if self.index == 0:
                self.index=len(self.applist)-1
            else:
                self.index-=1
            self.draw(self.index)
        elif argument == 2:
            return self.index
        elif argument == 3:
            if self.index == len(self.applist)-1:
                self.index = 0
            else:
                self.index +=1
            self.draw(self.index)
        return -1
lcd.image(0,0,'m5stack.jpg')
utime.sleep(3)
lcd.clear(lcd.BLACK)
lcd.font('/flash/font/ep60.fon', fixedwidth=0)
lcd.setColor(lcd.RED,lcd.BLACK)
lcd.text(int((320-lcd.textWidth('APP'))/2),1,'APP')

appchose=List(applist)

while True:
    if buttonA.wasPressed():
        temp = appchose.event(1)
        if temp == -1:
            pass
        else:
            if applist[temp][0] == '/flash':
                exec(open(applist[temp][0] + "/" + applist[temp][1]).read())
            else:
                exec(open(applist[temp][0] + "/" + applist[temp][1] + "/" + "main.py").read())

    if buttonB.wasPressed():
        temp = appchose.event(2)
        if temp == -1:
            pass
        else:
            if applist[temp][0] == '/flash':
                lcd.image(0, 0, 'm5stack.jpg')
                exec(open(applist[temp][0] + "/" + applist[temp][1]).read())
            else:
                lcd.image(0, 0, 'm5stack.jpg')
                exec(open(applist[temp][0] + "/" + applist[temp][1] + "/" + "main.py").read())
            #appchose.draw(appchose.index)
            break
    if buttonC.wasPressed():
        temp = appchose.event(3)
        if temp == -1:
            pass
        else:
            if applist[temp][0] == '/flash':
                #lcd.clear(lcd.RED)
                exec(open(applist[temp][0] + "/" + applist[temp][1]).read())
            else:
                #lcd.clear(lcd.RED)
                exec(open(applist[temp][0] + "/" + applist[temp][1] + "/" + "main.py").read())
            #appchose.draw(appchose.index)
            break