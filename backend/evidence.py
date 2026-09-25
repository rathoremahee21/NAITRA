import cv2
import os


def create_evidence_clip(video_path, timestamp, output_path,
                         before=2, after=3):

    os.makedirs("clips", exist_ok=True)

    cap = cv2.VideoCapture(video_path)

    fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    start_time = max(0, timestamp - before)
    end_time = timestamp + after

    start_frame = int(start_time * fps)
    end_frame = min(
        total_frames - 1,
        int(end_time * fps)
    )

    cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)

    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    fourcc = cv2.VideoWriter_fourcc(*"mp4v")

    writer = cv2.VideoWriter(
        output_path,
        fourcc,
        fps,
        (width, height)
    )

    current_frame = start_frame

    while current_frame <= end_frame:

        ret, frame = cap.read()

        if not ret:
            break

        writer.write(frame)

        current_frame += 1

    cap.release()
    writer.release()

    return output_path