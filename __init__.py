from Images import Images
import matplotlib.pyplot as plt

if __name__ == '__main__':
    image = Images()
    image.load_image('Images/icon.png')
    # image.convert_to_gray()
    red = image.get_red()

    image.save_image()

    x_labels = range(255)
    data_values = range(255, 0, -1)
    data_values2 = range(255)

    plt.subplot(311)
    plt.plot(x_labels, red)
    plt.title('A tale of 2 subplots')
    plt.ylabel('Undamped1')

    plt.subplot(312)
    plt.plot(x_labels, data_values2)
    plt.xlabel('time (s)')
    plt.ylabel('Undamped2')

    plt.subplot(313)
    plt.plot(x_labels, data_values2)
    plt.xlabel('time (s)')
    plt.ylabel('Undamped3')

    plt.show()

