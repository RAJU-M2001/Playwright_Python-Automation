import json

# Load the JSON data from the file
with open('auth.json', 'r') as file:
    data = json.load(file)

# Navigate through the JSON structure to find the value
# woyage_user_session_value = None
for origin in data.get("origins", []):
    local_storage = origin.get("localStorage", [])
    for item in local_storage:
        if item.get("name") == "woyage_user_session":
            woyage_user_session_value = item.get("value")
            break
    if woyage_user_session_value:
        break

print("woyage_user_session value:", woyage_user_session_value)

