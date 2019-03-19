#1.2 版本 解决鼠标文本获取以及实现撤销操作
from tkinter import *
import hashlib
import time
from tkinter import filedialog
import chardet
import math
import tkinter

LOG_LINE_NUM = 0




class MY_GUI():


    def __init__(self,init_window_name):
        self.init_window_name = init_window_name



    #设置窗口
    def set_init_window(self):
        self.init_window_name.title("电子病历标注工具_v1.2   ")           #窗口名
        #self.init_window_name.geometry('320x160+10+10')                         #290 160为窗口大小，+10 +10 定义窗口弹出时的默认展示位置
        self.init_window_name.geometry('1068x681+10+10')
        #self.init_window_name["bg"] = "pink"                                    #窗口背景色，其他背景色见：blog.csdn.net/chl0000/article/details/7657887
        #self.init_window_name.attributes("-alpha",0.9)                          #虚化，值越小虚化程度越高
        #标签
        self.init_data_label = Label(self.init_window_name, text="待处理数据")
        self.init_data_label.grid(row=0, column=0)
        self.result_data_label = Label(self.init_window_name, text="输出结果")
        self.result_data_label.grid(row=0, column=12)
        self.log_label = Label(self.init_window_name, text="日志")
        self.log_label.grid(row=12, column=0)
        #文本框

        self.init_data_Text = Text(self.init_window_name, width=67, height=35)  #原始数据录入框
        #self.init_data_Text.
        self.init_data_Text.grid(row=1, column=0, rowspan=10, columnspan=10)
        self.result_data_Text = Text(self.init_window_name, width=70, height=49)  #处理结果展示
        self.result_data_Text.grid(row=1, column=12, rowspan=15, columnspan=10)
        self.log_data_Text = Text(self.init_window_name, width=66, height=9)  # 日志框
        self.log_data_Text.grid(row=13, column=0, columnspan=10)
        self.init_data_Text.bind("<Button-1>", self.button_start)
        self.init_data_Text.bind("<ButtonRelease-1>", self.button_end)
        #按钮
        # self.str_trans_to_md5_button = Button(self.init_window_name, text="字符串转MD5", bg="lightblue", width=10,command=self.str_trans_to_md5)  # 调用内部方法  加()为直接调用
        # self.str_trans_to_md5_button.grid(row=1, column=11)
        #导入文件按钮
        self.input_button = Button(self.init_window_name,text="导入文件",bg="lightgreen",width=8,command=self.openfile)
        self.input_button.grid(row=0, column=2)
        # 输入窗口清空按钮
        self.delet_input_button = Button(self.init_window_name, text="一键清空", bg="red", width=8,command=self.delet_ofInput)
        self.delet_input_button.grid(row=0, column=3)
        #展示窗口清空按钮
        self.delet_result_button = Button(self.init_window_name, text="一键清空", bg="red", width=8,command=self.delet_ofResult)
        self.delet_result_button.grid(row=0,column=13)
        #导出文件按钮
        self.output_button = Button(self.init_window_name,text="导出文件",bg="lightgreen",width=8,command=self.outputfile)
        self.output_button.grid(row=0,column=14)
        #标记解剖部位按钮
        self.show_button = Button(self.init_window_name,text="解剖部位",width='8',command=self.show_jpbw)
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
        start_index = str(s)
        start_index = start_index[2:]
        start_index = int(start_index)

        end_index = str(e)
        end_index = end_index[2:]
        end_index = int(end_index)
        print(self.init_data_Text.selection_get()+"\t"+"解剖部位"+"\n")
        self.result_data_Text.insert(END,self.init_data_Text.selection_get()+"\t" + str(start_index) + "\t" + str(end_index) + "\t" +"解剖部位"+"\n")
        print(self.result_data_Text.get(END))

    # 导出文件功能
    def outputfile(self):
        fname = filedialog.askopenfilename(title='打开文件', filetypes=[('All Files', '*')])
        f = open(fname, 'w', encoding='utf-8', errors='ignore')
        f.write(self.result_data_Text.get("1.0","end"))

    # 标记症状描述
    def show_zzms(self):
        start_index = str(s)
        start_index = start_index[2:]
        start_index = int(start_index)

        end_index = str(e)
        end_index = end_index[2:]
        end_index = int(end_index)

        print(self.init_data_Text.selection_get() + "\t" + str(start_index) + "\t" + str(end_index) + "症状描述" + "\n")
        self.result_data_Text.insert(END, self.init_data_Text.selection_get() + "\t"+ str(start_index) + "\t" + str(end_index)  + "症状描述" + "\n")

    # 标记独立症状
    def show_dlzz(self):
        start_index = str(s)
        start_index = start_index[2:]
        start_index = int(start_index)

        end_index = str(e)
        end_index = end_index[2:]
        end_index = int(end_index)
        print(self.init_data_Text.selection_get() + "\t"+ str(start_index) + "\t" + str(end_index)  + "独立症状" + "\n")
        self.result_data_Text.insert(END, self.init_data_Text.selection_get() + "\t" + str(start_index) + "\t" + str(end_index) + "独立症状" + "\n")


    # 标记药物
    def show_yw(self):
        start_index = str(s)
        start_index = start_index[2:]
        start_index = int(start_index)

        end_index = str(e)
        end_index = end_index[2:]
        end_index = int(end_index)
        print(self.init_data_Text.selection_get() + "\t" + "药物" + "\n")
        self.result_data_Text.insert(END, self.init_data_Text.selection_get() + "\t" + str(start_index) + "\t" + str(end_index) + "药物" + "\n")


    # 标记手术
    def show_ss(self):
        start_index = str(s)
        start_index = start_index[2:]
        start_index = int(start_index)

        end_index = str(e)
        end_index = end_index[2:]
        end_index = int(end_index)
        print(self.init_data_Text.selection_get() + "\t" + "手术" + "\n")
        self.result_data_Text.insert(END, self.init_data_Text.selection_get() + "\t"+ str(start_index) + "\t" + str(end_index) + "手术" + "\n")



    #输入窗口一键清空功能
    def delet_ofInput(self):
        self.init_data_Text.delete('1.0','end')

    #结果窗口一键清空功能
    def delet_ofResult(self):
        self.result_data_Text.delete('1.0','end')

    #打开文件功能
    def openfile(self):
        fname = filedialog.askopenfilename(title='打开文件', filetypes=[('All Files', '*')])
        f=open(fname,'r',encoding='utf-8',errors='ignore')
        f_contet = f.read()
        self.init_data_Text.insert(END,f_contet)






    #获取当前时间
    def get_current_time(self):
        current_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        return current_time



    #日志动态打印
    def write_log_to_Text(self,logmsg):
        global LOG_LINE_NUM
        current_time = self.get_current_time()
        logmsg_in = str(current_time) +" " + str(logmsg) + "\n"      #换行
        if LOG_LINE_NUM <= 7:
            self.log_data_Text.insert(END, logmsg_in)
            LOG_LINE_NUM = LOG_LINE_NUM + 1
        else:
            self.log_data_Text.delete(1.0,2.0)
            self.log_data_Text.insert(END, logmsg_in)







def gui_start():
    init_window = tkinter.Tk()              #实例化出一个父窗口
    ZMJ_PORTAL = MY_GUI(init_window)
    # 设置根窗口默认属性
    ZMJ_PORTAL.set_init_window()



    init_window.mainloop()          #父窗口进入事件循环，可以理解为保持窗口运行，否则界面不展示

gui_start()

