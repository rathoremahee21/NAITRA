from query_parser import parse_query
from search import investigate
from evidence import create_evidence_clip
from sightings import group_sightings

import os


print("================================")
print("        NAITRA INVESTIGATOR")
print("================================")

query = input("\nAsk NAITRA: ")

parsed = parse_query(query)

print("\nUNDERSTOOD:")
print(parsed)


results = investigate(
    location=parsed["location"],
    start_time=parsed["start_time"]
)


print("\n================================")
print("        EVIDENCE FOUND")
print("================================")


if not results:

    print("No matching evidence found.")

else:

    for index, result in enumerate(results):

        person_id = result[0]
        camera_id = result[1]
        location = result[2]
        timestamp = result[3]
        confidence = result[4]
        video_path = result[5]

        print(
            f"\nPerson #{person_id}"
            f"\nCamera: {camera_id}"
            f"\nLocation: {location}"
            f"\nTimestamp: {timestamp} sec"
            f"\nConfidence: {confidence}"
        )

        # Create evidence clip
        output_path = (
            f"clips/person_{person_id}_"
            f"{timestamp:.2f}.mp4"
        )

        create_evidence_clip(
            video_path,
            timestamp,
            output_path
        )

        print(f"Evidence clip: {output_path}")