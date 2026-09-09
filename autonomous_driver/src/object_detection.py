from pathlib import Path
from ultralytics import YOLO


class ObjectDetector:

    def __init__(self):

        model_path = (
            Path(__file__).resolve().parent.parent
            / "models"
            / "yolo_detector.pt"
        )

        self.model = YOLO(str(model_path))

    def detect(self, frame):

        return self.model(frame, conf=0.18)