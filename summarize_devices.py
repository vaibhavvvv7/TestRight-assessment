"""Device telemetry summarizer CLI.

Reads device telemetry from CSV, aggregates metrics per device, filters out
hot devices (average temperature > 80.0), writes JSON, and prints a table.
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any

REQUIRED_COLUMNS = {"device_id", "status", "temperature"}
MAX_ALLOWED_AVERAGE = 80.0


def load_and_aggregate(csv_path: Path) -> dict[str, dict[str, Any]]:
    """Load CSV rows and aggregate valid records by device_id.

    Rows with a missing device_id or invalid temperature are skipped with a
    warning instead of terminating the program.
    """
    aggregates: dict[str, dict[str, Any]] = defaultdict(
        lambda: {"total_records": 0, "temperature_sum": 0.0, "error_count": 0}
    )

    try:
        file_handle = csv_path.open("r", encoding="utf-8-sig", newline="")
    except FileNotFoundError as exc:
        raise FileNotFoundError(f"CSV file not found: {csv_path}") from exc
    except OSError as exc:
        raise OSError(f"Unable to open CSV file '{csv_path}': {exc}") from exc

    with file_handle:
        reader = csv.DictReader(file_handle)

        if reader.fieldnames is None:
            raise ValueError("CSV file is empty or has no header row.")

        missing_columns = REQUIRED_COLUMNS - set(reader.fieldnames)
        if missing_columns:
            missing = ", ".join(sorted(missing_columns))
            raise ValueError(f"CSV is missing required column(s): {missing}")

        for row_number, row in enumerate(reader, start=2):
            device_id = (row.get("device_id") or "").strip()
            status = (row.get("status") or "").strip().upper()
            temperature_text = (row.get("temperature") or "").strip()

            if not device_id:
                print(
                    f"Warning: skipping row {row_number} because device_id is missing.",
                    file=sys.stderr,
                )
                continue

            try:
                temperature = float(temperature_text)
            except (TypeError, ValueError):
                print(
                    f"Warning: skipping row {row_number} because temperature "
                    f"'{temperature_text}' is invalid.",
                    file=sys.stderr,
                )
                continue

            # Reject NaN/Infinity because they would make averages unreliable.
            if temperature != temperature or temperature in (float("inf"), float("-inf")):
                print(
                    f"Warning: skipping row {row_number} because temperature is not finite.",
                    file=sys.stderr,
                )
                continue

            item = aggregates[device_id]
            item["total_records"] += 1
            item["temperature_sum"] += temperature
            if status == "ERROR":
                item["error_count"] += 1

    return dict(aggregates)


def build_summary(
    aggregates: dict[str, dict[str, Any]],
    max_average: float = MAX_ALLOWED_AVERAGE,
) -> list[dict[str, Any]]:
    """Calculate averages and keep devices with average temperature <= limit."""
    summary: list[dict[str, Any]] = []

    for device_id in sorted(aggregates):
        item = aggregates[device_id]
        total_records = item["total_records"]
        if total_records == 0:
            continue

        average_temperature = item["temperature_sum"] / total_records

        # Requirement: filter out devices whose average is above 80.0.
        if average_temperature > max_average:
            continue

        summary.append(
            {
                "device_id": device_id,
                "total_records": total_records,
                "average_temperature": round(average_temperature, 2),
                "error_count": item["error_count"],
            }
        )

    return summary


def save_json(summary: list[dict[str, Any]], output_path: Path) -> None:
    """Write summary data as formatted JSON."""
    try:
        output_path.write_text(
            json.dumps(summary, indent=2) + "\n",
            encoding="utf-8",
        )
    except OSError as exc:
        raise OSError(f"Unable to write JSON file '{output_path}': {exc}") from exc


def print_summary_table(summary: list[dict[str, Any]]) -> None:
    """Print a small dependency-free table to the terminal."""
    headers = ("Device ID", "Records", "Avg Temp", "Errors")
    rows = [
        (
            item["device_id"],
            str(item["total_records"]),
            f'{item["average_temperature"]:.2f}',
            str(item["error_count"]),
        )
        for item in summary
    ]

    if not rows:
        print("No devices matched the filtering criteria.")
        return

    widths = [len(header) for header in headers]
    for row in rows:
        for index, value in enumerate(row):
            widths[index] = max(widths[index], len(value))

    def format_row(row: tuple[str, ...]) -> str:
        return " | ".join(value.ljust(widths[i]) for i, value in enumerate(row))

    separator = "-+-".join("-" * width for width in widths)
    print(format_row(headers))
    print(separator)
    for row in rows:
        print(format_row(row))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Summarize device telemetry CSV data.")
    parser.add_argument(
        "input_csv",
        nargs="?",
        default="device_telemetry.csv",
        help="Path to input CSV (default: device_telemetry.csv)",
    )
    parser.add_argument(
        "-o",
        "--output",
        default="device_summary.json",
        help="Path to output JSON (default: device_summary.json)",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    input_path = Path(args.input_csv)
    output_path = Path(args.output)

    try:
        aggregates = load_and_aggregate(input_path)
        summary = build_summary(aggregates)
        save_json(summary, output_path)
    except (FileNotFoundError, OSError, ValueError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    print_summary_table(summary)
    print(f"\nSaved JSON summary to: {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
