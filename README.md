# m5stack
gui for m5stack by micropython
hi，everyone：

我用micropython写的M5stack的简易文本GUI，带button，lable,textbox,CheckBox,HProgressBar,VProgressBar,TextBox,

ListBox,DebugBox这几个控件，具体使用方法可以参加源码。

值得说的是m5gui.py中有一个class Window和class
Page,实例化后的Page用于存放上述的控件，Window里面的page列表存放Page，这样window.active后只需给window.event传入数字1（buttonA），2（buttonB），3（buttonC）即可执行相应的控件切换以及控件connect的函数事件，具体可参照附件TT.app.py源码，此源码中包含更多的控件的用法。

PS:

1.  boot.py后运行main.py，main.py会挂载SD卡，并扫描flash和sd两处里面的文件（flash里面读到以.app.py结尾的文件视为APP，sd卡读到.app结尾的文件夹视为APP（此时文件夹内的APP文件名为main.py））

2.  main.py运行是需要的字体文件在font文件夹，将文件夹内的字体文件拷贝到/flash/font文件夹内

3.  main.py运行是需要图片文件“m5stack.jpg”，放入/flash

4.  例子TT.app.py中除了checkbox外，其余看见都有用到，可以参考，此例子是通过网络获取基金的实时涨跌，也算一个小看板，另外此例子还需要用到TTwatcher_datebase.json，一并放入/flash

5.  此GUI是我业余时间断断续续写的，再加上我是业余的，有闹笑话之处，欢迎指出！谢谢

6.  视频地址：[Youku](https://v.youku.com/v_show/id_XMzgwMTUxMTAxMg==.html?spm=a2h0k.11417342.soresults.dposter)

>   [Youtube](https://youtu.be/mV5-a0F4_p8)

