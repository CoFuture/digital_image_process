import math
import numpy as np


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


# 图像放大
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
    temp_y_low = (int(source_image[x_high][y_low]) - int(source_image[x_low][y_low])) * (pos_x - x_low) + int(
        source_image[x_low][y_low])
    temp_y_high = (int(source_image[x_high][y_high]) - int(source_image[x_low][y_high])) * (pos_x - x_low) + int(
        source_image[x_low][y_high])
    # 在y轴上做插值
    return int(round((temp_y_high - temp_y_low) * (pos_y - y_low) + temp_y_low))


# 映射到8bit空间
def to8BitImage(image):
    array = np.array(image)
    m_min = np.min(array)
    m_max = np.max(array)
    # matrix = array - m_min
    # matrix = (matrix - m_min) / float(m_max - m_min) * 255.0
    # matrix = np.rint(matrix)
    # matrix = np.array(matrix, dtype=np.uint8)
    # return matrix
    return np.array(np.rint((array - m_min) / float(m_max - m_min) * 255.0), dtype=np.uint8)
