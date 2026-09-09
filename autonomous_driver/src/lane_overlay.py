import cv2
import numpy as np

def draw_lane_overlay(frame, results):

    output = frame.copy()

    if results[0].masks is None:
        return output

    masks = results[0].masks.data.cpu().numpy()

    for mask in masks:

        mask = cv2.resize(
            mask,
            (frame.shape[1], frame.shape[0])
        )

        color = np.zeros_like(frame)
        color[:] = (0, 255, 255)      # Yellow

        output[mask > 0.5] = (
            output[mask > 0.5] * 0.8 +
            color[mask > 0.5] * 0.2
        ).astype(np.uint8)

    return output