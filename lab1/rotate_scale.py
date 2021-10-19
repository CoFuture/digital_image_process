"""
题目要求
图像几何变换实验：以图像几何中心为参考点，对图像做顺时针方向旋转45度并放大3倍，
输出图像尺寸与输入图像相同，参考点在输出图像中仍位于图像几何中心位置。
其中，插值采用双线性插值算法。

要求：可以自选主流语言，图像几何变换的核心算法（包括坐标映射、像素遍历、灰度插值在内）
必须使用程序设计语言定义的语句（排除函数库中的工具）自行编程实现。
"""

from PIL import Image
import numpy as np


if __name__ == '__main__':
    image = Image.open("barbara.bmp")
    image = np.array(image)
    print(image)
    pass

