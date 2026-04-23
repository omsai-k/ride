import "dart:convert";

import "package:web_socket_channel/web_socket_channel.dart";

import "../models/app_models.dart";

class SignalingClient {
  SignalingClient({required this.wsBaseUrl});

  final String wsBaseUrl;
  WebSocketChannel? _channel;

  void connect({required String roomId, required String token}) {
    final uri = Uri.parse("$wsBaseUrl/ws/rtc/$roomId?token=$token");
    _channel = WebSocketChannel.connect(uri);
  }

  void send(SignalingEnvelope envelope) {
    final channel = _channel;
    if (channel == null) {
      throw Exception("WebSocket is not connected");
    }
    channel.sink.add(jsonEncode(envelope.toJson()));
  }

  Stream<dynamic> messages() {
    final channel = _channel;
    if (channel == null) {
      throw Exception("WebSocket is not connected");
    }
    return channel.stream;
  }

  void close() {
    _channel?.sink.close();
    _channel = null;
  }
}
