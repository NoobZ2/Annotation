#1.4 版本 使用ttk包重写程序，优化文件读取，提供历史查看
from tkinter import *
import hashlib
import time
from tkinter import filedialog
from tkinter import ttk
import chardet
import math
import tkinter
import numpy as np
from tkinter.scrolledtext import ScrolledText
import tkinter.font as tkFont
import os
from tkinter.messagebox import showinfo
import json

LOG_LINE_NUM = 0




class MY_GUI():




    def __init__(self,init_window_name):
        self.init_window_name = init_window_name
        self.max1=""
        self.filename=""


    #设置窗口
    def set_init_window(self):
        # 设置输入输出框字体
        ft = tkFont.Font(family='宋体', size=15)


        self.init_window_name.title("电子病历标注工具_v1.3   ")           #窗口名
        #self.init_window_name.geometry('320x160+10+10')                         #290 160为窗口大小，+10 +10 定义窗口弹出时的默认展示位置
        self.init_window_name.geometry('1500x1000+10+10')
        #self.init_window_name["bg"] = "pink"                                    #窗口背景色，其他背景色见：blog.csdn.net/chl0000/article/details/7657887
        #self.init_window_name.attributes("-alpha",0.9)                          #虚化，值越小虚化程度越高
        #标签
        self.init_data_label = ttk.Label(self.init_window_name, text="待处理数据")
        self.init_data_label.grid(row=0, column=0)
        self.result_data_label = ttk.Label(self.init_window_name, text="输出结果")
        self.result_data_label.grid(row=0, column=12)
        self.log_label = ttk.Label(self.init_window_name, text="日志")
        self.log_label.grid(row=12, column=0)
        self.cursorIndex = Label(self.init_window_name, text=("row: %s\ncol: %s" % (0, 0)))
        self.cursorIndex.grid(row=10, column=15, pady=4)

        #文本框

        self.init_data_Text = ScrolledText(self.init_window_name, width=67, height=35,font=ft)  #原始数据录入框
        self.init_data_Text.grid(row=1, column=0, rowspan=10, columnspan=10)
        self.result_data_Text = ScrolledText(self.init_window_name, width=70, height=49,font=ft)  #处理结果展示
        self.result_data_Text.grid(row=1, column=12, rowspan=15, columnspan=10)
        self.log_data_Text = ScrolledText(self.init_window_name, width=66, height=9)  # 日志框
        self.log_data_Text.grid(row=13, column=0, columnspan=10)
        self.init_data_Text.bind("<Button-1>", self.button_start)
        self.init_data_Text.bind("<ButtonRelease-1>", self.button_end)

        #按钮
        # self.str_trans_to_md5_button = Button(self.init_window_name, text="字符串转MD5", bg="lightblue", width=10,command=self.str_trans_to_md5)  # 调用内部方法  加()为直接调用
        # self.str_trans_to_md5_button.grid(row=1, column=11)
        #导入文件按钮
        self.input_button = ttk.Button(self.init_window_name,text="导入文件",width=8,command=self.openfile)
        self.input_button.grid(row=0, column=2)
        # 输入窗口清空按钮
        self.delet_input_button = ttk.Button(self.init_window_name, text="一键清空",  width=8,command=self.delet_ofInput)
        self.delet_input_button.grid(row=0, column=3)
        #展示窗口清空按钮
        self.delet_result_button = ttk.Button(self.init_window_name, text="一键清空",  width=8,command=self.delet_ofResult)
        self.delet_result_button.grid(row=0,column=13)
        #导出文件按钮
        self.output_button = ttk.Button(self.init_window_name,text="导出文件",width=8,command=self.outputfile)
        self.output_button.grid(row=0,column=14)
        #标记解剖部位按钮
        self.show_button = ttk.Button(self.init_window_name,text="解剖部位",width='8',command=self.show_jpbw)
        self.show_button.grid(row=2, column=11)
        # 标记症状描述按钮
        self.show_button = ttk.Button(self.init_window_name, text="症状描述", width='8', command=self.show_zzms)
        self.show_button.grid(row=3, column=11)
        # 标记独立症状按钮
        self.show_button = ttk.Button(self.init_window_name, text="独立症状", width='8', command=self.show_dlzz)
        self.show_button.grid(row=4, column=11)
        # 标记药物按钮
        self.show_button =ttk. Button(self.init_window_name, text="药物",width='8', command=self.show_yw)
        self.show_button.grid(row=5, column=11)
        # 标记手术按钮
        self.show_button = ttk.Button(self.init_window_name, text="手术", width='8', command=self.show_ss)
        self.show_button.grid(row=6, column=11)
        # 恢复操作按钮
        self.recover_button = ttk.Button(self.init_window_name, text="恢复", width='8', command=self.recover)
        self.recover_button.grid(row=0,column =15)
        # 标注撤销功能ctrl+z实现
        self.back_button = ttk.Button(self.init_window_name, text="撤销", width='8', command=self.backToHistory)
        self.back_button.grid(row=0, column=16)
        self.result_data_Text.bind('<Control-Key-z>',self.backToHistory)

        self.result_data_Text.edit_separator()

    #功能函数
    def str_trans_to_md5(self):
        src = self.init_data_Text.get(1.0,END).strip().replace("\n","").encode()
        #print("src =",src)
        if src:
            try:
                myMd5 = hashlib.md5()
                myMd5.update(src)
                myMd5_Digest = myMd5.hexdigest()
                #print(myMd5_Digest)
                #输出到界面
                self.result_data_Text.delete(1.0,END)
                self.result_data_Text.insert(1.0,myMd5_Digest)
                self.write_log_to_Text("INFO:str_trans_to_md5 success")
            except:
                self.result_data_Text.delete(1.0,END)
                self.result_data_Text.insert(1.0,"字符串转MD5失败")
        else:
            self.write_log_to_Text("ERROR:str_trans_to_md5 failed")
    #获取鼠标选中文本
    def button_start(self,event):
        global s
        s = self.init_data_Text.index('@%s,%s' % (event.x, event.y))

        print(event.x,event.y)


    def button_end(self,event):
        global e
        e = self.init_data_Text.index('@%s,%s' % (event.x, event.y))
        print(str(e))

    #标记解剖部位
    def show_jpbw(self):
        self.result_data_Text.edit_separator()
        print(self.init_data_Text.selection_get()+"\t"+"解剖部位"+"\n")

        start = self.init_data_Text.selection_get()[0]
        end=self.init_data_Text.selection_get()[-1]
        print(start,end)
        start_index=self.init_data_Text.get('1.0',END).index(self.init_data_Text.selection_get()[0])
        end_index=len(self.init_data_Text.selection_get())+start_index-1


        self.result_data_Text.insert(END,self.init_data_Text.selection_get()+"\t" + str(start_index) + "\t" + str(end_index) + "\t" +"解剖部位"+"\n")
        print(self.result_data_Text.get(END))
        self.max1 =self.result_data_Text.get('1.0',END)
        self.result_data_Text.edit_separator()




    # 标记症状描述
    def show_zzms(self,):
        start = self.init_data_Text.selection_get()[0]
        end = self.init_data_Text.selection_get()[-1]
        print(start, end)
        start_index = self.init_data_Text.get('1.0', END).index(self.init_data_Text.selection_get()[0])
        end_index = len(self.init_data_Text.selection_get()) + start_index - 1

        print(self.init_data_Text.selection_get() + "\t" + str(start_index) + "\t" + str(end_index) + "症状描述" + "\n")
        self.result_data_Text.insert(END, self.init_data_Text.selection_get() + "\t" + str(start_index) + "\t" + str(end_index)  +"\t" + "症状描述" + "\n")
        self.max1 = self.result_data_Text.get('1.0', END)
        self.result_data_Text.edit_separator()

    # 标记独立症状
    def show_dlzz(self):
        start = self.init_data_Text.selection_get()[0]
        end = self.init_data_Text.selection_get()[-1]
        print(start, end)
        start_index = self.init_data_Text.get('1.0', END).index(self.init_data_Text.selection_get()[0])
        end_index = len(self.init_data_Text.selection_get()) + start_index - 1

        print(self.init_data_Text.selection_get() + "\t"+ str(start_index) + "\t" + str(end_index)  + "独立症状" + "\n")
        self.result_data_Text.insert(END, self.init_data_Text.selection_get() + "\t" + str(start_index) + "\t" + str(end_index) + "\t" +"独立症状" + "\n")
        self.max1 = self.result_data_Text.get('1.0', END)
        self.result_data_Text.edit_separator()


    # 标记药物
    def show_yw(self):
        start = self.init_data_Text.selection_get()[0]
        end = self.init_data_Text.selection_get()[-1]
        print(start, end)
        start_index = self.init_data_Text.get('1.0', END).index(self.init_data_Text.selection_get()[0])
        end_index = len(self.init_data_Text.selection_get()) + start_index - 1

        print(self.init_data_Text.selection_get() + "\t" + "药物" + "\n")
        self.result_data_Text.insert(END, self.init_data_Text.selection_get() + "\t" + str(start_index) + "\t" + str(end_index) + "\t" +"药物" + "\n")
        self.max1 = self.result_data_Text.get('1.0', END)
        self.result_data_Text.edit_separator()


    # 标记手术
    def show_ss(self):
        start = self.init_data_Text.selection_get()[0]
        end = self.init_data_Text.selection_get()[-1]
        print(start, end)
        start_index = self.init_data_Text.get('1.0', END).index(self.init_data_Text.selection_get()[0])
        end_index = len(self.init_data_Text.selection_get()) + start_index - 1

        print(self.init_data_Text.selection_get() + "\t" + "手术" + "\n")
        self.result_data_Text.insert(END, self.init_data_Text.selection_get() + "\t"+ str(start_index) + "\t" + str(end_index) + "\t" +"手术" + "\n")
        self.max1 = self.result_data_Text.get('1.0', END)
        self.result_data_Text.edit_separator()

    #标注操作撤销功能
    def callback(self,event):
        # 每当有字符插入的时候，就自动插入一个分割符，主要是防止每次撤销的时候会全部撤销
        self.result_data_Text.edit_separator()



    def backToHistory(self):  #撤销操作
        if len(self.result_data_Text.get('1.0','end'))!=0:
            self.result_data_Text.edit_undo()
        else:  #无字符时不能撤销
            return

    def recover(self):   #恢复操作
        if len(self.max1) == len(self.result_data_Text.get('1.0',END)):
            return
        self.result_data_Text.edit_redo()






    #输入窗口一键清空功能
    def delet_ofInput(self):
        self.init_data_Text.delete('1.0','end')

    #结果窗口一键清空功能
    def delet_ofResult(self):
        self.result_data_Text.delete('1.0','end')

    #打开文件功能
    def openfile(self):
        #打开新文件前清空历史
        self.init_data_Text.delete('1.0',END)
        self.result_data_Text.delete('1.0',END)
        fname = filedialog.askopenfilename(title='打开文件', filetypes=[('All Files', '*')])
        self.filename = os.path.basename(fname)
        print(self.filename)

        f = open(fname, 'r', encoding='utf-8', errors='ignore')
        # 对文本数据存储进数组，方便后续操作
        line = f.readline()
        data_list = []
        while line:
            num = list(map(str, line.split()))
            data_list.append(num)
            line = f.readline()
        f.close()
        data_array = np.array(data_list)

        f_contet = data_array
        self.init_data_Text.insert(END, f_contet)
        self.write_log_to_Text()

    def readFile(self,filename):
        f = open(filename, "r")
        text = f.read()
        self.fileName = filename
        return text

    def setCursorLabel(self, cursor_index):
        row_column = cursor_index.split('.')
        cursor_text = ("row: %s\ncol: %s" % (row_column[0], row_column[-1]))
        self.cursorIndex.config(text=cursor_text)

    # 导出文件功能
    def outputfile(self):
        if self.filename!="":
          os.chdir(r'E:\GitTest\untitled\文本标注1.1\Annoation')
          f = open("ann"+self.filename, 'w', encoding='utf-8', errors='ignore')
          f.write(self.result_data_Text.get("1.0", "end"))
          json1 = json.dumps(self.result_data_Text.get("1.0",END))
          print(json1)
          showinfo(title="成功",message="标注文件已导出至Annoation文件夹")
        else:
            showinfo(title="错误",message="未找到指定文件")








    #获取当前时间
    def get_current_time(self):
        current_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        return current_time



    #日志动态打印
    def write_log_to_Text(self):
        global LOG_LINE_NUM
        current_time = self.get_current_time()
        logmsg_in = str(current_time) +" " + str(self.filename) + "\n"      #换行
        self.log_data_Text.insert(END, logmsg_in)







def gui_start():
    init_window = tkinter.Tk()              #实例化出一个父窗口
    ZMJ_PORTAL = MY_GUI(init_window)
    # 设置根窗口默认属性
    ZMJ_PORTAL.set_init_window()



    init_window.mainloop()          #父窗口进入事件循环，可以理解为保持窗口运行，否则界面不展示

gui_start()

