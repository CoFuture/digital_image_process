from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
import os
from PIL import ImageTk, Image
from final.ImageHandler import ImageReader, ImageWriter, ImageHandler
from final import basicTransform as T
import numpy as np


class Application:
    def __init__(self, window):
        assert window is not None
        self.window = window
        self.window.title("医学DR图像基本阅片")
        # screen_w = self.window.winfo_screenwidth()
        # screen_h = self.window.winfo_screenheight()
        self.window.geometry("1280x700")

        """图片功能控件"""
        # 全局的image array，用来暂存程序中的array
        self.image_8bit_show = None
        self.image_8bit_cur = None
        self.image_12bit_cur = None

        self.image_8bit_zoom = None
        self.image_tk = None

        self.reader = None
        self.handler = ImageHandler()
        self.writer = ImageWriter()

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

        self.scrollBarY = Scrollbar(self.frame2_left, orient=VERTICAL)
        self.scrollBarX = Scrollbar(self.frame2_left, orient=HORIZONTAL)

        self.canvas = Canvas(
            self.frame2_left,
            height=640,
            width=640,
            scrollregion=(0, 0, 640, 640),
            bg='gray',
            xscrollcommand=self.scrollBarX.set,
            yscrollcommand=self.scrollBarY.set
        )

        self.scrollBarX.config(command=self.canvas.xview)
        self.scrollBarY.config(command=self.canvas.yview)

        # 靠右，充满Y轴
        self.scrollBarY.pack(side=RIGHT, fill=Y)
        # 靠下，充满X轴
        self.scrollBarX.pack(side=BOTTOM, fill=X)

        self.canvas.pack(side=LEFT, expand=YES, fill=BOTH)

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
        self.fn1_btn1 = Button(self.fn1_frame3, text="打开文件", font=('微软雅黑', 10), width=8, bg="#B7B7B7",
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
        self.fn2_btn1 = Button(self.fn2_frame4, text="apply", font=('微软雅黑', 10), width=8, bg="#B7B7B7",
                               command=self.applyGrayWindowTransform)
        self.fn2_btn1.pack(side=LEFT, padx=12, pady=5)
        # self.fn2_btn2 = Button(self.fn2_frame4, text="reset", font=('微软雅黑', 10), width=8,
        #                        command=self.resetGrayWindowTransform)
        # self.fn2_btn2.pack(side=RIGHT, padx=12, pady=5)
        self.fn2_frame4.pack()

        self.fn2_frame.pack(side=TOP, fill=BOTH, pady=5)

        # 功能栏 功能3 图像细节增强——直方图均衡

        self.fn3_frame = Frame(self.frame2_mid, borderwidth=2, relief="solid")
        self.fn3_frame1 = Frame(self.fn3_frame)
        self.fn3_label1 = Label(self.fn3_frame1, text="直方图均衡", font=('微软雅黑', 15))
        self.fn3_label1.pack(side=LEFT)
        self.fn3_frame1.pack()

        self.fn3_frame2 = Frame(self.fn3_frame)
        self.fn3_btn1 = Button(self.fn3_frame2, text="apply", font=('微软雅黑', 10), width=8, bg="#B7B7B7",
                               command=self.applyHistEqual)
        self.fn3_btn1.pack(side=LEFT, padx=12, pady=5)
        # self.fn3_btn2 = Button(self.fn3_frame2, text="reset", font=('微软雅黑', 10), width=8,
        #                        command=self.resetHistEqual)
        # self.fn3_btn2.pack(side=RIGHT, padx=12, pady=5)
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
        self.fn4_btn1 = Button(self.fn4_frame3, text="apply", font=('微软雅黑', 10), width=8, bg="#B7B7B7",
                               command=self.applyAverageFilter)
        self.fn4_btn1.pack(side=LEFT, padx=12, pady=5)
        # self.fn4_btn2 = Button(self.fn4_frame3, text="reset", font=('微软雅黑', 10), width=8,
        #                        command=self.resetAverageFilter)
        # self.fn4_btn2.pack(side=RIGHT, padx=12, pady=5)
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
        self.fn5_btn1 = Button(self.fn5_frame4, text="apply", font=('微软雅黑', 10), width=8, bg="#B7B7B7",
                               command=self.applyGaussianFilter)
        self.fn5_btn1.pack(side=LEFT, padx=12, pady=5)
        # self.fn5_btn2 = Button(self.fn5_frame4, text="reset", font=('微软雅黑', 10), width=8,
        #                        command=self.resetGaussianFilter)
        # self.fn5_btn2.pack(side=RIGHT, padx=12, pady=5)
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
        self.fn6_btn1 = Button(self.fn6_frame2, text="apply", font=('微软雅黑', 10), width=8, bg="#B7B7B7",
                               command=self.applySobelSharpen)
        self.fn6_btn1.pack(side=LEFT, padx=12, pady=5)
        # self.fn6_btn2 = Button(self.fn6_frame2, text="reset", font=('微软雅黑', 10), width=8,
        #                        command=self.resetSobelSharpen)
        # self.fn6_btn2.pack(side=RIGHT, padx=12, pady=5)
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
                                      value=3)

        self.fn7_radio1.pack(side=LEFT, padx=5, pady=5)
        self.fn7_radio2.pack(side=LEFT, padx=5, pady=5)
        self.fn7_radio3.pack(side=LEFT, padx=5, pady=5)
        self.fn7_frame3.pack(side=TOP, fill=BOTH)

        self.fn7_frame2 = Frame(self.fn7_frame)
        self.fn7_btn1 = Button(self.fn7_frame2, text="apply", font=('微软雅黑', 10), width=8, bg="#B7B7B7",
                               command=self.applyLaplaceSharpen)
        self.fn7_btn1.pack(side=LEFT, padx=12, pady=5)
        # self.fn7_btn2 = Button(self.fn7_frame2, text="reset", font=('微软雅黑', 10), width=8,
        #                        command=self.resetLaplaceSharpen)
        # self.fn7_btn2.pack(side=RIGHT, padx=12, pady=5)

        self.fn7_frame2.pack()
        self.fn7_frame.pack(side=TOP, fill=BOTH, pady=5)

        # 功能栏 功能8 图像放大缩小
        self.fn8_frame = Frame(self.frame2_right, borderwidth=2, relief="solid")
        self.fn8_frame1 = Frame(self.fn8_frame)
        self.fn8_label1 = Label(self.fn8_frame1, text="放大和缩小", font=('微软雅黑', 15))
        self.fn8_label1.pack(side=LEFT)
        self.fn8_frame1.pack()

        self.fn8_frame2 = Frame(self.fn8_frame)
        self.fn8_label2 = Label(self.fn8_frame2, text="放大系数", font=('微软雅黑', 13))
        self.fn8_label2.pack(side=LEFT, padx=15, pady=5)
        self.fn8_entry1 = Entry(self.fn8_frame2, bd=2)
        self.fn8_entry1.pack(side=RIGHT, fill=BOTH, pady=5, padx=5)
        self.fn8_frame2.pack()

        self.fn8_frame3 = Frame(self.fn8_frame)
        self.fn8_btn1 = Button(self.fn8_frame3, text="apply", font=('微软雅黑', 10), width=8, bg="#B7B7B7",
                               command=self.applyZoom)
        self.fn8_btn1.pack(side=LEFT, padx=12, pady=5)
        self.fn8_btn2 = Button(self.fn8_frame3, text="reset", font=('微软雅黑', 10), width=8, bg="#B7B7B7",
                               command=self.resetZoom)
        self.fn8_btn2.pack(side=RIGHT, padx=12, pady=5)
        self.fn8_frame3.pack()

        self.fn8_frame.pack(side=TOP, fill=BOTH, pady=5)

        # 功能栏 功能9 图像重置
        self.fn9_frame = Frame(self.frame2_right, borderwidth=2, relief="solid")
        self.fn9_frame1 = Frame(self.fn9_frame)
        self.fn9_label1 = Label(self.fn9_frame1, text="图像重置", font=('微软雅黑', 15))
        self.fn9_label1.pack(side=LEFT)
        self.fn9_frame1.pack()

        self.fn9_frame2 = Frame(self.fn9_frame)
        self.fn9_btn = Button(self.fn9_frame2, text="重置", font=('微软雅黑', 10), width=8, bg="#B7B7B7",
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

        # self.fn10_frame3 = Frame(self.fn10_frame)
        # self.fn10_label2 = Label(self.fn10_frame3, text="文件名(无后缀)", font=('微软雅黑', 13))
        # self.fn10_label2.pack(side=LEFT, padx=5, pady=5)
        # self.fn10_entry1 = Entry(self.fn10_frame3, bd=2)
        # self.fn10_entry1.pack(side=RIGHT, fill=BOTH, pady=5, padx=5)
        # self.fn10_frame3.pack()

        self.fn10_frame2 = Frame(self.fn10_frame)
        self.fn10_btn1 = Button(self.fn10_frame2, text="保存Raw", font=('微软雅黑', 10), width=12, bg="#B7B7B7",
                                command=self.saveImageRaw)
        self.fn10_btn1.pack(side=LEFT, padx=12, pady=5)
        self.fn10_btn2 = Button(self.fn10_frame2, text="保存JPG/PNG", font=('微软雅黑', 10), width=12, bg="#B7B7B7",
                                command=self.saveImageFormat)

        self.fn10_btn2.pack(side=LEFT, padx=12, pady=5)
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

        image = Image.fromarray(self.reader.getImageArray().astype('uint8'), mode="L")
        image = image.resize((700, 700))
        image_tk = ImageTk.PhotoImage(image)
        self.canvas.create_image(0, 0, anchor=NW, image=image_tk)

    def openFile(self):
        filePath = filedialog.askopenfilename()
        print("open file", filePath)

        if len(filePath) != 0:
            file_name = os.path.basename(filePath)
            self.v_file_name.set(file_name)
            self.reader = ImageReader(filePath)

            # 设置画布中的图片
            # todo 画布size和图片的size
            self.image_8bit_cur = self.reader.getImageArray()
            self.image_12bit_cur = self.reader.getImageArrayRaw()

            self.image_8bit_show = Image.fromarray(self.image_8bit_cur.astype('uint8'), mode="L")
            self.image_8bit_show = self.image_8bit_show.resize((640, 640))
            image_h = self.image_8bit_show.height
            image_w = self.image_8bit_show.width

            # 设置canvas的滑动窗口
            self.canvas.config(scrollregion=(0, 0, image_w, image_h))
            self.image_tk = ImageTk.PhotoImage(self.image_8bit_show)
            self.canvas.create_image(0, 0, anchor=NW, image=self.image_tk)

            # 显示提示框
            messagebox.showinfo(title='提示', message='文件打开成功')

    # 图片重置
    def resetImage(self):
        if self.reader is None:
            messagebox.showerror(title="错误", message="图像不能为空")
            return

        self.image_8bit_cur = self.reader.getImageArray()
        self.image_12bit_cur = self.reader.getImageArrayRaw()
        self.image_8bit_zoom = None

        # 重新显示图片
        self.image_8bit_show = Image.fromarray(self.image_8bit_cur.astype('uint8'), mode="L")
        self.image_8bit_show = self.image_8bit_show.resize((640, 640))
        image_h = self.image_8bit_show.height
        image_w = self.image_8bit_show.width

        # 设置canvas的滑动窗口
        self.canvas.config(scrollregion=(0, 0, image_w, image_h))
        self.image_tk = ImageTk.PhotoImage(self.image_8bit_show)
        self.canvas.create_image(0, 0, anchor=NW, image=self.image_tk)

        # 重置button样式
        self.fn2_btn1.config(relief=RAISED, bg="#B7B7B7")
        self.fn3_btn1.config(relief=RAISED, bg="#B7B7B7")
        self.fn4_btn1.config(relief=RAISED, bg="#B7B7B7")
        self.fn5_btn1.config(relief=RAISED, bg="#B7B7B7")
        self.fn6_btn1.config(relief=RAISED, bg="#B7B7B7")
        self.fn7_btn1.config(relief=RAISED, bg="#B7B7B7")
        self.fn8_btn1.config(relief=RAISED, bg="#B7B7B7")

        # 显示提示框
        messagebox.showinfo(title='提示', message='图片重置成功')

    # 图片保存
    def saveImageRaw(self):
        if self.image_12bit_cur is None:
            messagebox.showerror(title='警告', message='图片不能为空')
            return

        fileSave = filedialog.asksaveasfilename(defaultextension='.raw', filetypes=[("raw image", ".raw")])
        print("save:", fileSave)

        if len(fileSave) != 0:
            # 初始化image writer
            self.writer.saveImageRaw(self.image_12bit_cur, fileSave)
            # 显示提示框
            messagebox.showinfo(title='提示', message='文件保存成功')

    def saveImageFormat(self):
        if self.image_8bit_cur is None:
            messagebox.showerror(title='警告', message='图片不能为空')
            return

        fileSave = filedialog.asksaveasfilename(defaultextension='.png', filetypes=[("png image", ".png"), ("jpg image", ".jpg")])

        if len(fileSave) != 0:
            # 初始化image writer
            self.writer.saveImageFormat(self.image_8bit_cur, fileSave)
            # 显示提示框
            messagebox.showinfo(title='提示', message='文件保存成功')

    """放大缩小"""
    def applyZoom(self):
        # 获取放大系数
        if len(self.fn8_entry1.get()) == 0:
            messagebox.showwarning(title="警告", message="参数不能为空")
            return
        elif self.image_8bit_cur is None:
            messagebox.showwarning(title="警告", message="图像不能为空")
            return
        elif float(self.fn8_entry1.get()) < 1.0:
            messagebox.showwarning(title="警告", message="参数非法")
            return

        factor = float(self.fn8_entry1.get())
        self.image_8bit_zoom = Image.fromarray((self.handler.zoomIn(self.image_8bit_show, factor)).astype('uint8'),
                                               mode="L")

        # 设置画布参数
        image_w = self.image_8bit_zoom.width
        image_h = self.image_8bit_zoom.height

        self.canvas.config(scrollregion=(0, 0, image_w, image_h))
        self.image_tk = ImageTk.PhotoImage(self.image_8bit_zoom)
        self.canvas.create_image(0, 0, anchor=NW, image=self.image_tk)

        # 设置放大系数
        self.fn8_btn1.config(
            relief=SUNKEN,
            bg="#555555"
        )
        messagebox.showinfo(title='提示', message='放大成功')

    def resetZoom(self):
        assert self.image_8bit_show is not None

        self.image_8bit_zoom = None
        # 设置画布参数
        image_w = self.image_8bit_show.width
        image_h = self.image_8bit_show.height

        self.canvas.config(scrollregion=(0, 0, image_w, image_h))

        self.image_tk = ImageTk.PhotoImage(self.image_8bit_show)
        self.canvas.create_image(0, 0, anchor=NW, image=self.image_tk)

        self.fn8_btn1.config(
            relief=RAISED,
            bg="#B7B7B7"
        )
        messagebox.showinfo(title='提示', message='重置成功')

    """灰度窗映射"""

    def applyGrayWindowTransform(self):
        if len(self.fn2_entry1.get()) == 0 or len(
                self.fn2_entry2.get()) == 0:
            messagebox.showerror(title='错误', message='参数不能为空')
            return

        # 获取参数
        win_size = int(self.fn2_entry1.get())
        win_pos = int(self.fn2_entry2.get())

        # 意外处理
        if win_size <= 0 or win_size > 4096 or win_pos < 0 or win_pos > 4095 or win_pos + int(
                round(win_size / 2)) > 4095 or win_pos - int(round(win_size / 2)) < 0:
            messagebox.showerror(title='错误', message='参数非法')
            return

        # 调用函数
        self.image_12bit_cur = self.handler.greyWindowMapping(self.image_12bit_cur, win_size, win_pos)
        self.image_8bit_cur = T.to8BitImage(self.image_12bit_cur)

        self.image_8bit_show = Image.fromarray(self.image_8bit_cur.astype('uint8'), mode="L")
        self.image_8bit_show = self.image_8bit_show.resize((640, 640))
        image_h = self.image_8bit_show.height
        image_w = self.image_8bit_show.width

        # 设置canvas的滑动窗口
        self.canvas.config(scrollregion=(0, 0, image_w, image_h))

        self.image_tk = ImageTk.PhotoImage(self.image_8bit_show)
        self.canvas.create_image(0, 0, anchor=NW, image=self.image_tk)

        self.fn2_btn1.config(
            relief=SUNKEN,
            bg="#555555"
        )

        messagebox.showinfo(title='提示', message='灰度窗映射成功')

    """直方图均衡"""

    def applyHistEqual(self):
        if self.image_12bit_cur is None:
            messagebox.showwarning(title='警告', message='图像为空')
            return

        self.image_12bit_cur = self.handler.histEqual(self.image_12bit_cur)
        self.image_8bit_cur = T.to8BitImage(self.image_12bit_cur)

        self.image_8bit_show = Image.fromarray(self.image_8bit_cur.astype('uint8'), mode="L")
        self.image_8bit_show = self.image_8bit_show.resize((640, 640))
        image_h = self.image_8bit_show.height
        image_w = self.image_8bit_show.width

        # 设置canvas的滑动窗口
        self.canvas.config(scrollregion=(0, 0, image_w, image_h))

        self.image_tk = ImageTk.PhotoImage(self.image_8bit_show)
        self.canvas.create_image(0, 0, anchor=NW, image=self.image_tk)

        self.fn3_btn1.config(
            relief=SUNKEN,
            bg="#555555"
        )
        messagebox.showinfo(title='提示', message='直方图均衡成功')

    """均值滤波"""

    def applyAverageFilter(self):
        # 获取参数
        if len(self.fn4_entry1.get()) == 0:
            messagebox.showerror(title='错误', message='参数不能为空')
            return
        elif int(self.fn4_entry1.get()) < 3 or int(self.fn4_entry1.get()) % 2 == 0:
            messagebox.showerror(title='错误', message='参数非法')
            return

        k_size = int(self.fn4_entry1.get())

        # 调用函数
        self.image_12bit_cur = self.handler.averageFilter(self.image_12bit_cur, k_size)
        self.image_8bit_cur = T.to8BitImage(self.image_12bit_cur)

        self.image_8bit_show = Image.fromarray(self.image_8bit_cur.astype('uint8'), mode="L")
        self.image_8bit_show = self.image_8bit_show.resize((640, 640))
        image_h = self.image_8bit_show.height
        image_w = self.image_8bit_show.width

        # 设置canvas的滑动窗口
        self.canvas.config(scrollregion=(0, 0, image_w, image_h))
        self.image_tk = ImageTk.PhotoImage(self.image_8bit_show)
        self.canvas.create_image(0, 0, anchor=NW, image=self.image_tk)

        self.fn4_btn1.config(
            relief=SUNKEN,
            bg="#555555"
        )

        messagebox.showinfo(title='提示', message='均值平滑成功')

    """高斯滤波"""

    def applyGaussianFilter(self):

        # 获取参数
        if len(self.fn5_entry1.get()) == 0 or len(self.fn5_entry2.get()) == 0:
            messagebox.showerror(title='错误', message='参数不能为空')
            return
        elif int(self.fn5_entry1.get()) < 3 or int(self.fn5_entry1.get()) % 2 == 0:
            messagebox.showerror(title='错误', message='参数非法')
            return

        k_size = int(self.fn4_entry1.get())
        sigma = int(self.fn5_entry1.get())

        # 调用函数
        self.image_12bit_cur = self.handler.gaussianFilter(self.image_12bit_cur, kernel_size=k_size, sigma=sigma)
        self.image_8bit_cur = T.to8BitImage(self.image_12bit_cur)

        self.image_8bit_show = Image.fromarray(self.image_8bit_cur.astype('uint8'), mode="L")
        self.image_8bit_show = self.image_8bit_show.resize((640, 640))
        image_h = self.image_8bit_show.height
        image_w = self.image_8bit_show.width

        # 设置canvas的滑动窗口
        self.canvas.config(scrollregion=(0, 0, image_w, image_h))
        self.image_tk = ImageTk.PhotoImage(self.image_8bit_show)
        self.canvas.create_image(0, 0, anchor=NW, image=self.image_tk)

        self.fn5_btn1.config(
            relief=SUNKEN,
            bg="#555555"
        )

        messagebox.showinfo(title='提示', message='高斯平滑成功')

    """锐化"""

    def applySobelSharpen(self):
        sobel_kind = self.v_sobel_select.get()

        # 调用函数
        self.image_12bit_cur = self.handler.sobelFilter(self.image_12bit_cur, filter_kind=sobel_kind)
        self.image_8bit_cur = T.to8BitImage(self.image_12bit_cur)

        self.image_8bit_show = Image.fromarray(self.image_8bit_cur.astype('uint8'), mode="L")
        self.image_8bit_show = self.image_8bit_show.resize((640, 640))
        image_h = self.image_8bit_show.height
        image_w = self.image_8bit_show.width

        # 设置canvas的滑动窗口
        self.canvas.config(scrollregion=(0, 0, image_w, image_h))
        self.image_tk = ImageTk.PhotoImage(self.image_8bit_show)
        self.canvas.create_image(0, 0, anchor=NW, image=self.image_tk)

        self.fn6_btn1.config(
            relief=SUNKEN,
            bg="#555555"
        )
        messagebox.showinfo(title='提示', message='Sobel锐化成功')

    def applyLaplaceSharpen(self):
        laplace_kind = self.v_laplace_select.get()

        # 调用函数
        self.image_12bit_cur = self.handler.laplaceFilter(self.image_12bit_cur, filter_kind=laplace_kind)
        self.image_8bit_cur = T.to8BitImage(self.image_12bit_cur)

        self.image_8bit_show = Image.fromarray(self.image_8bit_cur.astype('uint8'), mode="L")
        self.image_8bit_show = self.image_8bit_show.resize((640, 640))
        image_h = self.image_8bit_show.height
        image_w = self.image_8bit_show.width

        # 设置canvas的滑动窗口
        self.canvas.config(scrollregion=(0, 0, image_w, image_h))
        self.image_tk = ImageTk.PhotoImage(self.image_8bit_show)
        self.canvas.create_image(0, 0, anchor=NW, image=self.image_tk)

        self.fn7_btn1.config(
            relief=SUNKEN,
            bg="#555555"
        )

        messagebox.showinfo(title='提示', message='Sobel锐化成功')


if __name__ == '__main__':
    app_window = Tk()
    app = Application(app_window)
    app_window.mainloop()
