# RiderComm Delivery Plan

## Purpose
This document turns the architecture and implementation plan into a concrete delivery plan with milestones, assigned AI agent prompts, and a dependency matrix.

## Milestones

### Milestone 1: Architecture Validation and Setup
- Deliverables:
  - Final tech stack selection
  - Repo structure created
  - Core architecture docs approved
  - Shared conventions established
- Duration: 1 week
- Dependencies:
  - Architecture docs
  - Team agreement on platform choices

### Milestone 2: Backend Core and Data Model
- Deliverables:
  - PostgreSQL schema and migrations
  - REST API for auth, users, sessions, devices, messages
  - JWT auth middleware
  - API documentation
- Duration: 2 weeks
- Dependencies:
  - Data model definitions
  - API spec
  - Security requirements

### Milestone 3: RTC Signaling and Session Management
- Deliverables:
  - WebSocket RTC signaling server
  - RTC room lifecycle and transient state store
  - Secure WebSocket auth
  - Basic offer/answer/ICE exchange support
- Duration: 2 weeks
- Dependencies:
  - Backend API scaffold
  - Data model persistence
  - RTC architecture

### Milestone 4: Mobile App Core Flows
- Deliverables:
  - Cross-platform mobile app scaffold
  - Auth and ride session UI
  - Participant state and voice controls
  - REST API integration
- Duration: 3 weeks
- Dependencies:
  - Backend API endpoints
  - Mobile framework choice
  - Shared API contracts

### Milestone 5: WebRTC and Media Integration
- Deliverables:
  - Mobile WebRTC integration
  - Signaling client adapter
  - Peer connection lifecycle
  - Basic voice call working between two devices
- Duration: 3 weeks
- Dependencies:
  - Mobile app scaffold
  - Signaling server
  - STUN/TURN infrastructure

### Milestone 6: Audio and Bluetooth Management
- Deliverables:
  - Native audio routing modules
  - Audio DSP mix/duck implementation
  - Bluetooth profile detection and switching
  - Distributed logging for audio state
- Duration: 4 weeks
- Dependencies:
  - Mobile RTC integration
  - Native module strategy
  - Hardware test devices

### Milestone 7: Deployment and Observability
- Deliverables:
  - Dockerized backend services
  - Terraform/Kubernetes deployment
  - CI/CD pipelines
  - Monitoring dashboards and alerting
- Duration: 2 weeks
- Dependencies:
  - Backend and signaling services
  - Cloud provider selection
  - Security requirements

### Milestone 8: Validation, Testing, and Release
- Deliverables:
  - End-to-end validation tests
  - Performance and audio quality tests
  - Beta release builds
  - Feedback and iteration plan
- Duration: 2 weeks
- Dependencies:
  - Working mobile and backend systems
  - Test devices and pilot users
  - Monitoring and logging

## AI Agent Prompts

### Agent 1: Backend Core Developer
Prompt:
- Implement the RiderComm backend REST API using the selected backend stack.
- Build database schema and migrations for `User`, `Device`, `RideSession`, `Participant`, `Message`, `AudioEvent`, `RTCSession`.
- Add JWT-based authentication and role-based authorization.
- Implement API endpoints for ride session lifecycle, participant management, device registration, and messaging.
- Create OpenAPI documentation and basic integration tests.

Output:
- `backend/` project scaffold
- `infra/` schema migration files
- API docs and test cases

### Agent 2: RTC Signaling Developer
Prompt:
- Build the RTC signaling service for RiderComm using WebSocket.
- Support room join/leave, SDP offer/answer, ICE candidate exchange, mute/unmute events.
- Store transient room state in Redis and enforce JWT auth on connections.
- Provide a protocol definition for mobile clients.

Output:
- `backend/signaling/` service
- WebSocket message schema and handler docs
- Signaling tests and room lifecycle logic

### Agent 3: Mobile App Developer
Prompt:
- Create the RiderComm mobile app using the selected cross-platform framework.
- Implement auth, ride session screens, participant list, and voice control UI.
- Add REST API client integration, session state management, and background handling.
- Integrate with the signaling protocol for join/leave and participant events.

Output:
- `mobile/` app scaffold
- UI flows for onboarding, sessions, and voice controls
- API client and state management modules

### Agent 4: RTC / Media Developer
Prompt:
- Integrate native WebRTC on Android and iOS.
- Build peer connection management, signaling adapter, and audio session state.
- Validate audio send/receive between two mobile clients.
- Prepare architecture for optional SFU support.

Output:
- WebRTC client module
- Mobile signaling adapter code
- RTC state UI hooks and tests

### Agent 5: Audio / Bluetooth Developer
Prompt:
- Implement native audio routing and DSP modules for RiderComm.
- Support voice capture, music ducking, and noise suppression.
- Detect Bluetooth helmet profiles and switch between A2DP and HFP intelligently.
- Expose APIs to the mobile app for audio status and routing control.

Output:
- `native_audio/` and `native_bluetooth/` module implementations
- Mobile integration wrappers
- Audio profile state logging

### Agent 6: Deployment / DevOps Developer
Prompt:
- Containerize backend and signaling services.
- Provision cloud infrastructure with Terraform or chosen IaC.
- Build CI/CD pipelines for backend and mobile.
- Configure monitoring, alerting, and secrets management.

Output:
- `infra/` deployment manifests
- GitHub Actions workflows
- Monitoring dashboards and alert rules

### Agent 7: QA / Validation Lead
Prompt:
- Create an end-to-end validation plan for RiderComm.
- Build automated test coverage for API contracts, signaling, RTC, audio behavior, and Bluetooth switching.
- Define manual device test scenarios for Android and iOS helmet audio.
- Document acceptance criteria and pilot release checklist.

Output:
- Test plan document
- Automated test suites and scripts
- Pilot release report

## Dependency Matrix

| Component | Depends On | Notes |
|---|---|---|
| Mobile App | Backend API, RTC signaling, native audio/Bluetooth | Requires signed API contracts and native modules |
| Backend API | Data model, auth, security | Must be stable before mobile integration |
| Signaling | Backend auth, Redis, STUN/TURN | Needs secure socket auth and transient state management |
| WebRTC | Signaling, mobile app, TURN/STUN | Requires network infrastructure and mobile bindings |
| Audio DSP | Native audio routing, mobile integration | Device-level behavior must be validated on hardware |
| Bluetooth | Native platform APIs, audio pipeline | Platform behavior differs significantly between Android and iOS |
| Deployment | Backend, monitoring, security | Needs completed services and cloud provider plan |
| Validation | Entire system | Final verification depends on all previous milestones |

## Risk and Gap Notes
- The most critical execution risk is the Bluetooth/A2DP vs HFP limitation; this must be validated early in the audio/Bluetooth milestone.
- STUN/TURN infrastructure is a required dependency for reliable mobile RTC and should be provisioned before WebRTC integration.
- Platform-specific background audio and permission handling must be scoped as part of Milestone 4 and 6.

## Recommended Execution Strategy
1. Run Milestones 1-3 in parallel where possible, with separate agents for backend and signaling.
2. Start the mobile scaffold in parallel with backend work, using mock API responses initially.
3. Reserve hardware testing for Milestone 6 and make it an explicit acceptance gate.
4. Keep the dependency matrix updated as components become clarified.

## File References
- `architecture/implementation-plan.md`
- `architecture/workflows/` for agent-level task breakdown
- `architecture/data-models.md`
- `architecture/api.md`
- `architecture/rtc.md`
- `architecture/bluetooth.md`
- `architecture/audio-pipeline.md`
- `architecture/deployment.md`
- `architecture/monitoring.md`
