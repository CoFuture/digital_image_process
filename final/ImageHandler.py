import numpy as np
import cv2
from PIL import Image


class ImageReader:
    def __init__(self, path):
        self.image_path = path
        self.image_array = []
        with open(self.image_path, 'rb') as f:
            self.image_width = int.from_bytes(f.read(4), byteorder="little", signed=False)
            self.image_height = int.from_bytes(f.read(4), byteorder="little", signed=False)
            for i in range(self.image_height):
                line_temp = []
                for j in range(self.image_width):
                    pixel_data = int.from_bytes(f.read(2), byteorder="little", signed=False) & 4095
                    line_temp.append(pixel_data)
                self.image_array.append(line_temp)

    # 获取图像数组
    def getImageArrayRaw(self):
        return self.image_array

    def getImageArray(self):
        array = np.array(self.image_array)
        m_min = np.min(array)
        m_max = np.max(array)
        matrix = array - m_min
        return np.array(np.rint((matrix - m_min) / float(m_max - m_min) * 255.0), dtype=np.uint8)


class ImageWriter:
    def __init__(self, array):
        # 输入类型图像matrix
        self.image_array = array

    # 需要注意，这里使用的是12位的灰度图
    def saveImageRaw(self, save_path):
        image_height = self.image_array.shape[0]
        image_width = self.image_array.shape[1]
        with open(save_path, 'wb') as f:
            # 写入长宽高
            f.write(int(image_width).to_bytes(4, byteorder='little', signed=False))
            f.write(int(image_height).to_bytes(4, byteorder='little', signed=False))
            for i in range(image_height):
                for j in range(image_width):
                    pixel_byte = int(self.image_array[i][j]).to_bytes(2, byteorder='little', signed=False)
                    f.write(pixel_byte)


# 图像处理类，进行基本变换：灰度窗映射
class ImageHandler:
    def __init__(self, image):
        self.image = image

    # 灰度化处理
    def toGreyImage(self):
        pass

    # 灰度窗映射
    def greyWindowMapping(self, width, position):
        # input： 灰度窗的宽度，灰度窗位置
        pass

    # 局部放大
    def partZoom(self, position, factor):
        # input: 放大位置， 放大系数factor
        pass

    # 细节增强
    def detailAugment(self):
        pass


if __name__ == '__main__':
    # reader = ImageReader("images_raw/vertebra.raw")
    reader = ImageReader("test.raw")
    # print(b'\x01' + b'\x02')
    image_array = reader.getImageArray()
    # print(reader.image_height, reader.image_width, image_array.shape)
    #
    # # 测试写功能
    # writer = ImageWriter(image_array)
    # writer.saveImageRaw("test.raw")

    # # 图像保存
    # img_new = Image.fromarray(image_array.astype('uint8'), mode="L")
    # img_new.save("test.png")


