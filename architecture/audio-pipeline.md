# Audio Pipeline

## Overview
The audio pipeline is responsible for mixing music and voice, applying noise suppression, and managing Bluetooth profile switching to maintain high-quality music and clear voice communication.

## Pipeline Steps
1. **Audio Input**
   - Music: System audio capture (A2DP)
   - Voice: Helmet mic (HFP/SCO)
2. **Audio Routing**
   - Native OS APIs (Android/iOS)
   - Custom routing logic for profile switching
3. **Audio Mixing**
   - Duck music volume when voice detected
   - Overlay voice on music
   - Real-time mixing (native DSP)
4. **Noise Suppression**
   - Wind and road noise filtering (DSP, ML-based optional)
5. **Output**
   - Mixed stream sent to Bluetooth helmet
   - Maintain stereo for music, mono for voice overlay
6. **Bluetooth Profile Management**
   - Smart switching between A2DP (music) and HFP (voice)
   - Minimize switching latency
   - Attempt to keep A2DP active as much as possible

## Implementation Notes
- Use native C++/Rust for low-latency DSP
- FFI bindings to mobile framework
- Profile switching logic must be highly optimized
- Consider partial duplex/priority switching
- Future: Explore custom helmet firmware for better integration
