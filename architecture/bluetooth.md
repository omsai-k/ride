# Bluetooth Handling

## Overview
Bluetooth audio management is critical for RiderComm. The system must intelligently switch between A2DP (high-quality music) and HFP (voice/mic) profiles to enable simultaneous music and voice communication.

## Key Concepts
- **A2DP:** High-quality stereo music, no mic
- **HFP/SCO:** Mono, supports mic, low-quality audio
- **Limitation:** Most devices cannot use both at once

## Strategy
1. **Profile Detection**
   - Detect connected helmet and supported profiles
   - Query OS for Bluetooth capabilities
2. **Smart Switching**
   - Default to A2DP for music
   - Switch to HFP only when voice is detected (push-to-talk or open mic)
   - Return to A2DP immediately after voice ends
   - Minimize switching latency
3. **Audio Routing**
   - Use native APIs for routing (AudioManager on Android, AVAudioSession on iOS)
   - Attempt to keep music uninterrupted during short voice bursts
4. **Fallbacks**
   - If device supports dual profile, use both
   - If not, prioritize music unless voice is critical
5. **Future Exploration**
   - Investigate custom helmet firmware
   - Explore OS-level hacks for dual profile

## Implementation Notes
- Profile switching must be seamless to avoid user disruption
- Log all profile switches for debugging
- Provide user feedback on profile status
- Extensible for new Bluetooth standards
