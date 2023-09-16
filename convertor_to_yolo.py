import json
import os

with open('instances_default.json') as json_file:
    data = json.load(json_file)


def convert_to_yolo(json_data):
    yolo_annotations = {}

    for annotation in json_data['annotations']:
        image_id = annotation['image_id']
        category_id = annotation['category_id']
        bbox = annotation['bbox']

        image_info = json_data['images'][image_id - 1]
        image_width = image_info['width']
        image_height = image_info['height']

        x_center = (bbox[0] + bbox[2] / 2) / image_width
        y_center = (bbox[1] + bbox[3] / 2) / image_height
        width = bbox[2] / image_width
        height = bbox[3] / image_height

        yolo_annotation = f"{category_id-1} {x_center} {y_center} {width} {height}"

        if image_id in yolo_annotations:
            yolo_annotations[image_id].append(yolo_annotation)
        else:
            yolo_annotations[image_id] = [yolo_annotation]

    return yolo_annotations


# Преобразование в разметку YOLO
yolo_annotations = convert_to_yolo(data)

# Создание отдельного файла для каждого изображения
if not os.path.exists("labels"):
    os.makedirs("labels")

# Создание отдельного файла для каждого изображения
for image_id, annotations in yolo_annotations.items():
    image_info = data['images'][image_id - 1]
    filename = os.path.join("labels", image_info['file_name'].split('.')[0] + '.txt')

    with open(filename, 'w') as file:
        for annotation in annotations:
            file.write(annotation + '\n')
