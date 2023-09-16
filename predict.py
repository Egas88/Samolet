from ultralytics import YOLO

model = YOLO("yolo8_2.pt")

model.predict(source='1.jpg', show=True, save=True, conf=0.5, line_width=1)
