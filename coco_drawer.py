from PIL import Image, ImageDraw
import json
import os
from tqdm import tqdm

# Загрузка JSON данных
with open('instances_default.json') as json_file:
    data = json.load(json_file)

# Создайте папку для сохраненных изображений с разметкой
if not os.path.exists('output'):
    os.makedirs('output')

category_colors = {
    1: 'yellow',
    2: 'red',
    3: 'blue'
}

# Проход по каждой фотографии в данных JSON
for image_data in tqdm(data['images'], desc='Обработка изображений'):
    image_id = image_data['id']
    file_name = 'ПУТЬ ДО ФОТОК' + image_data['file_name']

    # Загрузка изображения
    image = Image.open(file_name)

    # Проход по аннотациям для текущей фотографии
    for annotation in data['annotations']:
        if annotation['image_id'] == image_id:
            bbox = annotation['bbox']
            x, y, width, height = bbox

            # Проверка на неверные координаты
            if width > 0 and height > 0:
                # Получение цвета для текущего класса
                category_id = annotation['category_id']
                category_color = category_colors.get(category_id, 'white')  # Белый цвет по умолчанию

                # Рисование рамки вокруг объекта с соответствующим цветом
                draw = ImageDraw.Draw(image)
                draw.rectangle([x, y, x + width, y + height], outline=category_color, width=3)

    # Сохранение фотографии с разметкой
    output_path = os.path.join('output', os.path.basename(file_name))
    image.save(output_path)

print('Готово!')
