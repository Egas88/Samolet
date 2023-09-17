from ultralytics import YOLO
import torch

if __name__ == '__main__':
    print(torch.cuda.is_available())
    print(torch.cuda.device_count())

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    model = YOLO("yolov8m.pt")
    model = model.to(device)

    model.train(data="data.yaml", batch=8, epochs=250, workers=4, patience=5)
