
from fall_detector import (
    magnitude,
    FREEFALL_THRESHOLD_G,
    MIN_FREEFALL_SAMPLES,
    IMPACT_THRESHOLD_G,
    IMPACT_WINDOW_SAMPLES,
)


class FallDetectorStream:
    # three possible states -- this is the whole state machine
    IDLE = "idle"                          # normal, nothing unusual
    IN_FREEFALL = "in_freefall"            # currently below the freefall threshold
    WATCHING_FOR_IMPACT = "watching"       # freefall just ended, waiting to see if a spike follows

    def __init__(self):
        self.state = self.IDLE
        self.freefall_len = 0
        self.samples_since_freefall_ended = 0

    def update(self, x, y, z):
        """
        Call this once per new sample, in order, as they arrive.
        Returns True the instant a fall is confirmed, False otherwise.
        """
        mag = magnitude(x, y, z)

        if self.state == self.IDLE:
            if mag < FREEFALL_THRESHOLD_G:
                self.state = self.IN_FREEFALL
                self.freefall_len = 1

        elif self.state == self.IN_FREEFALL:
            if mag < FREEFALL_THRESHOLD_G:
                self.freefall_len += 1
            else:
                # magnitude just came back up - freefall phase just ended
                if self.freefall_len >= MIN_FREEFALL_SAMPLES:
                    # long enough to be real - start watching for the impact spike
                    self.state = self.WATCHING_FOR_IMPACT
                    self.samples_since_freefall_ended = 0
                    if mag > IMPACT_THRESHOLD_G:
                        # the very sample that ended freefall IS the impact spike
                        self.state = self.IDLE
                        return True
                else:
                    # too brief to be a real freefall (a near-miss, sensor jitter, etc.)
                    self.state = self.IDLE

        elif self.state == self.WATCHING_FOR_IMPACT:
            if mag > IMPACT_THRESHOLD_G:
                self.state = self.IDLE
                return True
            self.samples_since_freefall_ended += 1
            if self.samples_since_freefall_ended >= IMPACT_WINDOW_SAMPLES - 1:
                # window expired with no impact spike - false alarm, reset
                self.state = self.IDLE

        return False