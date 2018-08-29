from m5stack import lcd
import ujson
import gc

import m5stack as m5
import utime

try:
    m5guiconfig = ujson.load(open("m5guiconfig.json"))
    BorderColor=m5guiconfig['BorderColor']
    WindowBColor=m5guiconfig['WindowBColor']
    FocusColor=m5guiconfig['FocusColor']
    BorderWidth=m5guiconfig['BorderWidth']
except:
    BorderColor = lcd.BLACK  # 边界框颜色
    # WindowBColor = 0x00979d  # 窗口背景色
    #WindowBColor = lcd.BLACK  # 窗口背景色
    WindowBColor = lcd.DARKCYAN  # 窗口背景色
    # FocusColor = lcd.BLACK
    # FocusColor = 0x993300
    #FocusColor = lcd.RED
    FocusColor = lcd.PURPLE
    BorderWidth = 2  # 边框宽度
ScreenWidth, ScreenHeight = lcd.screensize()  # 获取屏幕尺寸


##################################################
def getstrbylength(text, length, font, fixedwidth=0):  # 更具长度参数获取字符串
    lcd.font(font, fixedwidth=fixedwidth)
    if lcd.textWidth(text) < length or lcd.textWidth(text) == length:
        return text
    else:
        for i in range(1, len(text)):
            textwidth = lcd.textWidth(text[:-i])
            if textwidth < length or textwidth == length:
                return text[:-i]
            else:
                pass
        return -1


##################################################
class Window:  # 主窗口
    def __init__(self, btnAtext="<", btnBtext="OK", btnCtext=">", hidebtn=0, bcolor=WindowBColor):
        global ScreenWidth
        global ScreenHeight
        global BorderWidth
        global BorderColor
        global WindowBColor
        WindowBColor = bcolor
        self.font = lcd.FONT_DejaVu24
        lcd.font(self.font, fixedwidth=0)
        self.fontheight = lcd.fontSize()[1]
        self.fontcolor = lcd.WHITE
        self.defautbtnwidth = 60
        self.btnAtext = btnAtext
        self.btnBtext = btnBtext
        self.btnCtext = btnCtext
        self.hidebtn = hidebtn

        self.page = []  # 页面池
        self.current_page = 0  # 当前页码
        self.current_widget = 0  # 当前页的当前控件
        self.len_page = 0  # 页面长度，active后赋值为实际长度

        self.textboxflag = 0
        self.listboxflag = 0

        self.brightness=500
        self.setbrightness(self.brightness)
        self.edit = None

    def setbrightness(self,value):
        self.brightness=value
        lcd.setBrightness(value)

    def screen_off(self):
        lcd.setBrightness(0)

    def screen_on(self):
        lcd.setBrightness(self.brightness)

    def draw(self):  # 画基本界面
        lcd.clear(WindowBColor)
        if self.hidebtn == 0:
            temp = int((ScreenWidth - self.defautbtnwidth * 3) / 4)

            # lcd.clear(BorderColor)
            # lcd.roundrect(BorderWidth, BorderWidth, ScreenWidth - BorderWidth * 2, ScreenHeight - BorderWidth * 2, 20,WindowBColor, WindowBColor)

            lcd.roundrect(temp, ScreenHeight - (self.fontheight + 4), self.defautbtnwidth, self.fontheight + 4, 5,
                          BorderColor, BorderColor)
            lcd.font(self.font, fixedwidth=0)
            lcd.setColor(self.fontcolor, BorderColor)
            lcd.text(temp + int((self.defautbtnwidth - lcd.textWidth(self.btnAtext)) / 2),
                     ScreenHeight - self.fontheight,
                     self.btnAtext)

            lcd.roundrect(temp * 2 + self.defautbtnwidth, ScreenHeight - (self.fontheight + 4), self.defautbtnwidth,
                          self.fontheight + 4, 5, BorderColor, BorderColor)
            lcd.font(self.font, fixedwidth=0)
            lcd.setColor(self.fontcolor, BorderColor)
            lcd.text(temp * 2 + self.defautbtnwidth + int((self.defautbtnwidth - lcd.textWidth(self.btnBtext)) / 2),
                     ScreenHeight - self.fontheight, self.btnBtext)

            lcd.roundrect(temp * 3 + self.defautbtnwidth * 2, ScreenHeight - (self.fontheight + 4), self.defautbtnwidth,
                          self.fontheight + 4, 5, BorderColor, BorderColor)
            lcd.font(self.font, fixedwidth=0)
            lcd.setColor(self.fontcolor, BorderColor)
            lcd.text(temp * 3 + self.defautbtnwidth * 2 + int((self.defautbtnwidth - lcd.textWidth(self.btnCtext)) / 2),
                     ScreenHeight - self.fontheight, self.btnCtext)
            del temp

    def updatebtntext(self, btnAtext=None, btnBtext=None, btnCtext=None):  # 更新三颗主按钮文本
        if self.hidebtn == 0:
            temp = int((ScreenWidth - self.defautbtnwidth * 3) / 4)
            lcd.font(self.font, fixedwidth=0)
            lcd.setColor(self.fontcolor, BorderColor)
            if btnAtext is not None:
                self.btnAtext = btnAtext
                lcd.roundrect(temp, ScreenHeight - (self.fontheight + 4), self.defautbtnwidth, self.fontheight + 4, 5,
                              BorderColor, BorderColor)
                lcd.text(temp + int((self.defautbtnwidth - lcd.textWidth(self.btnAtext)) / 2),
                         ScreenHeight - (self.fontheight), self.btnAtext)
            if btnBtext is not None:
                self.btnBtext = btnBtext
                lcd.roundrect(temp * 2 + self.defautbtnwidth, ScreenHeight - (self.fontheight + 4), self.defautbtnwidth,
                              self.fontheight + 4, 5, BorderColor, BorderColor)
                lcd.text(temp * 2 + self.defautbtnwidth + int((self.defautbtnwidth - lcd.textWidth(self.btnBtext)) / 2),
                         ScreenHeight - (self.fontheight), self.btnBtext)
            if btnCtext is not None:
                self.btnCtext = btnCtext
                lcd.roundrect(temp * 3 + self.defautbtnwidth * 2, ScreenHeight - (self.fontheight + 4),
                              self.defautbtnwidth,
                              self.fontheight + 4, 5, BorderColor, BorderColor)
                lcd.text(
                    temp * 3 + self.defautbtnwidth * 2 + int((self.defautbtnwidth - lcd.textWidth(self.btnCtext)) / 2),
                    ScreenHeight - (self.fontheight), self.btnCtext)
        else:
            if btnAtext is not None:
                self.btnAtext = btnAtext
            if btnBtext is not None:
                self.btnBtext = btnBtext
            if btnCtext is not None:
                self.btnCtext = btnCtext

    # 页面清理
    def page_clear(self, page):
        self.draw()
        if len(page.action_widget_box) != 0:
            for i in page.action_widget_box:
                i.hide()
        if len(page.vivew_widget_box) != 0:
            for i in page.vivew_widget_box:
                i.hide()

    # 页面显示
    def page_show(self, page):
        if len(page.action_widget_box) != 0:
            for i in page.action_widget_box:
                i.draw()
            self.current_widget = self.page[self.current_page].widget_index
            self.page[self.current_page].action_widget_box[self.current_widget].focus()

        if len(page.vivew_widget_box) != 0:
            for i in page.vivew_widget_box:
                i.draw()

    def event(self, btn_number):
        if self.len_page > 0:  # 如果有page
            if self.textboxflag == 1:
                # print("#1 EVENT")
                # print("textboxflag:", self.textboxflag)
                temp = self.edit.event(btn_number)
                if temp == 0:  # 返回0 编辑结束， 清除页面
                    self.page_clear(self.edit.page)
                    self.page_show(self.page[self.current_page])
                    self.page[self.current_page].action_widget_box[self.current_widget].focus()
                    self.textboxflag = 0
                    del self.edit
                    self.edit = None
                    gc.collect()
                    # print("textboxflag:", self.textboxflag)
            elif self.listboxflag == 1:
                temp = self.edit.event(btn_number)
                if temp == 0:
                    self.edit.clearlist()
                    self.page_show(self.page[self.current_page])
                    self.page[self.current_page].action_widget_box[self.current_widget].focus()
                    self.listboxflag = 0
                    del self.edit
                    self.edit = None
                    gc.collect()
            else:
                # print("#3 EVENT")
                if len(self.page[self.current_page].action_widget_box) > 0:
                    # print("#3-1 EVENT")
                    if btn_number == 1:  # A健按下事件
                        # print("#3-1-1 EVENT")
                        if self.current_widget == 0:
                            # print("#3-1-1-1 EVENT")
                            if self.page[self.current_page].previous_page is None:
                                pass
                            else:
                                self.page_clear(self.page[self.current_page])
                                self.current_page = self.page[self.current_page].previous_page
                                self.page_show(self.page[self.current_page])
                                self.current_widget = len(self.page[self.current_page].action_widget_box) - 1
                                self.page[self.current_page].widget_index=self.current_widget
                                self.page[self.current_page].action_widget_box[self.current_widget].focus()
                        else:
                            # print("#3-1-1-2 EVENT")
                            self.page[self.current_page].action_widget_box[self.current_widget].unfocused()
                            self.current_widget = self.current_widget - 1
                            self.page[self.current_page].widget_index = self.current_widget
                            self.page[self.current_page].action_widget_box[self.current_widget].focus()

                    elif btn_number == 2:  # B健按下事件
                        # print("#3-1-2 EVENT")
                        # 如果是textbox按下OK键
                        if isinstance(self.page[self.current_page].action_widget_box[self.current_widget], TextBox):
                            # print("#3-1-2-1 EVENT")
                            self.textboxflag = 1
                            self.edit = Edit(self.page[self.current_page].action_widget_box[self.current_widget])

                            self.page_clear(self.page[self.current_page])

                            self.page_show(self.edit.page)
                            self.edit.current_btn = 0
                            self.edit.current_str = 0
                            print(self.page[self.current_page].action_widget_box[self.current_widget].value)
                            self.edit.page.action_widget_box[0].focus()

                        elif isinstance(self.page[self.current_page].action_widget_box[self.current_widget], ListBox):
                            self.listboxflag = 1
                            self.page_clear(self.page[self.current_page])
                            self.edit = None
                            self.edit = List()
                            self.edit.widget = self.page[self.current_page].action_widget_box[self.current_widget]
                            self.edit.init()
                            self.edit.draw(self.page[self.current_page].action_widget_box[self.current_widget].index)

                        else:
                            # print("#3-1-2-2 EVENT")
                            self.page[self.current_page].action_widget_box[self.current_widget].click()

                    elif btn_number == 3:  # C健按下事件
                        # print("#3-1-3 EVENT")
                        if self.current_widget == len(self.page[self.current_page].action_widget_box) - 1:
                            # print("#3-1-3-1 EVENT")
                            if self.page[self.current_page].next_page is None:
                                pass
                            else:
                                self.page_clear(self.page[self.current_page])
                                self.current_page = self.page[self.current_page].next_page
                                self.page_show(self.page[self.current_page])
                                self.current_widget = 0
                                self.page[self.current_page].widget_index = self.current_widget
                                self.page[self.current_page].action_widget_box[self.current_widget].focus()
                        else:
                            # print("#3-1-3-2 EVENT")
                            self.page[self.current_page].action_widget_box[self.current_widget].unfocused()
                            self.current_widget = self.current_widget + 1
                            self.page[self.current_page].widget_index = self.current_widget
                            self.page[self.current_page].action_widget_box[self.current_widget].focus()
                else:
                    # print("#3-2 EVENT")
                    if btn_number == 1:  # A健按下事件
                        if self.page[self.current_page].previous_page is None:
                            pass
                        else:
                            self.page_clear(self.page[self.current_page])
                            self.current_page = self.page[self.current_page].previous_page
                            self.page_show(self.page[self.current_page])
                    elif btn_number == 2:  # B健按下事件
                        pass
                    elif btn_number == 3:  # C健按下事件
                        if self.page[self.current_page].next_page is None:
                            pass
                        else:
                            self.page_clear(self.page[self.current_page])
                            self.current_page = self.page[self.current_page].next_page
                            self.page_show(self.page[self.current_page])

    '''
    # 总回调
    def btn_callback(self, btn_number):
        if btn_number == 1:
            # print('btnA press')
            # self.page_event(1)
            self.event(1)
        elif btn_number == 2:
            # print('btnB press')
            # self.page_event(2)
            self.event(2)
        elif btn_number == 3:
            # print('btnC press')
            # self.page_event(3)
            self.event(3)
        else:
            pass

    # btnA回调
    def btnA_callback(self):
        self.btn_callback(1)

    # btnB回调
    def btnB_callback(self):
        self.btn_callback(2)

    # btnC回调
    def btnC_callback(self):
        self.btn_callback(3)

    # 键盘回调函数
    def keyboard_callback(self, key):
        print("KEYBOARD:", key)
        self.event(key)

    # 物理按钮绑定事件
    def phy_btn_set(self):
        m5.buttonA.wasPressed(self.btnA_callback)
        m5.buttonB.wasPressed(self.btnB_callback)
        m5.buttonC.wasPressed(self.btnC_callback)
        keyboard.callback(self.keyboard_callback)
    '''

    def active(self):
        self.len_page = len(self.page)
        self.draw()
        self.page_show(self.page[self.current_page])
        # self.phy_btn_set()
        if len(self.page[self.current_page].action_widget_box) == 0:
            pass
        else:
            self.page[self.current_page].action_widget_box[self.current_widget].focus()




##################################################
class Page:
    def __init__(self):
        self.action_widget_box = []  # 控件池i
        self.vivew_widget_box = []  # 控件池
        self.next_page = None  # 下一页在页面池的编号
        self.previous_page = None  # 下一页在页面池的编号
        self.widget_index=0       #当前控件索引

    def add(self, widget, *args):  # 向页面添加控件
        if isinstance(widget, (Button, CheckBox, TextBox, ListBox)):  ########动作执行控件#######
            self.action_widget_box.append(widget)
        elif isinstance(widget, (Lable, HProgressBar, VProgressBar, DebugBox)):  ########显示控件##############
            self.vivew_widget_box.append(widget)
        else:
            print('ERROR:GUI-Page-add(', widget, ')')
        if len(args) > 0:
            for i in args:
                if isinstance(i, (Button, CheckBox, TextBox, ListBox)):  ########动作执行控件#######
                    self.action_widget_box.append(i)
                elif isinstance(i, (Lable, HProgressBar, VProgressBar, DebugBox)):  ########显示控件##############
                    self.vivew_widget_box.append(i)
                else:
                    print('ERROR:GUI-Page-add(', i, ')')
        # print(self.action_widget_box)
        # print(self.vivew_widget_box)


#################################################
class Edit:
    def __init__(self, widget):

        self.widget = widget

        self.page = Page()
        self.strdate = ["ABCabc", "DEFdef", "GHIghi", "JKLjkl", "MNOmon", "PQRSpqrs", "TUVtuv", "WXYZwxyz",
                        "1234567890", "DEL",
                        " '!\"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'", "OK"]

        x = 13
        y = 120

        for i in range(3):
            for n in range(4):
                self.page.add(
                    Button(x + n * 75, y + i * 30, text=self.strdate[i * 4 + n], length=70, font=lcd.FONT_DejaVu18))

        self.lable = Lable(10, 10, text=self.widget.value, length=300, underline=1, pc=0)

        self.page.add(self.lable)

        lcd.font(lcd.FONT_DejaVu18, fixedwidth=1)  # 设置成等宽字符
        self.fontwidth, self.fontheight = lcd.fontSize()  # 获取字符长宽
        # print(self.fontwidth, self.fontheight)
        self.strchoseflag = 0
        self.current_str = 0
        self.current_btn = 0

    def btncallback(self, argument):
        pass

    def drawstr(self):
        x = 10
        y = 50
        strnumber = int(300 / self.fontwidth)
        a, b = divmod(len(self.strdate[self.current_btn]), strnumber)
        # a 行数 ，b 最后一行字符数
        lcd.setColor(lcd.WHITE, WindowBColor)
        lcd.font(lcd.FONT_DejaVu18, fixedwidth=1)
        if a == 0:
            # lcd.text(x,y,self.strdate[self.current_btn])
            for i in range(len(self.strdate[self.current_btn])):
                lcd.text(x + i * self.fontwidth, y, self.strdate[self.current_btn][i])
        else:
            for i in range(a):
                # lcd.text(x,y+i*20,self.strdate[self.current_btn][i*strnumber:(i+1)*strnumber])

                temp = self.strdate[self.current_btn][i * strnumber:(i + 1) * strnumber]
                for n in range(len(temp)):
                    lcd.text(x + n * self.fontwidth, y + i * 20, temp[n])
                    # print(temp[n]," X: ",x+n*self.fontwidth," Y: ",y+i*20)

            if b != 0:
                # lcd.text(x,y+a*20,self.strdate[self.current_btn][a*strnumber:])
                temp = self.strdate[self.current_btn][a * strnumber:]
                for n in range(len(temp)):
                    lcd.text(x + n * self.fontwidth, y + a * 20, temp[n])
                    # print(temp[n], " X: ", x + n * self.fontwidth, " Y: ", y + a * 20)

    def focusstr(self):
        x = 10
        y = 50
        strnumber = int(300 / self.fontwidth)
        a, b = divmod(self.current_str, strnumber)
        lcd.rect(x + b * self.fontwidth, y + a * 20 - 2, self.fontwidth, self.fontheight + 2, lcd.WHITE)
        # print("  FOCUS","X:",x+b*self.fontwidth,"Y:",y+a*20-2)

    def unfocusedstr(self):
        x = 10
        y = 50
        strnumber = int(300 / self.fontwidth)
        a, b = divmod(self.current_str, strnumber)
        lcd.rect(x + b * self.fontwidth, y + a * 20 - 2, self.fontwidth, self.fontheight + 2, WindowBColor)
        # print("UNFOCUS","X:", x + b * self.fontwidth, "Y:", y + a * 20 - 2)

    def clearstr(self):
        lcd.rect(10, 40, 300, 75, WindowBColor, WindowBColor)

    def event(self, argument):
        if self.strchoseflag == 0:
            if argument == 1:  # 左键
                if self.current_btn == 0:
                    self.page.action_widget_box[self.current_btn].unfocused()
                    self.current_btn = len(self.page.action_widget_box) - 1
                    self.page.action_widget_box[self.current_btn].focus()
                else:
                    self.page.action_widget_box[self.current_btn].unfocused()
                    self.current_btn = self.current_btn - 1
                    self.page.action_widget_box[self.current_btn].focus()
            elif argument == 2:  # 中键
                if self.strdate[self.current_btn] == "OK":
                    self.widget.update(self.lable.text)
                    self.clearstr()
                    return 0
                elif self.strdate[self.current_btn] == "DEL":
                    self.lable.update(self.lable.text[:-1])
                else:
                    self.strchoseflag = 1  # 改变标志位
                    self.clearstr()  # 清楚字符
                    self.drawstr()  # 显示字符
                    self.focusstr()  # focus current_str 字符
            elif argument == 3:  # 右键
                if self.current_btn == len(self.page.action_widget_box) - 1:
                    self.page.action_widget_box[self.current_btn].unfocused()
                    self.current_btn = 0
                    self.page.action_widget_box[self.current_btn].focus()
                else:
                    self.page.action_widget_box[self.current_btn].unfocused()
                    self.current_btn = self.current_btn + 1
                    self.page.action_widget_box[self.current_btn].focus()
            else:  # keyboard
                if argument == b'\x08':
                    self.lable.update(self.lable.text[:-1])
                elif argument == b'\r':
                    self.widget.update(self.lable.text)
                    self.clearstr()
                    return 0
                else:
                    print("ADD str:", )
                    self.lable.update(self.lable.text + str(argument, "utf8"))


        else:
            if argument == 1:  # 左键
                if self.current_str == 0:
                    self.unfocusedstr()
                    self.current_str = len(self.strdate[self.current_btn]) - 1
                    self.focusstr()
                else:
                    self.unfocusedstr()
                    self.current_str -= 1
                    self.focusstr()
            elif argument == 2:  # 中键
                self.strchoseflag = 0
                self.lable.update(self.lable.text + self.strdate[self.current_btn][self.current_str])
                self.unfocusedstr()
                self.current_str = 0
            elif argument == 3:  # 右键
                if self.current_str == len(self.strdate[self.current_btn]) - 1:
                    self.unfocusedstr()
                    self.current_str = 0
                    self.focusstr()
                else:
                    self.unfocusedstr()
                    self.current_str += 1
                    self.focusstr()
            else:  # keyboard
                pass


class List:
    def __init__(self):
        # 第一次显示应该显示widget的当前索引
        self.x = 10
        self.y = 8
        self.length = 300
        self.width = 200

        self.widget = None

        self.color_1 = [lcd.WHITE, WindowBColor]  # 普通未选中
        self.color_2 = [lcd.WHITE, lcd.DARKGREEN]  # 普通选中
        self.color_3 = [lcd.BLACK, lcd.RED]  # index 选中

        self.font = lcd.FONT_DejaVu24
        lcd.font(self.font, fixedwidth=0)
        self.fontheight = lcd.fontSize()[1]  # 获取字符高度
        self.lines = int(200 / self.fontheight)  # 每页显示的行数

    def init(self):
        self.widget_index = self.widget.index
        self.index = self.widget_index
        self.previous_index = None

    def draw(self, index):
        a, b = divmod(len(self.widget.listdate), self.lines)  # a 完整行数的页数 b 最后一页行数（如果b！=0）
        A, B = divmod(index, self.lines)  # A 当前索引之前完整的页数 B 当前索引所在页的行数（如果b！=0）
        wa, wb = divmod(self.widget_index, self.lines)  # wa widget当前索引之前完整页 wb 最后一页行数（如果b！=0）
        print("lines:", self.lines, " a:", a, " b:", b, " A:", A, " B:", B, " wa:", wa, " wa:", wb)

        if a == A:
            frontlist = self.widget.listdate[a * self.lines:]
        else:
            frontlist = self.widget.listdate[A * self.lines:(A + 1) * self.lines]
        print(frontlist)

        if self.previous_index is None:  # 第一次显示
            self.clearlist()
            lcd.font(self.font, fixedwidth=0)
            if wa == A:  # 选定index和widget index 在同一页
                if B == wb:
                    for i in range(len(frontlist)):
                        if isinstance(frontlist[i], str):
                            text = getstrbylength(frontlist[i], self.length, self.font)
                        else:
                            text = getstrbylength(str(frontlist[i]), self.length, self.font)
                        if i == B:
                            lcd.setColor(self.color_3[0], self.color_3[1])
                            lcd.rect(self.x, self.y + i * self.fontheight, self.length, self.fontheight,
                                     self.color_3[1], self.color_3[1])
                            lcd.text(self.x + int((self.length - lcd.textWidth(text)) / 2),
                                     self.y + i * self.fontheight, text)

                        else:
                            lcd.setColor(self.color_1[0], self.color_1[1])
                            lcd.rect(self.x, self.y + i * self.fontheight, self.length, self.fontheight,
                                     self.color_1[1], self.color_1[1])
                            lcd.text(self.x + int((self.length - lcd.textWidth(text)) / 2),
                                     self.y + i * self.fontheight, text)
                else:
                    for i in range(len(frontlist)):
                        if isinstance(frontlist[i], str):
                            text = getstrbylength(frontlist[i], self.length, self.font)
                        else:
                            text = getstrbylength(str(frontlist[i]), self.length, self.font)
                        if i == B:
                            lcd.setColor(self.color_2[0], self.color_2[1])
                            lcd.rect(self.x, self.y + i * self.fontheight, self.length, self.fontheight,
                                     self.color_2[1], self.color_2[1])
                            lcd.text(self.x + int((self.length - lcd.textWidth(text)) / 2),
                                     self.y + i * self.fontheight, text)
                        elif i == wb:
                            lcd.setColor(self.color_3[0], self.color_3[1])
                            lcd.rect(self.x, self.y + i * self.fontheight, self.length, self.fontheight,
                                     self.color_3[1], self.color_3[1])
                            lcd.text(self.x + int((self.length - lcd.textWidth(text)) / 2),
                                     self.y + i * self.fontheight, text)
                        else:
                            lcd.setColor(self.color_1[0], self.color_1[1])
                            lcd.rect(self.x, self.y + i * self.fontheight, self.length, self.fontheight,
                                     self.color_1[1], self.color_1[1])
                            lcd.text(self.x + int((self.length - lcd.textWidth(text)) / 2),
                                     self.y + i * self.fontheight, text)
            else:
                for i in range(len(frontlist)):
                    if isinstance(frontlist[i], str):
                        text = getstrbylength(frontlist[i], self.length, self.font)
                    else:
                        text = getstrbylength(str(frontlist[i]), self.length, self.font)
                    if i == B:
                        lcd.setColor(self.color_2[0], self.color_2[1])
                        lcd.rect(self.x, self.y + i * self.fontheight, self.length, self.fontheight, self.color_2[1],
                                 self.color_2[1])
                        lcd.text(self.x + int((self.length - lcd.textWidth(text)) / 2), self.y + i * self.fontheight,
                                 text)
                    else:
                        lcd.setColor(self.color_1[0], self.color_1[1])
                        lcd.rect(self.x, self.y + i * self.fontheight, self.length, self.fontheight, self.color_1[1],
                                 self.color_1[1])
                        lcd.text(self.x + int((self.length - lcd.textWidth(text)) / 2), self.y + i * self.fontheight,
                                 text)
            self.previous_index = index
        else:  # 不是第一次显示
            if A != divmod(self.previous_index, self.lines)[0]:
                self.previous_index = None
                self.draw(index)
            else:

                if index == self.widget_index:
                    pa, pb = divmod(self.previous_index, self.lines)
                    if isinstance(frontlist[pb], str):
                        text = getstrbylength(frontlist[pb], self.length, self.font)
                    else:
                        text = getstrbylength(str(frontlist[pb]), self.length, self.font)
                    lcd.setColor(self.color_1[0], self.color_1[1])
                    lcd.rect(self.x, self.y + pb * self.fontheight, self.length, self.fontheight, self.color_1[1],
                             self.color_1[1])
                    lcd.text(self.x + int((self.length - lcd.textWidth(text)) / 2), self.y + pb * self.fontheight, text)
                elif self.previous_index == self.widget_index:
                    if isinstance(frontlist[B], str):
                        text = getstrbylength(frontlist[B], self.length, self.font)
                    else:
                        text = getstrbylength(str(frontlist[B]), self.length, self.font)
                    lcd.setColor(self.color_2[0], self.color_2[1])
                    lcd.rect(self.x, self.y + B * self.fontheight, self.length, self.fontheight, self.color_2[1],
                             self.color_2[1])
                    lcd.text(self.x + int((self.length - lcd.textWidth(text)) / 2), self.y + B * self.fontheight, text)
                else:
                    pa, pb = divmod(self.previous_index, self.lines)
                    if isinstance(frontlist[pb], str):
                        text = getstrbylength(frontlist[pb], self.length, self.font)
                    else:
                        text = getstrbylength(str(frontlist[pb]), self.length, self.font)
                    lcd.setColor(self.color_1[0], self.color_1[1])
                    lcd.rect(self.x, self.y + pb * self.fontheight, self.length, self.fontheight, self.color_1[1],
                             self.color_1[1])
                    lcd.text(self.x + int((self.length - lcd.textWidth(text)) / 2), self.y + pb * self.fontheight, text)

                    if isinstance(frontlist[B], str):
                        text = getstrbylength(frontlist[B], self.length, self.font)
                    else:
                        text = getstrbylength(str(frontlist[B]), self.length, self.font)
                    lcd.setColor(self.color_2[0], self.color_2[1])
                    lcd.rect(self.x, self.y + B * self.fontheight, self.length, self.fontheight, self.color_2[1],
                             self.color_2[1])
                    lcd.text(self.x + int((self.length - lcd.textWidth(text)) / 2), self.y + B * self.fontheight, text)
                self.previous_index = index

    def clearlist(self):
        lcd.rect(self.x, self.y, self.length, self.width, WindowBColor, WindowBColor)

    def event(self, argument):
        if argument == 1:
            if self.index == 0:
                self.index = len(self.widget.listdate) - 1
            else:
                self.index -= 1
            self.draw(self.index)
        elif argument == 2:
            if self.index == self.widget_index:
                self.widget.updateindex(self.index)
                return 0
            else:
                self.widget_index = self.index
                self.previous_index = None
                self.draw(self.index)
        elif argument == 3:
            if self.index == len(self.widget.listdate) - 1:
                self.index = 0
            else:
                self.index += 1
            self.draw(self.index)

        return 1


##################################################
class Lable:
    def __init__(self, x, y, text, color=lcd.WHITE, bcolor=WindowBColor, font=lcd.FONT_DejaVu24, length=100,
                 underline=0, pc=0, hide=1):
        # pc=0 左对齐 pc=1 居中对齐 pc=2，右对齐
        global ScreenWidth
        global ScreenHeight
        global WindowBColor

        self.x = x
        self.y = y
        if isinstance(text, str):
            self.text = text
        else:
            self.text = str(text)

        self.color = color
        self.bcolor = bcolor
        self.font = font
        lcd.font(self.font, fixedwidth=0)
        self.textheight = lcd.fontSize()[1]
        self.length = length
        self.underline = underline
        self.pc = pc
        self.hideflag = hide

        if len(getstrbylength(text, self.length, self.font)) < len(self.text):
            self.fronttext = getstrbylength(text, self.length, self.font)
        else:
            self.fronttext = self.text

        self.width = self.textheight + 1

    def draw(self):
        lcd.rect(self.x, self.y, self.length, self.textheight + 2, self.bcolor, self.bcolor)
        if self.fronttext == "":
            lcd.rect(self.x, self.y, self.length, self.textheight, self.bcolor, self.bcolor)
        else:
            lcd.font(self.font, fixedwidth=0)

            lcd.setColor(self.color, self.bcolor)
            if self.pc == 0:
                lcd.text(self.x, self.y, self.fronttext)
            elif self.pc == 1:
                lcd.text(self.x + int((self.length - lcd.textWidth(self.fronttext)) / 2), self.y, self.fronttext)
            elif self.pc == 2:
                lcd.text(self.x + int(self.length - lcd.textWidth(self.fronttext)), self.y, self.fronttext)
        if self.underline == 1:
            lcd.line(self.x, self.y + self.textheight + 1, self.x + self.length, self.y + self.textheight + 1,
                     self.color)

        self.hideflag = 0

    def hide(self):
        lcd.rect(self.x, self.y, self.length, self.textheight + 2, self.bcolor, self.bcolor)
        self.hideflag = 1

    def update(self, text):
        if self.hideflag == 1:
            if isinstance(text, str):
                self.text = text
            else:
                self.text = str(text)
            self.fronttext = getstrbylength(text, self.length, self.font)
        else:

            if isinstance(text, str):
                self.text = text
            else:
                self.text = str(text)
            temptext = getstrbylength(self.text, self.length, self.font)
            lcd.font(self.font, fixedwidth=0)
            lcd.setColor(self.color, self.bcolor)
            if len(temptext) > len(self.fronttext) or len(temptext) == len(self.fronttext):
                self.fronttext = temptext
                if self.pc == 0:
                    lcd.text(self.x, self.y, self.fronttext)
                elif self.pc == 1:
                    lcd.text(self.x + int((self.length - lcd.textWidth(self.fronttext)) / 2), self.y, self.fronttext)
                elif self.pc == 2:
                    lcd.text(self.x + int(self.length - lcd.textWidth(self.fronttext)), self.y, self.fronttext)
            else:
                if self.pc == 0:
                    lcd.textClear(self.x, self.y, self.fronttext)
                    self.fronttext = temptext
                    lcd.text(self.x, self.y, self.fronttext)
                elif self.pc == 1:
                    lcd.textClear(self.x + int((self.length - lcd.textWidth(self.fronttext)) / 2), self.y,
                                  self.fronttext)
                    self.fronttext = temptext
                    lcd.text(self.x + int((self.length - lcd.textWidth(self.fronttext)) / 2), self.y, self.fronttext)
                elif self.pc == 2:
                    lcd.textClear(self.x + int(self.length - lcd.textWidth(self.fronttext)), self.y, self.fronttext)
                    self.fronttext = temptext
                    lcd.text(self.x + int(self.length - lcd.textWidth(self.fronttext)), self.y, self.fronttext)


class Button:
    def __init__(self, x, y, text, color=lcd.BLACK, bcolor=0xF39C12, disablecolor=0x808080, font=lcd.FONT_DejaVu24,
                 length=50, hide=1, enable=1, callback=None, argument=None):
        self.x = x
        self.y = y
        if isinstance(text, str):
            self.text = text
        else:
            self.text = str(text)

        self.color = color
        self.bcolor = bcolor
        self.disablecolor = disablecolor
        self.font = font

        lcd.font(self.font, fixedwidth=0)
        self.fontheight = lcd.fontSize()[1]
        self.borderwidth = 2
        self.r = int((self.fontheight + self.borderwidth * 2) / 3)

        self.length = length

        self.callback = callback
        self.argument = argument
        self.hideflag = hide
        self.enableflag = enable

        self.text = getstrbylength(self.text, self.length - self.borderwidth * 2 - 4, self.font)

        self.width = self.fontheight + 4 + self.borderwidth * 2

    def draw(self):

        lcd.font(self.font, fixedwidth=0)
        if self.enableflag == 1:
            lcd.roundrect(self.x, self.y, self.length, self.fontheight + 4 + self.borderwidth * 2, self.r, self.bcolor,
                          self.bcolor)
            lcd.setColor(self.color, self.bcolor)
        else:
            lcd.roundrect(self.x, self.y, self.length, self.fontheight + 4 + self.borderwidth * 2, self.r,
                          self.disablecolor,
                          self.disablecolor)
            lcd.setColor(self.color, self.disablecolor)
        lcd.text(self.x + int((self.length - lcd.textWidth(self.text)) / 2), self.y + self.borderwidth + 3, self.text)
        self.hideflag = 0

    def updatetext(self, argument):
        if isinstance(argument, str):
            self.text = getstrbylength(argument, self.length - self.borderwidth * 2 - 4, self.font)
        else:
            self.text = getstrbylength(str(argument), self.length - self.borderwidth * 2 - 4, self.font)
        if self.hideflag == 0:
            self.draw()
            self.focus()

    def hide(self):
        lcd.rect(self.x, self.y, self.length, self.fontheight + 4 + self.borderwidth * 2, WindowBColor,
                 WindowBColor)
        self.hideflag = 1

    def enble(self):
        self.enableflag = 1
        if self.hideflag == 0:
            self.draw()

    def disable(self):
        self.enableflag = 0
        if self.hideflag == 0:
            self.draw()

    def focus(self):
        if self.hideflag == 1:
            pass
        else:

            for i in range(4):
                lcd.roundrect(self.x + i, self.y + i, self.length - 2 * i,
                              self.fontheight + 4 + self.borderwidth * 2 - 2 * i, self.r - i, FocusColor)

    def unfocused(self):
        if self.hideflag == 1:
            pass
        else:
            if self.enableflag == 1:
                for i in range(4):
                    lcd.roundrect(self.x + i, self.y + i, self.length - 2 * i,
                                  self.fontheight + 4 + self.borderwidth * 2 - 2 * i, self.r - i, self.bcolor)
            else:
                for i in range(4):
                    lcd.roundrect(self.x + i, self.y + i, self.length - 2 * i,
                                  self.fontheight + 4 + self.borderwidth * 2 - 2 * i, self.r - i, self.disablecolor)

    def click(self):
        if self.enableflag == 1:
            if self.callback is None:
                pass
            else:
                if self.argument is None:
                    self.callback()
                else:
                    self.callback(self.argument)


class CheckBox:
    def __init__(self, x, y, width=30, color=0xF39C12, callback=None, status=0, hide=1):
        self.x = x
        self.y = y
        self.width = width
        self.boardwidth = 4
        self.color = color
        self.status = status
        self.callback = callback
        self.hideflag = hide

    def draw(self):
        lcd.roundrect(self.x, self.y, self.width, self.width, 5, self.color, self.color)
        lcd.rect(self.x + self.boardwidth, self.y + self.boardwidth, self.width - self.boardwidth * 2,
                 self.width - self.boardwidth * 2, WindowBColor, WindowBColor)
        if self.status == 1:
            lcd.circle(self.x + int(self.width / 2), self.y + int(self.width / 2),
                       int(self.width / 2 - self.boardwidth - 2), self.color, self.color)
        else:
            pass
        self.hideflag = 0

    def hide(self):
        lcd.roundrect(self.x, self.y, self.width, self.width, 5, WindowBColor, WindowBColor)
        self.hideflag = 1

    def checked(self):
        if self.hideflag == 0:
            lcd.circle(self.x + int(self.width / 2), self.y + int(self.width / 2),
                       int(self.width / 2 - self.boardwidth - 1), self.color, self.color)

        self.status = 1

    def unchecked(self):
        if self.hideflag == 0:
            lcd.circle(self.x + int(self.width / 2), self.y + int(self.width / 2),
                       int(self.width / 2 - self.boardwidth - 1), WindowBColor, WindowBColor)

        self.status = 0

    def focus(self):
        if self.hideflag == 0:
            for i in range(self.boardwidth):
                lcd.roundrect(self.x + i, self.y + i, self.width - i * 2, self.width - i * 2, 5 - i, FocusColor)
        else:
            pass

    def unfocused(self):
        if self.hideflag == 0:
            for i in range(self.boardwidth):
                lcd.roundrect(self.x + i, self.y + i, self.width - i * 2, self.width - i * 2, 5 - i, self.color)
        else:
            pass

    def click(self):
        if self.status == 1:
            self.unchecked()
        else:
            self.checked()
        if self.callback is not None:
            self.callback()


class HProgressBar:
    def __init__(self, x, y, length=100, width=20, color=lcd.RED, boardcolor=lcd.BLACK, value=0, minvalue=0,
                 maxvalue=100, hide=1, boardwidth=2):
        self.x = x
        self.y = y
        self.length = length
        self.width = width
        self.color = color
        self.boardcolor = boardcolor
        self.boardwidth = boardwidth
        self.minvalue = minvalue
        self.maxvalue = maxvalue
        if value < self.minvalue or value == self.minvalue:
            self.value = self.minvalue
        elif value > self.maxvalue or value == self.maxvalue:
            self.value = self.maxvalue
        else:
            self.value = value

        self.hideflag = hide

    def draw(self):
        lcd.roundrect(self.x, self.y, self.length, self.width, 4, self.boardcolor, self.boardcolor)
        lcd.rect(self.x + self.boardwidth, self.y + self.boardwidth, self.length - self.boardwidth * 2,
                 self.width - self.boardwidth * 2, WindowBColor, WindowBColor)
        if self.value == 0:
            pass
        else:
            temp = (self.value - self.minvalue) / (self.maxvalue - self.minvalue) * (self.length - self.boardwidth * 2)
            if temp == 0:
                pass
            elif temp < 1 or temp == 1:
                lcd.line(self.x + self.boardwidth, self.y + self.boardwidth, self.x + self.boardwidth,
                         self.y + self.boardwidth + self.width - self.boardwidth * 2, self.color)
            elif temp == self.length - self.boardwidth or temp > self.length - self.boardwidth:
                lcd.rect(self.x + self.boardwidth, self.y + self.boardwidth, self.length - self.boardwidth * 2,
                         self.width - self.boardwidth * 2, self.color, self.color)
            else:
                lcd.rect(self.x + self.boardwidth, self.y + self.boardwidth, round(temp),
                         self.width - self.boardwidth * 2, self.color, self.color)
            del temp
        self.hideflag = 0

    def hide(self):
        lcd.roundrect(self.x, self.y, self.length, self.width, 4, WindowBColor, WindowBColor)
        self.hideflag = 1

    def update(self, value=None):
        if self.hideflag == 0:

            if value is not None:
                if value < self.minvalue or value == self.minvalue:
                    value = self.minvalue
                elif value > self.minvalue and value < self.maxvalue:
                    pass
                elif value == self.maxvalue or value > self.maxvalue:
                    value = self.maxvalue
                else:
                    pass

                oldtemp = round((self.value - self.minvalue) / (self.maxvalue - self.minvalue) * (
                        self.length - self.boardwidth * 2))
                newtemp = round(
                    (value - self.minvalue) / (self.maxvalue - self.minvalue) * (self.length - self.boardwidth * 2))
                temp = newtemp - oldtemp
                if temp > 0:
                    lcd.rect(self.x + self.boardwidth + oldtemp, self.y + self.boardwidth, temp,
                             self.width - self.boardwidth * 2, self.color, self.color)
                elif temp < 0:
                    lcd.rect(self.x + self.boardwidth + newtemp, self.y + self.boardwidth, -temp,
                             self.width - self.boardwidth * 2, WindowBColor, WindowBColor)
                else:
                    pass
                self.value = value
                del oldtemp
                del newtemp
                del temp

        else:
            if value is None:
                pass
            else:
                if value > self.maxvalue:
                    self.value = self.maxvalue
                elif value < self.minvalue:
                    self.value = self.minvalue
                else:
                    self.value = value


class VProgressBar:
    def __init__(self, x, y, length=100, width=20, color=lcd.RED, boardcolor=lcd.WHITE, value=0, minvalue=0,
                 maxvalue=100, hide=1, boardwidth=4):
        self.x = x
        self.y = y
        self.length = length
        self.width = width
        self.color = color
        self.boardcolor = boardcolor
        self.boardwidth = boardwidth
        self.minvalue = minvalue
        self.maxvalue = maxvalue
        if value < self.minvalue or value == self.minvalue:
            self.value = self.minvalue
        elif value > self.maxvalue or value == self.maxvalue:
            self.value = self.maxvalue
        else:
            self.value = value

        self.hideflag = hide

    def draw(self):
        lcd.roundrect(self.x, self.y, self.width, self.length, 4, self.boardcolor, self.boardcolor)
        lcd.rect(self.x + self.boardwidth, self.y + self.boardwidth, self.width - self.boardwidth * 2,
                 self.length - self.boardwidth * 2, WindowBColor, WindowBColor)
        if self.value == 0:
            pass
        else:
            temp = (self.value - self.minvalue) / (self.maxvalue - self.minvalue) * (self.length - self.boardwidth * 2)
            if temp < 1 or temp == 1:
                lcd.line(self.x + self.boardwidth, self.y + self.length - self.boardwidth,
                         self.x + self.width - self.boardwidth, self.color)
            elif temp == self.length - self.boardwidth or temp > self.length - self.boardwidth:
                lcd.rect(self.x + self.boardwidth, self.y + self.boardwidth, self.width - self.boardwidth * 2,
                         self.length - self.boardwidth * 2, self.color, self.color)
            else:
                lcd.rect(self.x + self.boardwidth, self.y + self.length - self.boardwidth - round(temp),
                         self.width - self.boardwidth * 2, round(temp), self.color, self.color)
        self.hideflag = 0

    def hide(self):
        lcd.rect(self.x, self.y, self.width, self.length, WindowBColor, WindowBColor)
        self.hideflag = 1

    def update(self, value=None):
        if self.hideflag == 0:

            if value is not None:
                if value < self.minvalue or value == self.minvalue:
                    value = self.minvalue
                elif value > self.minvalue and value < self.maxvalue:
                    pass
                elif value == self.maxvalue or value > self.maxvalue:
                    value = self.maxvalue
                else:
                    pass
                oldtemp = round((self.value - self.minvalue) / (self.maxvalue - self.minvalue) * (
                        self.length - self.boardwidth * 2))
                newtemp = round((min(value, self.maxvalue) - self.minvalue) / (self.maxvalue - self.minvalue) * (
                        self.length - self.boardwidth * 2))
                temp = newtemp - oldtemp
                if temp > 0:
                    lcd.rect(self.x + self.boardwidth, self.y + self.length - self.boardwidth - newtemp,
                             self.width - self.boardwidth * 2, temp, self.color, self.color)
                    self.value = min(value, self.maxvalue)
                elif temp < 0:
                    lcd.rect(self.x + self.boardwidth, self.y + self.length - self.boardwidth - oldtemp,
                             self.width - self.boardwidth * 2, -temp, WindowBColor, WindowBColor)
                else:
                    pass
                self.value = value
                del oldtemp
                del newtemp
                del temp

        else:
            if value is None:
                pass
            else:
                if value > self.maxvalue:
                    self.value = self.maxvalue
                elif value < self.minvalue:
                    self.value = self.minvalue
                else:
                    self.value = value


class TextBox:
    def __init__(self, x, y, value="", color=lcd.WHITE, boardcolor=lcd.WHITE, bcolor=WindowBColor,
                 font=lcd.FONT_DejaVu24, length=100, pc=0, hide=1, boardwidth=2):
        # pc=0 左对齐 pc=1 居中对齐 pc=2，右对齐
        self.x = x
        self.y = y

        self.value = value

        self.color = color
        self.bcolor = bcolor
        self.boardcolor = boardcolor
        self.font = font
        lcd.font(self.font, fixedwidth=0)
        self.textheight = lcd.fontSize()[1]

        self.length = length
        self.pc = pc
        self.hideflag = hide

        self.boardwidth = boardwidth

        if isinstance(value, str):
            self.fronttext = getstrbylength(value, self.length - self.boardwidth * 2, self.font)
        else:
            self.fronttext = getstrbylength(str(value), self.length - self.boardwidth * 2, self.font)

        self.width = self.textheight + 4 + self.boardwidth * 2

    def draw(self):
        lcd.rect(self.x, self.y, self.length, self.textheight + self.boardwidth * 2 + 4, self.boardcolor,
                 self.boardcolor)
        lcd.rect(self.x + self.boardwidth, self.y + self.boardwidth, self.length - self.boardwidth * 2,
                 self.textheight + 4, self.bcolor, self.bcolor)
        if len(self.fronttext) == 0:
            pass
        else:
            lcd.font(self.font, fixedwidth=0)
            lcd.setColor(self.color, self.bcolor)
            lcd.text(self.x + self.boardwidth, self.y + self.boardwidth + 4, self.fronttext)
        self.hideflag = 0

    def hide(self):
        lcd.rect(self.x, self.y, self.length, self.textheight + self.boardwidth * 2 + 4, WindowBColor, WindowBColor)
        self.hideflag = 1

    def focus(self):
        if self.hideflag == 0:
            for i in range(self.boardwidth):
                lcd.rect(self.x + i, self.y + i, self.length - i * 2,
                         self.textheight + 4 + self.boardwidth * 2 - i * 2, FocusColor)

    def unfocused(self):
        if self.hideflag == 0:
            for i in range(self.boardwidth):
                lcd.rect(self.x + i, self.y + i, self.length - i * 2,
                         self.textheight + 4 + self.boardwidth * 2 - i * 2, self.boardcolor)

    def update(self, value):
        if self.hideflag == 0:

            if isinstance(value, str):
                temp = getstrbylength(value, self.length - self.boardwidth * 2, self.font)
            else:
                temp = getstrbylength(str(value), self.length - self.boardwidth * 2, self.font)
            lcd.font(self.font, fixedwidth=0)
            if lcd.textWidth(temp) > lcd.textWidth(self.fronttext):
                pass
            else:
                lcd.rect(self.x + self.boardwidth, self.y + self.boardwidth, self.length - self.boardwidth * 2,
                         self.textheight + 4, self.bcolor, self.bcolor)
            lcd.setColor(self.color, self.bcolor)
            lcd.text(self.x + self.boardwidth, self.y + self.boardwidth + 4, temp)
            self.fronttext = temp
            self.value = value

        else:
            self.value = value
            if isinstance(value, str):
                self.fronttext = getstrbylength(value, self.length - self.boardwidth * 2, self.font)
            else:
                self.fronttext = getstrbylength(str(value), self.length - self.boardwidth * 2, self.font)

    def click(self):
        pass


class ListBox:
    def __init__(self, x, y, listdate='None', index=0, length=100, font=lcd.FONT_DejaVu18, color=lcd.RED, boardcolor=0xF39C12,
                 bcolor=WindowBColor, boardwidth=4, hide=1):
        self.x = x
        self.y = y
        if isinstance(listdate,(list,tuple)):
            self.listdate = listdate
        else:
            self.listdate=[listdate]

        self.index = index
        self.length = length
        self.font = font
        self.color = color
        self.boardcolor = boardcolor
        self.bcolor = bcolor
        self.boardwidth = boardwidth

        lcd.font(self.font, fixedwidth=0)  # 设置成等宽字符
        self.fontheight = lcd.fontSize()[1]  # 获取字符长宽

        if isinstance(self.listdate[self.index], str):
            self.frontstr = getstrbylength(self.listdate[self.index],
                                           self.length - self.boardwidth * 3 - self.fontheight, self.font)
        else:
            self.frontstr = getstrbylength(str(self.listdate[self.index]),
                                           self.length - self.boardwidth * 3 - self.fontheight, self.font)

        self.hideflag = hide
        self.width = self.fontheight + self.boardwidth * 2 + 4

    def draw(self):
        lcd.rect(self.x, self.y, self.length, self.fontheight + self.boardwidth * 2 + 4, self.boardcolor,
                 self.boardcolor)
        lcd.rect(self.x + self.boardwidth, self.y + self.boardwidth, self.length - self.boardwidth * 2,
                 self.fontheight + 4, self.bcolor, self.bcolor)
        lcd.rect(self.x + self.length - self.boardwidth * 2 - self.fontheight, self.y + self.boardwidth,
                 self.boardwidth, self.fontheight + 4, self.boardcolor, self.boardcolor)
        lcd.triangle(self.x + self.length - self.boardwidth - self.fontheight, self.y + self.boardwidth * 2,
                     self.x + self.length - self.boardwidth, self.y + self.boardwidth * 2,
                     self.x + self.length - int(self.fontheight / 2) - self.boardwidth,
                     self.y + self.fontheight + self.boardwidth, self.color, self.color)
        if len(self.frontstr) == 0:
            pass
        else:
            lcd.font(self.font, fixedwidth=0)
            lcd.setColor(self.color, self.bcolor)
            lcd.text(self.x + self.boardwidth, self.y + self.boardwidth + 4, self.frontstr)
        self.hideflag = 0

    def hide(self):
        lcd.rect(self.x, self.y, self.length, self.fontheight + 4 + self.boardwidth * 2, WindowBColor, WindowBColor)
        self.hideflag = 1

    def focus(self):
        if self.hideflag == 0:
            for i in range(self.boardwidth):
                lcd.rect(self.x + i, self.y + i, self.length - 2 * i, self.fontheight + 4 + self.boardwidth * 2 - 2 * i,
                         FocusColor)

    def unfocused(self):
        if self.hideflag == 0:
            for i in range(self.boardwidth):
                lcd.rect(self.x + i, self.y + i, self.length - 2 * i, self.fontheight + 4 + self.boardwidth * 2 - 2 * i,
                         self.boardcolor)

    def add(self, value):
        self.listdate.append(value)

    def delete(self, index):
        if index > len(self.listdate) - 1:
            return 0
        else:
            del self.listdate[index]
            return 1

    def updatelistdate(self, argument):
        if isinstance(argument, (list, tuple)):
            self.listdate = argument
            self.index=0
            lcd.font(self.font, fixedwidth=0)  # 设置成等宽字符

            if isinstance(self.listdate[self.index], str):
                self.frontstr = getstrbylength(self.listdate[self.index],
                                               self.length - self.boardwidth * 3 - self.fontheight, self.font)
            else:
                self.frontstr = getstrbylength(str(self.listdate[self.index]),
                                               self.length - self.boardwidth * 3 - self.fontheight, self.font)
        else:
            print('listbox argument must be list or tuple!')
        if self.hideflag == 0 :
            lcd.rect(self.x + self.boardwidth, self.y + self.boardwidth,
                     self.length - self.boardwidth * 3 - self.fontheight, self.fontheight + 4, WindowBColor,
                     WindowBColor)
            if len(self.frontstr) == 0:
                pass
            else:
                lcd.font(self.font, fixedwidth=0)
                lcd.setColor(self.color, self.bcolor)
                lcd.text(self.x + self.boardwidth, self.y + self.boardwidth + 4, self.frontstr)

    def updatevalue(self, index, value):
        if index > len(self.listdate) - 1:
            return 0
        else:
            self.listdate[index] = value
            return 1

    def updateindex(self, index):
        if index > len(self.listdate) - 1:
            return 0
        else:
            self.index = index
            if isinstance(self.listdate[self.index], str):
                self.frontstr = getstrbylength(self.listdate[self.index],
                                               self.length - self.boardwidth * 3 - self.fontheight, self.font)
            else:
                self.frontstr = getstrbylength(str(self.listdate[self.index]),
                                               self.length - self.boardwidth * 3 - self.fontheight, self.font)
            if self.hideflag == 0:

                lcd.rect(self.x + self.boardwidth, self.y + self.boardwidth,
                         self.length - self.boardwidth * 3 - self.fontheight, self.fontheight + 4, WindowBColor,
                         WindowBColor)
                if len(self.frontstr) == 0:
                    pass
                else:
                    lcd.font(self.font, fixedwidth=0)
                    lcd.setColor(self.color, self.bcolor)
                    lcd.text(self.x + self.boardwidth, self.y + self.boardwidth + 4, self.frontstr)

        return 1

    def click(self):
        pass


##################################################

class DebugBox:
    def __init__(self, x, y, length, width, font=lcd.FONT_Default, bcolor=WindowBColor, fontcolor=lcd.WHITE,
                 hide=1):
        self.x = x
        self.y = y
        self.length = length
        self.width = width
        self.fontcolor = fontcolor
        self.bcolor = bcolor
        self.font = font

        lcd.font(self.font, fixedwidth=0)
        self.textheight = lcd.fontSize()[1]

        self.lines = int(self.width / self.textheight)
        self.dateche = [[0, ""] for i in range(self.lines)]

        self.hideflag = hide

        self.count = 0

    def draw(self):
        lcd.rect(self.x, self.y, self.length, self.width, self.bcolor, self.bcolor)
        lcd.setColor(self.fontcolor, self.bcolor)
        lcd.font(self.font, fixedwidth=0)
        for i in range(len(self.dateche)):
            if self.dateche[i][0] != 0:
                lcd.text(self.x, self.y + i * self.textheight, self.dateche[i][1])
        self.hideflag = 0

    def clear(self):
        if self.hideflag != 1:
            lcd.rect(self.x, self.y, self.length, self.width, self.bcolor, self.bcolor)

    def hide(self):
        lcd.rect(self.x, self.y, self.length, self.width, WindowBColor, WindowBColor)
        self.hideflag = 1

    def update(self, argument):
        if isinstance(argument, str):  # 获取字符串
            argument = argument
        else:
            argument = str(argument)
        temp = []
        lcd.font(self.font, fixedwidth=0)
        if lcd.textWidth(argument) <= self.length:
            temp = [[lcd.textWidth(argument), argument]]
        else:
            while True:
                a = getstrbylength(argument, self.length, self.font, fixedwidth=0)
                temp.append([lcd.textWidth(a), a])
                argument = argument[len(a) + 1:]
                if lcd.textWidth(argument) <= self.length:
                    temp.append([lcd.textWidth(argument), argument])
                    break
                else:
                    pass
        if len(temp) > 0:  # 数据不为0

            lcd.setColor(self.fontcolor, self.bcolor)
            lcd.font(self.font, fixedwidth=0)
            for i in range(len(temp)):
                if self.count <= self.lines - 1:
                    self.dateche[self.count] = temp[i]
                    if self.hideflag == 0:
                        lcd.text(self.x, self.y + self.textheight * self.count, self.dateche[self.count][1])

                    self.count += 1
                else:
                    for n in range(self.lines - 1):
                        if self.hideflag == 0:

                            if self.dateche[n][0] <= self.dateche[n + 1][0]:
                                lcd.text(self.x, self.y + self.textheight * n, self.dateche[n + 1][1])
                            else:
                                lcd.rect(self.x, self.y + self.textheight * n, self.dateche[n][0], self.textheight,
                                         self.bcolor, self.bcolor)
                                lcd.text(self.x, self.y + self.textheight * n, self.dateche[n + 1][1])
                            self.dateche[n] = self.dateche[n + 1]

                    if self.hideflag == 0:

                        if self.dateche[self.lines - 1][0] <= temp[i][0]:
                            lcd.text(self.x, self.y + self.textheight * (self.lines - 1), temp[i][1])
                        else:
                            lcd.rect(self.x, self.y + self.textheight * (self.lines - 1),
                                     self.dateche[self.lines - 1][0], self.textheight, self.bcolor, self.bcolor)
                            lcd.text(self.x, self.y + self.textheight * (self.lines - 1), temp[i][1])

                    self.dateche[self.lines - 1] = temp[i]
                    self.count += 1
