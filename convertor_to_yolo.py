import json
import os

with open('Finisher.json') as json_file:
    data = json.load(json_file)


def find_image_by_id(json_data, image_id):
    for image in json_data['images']:
        if image['id'] == image_id:
            return image



def convert_to_yolo(json_data):
    yolo_annotations = {}

    for annotation in json_data['annotations']:
        image_id = annotation['image_id']
        category_id = annotation['category_id']
        bbox = annotation['bbox']

        image_info = find_image_by_id(json_data, image_id)
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
    image_info = find_image_by_id(data, image_id)
    filename = os.path.join("labels", image_info['file_name'].split('.')[0] + '.txt')
    print(filename)

    with open(filename, 'w') as file:
        for annotation in annotations:
            file.write(annotation + '\n')
