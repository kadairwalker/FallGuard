# Hardware

## Components
- Raspberry Pi kit
- Male to female wires
- Female to female wires
- Buzzer
- 3-axis digital accelerometer
- Grove to Grove wires
- Solderless bread board
- Micro SD adapter

## Utlilization
- Raspberry Pi reads data from the accelerometer
- Accelerometer tracks movement on X, Y, and Z axes
- Python calculates overall acceleration
- Detects a freefall → impact → stillness pattern
- Buzzer activates when a fall is detected
- Data can be recorded for testing and improving accuracy


## Execution
- Connect accelerometer and buzzer to Raspberry Pi
- Run the Python fall-detection program
- Continuously monitor movement
- Detect possible falls using acceleration thresholds
- Confirm fall using impact and stillness
- Activate buzzer when a fall is confirmed
- Test with simulated falls and normal movements


