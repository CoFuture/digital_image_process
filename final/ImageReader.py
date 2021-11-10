import numpy as np
import cv2
from PIL import Image


class ImageReader:
    def __init__(self, path):
        self.image_path = path
        self.image_array = []
        self.image_height = -1

        with open(self.image_path, 'rb') as f:
            self.image_width = int.from_bytes(f.read(4), byteorder="little", signed=False)
            self.image_height = int.from_bytes(f.read(4), byteorder="little", signed=False)
            for i in range(self.image_height):
                line_temp = []
                for j in range(self.image_width):
                    pixel_data = int.from_bytes(f.read(2), byteorder="little", signed=False) & 4095
                    line_temp.append(pixel_data)
                self.image_array.append(line_temp)

    def read(self):
        pass

    # 获取图像数组
    def getImageArrayRaw(self):

        pass

    def getImageArray(self):
        array = np.array(self.image_array)
        m_min = np.min(array)
        m_max = np.max(array)
        matrix = array - m_min
        return np.array(np.rint((matrix - m_min) / float(m_max - m_min) * 255.0), dtype=np.uint8)


if __name__ == '__main__':
    reader = ImageReader("images_raw/vertebra.raw")
    # print(b'\x01' + b'\x02')
    image_array = reader.getImageArray()
    print(reader.image_height, reader.image_width, image_array.shape)

    # 图像保存
    img_new = Image.fromarray(image_array.astype('uint8'), mode="L")
    img_new.save("vertebra.png")
    pass
