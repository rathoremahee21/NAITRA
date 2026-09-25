import re


def parse_query(query):

    query_lower = query.lower()

    location = None
    start_time = None

    # Detect known locations
    locations = ["lobby", "corridor", "parcel room"]

    for place in locations:
        if place in query_lower:
            location = place.title()
            break

    # Detect "after X seconds"
    match = re.search(r"after\s+(\d+(?:\.\d+)?)\s*seconds?", query_lower)

    if match:
        start_time = float(match.group(1))

    return {
        "location": location,
        "start_time": start_time
    }


# Test
query = input("Enter investigation query: ")

result = parse_query(query)

print("\nUNDERSTOOD QUERY:")
print(result)