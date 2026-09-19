import csv
import time
 
from hardware.i2c_reader import init_accelerometer, read_accelerometer
from fall_detector import magnitude, FREEFALL_THRESHOLD_G, IMPACT_THRESHOLD_G
 
DURATION_S = 10
SAMPLE_RATE_HZ = 50
 
 
def main():
    init_accelerometer()
    print(f"Recording for up to {DURATION_S}s -- drop the sensor NOW")
    print(f"(freefall threshold: {FREEFALL_THRESHOLD_G}g   impact threshold: {IMPACT_THRESHOLD_G}g)")
    print("Press Ctrl+C any time to stop early and still see the summary.")
    print("-" * 60)
 
    rows = []
    start = time.time()
    lowest_seen = float("inf")
    highest_seen = float("-inf")
 
    try:
        while time.time() - start < DURATION_S:
            x, y, z = read_accelerometer()
            mag = magnitude(x, y, z)
            lowest_seen = min(lowest_seen, mag)
            highest_seen = max(highest_seen, mag)
 
            flag = ""
            if mag < FREEFALL_THRESHOLD_G:
                flag = "  <-- FREEFALL RANGE"
            elif mag > IMPACT_THRESHOLD_G:
                flag = "  <-- IMPACT RANGE"
 
            t = time.time() - start
            print(f"t={t:6.2f}s  mag={mag:6.3f}g{flag}")
            rows.append((t, x, y, z, mag))
            time.sleep(1 / SAMPLE_RATE_HZ)
    except KeyboardInterrupt:
        print("\nStopped early by Ctrl+C -- still saving what was captured.")
 
    with open("real_data_recording.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["t", "x", "y", "z", "magnitude"])
        writer.writerows(rows)
 
    print("-" * 60)
    if rows:
        print(f"Lowest magnitude seen:  {lowest_seen:.3f}g   (needed BELOW {FREEFALL_THRESHOLD_G} to trigger freefall)")
        print(f"Highest magnitude seen: {highest_seen:.3f}g   (needed ABOVE {IMPACT_THRESHOLD_G} to trigger impact)")
        print(f"Saved {len(rows)} samples to real_data_recording.csv")
    else:
        print("No samples were recorded.")
 
 
if __name__ == "__main__":
    main()
 
