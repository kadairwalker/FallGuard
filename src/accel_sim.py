"""
Fake accelerometer data generator.

Units are "g" (1g = 9.8 m/s^2, standing still on Earth). At rest, gravity
pulls on the sensor no matter which way it's mounted, so the reading is
never (0,0,0) -- it's usually close to 1g on whichever axis points "down"
relative to the sensor.
"""

import numpy as np

SAMPLE_RATE_HZ = 50  # how many readings per second


def _rest(duration_s, noise=0.03):
    """Sitting/standing still. ~1g total, mostly on one axis, tiny sensor jitter."""
    n = int(duration_s * SAMPLE_RATE_HZ)
    x = np.random.normal(0, noise, n)
    y = np.random.normal(0, noise, n)
    z = np.random.normal(1.0, noise, n)
    return x, y, z


def _walking(duration_s):
    """Normal walking. Rhythmic ~1-1.3g bumps from footsteps, no freefall dip."""
    n = int(duration_s * SAMPLE_RATE_HZ)
    t = np.linspace(0, duration_s, n)
    step = 0.3 * np.sin(2 * np.pi * 2 * t)  # ~2 steps/sec
    x = np.random.normal(0, 0.1, n)
    y = np.random.normal(0, 0.1, n) + step
    z = np.random.normal(1.0, 0.1, n)
    return x, y, z


def _sit_fast(duration_s):
    """Sitting down quickly / bumping the device. A firm landing, but NOT a real fall:
    there's no freefall dip beforehand, just a moderate bump."""
    n = int(duration_s * SAMPLE_RATE_HZ)
    x, y, z = _rest(duration_s, noise=0.05)
    mid = n // 2
    spike_len = int(0.15 * SAMPLE_RATE_HZ)
    z[mid:mid + spike_len] += np.linspace(0, 0.6, spike_len)  # up to ~1.6g 
    return x, y, z


def _fall(duration_s):
    """A real fall: brief near-weightlessness (falling), then a hard impact spike,
    then stillness (lying on the ground)."""
    n = int(duration_s * SAMPLE_RATE_HZ)
    x, y, z = _rest(duration_s, noise=0.03)
    mid = n // 2

    freefall_len = int(0.4 * SAMPLE_RATE_HZ)  # ~400ms of falling
    impact_len = int(0.08 * SAMPLE_RATE_HZ)   # sharp, short impact

    # freefall: nothing is pushing against gravity, so all axes drop toward 0
    x[mid:mid + freefall_len] = np.random.normal(0, 0.05, freefall_len)
    y[mid:mid + freefall_len] = np.random.normal(0, 0.05, freefall_len)
    z[mid:mid + freefall_len] = np.random.normal(0.05, 0.05, freefall_len)

    # impact: sharp spike well above 1g right after freefall ends
    imp_start = mid + freefall_len
    x[imp_start:imp_start + impact_len] += np.random.normal(0, 0.3, impact_len)
    y[imp_start:imp_start + impact_len] += np.random.normal(0.5, 0.3, impact_len)
    z[imp_start:imp_start + impact_len] += np.linspace(1.5, 2.8, impact_len)

    # settle: lying still afterward
    settle_start = imp_start + impact_len
    remaining = n - settle_start
    x[settle_start:] = np.random.normal(0, 0.02, remaining)
    y[settle_start:] = np.random.normal(0.3, 0.02, remaining)
    z[settle_start:] = np.random.normal(0.9, 0.02, remaining)

    return x, y, z


SCENARIOS = {
    "resting": lambda: _rest(3.0),
    "walking": lambda: _walking(3.0),
    "sitting_fast": lambda: _sit_fast(3.0),
    "fall": lambda: _fall(3.0),
}


def generate(scenario_name):
    if scenario_name not in SCENARIOS:
        raise ValueError(f"unknown scenario '{scenario_name}', pick from {list(SCENARIOS)}")
    return SCENARIOS[scenario_name]()
