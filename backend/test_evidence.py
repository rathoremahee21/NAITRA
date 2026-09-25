from evidence import create_evidence_clip

video_path = "videos/sample-30s.mp4"

output_path = "clips/test_evidence.mp4"

create_evidence_clip(
    video_path,
    timestamp=13.3,
    output_path=output_path
)

print("Evidence clip created!")
print(output_path)