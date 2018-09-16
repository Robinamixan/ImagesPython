import array
import png


class Images:
    def __init__(self):
        c = 3

    def create_image(self):
        width = 255
        height = 255

        pixel_byte_width = 3
        pixels = self.create_empty_canvas(width, height, pixel_byte_width)

        pixels = self.process_pixels(pixels, width, height, pixel_byte_width)

        self.save_pixels(pixels, width, height, pixel_byte_width)

    def load_image(self, filename):
        reader = png.Reader(filename='Images/apple_alpha_1.1.png')
        width, height, raw_pixels, metadata = reader.read()

        pixel_byte_width = 4 if metadata['alpha'] else 3
        pixels = self.convert_to_lists(raw_pixels, pixel_byte_width)

        pixels = self.process_pixels(pixels, width, height, pixel_byte_width)

        self.save_image(pixels, width, height, metadata)

    def process_pixels(self, pixels, width, height, pixel_byte_width):
        for i in range(0, width):
            new_pixel = [0, i*10, 0, 255] if pixel_byte_width == 4 else [0, i, 0]
            pixels[0][i] = new_pixel

        return pixels

    def save_pixels(self, pixels, width, height, pixel_byte_width):
        raw_pixels = self.convert_to_array(pixels, pixel_byte_width)
        output = open('image-with-red-dot.png', 'wb')
        writer = png.Writer(width, height)
        writer.write_array(output, raw_pixels)
        output.close()

    def save_image(self, pixels, width, height, metadata):
        pixel_byte_width = 4 if metadata['alpha'] else 3
        raw_pixels = self.convert_to_array(pixels, pixel_byte_width)
        output = open('image-with-red-dot.png', 'wb')
        writer = png.Writer(width, height, **metadata)
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

    def convert_to_lists(self, raw_pixels, pixel_width):
        index = 0
        pixels = []
        for line in list(raw_pixels):
            pixels.append([])
            line = list(line)
            for i in range(0, len(line), pixel_width):
                pixel = line[i:i + pixel_width]
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