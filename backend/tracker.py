

from ultralytics import YOLO
import cv2
from event_store import create_database, save_event
import os

create_database()

# Load model
model = YOLO("yolo11n.pt")

video_path = "videos/sample-30s.mp4"

# Open video
cap = cv2.VideoCapture(video_path)

fps = cap.get(cv2.CAP_PROP_FPS)

camera_id = "CAM01"
location = "Lobby"

events = []

while True:

    ret, frame = cap.read()

    if not ret:
        break

    # Current video time
    frame_number = int(cap.get(cv2.CAP_PROP_POS_FRAMES))
    timestamp = frame_number / fps

    # Track people
    results = model.track(
        frame,
        persist=True,
        tracker="bytetrack.yaml",
        classes=[0],
        verbose=False
    )

    result = results[0]

    if result.boxes.id is not None:

        person_ids = result.boxes.id.int().cpu().tolist()
        confidences = result.boxes.conf.cpu().tolist()

        for person_id, confidence in zip(person_ids, confidences):

            event = {
      "person_id": person_id,
    "camera_id": camera_id,
    "location": location,
    "timestamp": round(timestamp, 2),
    "confidence": round(float(confidence), 2),
    "video_path": video_path
}
            save_event(event) 
            events.append(event)

cap.release()

print("\nEVENTS FOUND:\n")

for event in events[:20]:
    print(event)

print("\nTotal events:", len(events))