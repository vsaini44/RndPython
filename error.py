import json


def load_devices(filename):
    try:
        with open(filename, "r") as file:
            devices = [d for d in file.read().splitlines() if d]  # remove empty lines
            return devices
    except FileNotFoundError:
        print(f"Error: {filename} was not found")
        return []


def load_device_config(device_name):
    try:
        filename = f"configs/{device_name}.json"
        with open(filename, "r") as file:
            config = json.load(file)
            return config
    except FileNotFoundError:
        print(f"Error: config file for {device_name} was not found")
        return None
    except json.JSONDecodeError as e:
        print(f"Invalid JSON in {device_name}: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error while loading {device_name}: {e}")
        return None


def get_device_info(config):
    try:
        hostname    = config["hostname"]
        ip          = config["ip"]
        device_type = config["type"]
        return f"Hostname: {hostname}, IP: {ip}, Type: {device_type}"
    except KeyError as e:
        print(f"Missing required field: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error while reading config: {e}")
        return None


def main():
    devices = load_devices("devices.txt")

    for device in devices:
        config = load_device_config(device)
        if config:
            info = get_device_info(config)
            print(info)


if __name__ == "__main__":
    main()
