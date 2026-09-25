import sqlite3

DB_PATH = "data/naitra.db"


def investigate(location=None, person_id=None, start_time=None, end_time=None):

    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    query = """
        SELECT person_id, camera_id, location, timestamp, confidence, video_path
FROM events
        WHERE 1=1
    """

    parameters = []

    # Filter by location
    if location:
     query += " AND LOWER(location) = LOWER(?)"
    parameters.append(location)

    # Filter by person
    if person_id:
        query += " AND person_id = ?"
        parameters.append(person_id)

    # Filter by starting time
    if start_time is not None:
        query += " AND timestamp >= ?"
        parameters.append(start_time)

    # Filter by ending time
    if end_time is not None:
        query += " AND timestamp <= ?"
        parameters.append(end_time)

    query += " ORDER BY timestamp"

    cursor.execute(query, parameters)

    results = cursor.fetchall()

    connection.close()

    return results


# Test investigation
results = investigate(
    location="Lobby",
    start_time=13.3
)

print("\nINVESTIGATION RESULTS:\n")

if not results:
    print("No evidence found.")

else:
    for result in results:
        print(
            f"Person {result[0]} | "
            f"Camera: {result[1]} | "
            f"Location: {result[2]} | "
            f"Time: {result[3]} sec | "
            f"Confidence: {result[4]}"
        )