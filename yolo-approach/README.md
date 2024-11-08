### Label Studio
we used Label Studio to label objects in images and use them for yolo model traning.
- https://labelstud.io/
- https://github.com/HumanSignal/label-studio/


### Yolo
- Model Train command `yolo detect train data=< path to data.yaml file> model=yolov8n.pt epochs=200 imgsz=640 device=mps`
- Predict Command `yolo predict model=<trained model path> source=<input image/video path> imgsz=640`