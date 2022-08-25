import cv2
from cvzone.SelfiSegmentationModule import SelfiSegmentation
import webcolors
from PIL import Image
import statistics
import os
import mediapipe


def closest_colour(requested_colour):
    min_colours = {}
    for key, name in webcolors.CSS3_HEX_TO_NAMES.items():
        r_c, g_c, b_c = webcolors.hex_to_rgb(key)
        rd = (r_c - requested_colour[0]) ** 2
        gd = (g_c - requested_colour[1]) ** 2
        bd = (b_c - requested_colour[2]) ** 2
        min_colours[(rd + gd + bd)] = name
    return min_colours[min(min_colours.keys())]


def get_colour_name(requested_colour):
    try:
        closest_name = actual_name = webcolors.rgb_to_name(requested_colour)
    except ValueError:
        closest_name = closest_colour(requested_colour)
        actual_name = None
    return closest_name


COLORS = (
    (0, 0, 0),  # black
    (253, 253, 253),  # white
    (255, 0, 0),  # red
    (144, 238, 144),  # lightgreen
    (0, 0, 255),  # blue
    (245, 245, 10),  # yellow
    (0, 255, 255),  # cyan
    (255, 0, 255),  # magenta
    (128, 128, 128),  # gray
    (0, 128, 0),  # green
    (255, 180, 0),  # orange
    (165, 42, 42),  # brown
    (100, 0, 100),  # indigo
    (20, 20, 128),  # midnightblue
    (147, 112, 219),  # mediumpurple
    (180, 180, 180),  # darkgray
    (240, 190, 200),  # pink
    (200, 70, 0),  # chocolate
    (165, 120, 75),  # peru
    (205, 50, 125)  # mediumvioletred
)


def closest_list_color(rgb):
    r, g, b = rgb
    color_diffs = []
    for color in COLORS:
        cr, cg, cb = color
        color_diff = (abs(r - cr) ** 2 + abs(g - cg) ** 2 + abs(b - cb) ** 2) ** .5
        color_diffs.append((color_diff, color))
    return min(color_diffs)[1]


file_list = onlyfiles = [f for f in os.listdir('input_images') if os.path.isfile(os.path.join('input_images', f))]
for image_name in file_list:
    segmentor = SelfiSegmentation()
    img = cv2.imread('input_images/' + image_name)
    img_Out = segmentor.removeBG(img, (255, 255, 255), threshold=0.99)

    cv2.imwrite('output.png', img_Out)

    im = Image.open('output.png')  # Can be many different formats.
    im = im.crop((0, round(im.size[1] * .38), im.size[0], im.size[1]))
    im.save('output.png')
    pix = im.load()
    # if image_name == '1_aO1T5_eARy5XvOu3L_7qyQ.jpeg':
    #    time.sleep(7)
    os.remove('output.png')

    all_pixels = []
    for x in range(im.size[0]):
        for y in range(im.size[1]):
            if pix[x, y] != (255.0, 255.0, 255.0):
                all_pixels.append(pix[x, y])
    color_median = [statistics.mode([x[0] for x in all_pixels]),
                    statistics.mode([x[1] for x in all_pixels]),
                    statistics.mode([x[2] for x in all_pixels])]

    color_output = get_colour_name(closest_list_color(color_median))
    if color_output == 'darkgray':
        color_output = 'gray'
    if color_output == 'mediumpurple':
        color_output = 'purple'
    if color_output == 'midnightblue':
        color_output = 'blue'
    if color_output == 'cyan':
        color_output = 'blue'
    if color_output == 'indigo':
        color_output = 'purple'
    if color_output == 'lightgreen':
        color_output = 'green'
    if color_output == 'chocolate':
        color_output = 'orange'
    if color_output == 'peru':
        color_output = 'brown'
    if color_output == 'mediumvioletred':
        color_output = 'magenta'

    print(color_median, image_name)
    print(color_output)

    im = Image.open('input_images/' + image_name)
    dir = 'output_colors/' + color_output + ''
    if not os.path.isdir(dir):
        os.mkdir(dir)
    im.save(dir + '/' + image_name)
