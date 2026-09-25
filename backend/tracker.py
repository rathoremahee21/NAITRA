from ultralytics import YOLO
import cv2
from event_store import create_database, save_event
import os


# Create database/table if it does not already exist
create_database()


# ============================================================
# VIDEOS TO PROCESS
# ============================================================

videos = [
    {
        "path": "videos/Dog attack.mp4",
        "camera_id": "CAM01",
        "location": "Location 1"
    },
    {
        "path": "videos/parcel stolen.mp4",
        "camera_id": "CAM02",
        "location": "Location 2"
    },
    {
        "path": "videos/Snatching incident.mp4",
        "camera_id": "CAM03",
        "location": "Location 3"
    },
    {
        "path": "videos/Two Car.mp4",
        "camera_id": "CAM04",
        "location": "Location 4"
    },
    {
        "path": "videos/women waiting.mp4",
        "camera_id": "CAM05",
        "location": "Location 5"
    }
]


# Store all events found
events = []


# ============================================================
# PROCESS EACH VIDEO
# ============================================================

for video in videos:

    video_path = video["path"]
    camera_id = video["camera_id"]
    location = video["location"]

    print("\n========================================")
    print("Processing:", video_path)
    print("Camera:", camera_id)
    print("Location:", location)
    print("========================================")

    # Check that video exists
    if not os.path.exists(video_path):
        print("ERROR: Video not found:", video_path)
        continue

    # Load a fresh model for this video.
    # This also resets ByteTrack state between videos.
    model = YOLO("yolo11n.pt")

    # Open video
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print("ERROR: Could not open:", video_path)
        continue

    # Get FPS
    fps = cap.get(cv2.CAP_PROP_FPS)

    if fps <= 0:
        print("ERROR: Could not read FPS:", video_path)
        cap.release()
        continue

    frame_count = 0

    # ========================================================
    # READ FRAMES
    # ========================================================

    while True:

        ret, frame = cap.read()

        if not ret:
            break

        frame_count += 1

        # Current video timestamp
        timestamp = frame_count / fps

        # ====================================================
        # YOLO + BYTETRACK
        # ====================================================

        results = model.track(
            frame,
            persist=True,
            tracker="bytetrack.yaml",
            classes=[0],       # 0 = person
            verbose=False
        )

        result = results[0]

        # ====================================================
        # SAVE DETECTED PEOPLE
        # ====================================================

        if result.boxes.id is not None:

            person_ids = result.boxes.id.int().cpu().tolist()
            confidences = result.boxes.conf.cpu().tolist()

            for person_id, confidence in zip(
                person_ids,
                confidences
            ):

                event = {
                    "person_id": int(person_id),
                    "camera_id": camera_id,
                    "location": location,
                    "timestamp": round(timestamp, 2),
                    "confidence": round(float(confidence), 2),
                    "video_path": video_path
                }

                save_event(event)
                events.append(event)

    # Finished this video
    cap.release()

    print("Finished:", video_path)
    print("Frames processed:", frame_count)


# ============================================================
# FINAL SUMMARY
# ============================================================

print("\n========================================")
print("ALL VIDEOS PROCESSED")
print("========================================")

print("\nFirst 20 events:\n")

for event in events[:20]:
    print(event)

print("\nTotal events:", len(events))