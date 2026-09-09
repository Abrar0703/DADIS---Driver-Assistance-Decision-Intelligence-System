import cv2
import numpy as np


class LaneGeometry:

    @staticmethod
    def get_centerline(results, frame_shape):

        h, w = frame_shape[:2]

        merged = np.zeros((h, w), dtype=np.uint8)

        if results[0].masks is None:
            return [], [], [], merged

        masks = results[0].masks.data.cpu().numpy()

        for mask in masks:

            mask = cv2.resize(mask, (w, h))

            merged = np.maximum(
                merged,
                (mask > 0.5).astype(np.uint8)
            )

        left_boundary = []
        right_boundary = []
        center_points = []

        # scan from bottom upward
        for y in range(h - 20, 0, -6):

            xs = np.where(merged[y] == 1)[0]

            if len(xs) < 2:
                continue

            groups = np.split(
                xs,
                np.where(np.diff(xs) > 20)[0] + 1
            )

            if len(groups) < 2:
                continue

            # take the two largest lane markings
            groups = sorted(groups, key=len, reverse=True)[:2]

            groups = sorted(groups, key=lambda g: np.mean(g))

            left_x = int(np.mean(groups[0]))
            right_x = int(np.mean(groups[1]))

            center_x = (left_x + right_x) // 2

            left_boundary.append((left_x, y))
            right_boundary.append((right_x, y))
            center_points.append((center_x, y))

        return (
            center_points,
            left_boundary,
            right_boundary,
            merged
        )