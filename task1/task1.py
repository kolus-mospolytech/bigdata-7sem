import csv
import io

import matplotlib.pyplot as plt
from PIL import Image


# Конвертирование изображения в оттенки серого:
def convert_image(input_image):
    # сначала копируем исходное изображение
    output_image = input_image.copy()

    # затем обходим каждый пиксель
    for x in range(output_image.width):
        for y in range(output_image.height):
            # вычисляем его яркость по формуле
            r, g, b = output_image.getpixel((x, y))
            brightness = int(0.299 * r + 0.587 * g + 0.114 * b)
            # получившимся значением яркости перезаписываем цвета пикселя
            output_image.putpixel((x, y), (brightness, brightness, brightness))
    return output_image


def create_histogram(input_image):
    # инициализируем пустой массив для данных гистограммы
    data = []

    # обходим картинку и заносим в массив яркость каждого пикселя
    for x in range(input_image.width):
        for y in range(input_image.height):
            brightness = input_image.getpixel((x, y))
            data.append(brightness[0])

    # собираем гистограмму
    plt.hist(x=data, bins='auto')
    plt.grid(axis='y', alpha=0.75)
    plt.xlabel('Частота')
    plt.ylabel('Яркость')

    # сохраняем гистограмму во временный буфер и затем открываем как PIL-объект
    img_buf = io.BytesIO()
    plt.savefig(img_buf, format='png')
    output_image = Image.open(img_buf)

    return output_image


# замена цветов пикселей в первой области однородности
def swap_color(input_image):
    # копируем входное изображение
    output_image = input_image.copy()

    # обходим пиксели
    for x in range(output_image.width):
        for y in range(output_image.height):
            # из гистограммы выяснили, что первая область
            # однородности начинается на значении 0, а заканчивается на 25,
            # поэтому все пиксели с яркостью не более 25 красим в красный
            brightness = output_image.getpixel((x, y))
            if brightness[0] <= 25:
                output_image.putpixel((x, y), (255, 0, 0))
    return output_image


# заполнение .csv файла
def fill_csv(input_file, normal_image, grayscale_image):
    # инициализируем csv-писателя
    writer = csv.writer(input_file)

    # заполняем шапку
    writer.writerow(['R', 'G', 'B', 'label'])

    # обходим пиксели, из цветной версии изображения берем
    # значения RGB для каждого пикселя, а из Ч/Б - яркость
    # и заносим в .csv; RGB как R, G и B, а яркость как label
    for x in range(normal_image.width):
        for y in range(normal_image.height):
            r, g, b = normal_image.getpixel((x, y))
            brightness = grayscale_image.getpixel((x, y))
            writer.writerow([r, g, b, brightness[0]])

    return input_file


# открываем изображение
img = Image.open(r"data/plane.png")

# генерируем картинки
grayscale_img = convert_image(img)
histogram = create_histogram(grayscale_img)
swapped_colors = swap_color(grayscale_img)

# сохраняем картинки
grayscale_img.save("output/plane_grayscale.png")
histogram.save("output/histogram.png")
swapped_colors.save("output/plane_red.png")

# заполняем .csv
with open('output/pixels.csv', 'w+') as file:
    fill_csv(file, img, grayscale_img)
