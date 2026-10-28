# AI Prompt Log

## Initial prompt

> Write a Python script using matplotlib that loads `device_summary.json`. The JSON contains a list of objects with `device_id`, `total_records`, `average_temperature`, and `error_count`. Create a bar chart comparing `average_temperature` for each device and save it as `average_temperature_chart.png`. Include basic error handling for a missing JSON file.

## Issue noticed in the first AI-generated version

The first version created the bar chart, but it used the default figure size and left the x-axis labels horizontal. With longer or numerous device IDs, the labels could overlap and become difficult to read. It also did not call `tight_layout()`, so labels could be clipped when saving the image.

## Follow-up prompt

> Update the chart so that device labels remain readable when there are several devices. Use a larger figure, rotate the x-axis labels, add a clear title and axis labels, call `tight_layout()` before saving, and close the figure after saving it.

## Changes I reviewed and kept

I reviewed the revised script and kept the larger figure size, 45-degree x-axis label rotation, chart title, axis labels, `tight_layout()`, and `plt.close()` call. I also kept validation for empty JSON data so the script fails with a clear message instead of producing a blank chart.
