import time

from streaming_fall_detector import FallDetectorStream
from accel_sim import generate

SAMPLE_RATE_HZ = 50

# False keeps using fake data, for continued testing.
USE_REAL_SENSOR = True


if USE_REAL_SENSOR:
    from hardware.i2c_reader import init_accelerometer, read_accelerometer
    from hardware.buzzer import trigger_buzzer
else:
    def trigger_buzzer():
        """STAND-IN for fake-data testing -- the real GPIO version is imported above instead."""
        print("    >>> BUZZER ON <<<")


def fake_sensor_stream():
    """Concatenates a few scenarios back to back to simulate a longer live session."""
    for name in ["resting", "walking", "fall", "resting"]:
        x, y, z = generate(name)
        for i in range(len(x)):
            yield x[i], y[i], z[i]


def main():
    detector = FallDetectorStream()
    sample_count = 0

    if USE_REAL_SENSOR:
        init_accelerometer()
        print("Starting fall detection loop (REAL sensor mode)...")
        print("-" * 50)
        while True:  # a real device runs forever, there's no "end of clip"
            x, y, z = read_accelerometer()
            fall_detected = detector.update(x, y, z)
            sample_count += 1

            if fall_detected:
                t = sample_count / SAMPLE_RATE_HZ
                print(f"[{t:6.2f}s] FALL DETECTED (sample #{sample_count})")
                trigger_buzzer()

            time.sleep(1 / SAMPLE_RATE_HZ)  # real pacing matters here - not optional like in fake mode

    else:
        print("Starting fall detection loop (fake sensor mode)...")
        print("-" * 50)
        for x, y, z in fake_sensor_stream():
            fall_detected = detector.update(x, y, z)
            sample_count += 1

            if fall_detected:
                t = sample_count / SAMPLE_RATE_HZ
                print(f"[{t:6.2f}s] FALL DETECTED (sample #{sample_count})")
                trigger_buzzer()
            # no sleep here - lets the fake-data demo finish instantly instead of taking ~9 real seconds

        print("-" * 50)
        print(f"Done. Processed {sample_count} samples.")


if __name__ == "__main__":
    main()
