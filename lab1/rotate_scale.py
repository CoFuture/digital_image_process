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
import math


# 坐标轴平移变化
def translate(vector_in, vector_center):
    # vector in 1x3  vector_center 1x2
    if len(vector_in) != 3 or len(vector_center) != 2:
        return -1

    x_in = vector_in[0]
    y_in = vector_in[1]
    x_center = vector_center[0]
    y_center = vector_center[1]
    x_out = x_in - x_center
    y_out = y_in - y_center

    return [x_out, y_out, 1]


# 输入 1x3 输出 1x3 默认正方形为逆时针
def rotate(vector_in, theta):
    if len(vector_in) != 3:
        return -1

    x_in = vector_in[0]
    y_in = vector_in[1]
    x_out = np.cos(theta) * x_in - np.sin(theta) * y_in
    y_out = np.sin(theta) * x_in + np.cos(theta) * y_in

    return [x_out, y_out, 1]


# 输入 1x3  输出 1x3
def scale(vector_in, scale_x, scale_y):
    if len(vector_in) != 3:
        return -1

    x_in = vector_in[0]
    y_in = vector_in[1]

    x_out = scale_x * x_in
    y_out = scale_y * y_in

    return [x_out, y_out, 1]


# 双线性插值 输入像素位置，原图像
def bilinear_interpolation(pos, source_image):
    pos_x = pos[0]
    pos_y = pos[1]

    x_low = int(math.floor(pos_x))
    x_high = int(math.ceil(pos_x))
    y_low = int(math.floor(pos_y))
    y_high = int(math.ceil(pos_y))

    # 在x轴上做插值
    temp_y_low = (int(source_image[x_high][y_low]) - int(source_image[x_low][y_low])) * (pos_x - x_low) + int(source_image[x_low][y_low])
    temp_y_high = (int(source_image[x_high][y_high]) - int(source_image[x_low][y_high])) * (pos_x - x_low) + int(source_image[x_low][y_high])
    # 在y轴上做插值
    return int(round((temp_y_high - temp_y_low) * (pos_y - y_low) + temp_y_low))


if __name__ == '__main__':
    image = Image.open("barbara.bmp")
    image = np.array(image)

    center_x = int(round(image.shape[0] / 2))
    center_y = int(round(image.shape[1] / 2))

    result = np.zeros((image.shape[0], image.shape[1]), dtype=int)

    for row in range(result.shape[0]):
        for col in range(result.shape[1]):
            pos_vec = [row, col, 1]
            pos_vec = translate(pos_vec, [center_x, center_y])
            pos_vec = scale(pos_vec, 1/3, 1/3)
            pos_vec = rotate(pos_vec, math.pi/4)
            pos_vec = translate(pos_vec, [-center_x, -center_y])

            if pos_vec[0] < 0 or pos_vec[0] > (image.shape[0] - 1) or pos_vec[1] < 0 or pos_vec[1] > (image.shape[1] - 1):
                result[row][col] = 1
            else:
                result[row][col] = bilinear_interpolation(pos_vec, image)

    # print(image)

    # print(result)

    img_new = Image.fromarray(result.astype('uint8'), mode="L")
    img_new.save("result.bmp")
    pass
