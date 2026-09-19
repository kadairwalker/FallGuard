"""
The detection logic:

Two-phase signature of a real fall:
  1. FREEFALL: acceleration magnitude drops close to 0g. This happens because
     during a fall, nothing is pushing back against gravity (the same
     "weightless" feeling you get at the top of a roller coaster drop).
  2. IMPACT: shortly after, magnitude spikes well above 1g as the body/device
     suddenly decelerates hitting the ground.

Sitting down fast or bumping the device produces an impact-like spike WITHOUT
the freefall dip beforehand.
"""

import numpy as np

SAMPLE_RATE_HZ = 50

# --- Tunable thresholds -----------------------------------------------------

FREEFALL_THRESHOLD_G = 0.35          # below this = "near weightless"
MIN_FREEFALL_SAMPLES = int(0.15 * SAMPLE_RATE_HZ)   # freefall must last >= ~150ms
IMPACT_THRESHOLD_G = 1.8             # above this = "impact spike"
IMPACT_WINDOW_SAMPLES = int(0.3 * SAMPLE_RATE_HZ)   # impact must land within ~300ms of freefall ending
# -----------------------------------------------------------------------------


def magnitude(x, y, z):
    """Combine 3 axes into one number, in g. This is what makes the detector
    independent of how the sensor is mounted/rotated -- you don't care which
    axis points 'down', only the total force."""
    return np.sqrt(x**2 + y**2 + z**2)


def detect_fall(x, y, z):
    """
    Scans the whole trace for: a sustained freefall dip, followed shortly by
    an impact spike.

    Returns:
        (fall_detected, freefall_start_index, impact_index)
        indices are None if no fall was found.
    """
    mag = magnitude(x, y, z)
    n = len(mag)

    in_freefall = False
    freefall_len = 0
    freefall_start = None

    for i in range(n):
        if mag[i] < FREEFALL_THRESHOLD_G:
            if not in_freefall:
                in_freefall = True
                freefall_start = i
                freefall_len = 0
            freefall_len += 1
        else:
            if in_freefall and freefall_len >= MIN_FREEFALL_SAMPLES:
                window_end = min(n, i + IMPACT_WINDOW_SAMPLES)
                for j in range(i, window_end):
                    if mag[j] > IMPACT_THRESHOLD_G:
                        return True, freefall_start, j
            in_freefall = False
            freefall_len = 0

    return False, None, None