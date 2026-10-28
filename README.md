# Device Log Summarizer

A small command-line project for cleaning sensor values, summarizing device telemetry from CSV, exporting JSON, and visualizing average temperatures.

## Requirements

- Python 3.9+
- `matplotlib` for the charting step

Install the chart dependency with:

```bash
python -m pip install matplotlib
```

## Section 1: Clean sensor readings

Run the included simple tests:

```bash
python test_sensor_utils.py
```

The cleaning function:

- converts valid values to `float`
- drops `None`, non-numeric values, and negative numbers
- caps values above `500.0` at `500.0`
- safely returns an empty list for empty or invalid-only input

## Section 2: Summarize telemetry

By default, the program expects `device_telemetry.csv` in the current directory:

```bash
python summarize_devices.py
```

Or provide explicit input/output paths:

```bash
python summarize_devices.py path/to/device_telemetry.csv -o device_summary.json
```

For each device, the program calculates:

- total valid records
- average temperature
- number of `ERROR` records

Devices with an average temperature above `80.0` are excluded from the final JSON output.

Rows with a missing device ID or invalid/non-finite temperature are skipped with a warning. Missing files, missing columns, and malformed input are handled with clear error messages.

## Section 3: Generate chart

```bash
python chart_average_temperature.py device_summary.json -o average_temperature_chart.png
```

This produces a bar chart comparing average temperature across the devices that remain after filtering.

## Files

- `sensor_utils.py` - Section 1 cleaning function
- `test_sensor_utils.py` - Section 1 test cases
- `summarize_devices.py` - Section 2 CLI
- `device_telemetry.csv` - sample input used for demonstration
- `device_summary.json` - generated sample JSON output
- `chart_average_temperature.py` - Section 3 matplotlib script
- `average_temperature_chart.png` - generated sample chart
- `PROMPT_LOG.md` - AI interaction record

> Note: The included CSV is sample data created for demonstration. Replace it with the assessment-provided `device_telemetry.csv` when submitting if a separate official CSV was supplied.

## Author

- **Vaibhav** ([@vaibhavvvv7](https://github.com/vaibhavvvv7))

