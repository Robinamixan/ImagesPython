import array
import math
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
        self.convert_pixels_to_int()

    def convert_to_gray(self):
        for i in range(0, self.height):
            for j in range(0, self.width):
                color = self.pixels[i][j]
                gray = int(round(color[0] * 0.3 + color[1] * 0.59 + color[2] * 0.11))
                self.pixels[i][j] = [gray, gray, gray, color[3]] if self.pixel_byte_width == 4 else [gray, gray, gray]

        self.full_file_name = 'gray_' + self.full_file_name
        self.convert_pixels_to_int()

    def get_amount_colors(self):
        colors_amount = {
            'red': [0] * 256,
            'green': [0] * 256,
            'blue': [0] * 256,
        }
        for i in range(0, self.height):
            for j in range(0, self.width):
                color = self.pixels[i][j]
                if self.pixel_byte_width == 4 and color[3] == 0:
                    continue
                colors_amount['red'][color[0]] += 1
                colors_amount['green'][color[1]] += 1
                colors_amount['blue'][color[2]] += 1

        del colors_amount['red'][0]
        del colors_amount['green'][0]
        del colors_amount['blue'][0]

        return colors_amount

    def set_log_correction(self, c_coef):
        for i in range(0, self.height):
            for j in range(0, self.width):
                color = self.pixels[i][j]
                if self.pixel_byte_width == 4 and color[3] == 0:
                    continue
                for color_number in range(0, 3):
                    color[color_number] = c_coef * math.log(1 + color[color_number])

        self.full_file_name = 'log_' + self.full_file_name
        self.convert_pixels_to_int()

    def set_filter(self):
        self.convert_to_gray()
        self.copy_borders()

        filtered_pixels = []

        core_left = [0, 1, -1, 0]
        core_right = [1, 0, 0, -1]

        for i in range(0, self.height):
            filtered_pixels.append([])
            for j in range(0, self.width):
                current_arrea = [self.pixels[i][j], self.pixels[i][j+1], self.pixels[i+1][j], self.pixels[i+1][j+1]]

                current_core_left = self.procces_filter_core(core_left, current_arrea)
                current_core_right = self.procces_filter_core(core_right, current_arrea)

                new_light = math.sqrt(math.pow(current_core_left, 2) + math.pow(current_core_right, 2))

                new_color = [new_light, new_light, new_light]
                if self.pixel_byte_width == 4:
                    new_color.append(self.pixels[i][j][3])

                filtered_pixels[i].append(new_color)

            filtered_pixels.append([])

        self.pixels = filtered_pixels
        self.full_file_name = 'filtered_' + self.full_file_name
        self.convert_pixels_to_int()

    def procces_filter_core(self, core, area):
        filled_core = list(core)
        for index, item in enumerate(area):
            filled_core[index] *= item[0]

        # result = math.sqrt(math.pow(filled_core[1] - filled_core[2], 2) + math.pow(filled_core[0] - filled_core[3], 2))
        result = filled_core[0] + filled_core[1] + filled_core[2] + filled_core[3]

        return result

    def copy_borders(self):
        for i in range(0, self.height):
            self.pixels[i].append(self.pixels[i][self.width - 1])

        self.pixels.append(self.pixels[self.height - 1])

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

    def convert_pixels_to_int(self):
        for i in range(0, self.height):
            for j in range(0, self.width):
                color = self.pixels[i][j]
                for c in range(0, len(color)):
                    self.pixels[i][j][c] = int(self.pixels[i][j][c])

    def convert_to_array(self, pixels, pixel_width):
        merged_list = []
        for line in pixels:
            for pixel in line:
                merged_list += pixel

        raw_pixels = array.array('B', merged_list)
        return raw_pixels