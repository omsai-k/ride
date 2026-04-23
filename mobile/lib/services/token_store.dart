import "dart:convert";

import "package:shared_preferences/shared_preferences.dart";

import "../models/app_models.dart";

class PersistedSession {
  PersistedSession({required this.user, required this.token});

  final UserModel user;
  final String token;
}

class TokenStore {
  static const String _tokenKey = "ride.access_token";
  static const String _userKey = "ride.user";

  Future<void> saveSession({required UserModel user, required String token}) async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.setString(_tokenKey, token);
    await prefs.setString(
      _userKey,
      jsonEncode(
        <String, dynamic>{
          "id": user.id,
          "email": user.email,
          "display_name": user.displayName,
        },
      ),
    );
  }

  Future<PersistedSession?> loadSession() async {
    final prefs = await SharedPreferences.getInstance();
    final token = prefs.getString(_tokenKey);
    final userJson = prefs.getString(_userKey);

    if (token == null || userJson == null) {
      return null;
    }

    final user = UserModel.fromJson(jsonDecode(userJson) as Map<String, dynamic>);
    return PersistedSession(user: user, token: token);
  }

  Future<void> clearSession() async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.remove(_tokenKey);
    await prefs.remove(_userKey);
  }
}
