from pathlib import Path
from ultralytics import YOLO


class LaneSegmentor:

    def __init__(self):

        model_path = (
            Path(__file__).resolve().parent.parent
            / "models"
            / "lane_segmentor_culane.pt"
        )

        self.model = YOLO(str(model_path))

    def segment(self, frame):

        results = self.model(frame, conf=0.10)

        return results