def group_sightings(events, gap=2.0):

    if not events:
        return []

    sightings = []

    current = {
        "person_id": events[0][0],
        "camera_id": events[0][1],
        "location": events[0][2],
        "start_time": events[0][3],
        "end_time": events[0][3],
        "confidence": events[0][4],
        "video_path": events[0][5]
    }

    for event in events[1:]:

        person_id = event[0]
        camera_id = event[1]
        location = event[2]
        timestamp = event[3]
        confidence = event[4]
        video_path = event[5]

        # Same person and same camera
        # and event is close enough in time
        if (
            person_id == current["person_id"]
            and camera_id == current["camera_id"]
            and location == current["location"]
            and timestamp - current["end_time"] <= gap
        ):

            current["end_time"] = timestamp

            # Keep the highest confidence
            current["confidence"] = max(
                current["confidence"],
                confidence
            )

        else:

            sightings.append(current)

            current = {
                "person_id": person_id,
                "camera_id": camera_id,
                "location": location,
                "start_time": timestamp,
                "end_time": timestamp,
                "confidence": confidence,
                "video_path": video_path
            }

    sightings.append(current)

    return sightings