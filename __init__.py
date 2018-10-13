from Images import Images
import matplotlib.pyplot as plt


def show_gistogram(colors_amount):
    x_labels = range(255)

    print(colors_amount['red'])
    plt.subplot(311)
    plt.plot(x_labels, colors_amount['red'])
    plt.title('A tale of 2 subplots')
    plt.xlabel('color light')
    plt.ylabel('Red layer')

    print(colors_amount['green'])
    plt.subplot(312)
    plt.plot(x_labels, colors_amount['green'])
    plt.xlabel('color light')
    plt.ylabel('Green layer')

    print(colors_amount['blue'])
    plt.subplot(313)
    plt.plot(x_labels, colors_amount['blue'])
    plt.xlabel('color light')
    plt.ylabel('Blue layer')

    plt.show()


if __name__ == '__main__':
    image = Images()
    image.load_image('Images/56465465456.png')
    # colors_amount = image.get_amount_colors()
    # show_gistogram(colors_amount)

    image.set_filter()
    # image.convert_to_gray()
    # image.set_log_correction(15)

    image.save_image()



