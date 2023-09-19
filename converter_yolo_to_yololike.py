import os
from PIL import Image


def calculate_yololike_coorinates(x_center_coef, y_center_coef, x_width_coef, y_height_coef, img_width, img_height):
    x_center = float(x_center_coef) * img_width
    y_center = float(y_center_coef) * img_height
    x_width = float(x_width_coef) * img_width
    y_height = float(y_height_coef) * img_height

    x_min = round(x_center - x_width / 2)
    y_min = round(y_center - y_height / 2)
    x_max = round(x_center + x_width / 2)
    y_max = round(y_center + y_height / 2)

    if x_min < 0: x_min = 0  # out-of-bounds check
    if x_max > img_width: x_max = int(img_width)
    if y_min < 0: y_min = 0
    if y_max > img_height: y_max = int(img_height)

    return x_min, y_min, x_max, y_max

def convert_to_yololike():
    dir_path = r"/runs/detect/predict_v1_epoch250_labels"  # path to directory with images
    labels_path = dir_path + "\\labels\\"
    labels_yololike_path = dir_path + "\\labels_yololike\\"

    os.makedirs(labels_yololike_path, exist_ok=True)

    for label_file in os.listdir(labels_path):
        width, height = Image.open(dir_path + "\\" + str(label_file)[:-4] + ".jpg").size
        labels = open(labels_path + label_file).read().splitlines()
        stream = open( (labels_yololike_path + str(label_file)), mode='w' )
        for label_ns in labels:
            label = label_ns.split()

            x_min, y_min, x_max, y_max = calculate_yololike_coorinates(label[1], label[2], label[3], label[4], width, height)

            score = label[5]
            predicted_class = int(label[0]) + 1

            s = str(predicted_class) + " " + str(score) + " " + str(x_min) + " " + str(y_min) + " " + str(x_max) + " " + str(y_max) + "\n"
            stream.write(s)
        stream.close()


if __name__ == '__main__':
    convert_to_yololike()
