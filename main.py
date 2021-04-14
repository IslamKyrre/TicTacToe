import sys

from PIL import Image, ImageDraw
from math import floor
from collections import Counter


def is_black(pixel):
    r, g, b, a = pixel
    return max(r, g, b) < 10 and not a == 0


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: python3 main.py <path_to_input_image> <path_to_output_image>")

    input_image = sys.argv[1]
    output_image = sys.argv[2]

    with Image.open(input_image) as img:
        pixels = img.load()

        draw = ImageDraw.Draw(img)

        # Ищем границы
        min_x, min_y, max_x, max_y = img.width, img.height, 0, 0
        for x in range(img.width):
            for y in range(img.height):
                if is_black(pixels[x, y]):
                    min_x = min(min_x, x)
                    min_y = min(min_y, y)
                    max_x = max(max_x, x)
                    max_y = max(max_y, y)

        # Ширина и высота
        wx = max_x - min_x + 1
        wy = max_y - min_y + 1

        # Поле и крестики/нолики
        field = [[0] * 3 for _ in range(3)]

        #  0 - empty
        #  1 - X
        #  2 - O

        for px in range(3):
            for py in range(3):
                # Нижний левый
                xs = min_x + floor(px * wx / 3)
                ys = min_y + floor(py * wy / 3)

                # Правый верхний
                xf = min_x + floor((px + 1) * wx / 3) - 1
                yf = min_y + floor((py + 1) * wy / 3) - 1

                xm = (xs + xf) // 2
                ym = (ys + yf) // 2

                # Здесь идёт подсчёт количества пересечений с двумя основными прямыми

                S1, S2 = 0, 0
                last1, last2 = True, True

                for x in range(xs, xf):
                    yd = max(ys, yf - (x - xs))

                    current1 = is_black(pixels[x, yd])
                    if current1 != last1:
                        S1 += int(current1)
                        last1 = current1

                    current2 = is_black(pixels[x, ym])
                    if current2 != last2:
                        S2 += int(current2)
                        last2 = current2

                # Если граница черная
                if is_black(pixels[x, yd]):
                    S1 -= 1

                if is_black(pixels[x, ym]):
                    S2 -= 1

                S3, S4 = 0, 0
                last3, last4 = True, True

                for y in range(ys, yf):
                    xd = min(xf, xs + (y - ys))

                    current3 = is_black(pixels[xd, y])
                    if current3 != last3:
                        S3 += int(current3)
                        last3 = current3

                    current4 = is_black(pixels[xm, y])
                    if current4 != last4:
                        S4 += int(current4)
                        last4 = current4

                # Если граница черная
                if is_black(pixels[xd, y]):
                    S3 -= 1

                if is_black(pixels[xm, y]):
                    S4 -= 1

                # Отображение сетки
                # draw.line((xs, yf, xf, ys), fill=(0, 0, 255), width=10)
                # draw.line((xs, ym, xf, ym), fill=(255, 0, 0), width=10)
                #
                # draw.line((xs, ys, xf, yf), fill=(0, 255, 0), width=10)
                # draw.line((xm, ys, xm, yf), fill=(0, 0, 0), width=10)

                # Грязный трюк, голосует большинство
                field[px][py] = Counter([S1, S2, S3, S4]).most_common(1)[0][0]

        # Горизонтальные + Вертикальные + Побочная Диагональ + Главная Диагональ
        winning_lines = [
                            [(x, y, 0) for y in range(3)]
                            for x in range(3)] \
                        + [[(x, y, 1) for x in range(3)]
                           for y in range(3)] \
                        + [[(i, i, 2) for i in range(3)]] \
                        + [[(i, 2 - i, 3) for i in range(3)]
                           ]

        for line in winning_lines:
            # Если все одного цвета
            if all(map(lambda c: field[c[0]][c[1]] == 1, line)) or \
                    all(map(lambda c: field[c[0]][c[1]] == 2, line)):
                for px, py, t in line:
                    xs = min_x + floor(px * wx / 3)
                    ys = min_y + floor(py * wy / 3)

                    xf = min_x + floor((px + 1) * wx / 3) - 1
                    yf = min_y + floor((py + 1) * wy / 3) - 1

                    xm = (xs + xf) // 2
                    ym = (ys + yf) // 2

                    if t == 1:
                        draw.line((xs, ym, xf, ym), fill=(0, 0, 0), width=10)
                    elif t == 2:
                        draw.line((xm, ys, xm, yf), fill=(0, 0, 0), width=10)
                    elif t == 3:
                        draw.line((xs, yf, xf, ys), fill=(0, 0, 0), width=10)
                    elif t == 4:
                        draw.line((xs, ys, xf, yf), fill=(0, 0, 0), width=10)

        img.save(output_image)
