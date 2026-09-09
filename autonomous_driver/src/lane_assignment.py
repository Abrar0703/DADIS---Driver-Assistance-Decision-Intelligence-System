import cv2
import numpy as np


class LaneAssignment:

    @staticmethod
    def get_box_center(box):

        x1, y1, x2, y2 = box

        cx = int((x1 + x2) / 2)
        cy = int(y2)      # Bottom center of the box

        return cx, cy

    @staticmethod
    def is_inside_lane(box, lane_mask):

        cx, cy = LaneAssignment.get_box_center(box)

        h, w = lane_mask.shape[:2]

        if cx < 0 or cx >= w:
            return False

        if cy < 0 or cy >= h:
            return False

        return lane_mask[cy, cx] > 0

    @staticmethod
    def draw_status(frame, box, inside):

        x1, y1, x2, y2 = box

        if inside:

            color = (0, 0, 255)
            text = "IN LANE"

        else:

            color = (0, 255, 0)
            text = "OUTSIDE"

        cv2.putText(
            frame,
            text,
            (x1, y2 + 20),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            color,
            2
        )

        return frame