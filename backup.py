from __future__ import annotations

import os
from datetime import datetime
import yaml


def load_devices(path: str = "devices.yaml") -> list[dict]:
    """Read devices from YAML file."""
    with open(path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    devices = data.get("devices", [])
    if not devices:
        raise ValueError("No devices found in devices.yaml")
    return devices


def simulate_get_running_config(device: dict) -> str:
    """
    This simulates what you'd get from:
      - show running-config (Cisco)
      - show config (other vendors)
    Later we will replace this with real SSH (Netmiko).
    """
    now = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
    return (
        f"! BACKUP TIME: {now}\n"
        f"hostname {device['name']}\n"
        f"!\n"
        f"interface GigabitEthernet0/0\n"
        f" ip address {device['ip']} 255.255.255.0\n"
        f" no shutdown\n"
        f"!\n"
        f"end\n"
    )


def save_backup(device_name: str, config_text: str, folder: str = "backups") -> str:
    """Save config to a file."""
    os.makedirs(folder, exist_ok=True)
    filename = f"{device_name}_running_config.txt"
    path = os.path.join(folder, filename)

    with open(path, "w", encoding="utf-8") as f:
        f.write(config_text)

    return path


def main() -> None:
    devices = load_devices()

    print(f"Found {len(devices)} devices. Starting backups...\n")

    for device in devices:
        name = device["name"]
        ip = device["ip"]

        print(f"Connecting to {name} ({ip}) ...")
        config = simulate_get_running_config(device)
        saved_path = save_backup(name, config)

        print(f"Saved backup: {saved_path}\n")

    print("✅ All backups completed!")


if __name__ == "__main__":
    main()