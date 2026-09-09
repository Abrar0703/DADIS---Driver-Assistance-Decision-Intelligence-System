import cv2
import time
import numpy as np
from pathlib import Path

from object_detection import ObjectDetector
from lane_segmentation import LaneSegmentor
from lane_overlay import draw_lane_overlay
from lane_geometry import LaneGeometry
from ui import draw_corner_box

from world_model import WorldModel
from distance_estimator import DistanceEstimator
from relative_speed import RelativeSpeedEstimator
from ttc import TimeToCollision
from motion_state import MotionState
from collision_probability import CollisionProbability
from lane_classifier import LaneClassifier
from risk_assessment import RiskAssessment
from world_analyzer import WorldAnalyzer
from decision_engine import DecisionEngine


# ==========================================================
# Initialize Modules
# ==========================================================

object_detector = ObjectDetector()
lane_segmentor = LaneSegmentor()

world = WorldModel()
speed_estimator = RelativeSpeedEstimator()


# ==========================================================
# Paths
# ==========================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

VIDEO_PATH = PROJECT_ROOT / "dashcam.mp4"

OUTPUT_DIR = PROJECT_ROOT / "output"
OUTPUT_DIR.mkdir(exist_ok=True)

OUTPUT_VIDEO = OUTPUT_DIR / "final_output.mp4"


# ==========================================================
# Video
# ==========================================================

cap = cv2.VideoCapture(str(VIDEO_PATH))

if not cap.isOpened():
    raise FileNotFoundError("Could not open dashcam.mp4")

width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
video_fps = cap.get(cv2.CAP_PROP_FPS)

HUD_HEIGHT = 140

writer = cv2.VideoWriter(
    str(OUTPUT_VIDEO),
    cv2.VideoWriter_fourcc(*"mp4v"),
    video_fps,
    (width, height + HUD_HEIGHT)
)

print("Recording Started...")


# ==========================================================
# UI Constants
# ==========================================================

DISPLAY_NAMES = {
    "car": "Car",
    "truck": "Truck",
    "bus": "Bus",
    "motor": "Motorcycle",
    "bike": "Bicycle",
    "person": "Person",
    "traffic light": "Traffic Light",
    "traffic sign": "Traffic Sign",
    "train": "Train",
    "rider": "Rider"
}

CLASS_COLORS = {
    "car": (255,220,0),          # Cyan
    "truck": (0,140,255),        # Orange
    "bus": (255,0,255),          # Magenta
    "person": (0,255,0),         # Green
    "bike": (255,255,0),         # Yellow
    "motor": (255,120,0),        # Dark Orange
    "traffic light": (0,255,255),# Light Yellow
    "traffic sign": (0,180,255), # Amber
    "train": (180,180,255),      # Lavender
    "rider": (255,0,0)           # Blue (BGR)
}

TARGET_COLOR = (0,0,255)
TEXT_COLOR = (25,25,25)

FONT = cv2.FONT_HERSHEY_SIMPLEX
FONT_SCALE = 0.55
FONT_THICKNESS = 1

MIN_BOX_SIZE = 22
MIN_CONFIDENCE = 0.50




# ==========================================================
# Main Loop
# ==========================================================

while True:

    ret, frame = cap.read()

    if not ret:
        break

    frame_start = time.time()

    world.clear()

    # ------------------------------------------------------
    # AI Inference
    # ------------------------------------------------------

    object_results = object_detector.detect(frame)

    lane_results = lane_segmentor.segment(frame)

    final_frame = draw_lane_overlay(
    frame,
    lane_results
)

    center_points, left_boundary, right_boundary, lane_mask = \
    LaneGeometry.get_centerline(
        lane_results,
        frame.shape
)

    boxes = object_results[0].boxes
    names = object_results[0].names

    # ======================================================
    # Build World Model
    # ======================================================

    if boxes is not None:

        for box in boxes:

            x1, y1, x2, y2 = map(
                int,
                box.xyxy[0]
            )

            cls = int(box.cls[0])

            confidence = float(box.conf[0])

            if confidence < MIN_CONFIDENCE:
                continue

            if (
                x2-x1 < MIN_BOX_SIZE or
                y2-y1 < MIN_BOX_SIZE
            ):
                continue
           
            world.add_vehicle(

                vehicle_id=len(world.get_vehicles()),

                vehicle_class=names[cls],

                box=(x1,y1,x2,y2),

                confidence=confidence

            )

            vehicle = world.get_vehicles()[-1]

            

            # -----------------------------------------
            # Intelligence Pipeline
            # -----------------------------------------

            DYNAMIC_CLASSES = {
                "car",
                "truck",
                "bus",
                "motor",
                "bike",
                "person",
                "rider",
                "train"
            }

            if vehicle.cls.lower() in DYNAMIC_CLASSES:

                vehicle.distance = DistanceEstimator.estimate(vehicle)

                vehicle.relative_speed = speed_estimator.estimate(vehicle)

                vehicle.ttc = TimeToCollision.calculate(vehicle)

                vehicle.motion = MotionState.classify(vehicle)

                vehicle.collision_probability = (
                    CollisionProbability.calculate(vehicle)
                )

                vehicle.lane = LaneClassifier.classify(
                    vehicle,
                    left_boundary,
                    right_boundary
                )

                vehicle.risk = RiskAssessment.calculate(vehicle)

    # ======================================================
    # Analyze Scene
    # ======================================================

    scene = WorldAnalyzer.analyze(
        world.get_vehicles()
    )

    decision = DecisionEngine.analyze(
        scene
    )

    target = decision["vehicle"]


    # ======================================================
    # Draw Vehicles
    # ======================================================

    for vehicle in world.get_vehicles():

        x1, y1, x2, y2 = vehicle.box

        # ---------------------------------
        # Highlight Target Vehicle
        # ---------------------------------

        is_target = (
            target is not None and
            vehicle == target
        )

        box_color = CLASS_COLORS.get(
        vehicle.cls.lower(),
        (255,220,0)
        )

        thickness = 1

        draw_corner_box(

            final_frame,

            x1,
            y1,
            x2,
            y2,

            box_color,

            thickness

        )

        # ---------------------------------
        # Vehicle Label
        # ---------------------------------

        label = DISPLAY_NAMES.get(
            vehicle.cls.lower(),
            vehicle.cls.upper()
        )

        padding = 6

        (tw, th), _ = cv2.getTextSize(

            label,

            FONT,

            FONT_SCALE,

            FONT_THICKNESS

        )

        cv2.rectangle(

            final_frame,

            (x1, y1-th-padding*2),

            (x1+tw+padding*2, y1),

            box_color,

            -1

        )

        cv2.putText(

            final_frame,

            label,

            (x1+padding, y1-padding),

            FONT,

            FONT_SCALE,

            TEXT_COLOR,

            FONT_THICKNESS

        )

        
        # ---------------------------------
        # Distance
        # ---------------------------------

        if vehicle.distance is not None:

            cv2.putText(

                final_frame,

                f"{vehicle.distance:.1f}m",

                (x1, y2+18),

                FONT,

                0.45,

                (255,255,255),

                1

            )

        # ---------------------------------
        # Motion State
        # ---------------------------------

        motion_color = (200,200,200)

        if vehicle.motion == "CLOSING FAST":

            motion_color = (0,0,255)

        elif vehicle.motion == "CLOSING":

            motion_color = (0,165,255)

        elif vehicle.motion == "MOVING AWAY":

            motion_color = (0,255,0)

        if vehicle.motion != "UNKNOWN":

            cv2.putText(

                final_frame,

                vehicle.motion,

                (x1, y2+36),

                FONT,

                0.42,

                motion_color,

                1

            )


        
    # ======================================================
    # DASHBOARD CANVAS
    # ======================================================


    dashboard = np.full(
        (HUD_HEIGHT + height, width, 3),
        22,
        dtype=np.uint8
    )

    dashboard[HUD_HEIGHT:, :] = final_frame


    # ======================================================
    # HEADER
    # ======================================================

    cv2.rectangle(
        dashboard,
        (0, 0),
        (width, HUD_HEIGHT),
        (22, 22, 22),
        -1
    )

    cv2.line(
        dashboard,
        (0, HUD_HEIGHT),
        (width, HUD_HEIGHT),
        (70, 70, 70),
        2
    )

    section1 = width // 3
    section2 = (width // 3) * 2

    cv2.line(
        dashboard,
        (section1, 15),
        (section1, HUD_HEIGHT-15),
        (60,60,60),
        1
    )

    cv2.line(
        dashboard,
        (section2, 15),
        (section2, HUD_HEIGHT-15),
        (60,60,60),
        1
    )

    elapsed = max(time.time() - frame_start, 1e-6)
    fps = 1 / elapsed

    vehicle_count = len(world.get_vehicles())

    cv2.putText(
        dashboard,
        "SYSTEM",
        (20,30),
        FONT,
        0.7,
        (255,255,255),
        2
    )

    cv2.putText(
        dashboard,
        f"FPS : {fps:.1f}",
        (20,60),
        FONT,
        0.55,
        (230,230,230),
        1
    )

    cv2.putText(
        dashboard,
        f"Vehicles : {vehicle_count}",
        (20,85),
        FONT,
        0.55,
        (230,230,230),
        1
    )

    cv2.putText(
        dashboard,
        f"Inference : {elapsed*1000:.0f} ms",
        (20,110),
        FONT,
        0.55,
        (230,230,230),
        1
    )

    x = section1 + 20

    cv2.putText(
        dashboard,
        "FRONT VEHICLE",
        (x,30),
        FONT,
        0.7,
        (255,255,255),
        2
    )

    if target is not None:

        label = DISPLAY_NAMES.get(
            target.cls.lower(),
            target.cls.upper()
        )

        cv2.putText(
            dashboard,
            label,
            (x,60),
            FONT,
            0.60,
            (0,220,255),
            2
        )

        cv2.putText(
            dashboard,
            f"Distance : {target.distance:.1f} m",
            (x,85),
            FONT,
            0.5,
            (235,235,235),
            1
        )

        if target.ttc is not None:

            cv2.putText(
                dashboard,
                f"TTC : {target.ttc:.1f} s",
                (x,110),
                FONT,
                0.5,
                (235,235,235),
                1
            )

    x = section2 + 20

    cv2.putText(
        dashboard,
        "DECISION",
        (x,30),
        FONT,
        0.7,
        (255,255,255),
        2
    )

    cv2.putText(
        dashboard,
        decision["status"],
        (x,65),
        FONT,
        0.8,
        decision["color"],
        2
    )

    cv2.putText(
        dashboard,
        decision["reason"],
        (x,95),
        FONT,
        0.5,
        (235,235,235),
        1
    )

    if target is not None:

        cv2.putText(
            dashboard,
            f"Collision : {target.collision_probability*100:.0f}%",
            (x,120),
            FONT,
            0.5,
            (235,235,235),
            1
        )
    # ======================================================
    # DISPLAY
    # ======================================================

    cv2.imshow(
        "DADIS - Driver Assistance & Decision Intelligence System",
        dashboard
    )

    writer.write(dashboard)

    if cv2.waitKey(1) & 0xFF == 27:
        break