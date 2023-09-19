from PIL import Image, ImageDraw
import os
from tqdm import tqdm
from converter_yolo_to_yololike import calculate_yololike_coorinates

'''
MAKE SURE TO EDIT PATH ACCORDING TO YOUR SYSTEM OR WHATEVER. 
'''

yolo_labels_path = r"C:\Users\policelettuce\PycharmProjects\Samolet\!_YOLO_ANNOTATED"    # your path to YOLO .txt
images_path = r"D:\!_ITMO_24\HACKATON SAMOLET\!!_NEW_DATASET\_images"                    # your path to images

if not os.path.exists('yolo_output'):                                                   # make a dir in project folder
    os.makedirs('yolo_output')

category_colors = {
    0: (0, 150, 255, 84),               # window / light blue
    1: (128, 0, 128, 84),               # empty / purple
    2: (0, 0, 255, 84),                 # filled / blue
    3: (127, 255, 212, 84),             # balcony_window / aquamarine
    4: (255, 105, 180, 84)              # balcony_filled / pink
}

c = 1

for image_name in tqdm(os.listdir(images_path), desc='Drawing rectangles...'):
    image = Image.open(images_path + "\\" + str(image_name))
    width, height = image.size
    yolo_label_file_path = yolo_labels_path + "\\" + str(image_name).split('.')[0] + ".txt"         # find a .txt file named as image
    yolo_label_file = open(yolo_label_file_path).read().splitlines()                                # open file and split lines to list
    for annotation_line in yolo_label_file:
        annotation = annotation_line.split()                                                        # split annotation str into list of values
        x_min, y_min, x_max, y_max = calculate_yololike_coorinates(annotation[1], annotation[2],
                                                                   annotation[3], annotation[4],
                                                                   width, height)

        category_color = category_colors.get(int(annotation[0]), 'black')                           # defaults to black
        draw = ImageDraw.Draw(image, 'RGBA')
        '''
        # DEBUG INFO
        print(image_name)
        print("counter: " + str(c))
        print("annotation: ", annotation_line)
        print("width: " + str(width) + " height: " + str(height))
        c += 1
        print("x_min = " + str(x_min))
        print("y_min = " + str(y_min))
        print("x_max = " + str(x_max))
        print("y_max = " + str(y_max))
        print('\n\n')
        '''
        draw.rectangle([x_min, y_min, x_max, y_max], fill=category_color)                           # draw transparent bbox

    image_name_png = image_name.split('.')[0] + ".png"                                              # name as .png (supports RGBA)
    output_path = os.path.join('yolo_output', os.path.basename(image_name_png))                     # save image to local output dir
    image.save(output_path)
