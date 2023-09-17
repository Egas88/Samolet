import os
from PIL import Image

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

            x_center = float(label[1]) * width
            y_center = float(label[2]) * height
            x_width = float(label[3]) * width
            y_height = float(label[4]) * height

            x_min = round(x_center - x_width / 2)
            x_max = round(x_center + x_width / 2)
            y_min = round(y_center - y_height / 2)
            y_max = round(y_center + y_height / 2)

            if x_min < 0: x_min = 0                         # out-of-bounds check
            if x_max > width: x_max = int(width)
            if y_min < 0: y_min = 0
            if y_max > height: y_max = int(height)

            score = label[5]
            predicted_class = int(label[0]) + 1

            s = str(predicted_class) + " " + str(score) + " " + str(x_min) + " " + str(y_min) + " " + str(x_max) + " " + str(y_max) + "\n"
            stream.write(s)
        stream.close()


if __name__ == '__main__':
    convert_to_yololike()
