import "dart:convert";

import "package:http/http.dart" as http;

import "../models/app_models.dart";

class ApiClient {
  ApiClient({required this.baseUrl});

  final String baseUrl;

  Future<UserModel> register({
    required String email,
    required String password,
    required String displayName,
  }) async {
    final response = await http.post(
      Uri.parse("$baseUrl/auth/register"),
      headers: {"Content-Type": "application/json"},
      body: jsonEncode(
        {
          "email": email,
          "password": password,
          "display_name": displayName,
        },
      ),
    );
    _ensureSuccess(response);
    return UserModel.fromJson(jsonDecode(response.body) as Map<String, dynamic>);
  }

  Future<AuthResponse> login({
    required String email,
    required String password,
  }) async {
    final response = await http.post(
      Uri.parse("$baseUrl/auth/login"),
      headers: {"Content-Type": "application/json"},
      body: jsonEncode(
        {
          "email": email,
          "password": password,
        },
      ),
    );
    _ensureSuccess(response);
    return AuthResponse.fromJson(jsonDecode(response.body) as Map<String, dynamic>);
  }

  Future<UserModel> me({required String userId}) async {
    final response = await http.get(Uri.parse("$baseUrl/user/me/$userId"));
    _ensureSuccess(response);
    return UserModel.fromJson(jsonDecode(response.body) as Map<String, dynamic>);
  }

  Future<RideSessionModel> createRideSession({
    required String ownerUserId,
    required String title,
  }) async {
    final response = await http.post(
      Uri.parse("$baseUrl/ride-sessions"),
      headers: {"Content-Type": "application/json"},
      body: jsonEncode(
        {
          "owner_user_id": ownerUserId,
          "title": title,
        },
      ),
    );
    _ensureSuccess(response);
    return RideSessionModel.fromJson(jsonDecode(response.body) as Map<String, dynamic>);
  }

  Future<List<RideSessionModel>> listRideSessions() async {
    final response = await http.get(Uri.parse("$baseUrl/ride-sessions"));
    _ensureSuccess(response);
    final raw = jsonDecode(response.body) as List<dynamic>;
    return raw.map((item) => RideSessionModel.fromJson(item as Map<String, dynamic>)).toList();
  }

  Future<void> joinRideSession({
    required String rideSessionId,
    required String userId,
  }) async {
    final response = await http.post(
      Uri.parse("$baseUrl/participants/join"),
      headers: {"Content-Type": "application/json"},
      body: jsonEncode(
        {
          "ride_session_id": rideSessionId,
          "user_id": userId,
        },
      ),
    );
    _ensureSuccess(response);
  }

  void _ensureSuccess(http.Response response) {
    if (response.statusCode < 200 || response.statusCode >= 300) {
      throw Exception("Request failed: ${response.statusCode} ${response.body}");
    }
  }
}
