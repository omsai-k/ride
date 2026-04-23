class AuthResponse {
  AuthResponse({required this.accessToken, required this.tokenType});

  final String accessToken;
  final String tokenType;

  factory AuthResponse.fromJson(Map<String, dynamic> json) {
    return AuthResponse(
      accessToken: json["access_token"] as String,
      tokenType: json["token_type"] as String,
    );
  }
}

class UserModel {
  UserModel({required this.id, required this.email, required this.displayName});

  final String id;
  final String email;
  final String displayName;

  factory UserModel.fromJson(Map<String, dynamic> json) {
    return UserModel(
      id: json["id"] as String,
      email: json["email"] as String,
      displayName: json["display_name"] as String,
    );
  }
}

class RideSessionModel {
  RideSessionModel({required this.id, required this.title, required this.status});

  final String id;
  final String title;
  final String status;

  factory RideSessionModel.fromJson(Map<String, dynamic> json) {
    return RideSessionModel(
      id: json["id"] as String,
      title: json["title"] as String,
      status: json["status"] as String,
    );
  }
}

class SignalingEnvelope {
  SignalingEnvelope({
    required this.roomId,
    required this.userId,
    required this.type,
    required this.payload,
  });

  final String roomId;
  final String userId;
  final String type;
  final Map<String, dynamic> payload;

  Map<String, dynamic> toJson() {
    return {
      "room_id": roomId,
      "user_id": userId,
      "type": type,
      "payload": payload,
    };
  }
}
