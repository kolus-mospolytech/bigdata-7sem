import csv
import io

import matplotlib.pyplot as plt
from PIL import Image
from numpy import histogram as hist


# конвертирование изображения в оттенки серого:
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

    # собираем массив гистограммы
    hist_array = hist(data, 11)
    local_min = []
    local_min_values = []

    # находим позиции локальных минимумов
    for i in range(1, len(hist_array[0]) - 1):
        if (hist_array[0][i] < hist_array[0][i - 1]) & (hist_array[0][i] < hist_array[0][i + 1]):
            local_min.append(i)

    # находим промежутки локальных минимумов и берем середину промежутка как локальный минимум
    for i in local_min:
        local_min_values.append(int((hist_array[1][i] + hist_array[1][i + 1]) / 2))

    # записываем данные в .csv файл
    with open('output/histogram.csv', 'w+') as hist_text:
        writer = csv.writer(hist_text)
        writer.writerow(local_min_values)
        writer.writerow(hist_array)

    # собираем графическую гистограмму
    plt.hist(x=data, bins=11)
    plt.grid(axis='y', alpha=0.75)
    plt.xlabel('Яркость')
    plt.ylabel('Частота')

    # сохраняем гистограмму во временный буфер и затем открываем как PIL-объект
    img_buf = io.BytesIO()
    plt.savefig(img_buf, format='png')
    output_image = Image.open(img_buf)

    return output_image


# замена цветов пикселей в первой области однородности
def swap_color(input_image):
    # копируем входное изображение
    output_image = input_image.copy()

    # читаем массив локальных минимумов из файла
    with open('output/histogram.csv', 'r') as hist_text:
        reader = csv.reader(hist_text)
        for row in reader:
            threshold = row
            break

    # обходим пиксели
    for x in range(output_image.width):
        for y in range(output_image.height):
            # из массива с локальными минимумами берем первый
            # и используем как порог
            # красим все пиксели с яркостью не более пороговой в красный цвет
            brightness = output_image.getpixel((x, y))
            if brightness[0] <= int(threshold[0]):
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
    fill_csv(file, grayscale_img)
