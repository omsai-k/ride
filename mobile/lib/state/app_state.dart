import "../models/app_models.dart";

class AppState {
  const AppState({
    required this.initialized,
    required this.loading,
    required this.user,
    required this.token,
    required this.sessions,
    required this.activeRoomId,
    required this.lastSignalMessage,
    required this.error,
  });

  final bool initialized;
  final bool loading;
  final UserModel? user;
  final String? token;
  final List<RideSessionModel> sessions;
  final String? activeRoomId;
  final String? lastSignalMessage;
  final String? error;

  bool get authenticated => user != null && token != null;

  AppState copyWith({
    bool? initialized,
    bool? loading,
    UserModel? user,
    bool clearUser = false,
    String? token,
    bool clearToken = false,
    List<RideSessionModel>? sessions,
    String? activeRoomId,
    bool clearActiveRoomId = false,
    String? lastSignalMessage,
    bool clearLastSignalMessage = false,
    String? error,
    bool clearError = false,
  }) {
    return AppState(
      initialized: initialized ?? this.initialized,
      loading: loading ?? this.loading,
      user: clearUser ? null : (user ?? this.user),
      token: clearToken ? null : (token ?? this.token),
      sessions: sessions ?? this.sessions,
      activeRoomId: clearActiveRoomId ? null : (activeRoomId ?? this.activeRoomId),
      lastSignalMessage: clearLastSignalMessage ? null : (lastSignalMessage ?? this.lastSignalMessage),
      error: clearError ? null : (error ?? this.error),
    );
  }

  static const AppState initial = AppState(
    initialized: false,
    loading: false,
    user: null,
    token: null,
    sessions: <RideSessionModel>[],
    activeRoomId: null,
    lastSignalMessage: null,
    error: null,
  );
}
