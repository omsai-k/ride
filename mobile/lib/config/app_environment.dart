import "dart:io";

import "package:flutter/foundation.dart";

class AppEnvironment {
  AppEnvironment({required this.apiBaseUrl, required this.wsBaseUrl});

  final String apiBaseUrl;
  final String wsBaseUrl;

  static const String _apiHostOverride = String.fromEnvironment("RIDE_API_HOST", defaultValue: "");
  static const String _apiPortOverride = String.fromEnvironment("RIDE_API_PORT", defaultValue: "8000");

  factory AppEnvironment.fromCompileTime() {
    final host = _apiHostOverride.trim().isNotEmpty ? _apiHostOverride.trim() : _defaultHost();
    final port = _apiPortOverride.trim();
    return AppEnvironment(
      apiBaseUrl: "http://$host:$port",
      wsBaseUrl: "ws://$host:$port",
    );
  }

  static String _defaultHost() {
    if (kIsWeb) {
      return "localhost";
    }
    if (Platform.isAndroid) {
      return "10.0.2.2";
    }
    return "localhost";
  }
}
