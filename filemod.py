import csv
import json
import yaml
import pickle
import xml.etree.ElementTree as ET
import os

from dotenv import load_dotenv

# -----------------------------
# Read CSV
# -----------------------------
devices = []

with open("devices.csv", newline="") as file:
    reader = csv.DictReader(file)

    for row in reader:
        devices.append(row)

# -----------------------------
# Save JSON
# -----------------------------
with open("inventory.json", "w") as file:
    json.dump(devices, file, indent=4)

# -----------------------------
# Save YAML
# -----------------------------
with open("inventory.yaml", "w") as file:
    yaml.dump(devices, file)

# -----------------------------
# Save Pickle
# -----------------------------
with open("inventory.pkl", "wb") as file:
    pickle.dump(devices, file)

# -----------------------------
# Load Environment Variables
# -----------------------------
load_dotenv()

print("Username:", os.getenv("USERNAME"))
print("Password:", os.getenv("PASSWORD"))
print("SSH Port:", os.getenv("SSH_PORT"))

# -----------------------------
# Load JSON
# -----------------------------
with open("inventory.json") as file:
    json_data = json.load(file)

# -----------------------------
# Load YAML
# -----------------------------
with open("inventory.yaml") as file:
    yaml_data = yaml.safe_load(file)

# -----------------------------
# Load Pickle
# -----------------------------
with open("inventory.pkl", "rb") as file:
    pickle_data = pickle.load(file)

# -----------------------------
# Verify
# -----------------------------
if json_data == yaml_data == pickle_data:
    print("\nAll inventories contain identical data.")
else:
    print("\nInventory mismatch!")

