from tkinter import *
from PIL import ImageTk, Image
from final.ImageHandler import ImageReader, ImageWriter, ImageHandler
from final import basicTransform as T
import numpy as np


class Application:
    def __init__(self, window):
        assert window is not None
        self.window = window

        self.initWindow()

        # 图片功能控件
        self.reader = None
        self.handler = None
        self.writer = None

        """初始化UI控件"""
        # 顶部标签
        self.frame1 = Frame(self.window)

        # 标签变量
        self.v_title_text = StringVar()
        self.v_title_text.set("lumbar.raw")

        self.titleLabel = Label(self.frame1, textvariable=self.v_title_text, font=('微软雅黑', 20), fg="black")
        self.titleLabel.pack(pady=10)
        self.frame1.pack(side=TOP)

        # frame2 包括左侧的图片canvas 右侧的function block
        self.frame2 = Frame(self.window)
        self.frame2_left = Frame(self.frame2)
        self.frame2_right = Frame(self.frame2)

        self.canvas = Canvas(self.frame2_left, height=600, width=600, bg='gray')
        self.canvas.pack()

        # 功能栏 功能1 选择图像
        self.fn1_frame = Frame(self.frame2_right, borderwidth=2, relief="solid")
        self.fn1_frame1 = Frame(self.fn1_frame)
        self.label1 = Label(self.fn1_frame1, text="选择图像", font=('微软雅黑', 15))
        self.label1.pack()
        self.fn1_frame1.pack(side=TOP, fill=BOTH)

        self.v_img_select = IntVar()
        self.v_img_select.set(2)

        self.fn1_frame2 = Frame(self.fn1_frame)
        self.radio1 = Radiobutton(self.fn1_frame2, text="lumbar", font=('微软雅黑', 12), variable=self.v_img_select,
                                  value=1)
        self.radio2 = Radiobutton(self.fn1_frame2, text="lung", font=('微软雅黑', 12), variable=self.v_img_select, value=2)
        self.radio3 = Radiobutton(self.fn1_frame2, text="vertebra", font=('微软雅黑', 12), variable=self.v_img_select,
                                  value=3)

        self.radio1.pack(side=LEFT, padx=5, pady=10)
        self.radio2.pack(side=LEFT, padx=5, pady=10)
        self.radio3.pack(side=LEFT, padx=5, pady=10)
        self.fn1_frame2.pack(side=TOP, fill=BOTH)

        self.fn1_frame.pack(side=TOP, fill=BOTH, pady=10)
        # 功能栏 功能2 灰度窗映射
        self.fn2_frame = Frame(self.frame2_right)
        self.fn2_frame1 = Frame(self.frame2_right)
        self.label2 = Label(self.fn2_frame1, text="灰度窗映射", font=('微软雅黑', 10))
        self.label2.pack(side=LEFT)
        self.fn2_frame1.pack(side=TOP)

        self.frame2_left.pack(side=LEFT, padx=13, pady=13)
        self.frame2_right.pack(side=RIGHT, padx=13, pady=13)
        self.frame2.pack()

        # frame

    def initWindow(self):
        self.window.title("my window")
        screen_w = self.window.winfo_screenwidth()
        screen_h = self.window.winfo_screenheight()
        self.window.geometry(str(screen_h) + "x" + str(screen_w))
        print(screen_w, screen_h)

        pass

    # 选择图片
    def selectImage(self):
        pass

    # 应用变换
    def applyTransform(self):
        pass

    # 重置变换
    def resetTransform(self):
        pass

    # 保存图片
    def saveImage(self):
        pass


if __name__ == '__main__':
    app_window = Tk()
    app = Application(app_window)

    # 设定图片
    # reader = ImageReader("images_raw/lumbar.raw")
    # reader = ImageReader("images_raw/lung.raw")
    # reader = ImageReader("images_raw/vertebra.raw")
    #
    # image2show = Image.fromarray(reader.getImageArray().astype('uint8'), mode="L")
    #
    # image_h = image2show.height
    # image_w = image2show.width
    #
    # print(image_h, image_w)
    #
    # image2show = image2show.resize((800, 800))
    # photo = ImageTk.PhotoImage(image2show)
    #
    #
    # canvas = Canvas(window, height=800, width=800)
    # canvas.create_image(0, 0, anchor=NW, image=photo)
    # canvas.pack()

    app_window.mainloop()
