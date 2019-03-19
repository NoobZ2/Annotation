from tkinter import *
import hashlib
import time
from tkinter import filedialog
import chardet
import math
import pickle
import os.path
import platform
import tkinter
from tkinter import font as tkFont

LOG_LINE_NUM = 0


class Example(Frame):
    def __init__(self, init_window_name):
        Frame.__init__(self, init_window_name)
        self.Version = "YEDDA-V1.0 Annotator"
        self.init_window_name = init_window_name
        self.OS = platform.system().lower()
        self.parent = init_window_name
        self.fileName = ""
        self.debug = False
        self.colorAllChunk = True
        self.recommendFlag = True
        self.allKey = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
        self.controlCommand = {'q': "unTag", 'ctrl+z': 'undo'}
        self.labelEntryList = []
        self.shortcutLabelList = []
        self.configListLabel = None
        self.configListBox = None
        # default GUI display parameter
        self.textRow = 20
        self.textColumn = 5
        self.tagScheme = "BMES"
        self.onlyNP = False  ## for exporting sequence
        self.keepRecommend = True
        self.seged = True  ## False for non-segmentated Chinese, True for English or Segmented Chinese
        self.configFile = "configs/default.config"
        self.entityRe = r'\[\@.*?\#.*?\*\](?!\#)'
        self.insideNestEntityRe = r'\[\@\[\@(?!\[\@).*?\#.*?\*\]\#'
        self.recommendRe = r'\[\$.*?\#.*?\*\](?!\#)'
        self.goldAndrecomRe = r'\[\@.*?\#.*?\*\](?!\#)'
        if self.keepRecommend:
            self.goldAndrecomRe = r'\[[\@\$)].*?\#.*?\*\](?!\#)'
        ## configure color
        self.entityColor = "SkyBlue1"
        self.insideNestEntityColor = "light slate blue"
        self.recommendColor = 'lightgreen'
        self.selectColor = 'light salmon'
        self.textFontStyle = "Times"
        self.initUI()

    def initUI(self):
        self.init_window_name.title("电子病历标注工具_v1.1   by: 黄磊")  # 窗口名
        # self.init_window_name.geometry('320x160+10+10')                         #290 160为窗口大小，+10 +10 定义窗口弹出时的默认展示位置
        self.init_window_name.geometry('1068x681+10+10')
        # self.init_window_name["bg"] = "pink"                                    #窗口背景色，其他背景色见：blog.csdn.net/chl0000/article/details/7657887
        # self.init_window_name.attributes("-alpha",0.9)                          #虚化，值越小虚化程度越高
        # 标签
        self.init_data_label = Label(self.init_window_name, text="待处理数据")
        self.init_data_label.grid(row=0, column=0)
        self.result_data_label = Label(self.init_window_name, text="输出结果")
        self.result_data_label.grid(row=0, column=12)
        self.log_label = Label(self.init_window_name, text="日志")
        self.log_label.grid(row=12, column=0)
        self.lbl = Label(self, text="File: no file is opened")
        self.lbl.grid(sticky=W, pady=4, padx=5)
        # 文本框

        self.cursorIndex = Label(self, text=("row: %s\ncol: %s" % (0, 0)), foreground="red",
                                 font=(self.textFontStyle, 14, "bold"))
        self.cursorIndex.grid(row=10, column=self.textColumn + 1, pady=4)
        self.init_data_Text = Text(self.init_window_name, width=67, height=35)  # 原始数据录入框
        # self.init_data_Text.
        self.init_data_Text.grid(row=1, column=0, rowspan=10, columnspan=10)
        self.result_data_Text = Text(self.init_window_name, width=70, height=49)  # 处理结果展示
        self.result_data_Text.grid(row=1, column=12, rowspan=15, columnspan=10)
        self.log_data_Text = Text(self.init_window_name, width=66, height=9)  # 日志框
        self.log_data_Text.grid(row=13, column=0, columnspan=10)


        self.init_data_Text.bind("<ButtonRelease-1>", self.singleLeftClick)
        # 按钮
        # 标记解剖部位按钮
        self.show_button = Button(self.init_window_name, text="解剖部位", width='8', command=self.show_jpbw)
        self.show_button.grid(row=2, column=11)
        # 标记症状描述按钮
        self.show_button = Button(self.init_window_name, text="症状描述", width='8', command=self.show_zzms)
        self.show_button.grid(row=3, column=11)
        # 标记独立症状按钮
        self.show_button = Button(self.init_window_name, text="独立症状", width='8', command=self.show_dlzz)
        self.show_button.grid(row=4, column=11)
        # 标记药物按钮
        self.show_button = Button(self.init_window_name, text="药物", width='8', command=self.show_yw)
        self.show_button.grid(row=5, column=11)
        # 标记手术按钮
        self.show_button = Button(self.init_window_name, text="手术", width='8', command=self.show_ss)
        self.show_button.grid(row=6, column=11)
        # self.str_trans_to_md5_button = Button(self.init_window_name, text="字符串转MD5", bg="lightblue", width=10,command=self.str_trans_to_md5)  # 调用内部方法  加()为直接调用
        # self.str_trans_to_md5_button.grid(row=1, column=11)
        # 导入文件按钮
        self.input_button = Button(self.init_window_name, text="导入文件", bg="lightgreen", width=8, command=self.openfile)
        self.input_button.grid(row=0, column=2)
        # 输入窗口清空按钮
        self.delet_input_button = Button(self.init_window_name, text="一键清空", bg="red", width=8,
                                         command=self.delet_ofInput)
        self.delet_input_button.grid(row=0, column=3)
        # 展示窗口清空按钮
        self.delet_result_button = Button(self.init_window_name, text="一键清空", bg="red", width=8,
                                          command=self.delet_ofResult)

        self.delet_result_button.grid(row=0, column=13)




    def singleLeftClick(self, event):
        if self.debug:
            print ("Action Track: singleLeftClick")
        cursor_index = self.init_data_Text.index(INSERT)
        row_column = cursor_index.split('.')
        cursor_text = ("row: %s\ncol: %s" % (row_column[0], row_column[-1]))
        self.cursorIndex.config(text=cursor_text)
        print(cursor_text)

     # 标记解剖部位
    def show_jpbw(self):
        start_index = str(s)
        start_index = start_index[2:]
        start_index = int(start_index)

        end_index = str(e)
        end_index = end_index[2:]
        end_index = int(end_index)

        print(end_index)

        content = self.init_data_Text.get(s, e) + "\t" + str(start_index) + "\t" + str(
                end_index) + "\t" + "解剖部位" + "\n"
        print(content)
        self.result_data_Text.insert(END, content)

        # 标记症状描述
    def show_zzms(self):
        start_index = str(s)
        start_index = start_index[2:]
        start_index = int(start_index)

        end_index = str(e)
        end_index = end_index[2:]
        end_index = int(end_index)

        print(end_index)

        content1 = self.init_data_Text.get(s, e) + "\t" + str(start_index) + "\t" + str(
                end_index) + "\t" + "标记症状" + "\n"
        print(content1)
        self.result_data_Text.insert(END, content1)

        # 标记独立症状
    def show_dlzz(self):
        start_index = str(s)
        start_index = start_index[2:]
        start_index = int(start_index)

        end_index = str(e)
        end_index = end_index[2:]
        end_index = int(end_index)

        print(end_index)

        content2 = self.init_data_Text.get(s, e) + "\t" + str(start_index) + "\t" + str(
                end_index) + "\t" + "独立症状" + "\n"
        print(content2)
        self.result_data_Text.insert(END, content2)

        # 标记药物
    def show_yw(self):
        start_index3 = s
        end_index3 = e

        start_index3 = int(math.modf((start_index3 - 1) * pow(10, len(str(start_index3)) - 2))[1])

        end_index3 = int(math.modf((end_index3 - 1) * pow(10, len(str(end_index3)) - 2))[1])

        content3 = self.init_data_Text.get(s, e) + "\t" + str(start_index3) + "\t" + str(
                end_index3) + "\t" + "药物" + "\n"
        print(content3)
        self.result_data_Text.insert(END, content3)

        # 标记手术
    def show_ss(self):
        start_index4 = s
        end_index4 = e

        start_index4 = int(math.modf((start_index4 - 1) * pow(10, len(str(start_index4)) - 2))[1])

        end_index = int(math.modf((end_index4 - 1) * pow(10, len(str(end_index4)) - 2))[1])

        content4 = self.init_data_Text.get(s, e) + "\t" + str(start_index4) + "\t" + str(
                end_index4) + "\t" + "手术" + "\n"
        print(content4)
        self.result_data_Text.insert(END, content4)
     # 输入窗口一键清空功能
    def delet_ofInput(self):
        self.init_data_Text.delete('1.0', 'end')

        # 结果窗口一键清空功能
    def delet_ofResult(self):
        self.result_data_Text.delete('1.0', 'end')

        # 打开文件功能
    def openfile(self):
        ftypes = [('all files', '.*'), ('text files', '.txt'), ('ann files', '.ann')]
        dlg = filedialog.Open(self, filetypes=ftypes)
        # file_opt = options =  {}
        # options['filetypes'] = [('all files', '.*'), ('text files', '.txt')]
        # dlg = tkFileDialog.askopenfilename(**options)
        fl = dlg.show()
        if fl != '':
            self.init_data_Text.delete("1.0", END)
            text = self.readFile(fl)
            self.init_data_Text.insert(END, text)
            self.setNameLabel("File: " + fl)
            self.autoLoadNewFile(self.fileName, "1.0")
            # self.setDisplay()
            # self.initAnnotate()
            self.init_data_Text.mark_set(INSERT, "1.0")
            self.setCursorLabel(self.init_data_Text.index(INSERT))

    def readFile(self, filename):
        f = open(filename, "rU")
        text = f.read()
        self.fileName = filename
        return text

    def setFont(self, value):
        _family = self.textFontStyle
        _size = value
        _weight = "bold"
        _underline = 0
        fnt = tkFont.Font (family=_family, size=_size, weight=_weight, underline=_underline)
        Text(self, font=fnt)

    def setNameLabel(self, new_file):
        self.lbl.config(text=new_file)

    def setCursorLabel(self, cursor_index):
        if self.debug:
            print
            "Action Track: setCursorLabel"
        row_column = cursor_index.split('.')
        cursor_text = ("row: %s\ncol: %s" % (row_column[0], row_column[-1]))
        self.cursorIndex.config(text=cursor_text)

    def autoLoadNewFile(self, fileName, newcursor_index):
        if self.debug:
            print
            "Action Track: autoLoadNewFile"
        if len(fileName) > 0:
            self.init_data_Text.delete("1.0", END)
            text = self.readFile(fileName)
            self.init_data_Text.insert("end-1c", text)
            self.setNameLabel("File: " + fileName)
            self.init_data_Text.mark_set(INSERT, newcursor_index)
            self.init_data_Text.see(newcursor_index)
            self.setCursorLabel(newcursor_index)


        # 获取当前时间
    def get_current_time(self):
        current_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        return current_time

def main():
    print("SUTDAnnotator launched!")
    print(("OS:%s")%(platform.system()))
    root = Tk()
    root.geometry("1300x700+200+200")
    app = Example(root)
    app.setFont(17)
    root.mainloop()


if __name__ == '__main__':
    main()





