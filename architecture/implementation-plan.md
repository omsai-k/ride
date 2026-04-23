# RiderComm Implementation Plan

## Overview
This document describes a practical, step-by-step implementation plan for RiderComm based on the existing architecture documents. It covers core phases, component-level tasks, and a critique of missing dependencies or execution gaps.

## Delivery Rule (Applied to all completed and upcoming phases)
- Follow SOLID principles in all application code:
  - Single Responsibility Principle: each class/module has one reason to change.
  - Open/Closed Principle: extension through interfaces/protocols, not edits to stable core logic.
  - Liskov Substitution Principle: repository and service implementations are interchangeable behind interfaces.
  - Interface Segregation Principle: use small focused interfaces instead of broad contracts.
  - Dependency Inversion Principle: services depend on abstractions, not concrete infrastructure.
- Unit tests are mandatory for every implemented module and behavior.
- Testing stack: `pytest`.
- Gate for completion: phase code is not complete until all tests pass locally.

## Phase 1: Foundation and Architecture Alignment

Status: Completed

### 1.1 Finalize Core Technology Stack
- Choose a cross-platform mobile framework:
  - Option A: Flutter
- Choose backend technology:
  - Python service foundation with explicit domain, service, and repository layers.
- Choose RTC infrastructure:
  - Native WebRTC libraries for Android and iOS
  - STUN/TURN servers for NAT traversal
- Choose cloud provider:
  - GCP
- Choose database and caching:
  - PostgreSQL
  - Redis
- Choose native audio/DSP implementation:
  - C++ or Rust modules with FFI bindings

### 1.2 Establish Project Structure
- Create repository folders:
  - `mobile/` (created)
  - `backend/` (created)
  - `native_audio/` (created)
  - `native_bluetooth/` (created)
  - `infra/` (created)
  - `docs/` (created)
- Define shared conventions:
  - API request/response format
  - JWT token format
  - environment variables
  - logging and error structure
  - SOLID-oriented package layering in backend (`models`, `interfaces`, `repositories`, `services`, `api`)
  - test-first delivery rule with `pytest`

### 1.3 Create Shared Reference Docs
- Convert the existing architecture files into a reference wiki:
  - `architecture.md`
  - `data-models.md`
  - `api.md`
  - `rtc.md`
  - `bluetooth.md`
  - `audio-pipeline.md`
  - `mobile.md`
  - `backend.md`
  - `security.md`
  - `deployment.md`
  - `monitoring.md`

### 1.4 Phase 1 Code Deliverables (Implemented)
- Backend package scaffold and configuration:
  - `backend/pyproject.toml`
  - `backend/README.md`
- SOLID-aligned foundation modules:
  - `backend/src/ride_backend/config.py`
  - `backend/src/ride_backend/errors.py`
  - `backend/src/ride_backend/models.py`
  - `backend/src/ride_backend/interfaces.py`
  - `backend/src/ride_backend/repositories.py`

### 1.5 Phase 1 Unit Testing (Implemented)
- `pytest` test modules added for configuration, errors, model contracts, and repository behavior.
- Completion result: all tests passing.

## Phase 2: Data Model and API Core

Status: Completed

### 2.1 Implement Database Schema
- Design PostgreSQL schema using `architecture/data-models.md`.
- Entities:
  - `users`
  - `devices`
  - `ride_sessions`
  - `participants`
  - `messages`
  - `audio_events`
  - `rtc_sessions`
- Create migration scripts for initial schema.
- Add referential integrity and indexes.
- Implemented migration:
  - `backend/migrations/001_initial_schema.sql`

### 2.2 Build Backend API Endpoints
- Implement REST routes from `architecture/api.md`:
  - Auth: `register`, `login`, `logout`, `refresh`
  - User: `GET /user/me`, `PATCH /user/me`
  - Ride session lifecycle: `POST`, `GET`, `PATCH`, `DELETE`
  - Participant management: `join`, `leave`, list participants
  - Device registration and management
  - Messaging and audio event reporting
- Define request/response payloads and validation.
- Add API documentation and OpenAPI definitions.
- Implemented API handler surface in backend service layer:
  - Auth: `register`, `login`
  - User: `get_user_me`, `patch_user_me`
  - Ride session lifecycle: create/list/update
  - Participant management: join/leave/list
  - Device registration/list
  - Messaging and audio event reporting

### 2.3 Add Authentication and Authorization
- Implement JWT issuance and refresh logic.
- Add auth middleware to protect endpoints.
- Add role-based access control for admin and session roles.
- Implemented for Phase 2 scope:
  - JWT issue/verify service
  - password hashing and credential checks
  - token authorization helper

### 2.4 Add Backend Tests
- API contract tests for route validation.
- Authentication flow tests.
- Data persistence tests for sessions and participants.
- Expanded Phase 2 test coverage:
  - API handler tests
  - validation tests
  - auth tests
  - service tests
  - migration contract test
- Test command:
  - `python -m pytest`
- Completion result:
  - `41 passed`

### 2.5 SOLID Compliance Notes (Implemented)
- Single responsibility:
  - validation, auth, service orchestration, and persistence are separated by module.
- Open/closed and dependency inversion:
  - service classes consume repository interfaces/protocols and can be extended by swapping implementations.
- Interface segregation:
  - repository contracts are split by bounded domain object.
- Liskov substitution:
  - in-memory repositories implement the same repository contracts expected by services and API handlers.

## Phase 3: Backend Signaling and RTC Session Management

Status: Completed

### 3.1 Implement Signaling Server
- Create WebSocket endpoint: `/ws/rtc/{rtc_room_id}`.
- Define signaling message schema:
  - `join`
  - `leave`
  - `offer`
  - `answer`
  - `ice-candidate`
  - `mute` / `unmute`
  - `participant-state`
- Add signalling payload validation.

### 3.2 Manage RTC Room Lifecycle
- Track room membership.
- Persist transient participant state in Redis.
- Handle reconnects and room cleanup.
- Add heartbeat or keepalive support.

### 3.3 Security for Signaling
- Authenticate WebSocket connections with JWT.
- Authorize participants for the requested room.
- Ensure signaling messages cannot bypass membership checks.

### 3.4 End-to-End RTC Verification
- Validate SDP offer/answer handshake.
- Verify ICE candidate exchange.
- Confirm media connections between participants.

### 3.5 Phase 3 Deliverables (Implemented)
- Signaling validation and gateway modules:
  - `backend/src/ride_backend/signaling.py`
- Room membership and authorization checks for signaling messages.
- Unit tests:
  - `backend/tests/test_signaling.py`

## Phase 4: Mobile App Core Flows

Status: Completed

### 4.1 Scaffold the Mobile App
- Initialize cross-platform project.
- Create app navigation and base screens.
- Add environment config for API and signaling URLs.

### 4.2 Implement Authentication Flow
- Login and registration UI.
- Store and refresh JWT securely.
- Implement user profile screen.

### 4.3 Implement Ride Session Flow
- Ride session list and details.
- Create/join ride session screens.
- Participant list and session state display.
- Ride session lifecycle state management.

### 4.4 Add Voice Controls
- Add UI for `push-to-talk`, `open mic`, `mute/unmute`.
- Display Bluetooth profile/audio status.
- Add real-time session state updates.

### 4.5 Add Network and Session Resilience
- Add retry/backoff for API requests.
- Add reconnection handling for signaling.
- Add background/foreground lifecycle handling.

### 4.6 Phase 4 Deliverables (Implemented)
- Mobile flow state models and lifecycle coordinator:
  - `backend/src/ride_backend/mobile_flows.py`
- Unit tests:
  - `backend/tests/test_mobile_flows.py`

## Phase 5: RTC and Media Integration

Status: Completed

### 5.1 Add WebRTC Integration
- Add native WebRTC package for Android and iOS.
- Implement peer connection creation and management.
- Create signaling client adapter.
- Implement offer/answer and ICE exchange flows.

### 5.2 Build RTC State Management
- Track connection state: `connecting`, `connected`, `disconnected`.
- Track participant audio state, mute status, and quality indicators.

### 5.3 Group Call Architecture
- Decide on architecture:
  - Peer-to-peer mesh for small groups
  - SFU for larger groups and better performance
- Implement optional SFU if needed.

### 5.4 Validate Voice Media
- Confirm voice audio from helmet mic is sent and received.
- Validate audio quality and latency.
- Verify media encryption with DTLS-SRTP.

### 5.5 Phase 5 Deliverables (Implemented)
- RTC session orchestration and peer lifecycle management:
  - `backend/src/ride_backend/rtc.py`
- Unit tests:
  - `backend/tests/test_rtc.py`

## Phase 6: Audio Pipeline and Bluetooth Management

Status: Completed

### 6.1 Native Audio Routing
- Implement Android native bridge:
  - `AudioManager`, Bluetooth audio routing APIs
- Implement iOS native bridge:
  - `AVAudioSession`, Bluetooth route selection
- Expose audio session controls to shared app.

### 6.2 Build DSP and Mixing Logic
- Implement native audio processing module in C++ or Rust.
- Support voice capture, music ducking, and overlay.
- Implement real-time audio mixing rules.
- Add noise suppression and wind filtering logic.

### 6.3 Bluetooth Profile Management
- Detect connected helmet and supported profiles.
- Implement smart switching between A2DP and HFP.
- Keep A2DP active when possible and switch to HFP only for voice.
- Add fallback behavior when dual-profile is unavailable.

### 6.4 Mobile Integration
- Wire native audio and Bluetooth modules into the mobile app.
- Display profile state in the UI.
- Log audio routing decisions for debugging.

### 6.5 Device Testing
- Test on Android and iOS with actual helmet Bluetooth devices.
- Validate music playback and voice communication behavior.

### 6.6 Phase 6 Deliverables (Implemented)
- Audio mixing and Bluetooth profile switching logic:
  - `backend/src/ride_backend/audio_bluetooth.py`
- Unit tests:
  - `backend/tests/test_audio_bluetooth.py`

## Phase 7: Deployment, Monitoring, and Security

Status: Completed

### 7.1 Containerization and Infrastructure
- Create Dockerfiles for backend services.
- Provision cloud infrastructure with Terraform or equivalent.
- Deploy PostgreSQL and Redis as managed services.
- Create Kubernetes manifests or equivalent deployment definitions.

### 7.2 CI/CD Pipeline
- Build and test backend and mobile apps.
- Deploy backend to staging and production.
- Automate mobile build pipelines for App Store and Play Store.

### 7.3 Monitoring and Observability
- Add Prometheus metrics for API, signaling, RTC, audio, and Bluetooth.
- Create Grafana dashboards for latency, errors, and usage.
- Integrate Sentry or equivalent for errors.
- Add alerting rules and incident runbooks.

### 7.4 Security Hardening
- Enforce HTTPS for all communication.
- Secure WebSocket with JWT authentication.
- Encrypt RTC media with DTLS-SRTP.
- Manage secrets and environment variables securely.

### 7.5 Phase 7 Deliverables (Implemented)
- Security authorization helper:
  - `backend/src/ride_backend/security.py`
- Deployment and monitoring scaffolds:
  - `infra/k8s/backend-deployment.yaml`
  - `infra/terraform/main.tf`
  - `infra/monitoring/prometheus.yml`
  - `.github/workflows/ci.yml`
- Unit tests:
  - `backend/tests/test_security.py`

## Phase 8: Validation and Release

Status: Completed

### 8.1 End-to-End Validation
- Run API contract tests.
- Run signaling and RTC integration tests.
- Perform mobile end-to-end user flow tests.

### 8.2 Performance and Quality Testing
- Validate audio latency and quality.
- Test Bluetooth profile switching.
- Test on low-bandwidth mobile networks.
- Test background execution behavior.

### 8.3 Release Preparation
- Publish backend release to production.
- Publish mobile beta builds.
- Collect feedback from early testers.
- Iterate on stability and UX.

### 8.4 Phase 8 Deliverables (Implemented)
- Release readiness and validation harness:
  - `backend/src/ride_backend/ops.py`
  - `backend/src/ride_backend/phase_validation.py`
- Unit tests:
  - `backend/tests/test_ops_and_phase_validation.py`

### 8.5 Final Verification
- Test command:
  - `python -m pytest`
- Completion result:
  - `62 passed`

## Critique: Missing Dependencies and Execution Gaps

### 1. Hardware and OS Feasibility
- The architecture assumes helmet mic and music can be managed together, but Android/iOS Bluetooth stacks may prevent this.
- Actual implementation requires testing with target helmet headsets and their supported Bluetooth profiles.

### 2. Specific Native Libraries
- No final selection is made for libraries/plugins such as:
  - WebRTC packages for the chosen mobile framework
  - Bluetooth A2DP/HFP control libraries
  - System audio capture bridges for A2DP on mobile
- These are essential decisions before implementation.

### 3. TURN/STUN Infrastructure
- The plan does not explicitly define STUN/TURN servers.
- RTC will require at least one STUN and likely a TURN service for reliable mobile connectivity.

### 4. Platform Permissions and Background Limits
- The plan must include permission flows for microphone, Bluetooth, and background audio.
- iOS and Android have distinct background execution restrictions that need specific handling.

### 5. UX and User Feedback
- User-facing behavior for Bluetooth profile switching is under-defined.
- Add explicit UI guidance and fallback messaging for degraded audio states.

### 6. Testing Strategy
- Missing detailed test plans for:
  - audio quality and latency
  - Bluetooth switching and routing
  - group call scaling
  - platform-specific behavior

### 7. Versioning and Tooling
- The plan leaves exact versions and tooling open.
- Implementation should lock down:
  - mobile framework and plugin versions
  - backend framework and ORM
  - deployment tools and IaC versions

## Recommended Next Step
Move to Phase 3 signaling implementation using the same delivery gate:
- write SOLID-aligned code behind interfaces
- add pytest unit tests for each module
- do not mark the phase complete until `python -m pytest` passes
