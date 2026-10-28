"""Simple tests for Section 1."""

from sensor_utils import clean_sensor_readings


def run_tests() -> None:
    assert clean_sensor_readings([10, "20.5", None, -3, "bad", 700]) == [
        10.0,
        20.5,
        500.0,
    ]

    assert clean_sensor_readings([]) == []

    assert clean_sensor_readings([None, "invalid", -10, "-2.5"]) == []

    print("All sensor cleaning tests passed.")


if __name__ == "__main__":
    run_tests()
