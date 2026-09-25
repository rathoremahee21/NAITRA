from ultralytics import YOLO

# Load YOLO model
model = YOLO("yolo11n.pt")

# Track people in the video
results = model.track(
    source="videos/sample-30s.mp4",
    tracker="bytetrack.yaml",
    classes=[0],
    save=True,
    show=False
)

print("Tracking completed!")