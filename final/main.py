from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
import os

from PIL import ImageTk, Image
from final.ImageHandler import ImageReader, ImageWriter, ImageHandler
from final import basicTransform as T
import numpy as np

# 全局的image array，用来暂存程序中的array
image_current = None
image_pre = None

image_12bit_cur = None

image_tk = None


class Application:
    def __init__(self, window):
        assert window is not None
        self.window = window
        self.window.title("my window")
        # screen_w = self.window.winfo_screenwidth()
        # screen_h = self.window.winfo_screenheight()
        self.window.geometry("1350x720")

        # 图片功能控件
        self.image_8bit_cur = None
        self.image_8bit_pre = None

        self.image_12bit_cur = None
        self.image_12bit_pre = None

        self.image_tk = None

        self.reader = None
        self.handler = None
        self.writer = None

        """初始化UI控件"""
        # # 顶部标签
        # self.frame1 = Frame(self.window)
        #
        # # 标签变量
        # self.v_title_text = StringVar()
        # self.v_title_text.set("")
        #
        # self.titleLabel = Label(self.frame1, textvariable=self.v_title_text, font=('微软雅黑', 15), fg="black")
        # self.titleLabel.pack(pady=5)
        # self.frame1.pack(side=TOP)

        # frame2 包括左侧的图片canvas 右侧的function block
        self.frame2 = Frame(self.window)
        self.frame2_left = Frame(self.frame2)
        self.frame2_mid = Frame(self.frame2)
        self.frame2_right = Frame(self.frame2)

        self.canvas = Canvas(self.frame2_left, height=700, width=700, bg='gray')
        self.canvas.pack()

        # 功能栏 功能1 选择图像
        self.fn1_frame = Frame(self.frame2_mid, borderwidth=2, relief="solid")
        self.fn1_frame1 = Frame(self.fn1_frame)
        self.fn1_label1 = Label(self.fn1_frame1, text="选择图像", font=('微软雅黑', 15))
        self.fn1_label1.pack()
        self.fn1_frame1.pack()

        # 显示图片的名称
        self.v_file_name = StringVar()
        self.v_file_name.set("")
        self.fn1_frame2 = Frame(self.fn1_frame)
        self.fn1_label2 = Label(self.fn1_frame2, textvariable=self.v_file_name, font=('微软雅黑', 13))
        self.fn1_label2.pack()
        self.fn1_frame2.pack()

        #
        self.fn1_frame3 = Frame(self.fn1_frame)
        self.fn1_btn1 = Button(self.fn1_frame3, text="打开文件", font=('微软雅黑', 10), width=8,
                               command=self.openFile)
        self.fn1_btn1.pack(pady=5)
        self.fn1_frame3.pack()
        self.fn1_frame.pack(side=TOP, fill=BOTH, pady=5)

        # 功能栏 功能2 灰度窗映射
        self.fn2_frame = Frame(self.frame2_mid, borderwidth=2, relief="solid")
        self.fn2_frame1 = Frame(self.fn2_frame)
        self.fn2_label1 = Label(self.fn2_frame1, text="灰度窗映射", font=('微软雅黑', 15))
        self.fn2_label1.pack(side=LEFT)
        self.fn2_frame1.pack()

        self.fn2_frame2 = Frame(self.fn2_frame)
        self.fn2_label2 = Label(self.fn2_frame2, text="窗大小", font=('微软雅黑', 13))
        self.fn2_label2.pack(side=LEFT, padx=15, pady=5)
        self.fn2_entry1 = Entry(self.fn2_frame2, bd=2)
        self.fn2_entry1.pack(side=RIGHT, fill=BOTH, pady=5, padx=5)
        self.fn2_frame2.pack()

        self.fn2_frame3 = Frame(self.fn2_frame)
        self.fn2_label3 = Label(self.fn2_frame3, text="窗位置", font=('微软雅黑', 13))
        self.fn2_label3.pack(side=LEFT, padx=15, pady=5)
        self.fn2_entry2 = Entry(self.fn2_frame3, bd=2)
        self.fn2_entry2.pack(side=RIGHT, fill=BOTH, pady=5, padx=5)
        self.fn2_frame3.pack()

        self.fn2_frame4 = Frame(self.fn2_frame)
        self.fn2_btn1 = Button(self.fn2_frame4, text="apply", font=('微软雅黑', 10), width=8,
                               command=self.applyGrayWindowTransform)
        self.fn2_btn1.pack(side=LEFT, padx=12, pady=5)
        self.fn2_btn2 = Button(self.fn2_frame4, text="reset", font=('微软雅黑', 10), width=8,
                               command=self.resetGrayWindowTransform)
        self.fn2_btn2.pack(side=RIGHT, padx=12, pady=5)
        self.fn2_frame4.pack()

        self.fn2_frame.pack(side=TOP, fill=BOTH, pady=5)

        # 功能栏 功能3 图像细节增强——直方图均衡

        self.fn3_frame = Frame(self.frame2_mid, borderwidth=2, relief="solid")
        self.fn3_frame1 = Frame(self.fn3_frame)
        self.fn3_label1 = Label(self.fn3_frame1, text="直方图均衡", font=('微软雅黑', 15))
        self.fn3_label1.pack(side=LEFT)
        self.fn3_frame1.pack()

        self.fn3_frame2 = Frame(self.fn3_frame)
        self.fn3_btn1 = Button(self.fn3_frame2, text="apply", font=('微软雅黑', 10), width=8,
                               command=self.applyHistEqual)
        self.fn3_btn1.pack(side=LEFT, padx=12, pady=5)
        self.fn3_btn2 = Button(self.fn3_frame2, text="reset", font=('微软雅黑', 10), width=8,
                               command=self.resetHistEqual)
        self.fn3_btn2.pack(side=RIGHT, padx=12, pady=5)
        self.fn3_frame2.pack()

        self.fn3_frame.pack(side=TOP, fill=BOTH, pady=5)

        # 功能栏 功能3 平均平滑
        self.fn4_frame = Frame(self.frame2_mid, borderwidth=2, relief="solid")
        self.fn4_frame1 = Frame(self.fn4_frame)
        self.fn4_label1 = Label(self.fn4_frame1, text="平均平滑", font=('微软雅黑', 15))
        self.fn4_label1.pack(side=LEFT)
        self.fn4_frame1.pack()

        self.fn4_frame2 = Frame(self.fn4_frame)
        self.fn4_label2 = Label(self.fn4_frame2, text="核大小", font=('微软雅黑', 13))
        self.fn4_label2.pack(side=LEFT, padx=15, pady=5)
        self.fn4_entry1 = Entry(self.fn4_frame2, bd=2)
        self.fn4_entry1.pack(side=RIGHT, fill=BOTH, pady=5, padx=5)
        self.fn4_frame2.pack()

        self.fn4_frame3 = Frame(self.fn4_frame)
        self.fn4_btn1 = Button(self.fn4_frame3, text="apply", font=('微软雅黑', 10), width=8,
                               command=self.applyAverageFilter)
        self.fn4_btn1.pack(side=LEFT, padx=12, pady=5)
        self.fn4_btn2 = Button(self.fn4_frame3, text="reset", font=('微软雅黑', 10), width=8,
                               command=self.resetAverageFilter)
        self.fn4_btn2.pack(side=RIGHT, padx=12, pady=5)
        self.fn4_frame3.pack()

        self.fn4_frame.pack(side=TOP, fill=BOTH, pady=5)

        # 功能栏 功能4 高斯平滑
        self.fn5_frame = Frame(self.frame2_mid, borderwidth=2, relief="solid")
        self.fn5_frame1 = Frame(self.fn5_frame)
        self.fn5_label1 = Label(self.fn5_frame1, text="高斯平滑", font=('微软雅黑', 15))
        self.fn5_label1.pack(side=LEFT)
        self.fn5_frame1.pack()

        self.fn5_frame2 = Frame(self.fn5_frame)
        self.fn5_label2 = Label(self.fn5_frame2, text="核大小", font=('微软雅黑', 13))
        self.fn5_label2.pack(side=LEFT, padx=15, pady=5)
        self.fn5_entry1 = Entry(self.fn5_frame2, bd=2)
        self.fn5_entry1.pack(side=RIGHT, fill=BOTH, pady=5, padx=5)
        self.fn5_frame2.pack()

        self.fn5_frame3 = Frame(self.fn5_frame)
        self.fn5_label3 = Label(self.fn5_frame3, text="方差σ", font=('微软雅黑', 13))
        self.fn5_label3.pack(side=LEFT, padx=15, pady=5)
        self.fn5_entry2 = Entry(self.fn5_frame3, bd=2)
        self.fn5_entry2.pack(side=RIGHT, fill=BOTH, pady=5, padx=5)
        self.fn5_frame3.pack()

        self.fn5_frame4 = Frame(self.fn5_frame)
        self.fn5_btn1 = Button(self.fn5_frame4, text="apply", font=('微软雅黑', 10), width=8,
                               command=self.applyGaussianFilter)
        self.fn5_btn1.pack(side=LEFT, padx=12, pady=5)
        self.fn5_btn2 = Button(self.fn5_frame4, text="reset", font=('微软雅黑', 10), width=8,
                               command=self.resetGaussianFilter)
        self.fn5_btn2.pack(side=RIGHT, padx=12, pady=5)
        self.fn5_frame4.pack()

        self.fn5_frame.pack(side=TOP, fill=BOTH, pady=5)

        # 功能栏 功能6 sobel锐化
        self.fn6_frame = Frame(self.frame2_right, borderwidth=2, relief="solid")
        self.fn6_frame1 = Frame(self.fn6_frame)
        self.fn6_label1 = Label(self.fn6_frame1, text="Sobel算子锐化", font=('微软雅黑', 15))
        self.fn6_label1.pack(side=LEFT)
        self.fn6_frame1.pack()

        # 种类选择
        self.v_sobel_select = IntVar()
        self.v_sobel_select.set(1)

        self.fn6_frame3 = Frame(self.fn6_frame)
        self.fn6_radio1 = Radiobutton(self.fn6_frame3, text="x算子", font=('微软雅黑', 13), variable=self.v_sobel_select,
                                      value=1)
        self.fn6_radio2 = Radiobutton(self.fn6_frame3, text="y算子", font=('微软雅黑', 13), variable=self.v_sobel_select,
                                      value=2)

        self.fn6_radio1.pack(side=LEFT, padx=15, pady=5)
        self.fn6_radio2.pack(side=LEFT, padx=15, pady=5)
        self.fn6_frame3.pack(side=TOP, fill=BOTH)

        self.fn6_frame2 = Frame(self.fn6_frame)
        self.fn6_btn1 = Button(self.fn6_frame2, text="apply", font=('微软雅黑', 10), width=8,
                               command=self.applySobelSharpen)
        self.fn6_btn1.pack(side=LEFT, padx=12, pady=5)
        self.fn6_btn2 = Button(self.fn6_frame2, text="reset", font=('微软雅黑', 10), width=8,
                               command=self.resetSobelSharpen)
        self.fn6_btn2.pack(side=RIGHT, padx=12, pady=5)
        self.fn6_frame2.pack()
        self.fn6_frame.pack(side=TOP, fill=BOTH, pady=5)

        # 功能栏 功能7 laplace锐化
        self.fn7_frame = Frame(self.frame2_right, borderwidth=2, relief="solid")
        self.fn7_frame1 = Frame(self.fn7_frame)
        self.fn7_label1 = Label(self.fn7_frame1, text="Laplace算子锐化", font=('微软雅黑', 15))
        self.fn7_label1.pack(side=LEFT)
        self.fn7_frame1.pack()

        # 种类选择
        self.v_laplace_select = IntVar()
        self.v_laplace_select.set(1)

        self.fn7_frame3 = Frame(self.fn7_frame)
        self.fn7_radio1 = Radiobutton(self.fn7_frame3, text="算子1", font=('微软雅黑', 13), variable=self.v_laplace_select,
                                      value=1)
        self.fn7_radio2 = Radiobutton(self.fn7_frame3, text="算子2", font=('微软雅黑', 13), variable=self.v_laplace_select,
                                      value=2)
        self.fn7_radio3 = Radiobutton(self.fn7_frame3, text="算子3", font=('微软雅黑', 13), variable=self.v_laplace_select,
                                      value=2)

        self.fn7_radio1.pack(side=LEFT, padx=5, pady=5)
        self.fn7_radio2.pack(side=LEFT, padx=5, pady=5)
        self.fn7_radio3.pack(side=LEFT, padx=5, pady=5)
        self.fn7_frame3.pack(side=TOP, fill=BOTH)

        self.fn7_frame2 = Frame(self.fn7_frame)
        self.fn7_btn1 = Button(self.fn7_frame2, text="apply", font=('微软雅黑', 10), width=8,
                               command=self.applyLaplaceSharpen)
        self.fn7_btn1.pack(side=LEFT, padx=12, pady=5)
        self.fn7_btn2 = Button(self.fn7_frame2, text="reset", font=('微软雅黑', 10), width=8,
                               command=self.resetLaplaceSharpen)

        self.fn7_btn2.pack(side=RIGHT, padx=12, pady=5)
        self.fn7_frame2.pack()
        self.fn7_frame.pack(side=TOP, fill=BOTH, pady=5)

        # 功能栏 功能8 图像放大缩小
        self.fn8_frame = Frame(self.frame2_right, borderwidth=2, relief="solid")
        self.fn8_frame1 = Frame(self.fn8_frame)
        self.fn8_label1 = Label(self.fn8_frame1, text="放大和缩小", font=('微软雅黑', 15))
        self.fn8_label1.pack(side=LEFT)
        self.fn8_frame1.pack()

        self.fn8_frame2 = Frame(self.fn8_frame)
        # self.fn3_btn1 = Button(self.fn3_frame2, text="apply", font=('微软雅黑', 10), width=8,
        #                        command=self.applyHistEqual)
        # self.fn3_btn1.pack(side=LEFT, padx=12, pady=5)
        # self.fn3_btn2 = Button(self.fn3_frame2, text="reset", font=('微软雅黑', 10), width=8,
        #                        command=self.resetHistEqual)
        # self.fn3_btn2.pack(side=RIGHT, padx=12, pady=5)

        self.fn8_frame2.pack()
        self.fn8_frame.pack(side=TOP, fill=BOTH, pady=5)

        # 功能栏 功能9 图像重置
        self.fn9_frame = Frame(self.frame2_right, borderwidth=2, relief="solid")
        self.fn9_frame1 = Frame(self.fn9_frame)
        self.fn9_label1 = Label(self.fn9_frame1, text="图像重置", font=('微软雅黑', 15))
        self.fn9_label1.pack(side=LEFT)
        self.fn9_frame1.pack()

        self.fn9_frame2 = Frame(self.fn9_frame)
        self.fn9_btn = Button(self.fn9_frame2, text="重置", font=('微软雅黑', 10), width=8,
                              command=self.resetImage)
        self.fn9_btn.pack(side=LEFT, padx=12, pady=5)
        self.fn9_frame2.pack()
        self.fn9_frame.pack(side=TOP, fill=BOTH, pady=5)

        # 功能栏 功能10 图像保存
        self.fn10_frame = Frame(self.frame2_right, borderwidth=2, relief="solid")
        self.fn10_frame1 = Frame(self.fn10_frame)
        self.fn10_label1 = Label(self.fn10_frame1, text="图像保存", font=('微软雅黑', 15))
        self.fn10_label1.pack(side=LEFT)
        self.fn10_frame1.pack()

        self.fn10_frame3 = Frame(self.fn10_frame)
        self.fn10_label2 = Label(self.fn10_frame3, text="文件名(无后缀)", font=('微软雅黑', 13))
        self.fn10_label2.pack(side=LEFT, padx=5, pady=5)
        self.fn10_entry1 = Entry(self.fn10_frame3, bd=2)
        self.fn10_entry1.pack(side=RIGHT, fill=BOTH, pady=5, padx=5)
        self.fn10_frame3.pack()

        self.fn10_frame2 = Frame(self.fn10_frame)
        self.fn10_btn = Button(self.fn10_frame2, text="保存", font=('微软雅黑', 10), width=8,
                               command=self.saveImage)
        self.fn10_btn.pack(side=LEFT, padx=12, pady=5)
        self.fn10_frame2.pack()
        self.fn10_frame.pack(side=TOP, fill=BOTH, pady=5)

        # 父元素 pack
        self.frame2_left.pack(side=LEFT, padx=10, pady=5, fill=Y)
        self.frame2_mid.pack(side=LEFT, padx=5, pady=5, fill=Y)
        self.frame2_right.pack(side=LEFT, padx=5, pady=5, fill=Y)
        self.frame2.pack()

        # self.initImage()

    # 初始化图片 default = lumbar
    def initImage(self):
        self.v_file_name.set("lumbar.raw")
        self.reader = ImageReader("images_raw/lumbar.raw")

        global image
        global image_tk
        image = Image.fromarray(self.reader.getImageArray().astype('uint8'), mode="L")
        image = image.resize((700, 700))
        image_tk = ImageTk.PhotoImage(image)
        self.canvas.create_image(0, 0, anchor=NW, image=image_tk)

    def openFile(self):
        filePath = filedialog.askopenfilename()
        print("open file")
        print(filePath)

        file_name = os.path.basename(filePath)
        self.v_file_name.set(file_name)

        self.reader = ImageReader(filePath)

        # 设置画布中的图片
        # todo 画布size和图片的size
        self.image_8bit_cur = Image.fromarray(self.reader.getImageArray().astype('uint8'), mode="L")

        # image_h = image2show.height
        # image_w = image2show.width

        self.image_8bit_cur = self.image_8bit_cur.resize((700, 700))
        self.image_tk = ImageTk.PhotoImage(self.image_8bit_cur)
        self.canvas.create_image(0, 0, anchor=NW, image=self.image_tk)

        # 显示提示框
        messagebox.showinfo(title='提示', message='文件打开成功')

    # 图片重置
    def resetImage(self):
        pass

    # 图片保存
    def saveImage(self):
        print("aaaaa")
        fileSave = filedialog.asksaveasfilename(defaultextension='.raw', filetypes=[("raw image", ".raw")])
        print("save:", fileSave)

    """灰度窗映射"""

    def applyGrayWindowTransform(self):
        # 获取参数

        # 调用函数
        print("apply")
        pass

    def resetGrayWindowTransform(self):
        print("reset")
        pass

    """直方图均衡"""

    def applyHistEqual(self):
        pass

    def resetHistEqual(self):
        pass

    """均值滤波"""

    def applyAverageFilter(self):
        pass

    def resetAverageFilter(self):
        pass

    """高斯滤波"""

    def applyGaussianFilter(self):
        pass

    def resetGaussianFilter(self):
        pass

    """锐化"""

    def applySobelSharpen(self):
        pass

    def resetSobelSharpen(self):
        pass

    def applyLaplaceSharpen(self):
        pass

    def resetLaplaceSharpen(self):
        pass

    # 应用变换
    def applyTransform(self):
        pass

    # 重置变换
    def resetTransform(self):
        pass


if __name__ == '__main__':
    app_window = Tk()
    app = Application(app_window)
    app_window.mainloop()
