"""Generate a bar chart of average temperature by device."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import matplotlib.pyplot as plt


def load_summary(json_path: Path) -> list[dict]:
    try:
        with json_path.open("r", encoding="utf-8") as file_handle:
            data = json.load(file_handle)
    except FileNotFoundError as exc:
        raise FileNotFoundError(f"JSON file not found: {json_path}") from exc
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid JSON in '{json_path}': {exc}") from exc

    if not isinstance(data, list):
        raise ValueError("Expected the JSON root to be a list of device summaries.")

    return data


def create_chart(data: list[dict], output_path: Path) -> None:
    if not data:
        raise ValueError("No device data is available to chart.")

    device_ids = [str(item["device_id"]) for item in data]
    temperatures = [float(item["average_temperature"]) for item in data]

    fig, ax = plt.subplots(figsize=(9, 5))
    ax.bar(device_ids, temperatures)
    ax.set_title("Average Temperature by Device")
    ax.set_xlabel("Device ID")
    ax.set_ylabel("Average Temperature")
    ax.tick_params(axis="x", labelrotation=45)

    # Keep labels readable even when device IDs are longer.
    fig.tight_layout()
    fig.savefig(output_path, dpi=150)
    plt.close(fig)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Create a bar chart from a device summary JSON file."
    )
    parser.add_argument(
        "input_json",
        nargs="?",
        default="device_summary.json",
        help="Path to summary JSON (default: device_summary.json)",
    )
    parser.add_argument(
        "-o",
        "--output",
        default="average_temperature_chart.png",
        help="Path to output PNG",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    try:
        data = load_summary(Path(args.input_json))
        create_chart(data, Path(args.output))
    except (FileNotFoundError, OSError, ValueError, KeyError, TypeError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    print(f"Saved chart to: {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
