import csv
import io

import matplotlib.pyplot as plt
from PIL import Image
from numpy import histogram as hist


def convert_image(input_image):
    output_image = input_image.copy()

    for x in range(output_image.width):
        for y in range(output_image.height):
            r, g, b = output_image.getpixel((x, y))
            brightness = int(0.299 * r + 0.587 * g + 0.114 * b)
            output_image.putpixel((x, y), (brightness, brightness, brightness))

    return output_image


def create_histogram(input_image):
    data = []
    hist_data = []

    for x in range(input_image.width):
        for y in range(input_image.height):
            brightness = input_image.getpixel((x, y))
            data.append([x, y, brightness[0]])
            hist_data.append(brightness[0])

    plt.hist(x=hist_data, bins=30)
    plt.grid(axis='y', alpha=0.75)
    plt.xlabel('Яркость')
    plt.ylabel('Частота')
    plt.show()

    # img_buf = io.BytesIO()
    # plt.savefig(img_buf, format='png')
    # hist_1 = Image.open(img_buf)

    hist2_data_x = []
    hist2_data_y = []
    new_data = []

    for item in data:
        if (int(item[2]) >= 104) & (int(item[0] < 650)):
            new_data.append(item)
            hist2_data_x.append(item[0])
            hist2_data_y.append(item[1])

    plt.clf()
    plt.hist(x=hist2_data_x, bins=30)
    plt.grid(axis='y', alpha=0.75)
    plt.xlabel('x')
    plt.ylabel('Частота')
    plt.show()

    # img_buf = io.BytesIO()
    # plt.savefig(img_buf, format='png')
    # hist_x = Image.open(img_buf)

    plt.clf()
    plt.hist(x=hist2_data_y, bins=30)
    plt.grid(axis='y', alpha=0.75)
    plt.xlabel('y')
    plt.ylabel('Частота')
    plt.show()


    # img_buf = io.BytesIO()
    # plt.savefig(img_buf, format='png')
    # hist_y = Image.open(img_buf)

    # return hist_1, hist_x, hist_y


def swap_color(input_image):
    output_image = input_image.copy()

    for x in range(output_image.width):
        for y in range(output_image.height):
            brightness = output_image.getpixel((x, y))
            if (brightness[0] >= 104) & (x < 650) & (y < 500):
                output_image.putpixel((x, y), (255, 0, 0))

    return output_image


# заполнение .csv файла
def fill_csv(input_file, input_image):
    # инициализируем csv-писателя
    writer = csv.writer(input_file)

    # читаем массив локальных минимумов из файла
    with open('output/histogram.csv', 'r') as hist_text:
        reader = csv.reader(hist_text)
        for row in reader:
            mins = row
            break

    # обходим пиксели, из цветной версии изображения берем
    # значения RGB для каждого пикселя, а из Ч/Б - яркость
    # и заносим в .csv; RGB как R, G и B, а яркость как label
    for x in range(input_image.width):
        row = []
        for y in range(input_image.height):
            r, g, b = input_image.getpixel((x, y))
            label = len(mins)
            for i in range(len(mins)):
                if r <= int(mins[i]):
                    label = i
                    break

            row.append([r, g, b, label])
        writer.writerow(row)

    return input_file


# открываем изображение
img = Image.open(r"data/755850380797162.jpeg")

# генерируем картинки
grayscale_img = convert_image(img)
# histogram = create_histogram(grayscale_img)
create_histogram(grayscale_img)
swapped_colors = swap_color(grayscale_img)

# сохраняем картинки
grayscale_img.save("output/grayscale.png")
# histogram[0].save("output/histogram.png")
# histogram[1].save("output/histogram_x.png")
# histogram[2].save("output/histogram_y.png")
swapped_colors.save("output/colored.png")

# заполняем .csv
# with open('output/pixels.csv', 'w+') as file:
#     fill_csv(file, grayscale_img)
