# FallGuard

An application that detects falls for fall-risk individuals using a wearable accelerometer and a Raspberry Pi. It features a live-syncing web application accessible at `https://fallguard-demo.web.app`.

Built at SteelHacks 2026 - submitted to **Seed Round**, **No Wrapper**, and **Cold Start**.

## The Problem

Fall-risk individuals - elderly people, those with mobility impairments - often fall without anyone nearby to help. Most existing solutions require pressing a button after the fall, which isn't possible if someone is unconscious, disoriented, or injured.

**Who pays for this:** Elder care facilities and assisted living operators, who are liable for resident safety and already budget for monitoring systems, are the most realistic first buyer. Secondary buyer: adult children of aging parents living independently, as a lower-cost alternative to traditional medical alert subscriptions.

## Demo
* **Live Companion App:** https://fallguard-demo.web.app

* **Pitch Deck:** [View our SteelHacks Presentation](Docs/SteelHacks%202026%20-%20FallGuard%20Presentation%20.pdf)

## What it does

A wearable accelerometer streams motion data into a Raspberry Pi in real time. Detection logic looks for the distinct two-phase signature of a real fall - a brief freefall (near-zero acceleration) followed by a sharp impact spike and a period of stillness - and distinguishes it from normal movement like sitting down or walking. When a fall is confirmed, it triggers an audible alert. No LLM is used anywhere in this pipeline. Detection is classical signal processing / classical ML - a rule-based state machine.

The hardware is paired with a healthcare-themed companion web application. Users can select their role—such as care recipient, emergency contact, or caretaker—and input their first name for a personalized, real-time monitoring experience across devices.

## How it works

1. **Sensor** - 3-axis accelerometer (I2C), worn on the body.
2. **Read loop** - Raspberry Pi (Python) polls acceleration at ~50Hz.
3. **Detection** - A state machine (or classical ML classifier) looks for freefall -> impact -> stillness.
4. **Alert** - Buzzer fires on confirmed fall.
5. **Live Sync** - The system connects to a Firebase-hosted backend to sync state across devices in real time.

## Why waist, not wrist

We chose waist placement over a wrist-worn design deliberately. Wrist-worn accelerometers pick up a lot of normal arm movement - waving, reaching, bumping a hand against something - that can produce sharp acceleration spikes resembling a fall's impact signature, leading to false positives. The waist sits close to the body's center of mass, so it moves with overall body motion rather than swinging independently, which makes our threshold-based detection far more reliable without needing complex motion-filtering logic.

## Team

* **Kadair Walker | Project Manager & Front-End Lead**
  * Spearheaded the initial concept and oversaw end-to-end project execution.
  * Managed task delegation, team check-ins, and version control via GitHub.
  * Developed and styled the front-end web application interface.
  * Assisted across the stack with Raspberry Pi hardware assembly, Python scripting, and system testing.
* **Dharma Swaroop | Embedded Systems Developer**
  * Served as the lead programmer for the Raspberry Pi environment. 
  * Engineered the Python logic for the hardware system, including the classical rule-based state machine for fall detection.
* **Nidhi Mendu | QA Specialist & Lead Presenter**
  * Co-led the live pitch and physical demo presentation for the judges.
  * Designed and structured the final presentation deck.
  * Conducted rigorous quality assurance and physical drop-testing on the wearable device.
* **Pragnya Eranki | Hardware Engineer & Lead Presenter**
  * Co-led the live pitch and physical demo presentation for the judges.
  * Collaborated on the design and structuring of the presentation deck.
  * Assembled the physical Raspberry Pi hardware, I2C sensors, and wearable mounting components.

## Tech stack

* Python
* Raspberry Pi
* Grove 3-Axis Digital Accelerometer (MMA7660)
* Firebase Hosting
* HTML/Progressive Web App (PWA)

## Status
Built in 24 hours at SteelHacks.
