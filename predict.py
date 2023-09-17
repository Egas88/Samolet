from ultralytics import YOLO
import os

if __name__ == '__main__':

    model = YOLO("yolo8m_250epoch.pt")
    dir_path = "D:\!_ITMO_24\HACKATON SAMOLET\TEST_v1\\"        #MAKE SURE TO UPDATE PATH FOR YOUR PC

    for img in os.listdir(dir_path):
        file_path = dir_path + img
        print(file_path)
        print(type(file_path))
        model.predict(source=file_path, show=False, save=True, save_conf=True, save_txt=True, conf=0.5, line_width=1)
