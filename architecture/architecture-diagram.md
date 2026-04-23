# Architecture Diagram

Below is a description of the high-level system architecture. For implementation, use tools like draw.io, Lucidchart, or Mermaid for diagrams.

## High-Level System Diagram (Text)

```
+-------------------+        +-------------------+        +-------------------+
|                   |        |                   |        |                   |
|   Mobile Client   | <----> |  Signaling Server | <----> |   Database/Cache  |
| (Android/iOS App) |        |   (WebSocket)     |        | (Postgres/Redis)  |
|                   |        |                   |        |                   |
+-------------------+        +-------------------+        +-------------------+
         |                           |
         |                           |
         v                           v
+-------------------+        +-------------------+
|                   |        |                   |
|  RTC Media Server | <----> | Monitoring/Alert  |
|   (WebRTC/SFU)    |        | (Prometheus, etc) |
|                   |        |                   |
+-------------------+        +-------------------+
         |
         v
+-------------------+
|                   |
| Bluetooth Helmet  |
| (A2DP/HFP Device) |
|                   |
+-------------------+
```

## Component Legend
- Mobile Client: Flutter/React Native app with native modules
- Signaling Server: Node.js/Go WebSocket server for RTC
- Database/Cache: PostgreSQL, Redis
- RTC Media Server: WebRTC (SFU/mesh)
- Monitoring/Alert: Prometheus, Grafana, Sentry
- Bluetooth Helmet: End-user device

## Notes
- For detailed sequence diagrams, see each component's architecture file.
- Update this file with Mermaid or image diagrams as needed.
