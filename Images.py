import array
from builtins import range, open
from os.path import basename, splitext

import png


class Images:
    width = 0
    height = 0
    pixels = []
    metadata = []
    pixel_byte_width = 0
    full_file_name = ''

    def __init__(self):
        self.clear()

    def clear(self):
        self.width = 0
        self.height = 0
        self.pixels = []
        self.metadata = []
        self.pixel_byte_width = 0
        self.full_file_name = ''

    # def create_image(self):
    #     width = 255
    #     height = 255
    #
    #     pixel_byte_width = 3
    #     pixels = self.create_empty_canvas(width, height, pixel_byte_width)
    #
    #     pixels = self.process_pixels(pixels, width, height, pixel_byte_width)
    #
    #     self.save_pixels(pixels, width, height, pixel_byte_width)

    def load_image(self, filename):
        self.clear()

        reader = png.Reader(filename=filename)
        self.width, self.height, raw_pixels, self.metadata = reader.read()
        self.full_file_name = basename(reader.file.name)

        self.pixel_byte_width = 4 if self.metadata['alpha'] else 3
        self.pixels = self.convert_to_lists(raw_pixels)

    def convert_to_gray(self):
        for i in range(0, self.width):
            for j in range(0, self.height):
                color = self.pixels[i][j]
                gray = int(round(color[0] * 0.3 + color[1] * 0.59 + color[2] * 0.11))
                self.pixels[i][j] = [gray, gray, gray, color[3]] if self.pixel_byte_width == 4 else [gray, gray, gray]

        self.full_file_name = 'gray_' + self.full_file_name

    def get_red(self):
        red = [0] * 256
        for i in range(0, self.width):
            for j in range(0, self.height):
                color = self.pixels[i][j]
                red[color[0]] += 1

        del red[0]
        return red

    def save_pixels(self, pixels, width, height, pixel_byte_width, full_file_name):
        raw_pixels = self.convert_to_array(pixels, pixel_byte_width)
        output = open('image-with-red-dot.png', 'wb')
        writer = png.Writer(width, height)
        writer.write_array(output, raw_pixels)
        output.close()

    def save_image(self):
        pixel_byte_width = 4 if self.metadata['alpha'] else 3
        raw_pixels = self.convert_to_array(self.pixels, pixel_byte_width)
        filename, extension = splitext(self.full_file_name)

        output = open(filename + '_line' + extension, 'wb')
        writer = png.Writer(self.width, self.height, **self.metadata)
        writer.write_array(output, raw_pixels)
        output.close()

    def create_empty_canvas(self, width, height, pixel_width):
        pixels = []
        empty_pixel = [255, 255, 255, 255] if pixel_width == 4 else [255, 255, 255]
        for i in range(0, height):
            pixels.append([])
            for j in range(0, width):
                pixels[i].append(empty_pixel)

        return pixels

    def convert_to_lists(self, raw_pixels):
        index = 0
        pixels = []
        for line in list(raw_pixels):
            pixels.append([])
            line = list(line)
            for i in range(0, len(line), self.pixel_byte_width):
                pixel = line[i:i + self.pixel_byte_width]
                pixels[index].append(pixel)

            index += 1

        return pixels

    def convert_to_array(self, pixels, pixel_width):
        merged_list = []
        for line in pixels:
            for pixel in line:
                merged_list += pixel

        raw_pixels = array.array('B', merged_list)

        return raw_pixels