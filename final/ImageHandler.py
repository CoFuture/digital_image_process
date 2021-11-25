import numpy as np
import math
import copy
from final import basicTransform as T
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
        return np.array(self.image_array)

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
        # 输入图像 4096级灰度图像
        self.image = image

    # 灰度化处理
    def toGreyImage(self):
        pass

    # 灰度窗映射, 返回8bit图像
    # todo 转成4096级处理
    def greyWindowMapping(self, width, pos_value):
        # input： 灰度窗的宽度，灰度窗位置
        # 小于灰度窗 映射到 0
        # 大于灰度窗 映射到 255
        # 灰度窗之间 0～255线性映射

        window_min = pos_value - int(round(width / 2))
        window_max = pos_value + int(round(width / 2))

        assert window_min >= 0
        assert window_max <= 4095

        image_r = copy.deepcopy(self.image)

        for i in range(self.image.shape[0]):
            for j in range(self.image.shape[1]):
                if image_r[i][j] < window_min:
                    image_r[i][j] = 0
                elif image_r[i][j] > window_max:
                    image_r[i][j] = 255
                else:
                    # 线性映射
                    image_r[i][j] = int(math.floor((image_r[i][j] - window_min) / width * 255))

        return image_r

    # 局部放大，返回8bit图像
    def partZoom(self, center_h, center_w, scale_h, scale_w, window_w, window_h):
        # input: 放大位置， 放大系数factor, 放大后图片长、宽
        image_r = np.empty([window_h, window_w], dtype=int)

        for h in range(image_r.shape[0]):
            for w in range(image_r.shape[1]):
                pos_vec = [h, w, 1]
                """均采用逆变换"""
                # 坐标变换
                pos_vec = T.translate(pos_vec, [center_h, center_w])
                # zoom
                pos_vec = T.scale(pos_vec, 1/scale_h, 1/scale_w)
                # 坐标变换
                pos_vec = T.translate(pos_vec, [-center_h, -center_w])

                if pos_vec[0] < 0 or pos_vec[0] > (self.image.shape[0] - 1) or pos_vec[1] < 0 or pos_vec[1] > (
                        self.image.shape[1] - 1):
                    # 超出边界的部分使用黑色填充
                    image_r[h][w] = 0
                    print("out")
                else:
                    image_r[h][w] = T.bilinear_interpolation(pos_vec, self.image)

        return T.to8BitImage(image_r)

    # 细节增强
    def detailAugment(self):
        pass


if __name__ == '__main__':
    reader = ImageReader("images_raw/lumbar.raw")
    # reader = ImageReader("test.raw")
    # print(b'\x01' + b'\x02')
    image_array = reader.getImageArray()
    image_array_raw = reader.getImageArrayRaw()
    print(reader.image_height, reader.image_width)

    # img_origin = Image.fromarray(image_array.astype('uint8'), mode="L")
    # img_origin.save("origin.png")

    handler = ImageHandler(image_array_raw)
    image_temp = handler.partZoom(800, 800, 3, 3, 1000, 1000)
    img_result = Image.fromarray(image_temp.astype('uint8'), mode="L")
    img_result.show()
    # img_result.save("result.png")
    #
    # # 测试写功能
    # writer = ImageWriter(image_array)
    # writer.saveImageRaw("test.raw")

    # # 图像保存
    # img_new = Image.fromarray(image_array.astype('uint8'), mode="L")
    # img_new.save("test.png")

    # 图像展示

