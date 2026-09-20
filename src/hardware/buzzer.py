import time
from gpiozero import Buzzer, TonalBuzzer
 
BUZZER_PIN = 17
BUZZER_TYPE = "active"   # change to "passive" if this is a passive buzzer
 
if BUZZER_TYPE == "active":
    _buzzer = Buzzer(BUZZER_PIN)
else:
    _buzzer = TonalBuzzer(BUZZER_PIN)
 
 
def trigger_buzzer(duration_s=1.0):
    """
    Sounds the buzzer for duration_s seconds, then stops.
    Same name/shape as the print-based stand-in it's replacing in
    main.py -- nothing else in that file needs to change.
    """
    if BUZZER_TYPE == "active":
        _buzzer.on()
    else:
        _buzzer.play(440)  # 440Hz = a plain, audible A4 tone -- change if you want a different pitch
 
    time.sleep(duration_s)
    _buzzer.off() if BUZZER_TYPE == "active" else _buzzer.stop()
 
 
if __name__ == "__main__":
    print(f"Testing buzzer on GPIO{BUZZER_PIN} ({BUZZER_TYPE}) -- should sound for 1 second")
    trigger_buzzer(1.0)
    print("Done. If you didn't hear anything, try flipping BUZZER_TYPE and running again.")
