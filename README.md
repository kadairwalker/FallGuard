# FallGuard

An application that detects falls for fall-risk individuals using a wearable accelerometer and a Raspberry Pi.

Built at SteelHacks 2026 - submitted to **Seed Round**, **No Wrapper**, and **Cold Start**.

## The Problem

Fall-risk individuals - elderly people, those with mobility impairments - often fall without anyone nearby to help. Most existing solutions require pressing a button after the fall, which isn't possible if someone is unconscious, disoriented, or injured.

## What it does

A wearable accelerometer streams motion data into a Raspberry Pi in real time. Detection logic looks for the distinct two-phase signature of a real fall - a brief freefall (near-zero acceleration) followed by a sharp impact spike and a period of stillness - and distinguishes it from normal movement like sitting down or walking. When a fall is confirmed, it triggers an audible alert.

## How it works

1. **Sensor** - 3-axis accelerometer (I2C), worn on the body
2. **Read loop** - Raspberry Pi (Python) polls accceleration at ~50Hz
3. **Detection** - a state machine (or classical ML classifier) looks for freefall -> impact -> stillness
4. **Alert** - buzzer fires on confirmed fall

No LLM is used anywhere in this pipeline. Detection is classical signal processing / classical ML - a rule-based state machine, or a simple decision tree on windowed features.

## Team

-
-
-
-

## Tech stack

- Python
- Raspberry Pi
- [Accelerometer model]

## Status
Built in 24 hours at SteelHacks.