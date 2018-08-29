import ujson
import urequests
import m5gui
from m5stack import lcd
from m5stack import buttonA
from m5stack import buttonB
from m5stack import buttonC
import network
import utime
import gc
import faces
import _thread as thread
import machine

keyboard = faces.Faces()  # 键盘

window = m5gui.Window(hidebtn=1)  # 定义窗口

page1 = m5gui.Page()  # 页面1
page2 = m5gui.Page()  # 页面2

debug_date = []  # debug数据列表
debug_count = 0  # debug计数
internet_date = {}  # 网络数据
display_index = 0  # 显示序列
start_flag = 0  # 开始接收数据标志

wifi = network.WLAN(network.STA_IF)
wifi.active(True)

datebase = None
namelist = None
try:
    datebase = ujson.load(open("TTwatcher_datebase.json"))
    namelist = list(datebase['info'].keys())
    codelist = []
    for i in namelist:
        codelist.append(datebase['info'][i])
    debug_date.append('read datebase success')
    wifi.connect(datebase['wifi']['ssid'], datebase['wifi']['pwd'])
    window.setbrightness(datebase['brightness'])
except:
    debug_date.append('read datebase fail')
    datebase = {'info': {}, 'wifi': {'ssid': "", 'pwd': ""},'brightness':510}
#######################################################################################################################
title_lable = m5gui.Lable(0, 0, text="--------", length=320, pc=1, font="/flash/font/dg24.fon")  # 标题
jzrq_lable = m5gui.Lable(0, 27, text="--------", length=160, font="/flash/font/dg18.fon")  # 净值日期
dwjz_lable = m5gui.Lable(0, 47, text="--------", length=160, color=lcd.RED, font="/flash/font/dg18.fon")  # 单位净值
gsrq_lable = m5gui.Lable(160, 27, text="--------", pc=2, length=150, font="/flash/font/dg18.fon")
gsz_lable = m5gui.Lable(160, 47, text="--------", length=150, color=lcd.RED, pc=2, font="/flash/font/dg18.fon")
gszzl_lable = m5gui.Lable(0, 67, text="--------", length=320, color=lcd.RED, underline=1, font="/flash/font/ep48.fon",
                          pc=1)
debug = m5gui.DebugBox(2, 115, length=200, width=120, fontcolor=lcd.WHITE, bcolor=lcd.DARKGREY)

p_btn = m5gui.Button(210, 115, text="<", length=40)
n_btn = m5gui.Button(260, 115, text=">", length=40)

stop_btn = m5gui.Button(210, 165, text="STOP" if start_flag else "START", length=98, font="/flash/font/dg18.fon")
set_btn = m5gui.Button(210, 210, text="SET", length=98, font="/flash/font/dg18.fon")

page1.add(title_lable, jzrq_lable, dwjz_lable, gsrq_lable, gszzl_lable, gsz_lable, debug, p_btn, n_btn, stop_btn,
          set_btn)
#######################################################################################################################
y = 1

ssid_label = m5gui.Lable(0, y + 6, text="SSID:", length=48, pc=2, font=lcd.FONT_Default)
ssid_text = m5gui.TextBox(50, y, value="", length=80, font=lcd.FONT_Default)
pwd_label = m5gui.Lable(132, y + 6, text="PWD:", length=48, pc=2, font=lcd.FONT_Default)
pwd_text = m5gui.TextBox(182, y, value="", length=70, font=lcd.FONT_Default)
con_btn = m5gui.Button(260, y, text="GO", length=50, font=lcd.FONT_Default)

y = 29
del_name_label = m5gui.Lable(0, y + 6, text="Name:", length=48, pc=2, font=lcd.FONT_Default)
del_name_list = m5gui.ListBox(50, y, listdate=['None'], length=200, font=lcd.FONT_Default, boardwidth=2)
del_btn = m5gui.Button(260, y, text="DEL", length=50, font=lcd.FONT_Default)

y = 59

add_name_label = m5gui.Lable(0, y + 6, text="Name:", length=48, pc=2, font=lcd.FONT_Default)
add_name_text = m5gui.TextBox(50, y, value="", length=80, font=lcd.FONT_Default)
add_code_label = m5gui.Lable(132, y + 6, text="Code:", length=48, pc=2, font=lcd.FONT_Default)
add_code_text = m5gui.TextBox(182, y, value="", length=70, font=lcd.FONT_Default)
add_btn = m5gui.Button(260, y, text="ADD", length=50, font=lcd.FONT_Default)

y = 85

brightness_label = m5gui.Lable(0, y + 6, text="brightness", length=80, pc=2, font=lcd.FONT_Default)
brightness_up_btn = m5gui.Button(85, y, text="-", length=50, font="/flash/font/dg18.fon")
brightness_progressbar = m5gui.HProgressBar(140, y, 115, 25, value=datebase['brightness'], maxvalue=1010, minvalue=10)
brightness_down_btn = m5gui.Button(260, y, text="+", length=50, font="/flash/font/dg18.fon")

save_btn = m5gui.Button(210, 115, text="SAVE", length=98, font="/flash/font/dg18.fon")
wifi_info_btn = m5gui.Button(210, 165, text="INFO", length=98, font="/flash/font/dg18.fon")
return_btn = m5gui.Button(210, 210, text="RETURN", length=98, font="/flash/font/dg18.fon")

page2.add(ssid_label, ssid_text, pwd_label, pwd_text, con_btn, del_name_label, del_name_list, del_btn, add_name_label,
          add_name_text, add_code_label,
          add_code_text, add_btn, brightness_label, brightness_up_btn, brightness_progressbar, brightness_down_btn,
          save_btn, wifi_info_btn, return_btn, debug)


#######################################################################################################################

#######################################################################################################################
#连接wifi
def connect_wifi(ssid,pwd):
    global wifi
    wifi.connect(ssid,pwd)
# 亮度设置
def set_brightness(argument):
    global window
    if argument == 1:
        window.brightness += 50
        if window.brightness > brightness_progressbar.maxvalue:
            window.brightness = brightness_progressbar.maxvalue
        window.setbrightness(window.brightness)
    elif argument == 2:
        window.brightness -= 50
        if window.brightness < brightness_progressbar.minvalue:
            window.brightness = brightness_progressbar.minvalue
        window.setbrightness(window.brightness)
    brightness_progressbar.update(window.brightness)
    print(window.brightness)


# debug窗口显示函数
def de(argument):
    global debug
    global debug_count
    debug.update("{}:{}".format(debug_count, argument))
    debug_count += 1


# 页面切换函数
def pagechang(argument):
    global window
    if argument == 0:
        window.page_clear(window.page[window.current_page])
        window.current_page = 0
        window.page_show(window.page[window.current_page])
    elif argument == 1:
        window.page_clear(window.page[window.current_page])
        window.current_page = 1
        window.page_show(window.page[window.current_page])


# 获取网络数据线程函数
def get_date(id):
    thread.allowsuspend(True)
    global debug_date
    global datebase
    global namelist
    global internet_date
    global display_index
    global start_flag
    baseurl_1 = "http://fundgz.1234567.com.cn/js/"
    baseurl_2 = ".js?rt=1463558676006"
    while True:
        if start_flag == 1:
            utime.sleep(5)
            debug_date.append('start get date')
            url = baseurl_1 + datebase["info"][namelist[display_index]] + baseurl_2
            try:
                temp = urequests.get(url).text
                d = ujson.loads(temp[temp.find("(") + 1:temp.find(")")])
                internet_date[namelist[display_index]] = d
                del temp
            except:
                internet_date[namelist[display_index]] = None
            debug_date.append('finish')
            thread.notify(id, 1001)
            gc.collect()


# 显示函数
def display():
    global internet_date
    global display_index
    global debug_date
    global namelist
    global datebase
    if internet_date == {}:
        pass
    else:
        try:
            temp = internet_date[namelist[display_index]]
            if temp is not None:
                title_lable.update("{}-{}".format(namelist[display_index], temp['fundcode']))
                jzrq_lable.update(temp['jzrq'])

                if temp['dwjz'][0] == "-":
                    # dwjz_lable.color = lcd.DARKGREEN
                    dwjz_lable.color = lcd.BLACK
                else:
                    dwjz_lable.color = lcd.RED
                dwjz_lable.update(temp['dwjz'])

                gsrq_lable.update(temp['gztime'][temp['gztime'].find('-') + 1:])

                if temp['gsz'][0] == "-":
                    # gsz_lable.color = lcd.DARKGREEN
                    gsz_lable.color = lcd.BLACK
                else:
                    gsz_lable.color = lcd.RED
                gsz_lable.update(temp['gsz'])

                if temp['gszzl'][0] == "-":
                    # gszzl_lable.color = lcd.DARKGREEN
                    gszzl_lable.color = lcd.BLACK
                else:
                    gszzl_lable.color = lcd.RED
                gszzl_lable.update(temp['gszzl'])
        except:
            debug_date.append('{} date error!'.format(namelist[display_index]))

            title_lable.update("{}-{}".format(namelist[display_index], datebase['info'][namelist[display_index]]))
            dwjz_lable.update("---")
            jzrq_lable.update("---")
            gsrq_lable.update("---")
            gsz_lable.update("---")
            gszzl_lable.update("---")


# 显示索引切换函数
def display_index_switch(argumen):
    global display_index
    global namelist
    global display
    if argumen == 1:
        if display_index == len(namelist) - 1:
            display_index = 0
        else:
            display_index += 1
    elif argumen == 2:
        if display_index == 0:
            display_index = len(namelist) - 1
        else:
            display_index -= 1
    display()


# 获取wifi信息
def wifi_info():
    global wifi
    global debug_date
    temp = wifi.ifconfig()
    print("ifconfig:", temp)
    for i in temp:
        debug_date.append(i)

    temp = wifi.config('all')
    print("config:", temp)
    debug_date.append(temp)


# 连接wifi
def connect_wifi():
    global wifi
    global debug_date
    if wifi.isconnected():
        debug_date.append('disconnect wifi')

    if ssid_text.value != "":
        debug_date.append('connect to {}'.format(ssid_text.value))
        wifi.connect(ssid_text.value, pwd_text.value)
    else:
        debug_date.append('input ssid')


# 清除wifi输入窗口数据
def cls():
    ssid_text.update("")
    pwd_text.update("")


# 开始函数
def start_fun():
    global start_flag
    global stop_btn
    if start_flag == 1:
        start_flag = 0
        stop_btn.updatetext('START')
    elif start_flag == 0:
        start_flag = 1
        stop_btn.updatetext('STOP')


# 根据名字删除info条目
def del_name():
    global namelist
    global debug_date
    global datebase
    index = del_name_list.index
    if namelist is not None:
        if len(namelist) == 1:
            debug_date.append('can not del last one')
        else:
            debug_date.append('del {}'.format(namelist[index]))
            del datebase['info'][namelist[index]]
            namelist = list(datebase['info'].keys())
            del_name_list.updatelistdate(namelist)


# 增加条目
def add_name():
    global namelist
    global debug_date
    global datebase
    if namelist is not None:
        debug_date.append("add {}".format(add_name_text.value))
        datebase['info'][add_name_text.value] = add_code_text.value
        namelist = list(datebase['info'].keys())
        del_name_list.updatelistdate(namelist)


# 保存config到json文件
def save_datebase():
    global datebase
    datebase['wifi']['ssid'] = ssid_text.value
    datebase['wifi']['pwd'] = pwd_text.value
    datebase['brightness']=window.brightness
    f = open("TTwatcher_datebase.json", 'w')
    try:
        f = open("TTwatcher_datebase.json", 'w')
        f.write(ujson.dumps(datebase))
        f.close()
        debug_date.append('save file success')
    except:
        debug_date.append('save file fail')
    f.close()

#定时器函数
def timer_fun(t):
    print('time\'s up')
#######################################################################################################################
p_btn.callback = display_index_switch
p_btn.argument = 1
n_btn.callback = display_index_switch
n_btn.argument = 2

set_btn.callback = pagechang
set_btn.argument = 1
return_btn.callback = pagechang
return_btn.argument = 0

wifi_info_btn.callback = wifi_info

stop_btn.callback = start_fun

del_btn.callback = del_name
add_btn.callback = add_name
save_btn.callback = save_datebase

brightness_down_btn.callback = set_brightness
brightness_down_btn.argument = 1
brightness_up_btn.callback = set_brightness
brightness_up_btn.argument = 2

con_btn.callback=connect_wifi

# con_btn.callback=connect_wifi
# clear_btn.callback=cls
#######################################################################################################################
def main():
    thread.allowsuspend(True)
    gc_count = 0
    if datebase is None:
        pass
    else:
        ssid_text.update(datebase['wifi']['ssid'])
        pwd_text.update(datebase['wifi']['pwd'])
        del_name_list.updatelistdate(namelist)
    while True:
        if buttonA.wasPressed(callback=None):
            window.event(1)
        elif buttonB.wasPressed(callback=None):
            window.event(2)
        elif buttonC.wasPressed(callback=None):
            window.event(3)
        #temp = keyboard.read()
        #if temp != b'\x00':
            #window.event(temp)
            #print(temp)

        ntf = thread.getnotification()
        if ntf:
            if ntf == 1001:  # 获取数据
                # print(internet_date)
                display()
                gc_count += 1
                # gc.collect()

        # 将debug_date 数据显示到debug窗口
        if len(debug_date) > 0:
            de(debug_date[0])
            del debug_date[0]
            gc_count += 1

        if gc_count > 20:
            gc.collect()
            gc_count = 0


window.page.append(page1)
window.page.append(page2)
window.active()

# thread.stack_size(1024*8*10)

thread.stack_size(1024 * 8 * 10)
main_thread = thread.start_new_thread('main', main, ())  # windows线程
get_date_thread = thread.start_new_thread('get_date', get_date, (main_thread,))  # 获取数据线程

machine.heap_info()
thread.list()
