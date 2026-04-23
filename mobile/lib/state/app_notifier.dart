import "dart:async";

import "package:flutter_riverpod/flutter_riverpod.dart";

import "../models/app_models.dart";
import "../services/api_client.dart";
import "../services/signaling_client.dart";
import "../services/token_store.dart";
import "app_state.dart";

class AppNotifier extends StateNotifier<AppState> {
  AppNotifier({required ApiClient api, required SignalingClient signaling, required TokenStore tokenStore})
      : _api = api,
        _signaling = signaling,
        _tokenStore = tokenStore,
        super(AppState.initial);

  final ApiClient _api;
  final SignalingClient _signaling;
  final TokenStore _tokenStore;

  StreamSubscription<dynamic>? _signalSubscription;

  Future<void> initialize() async {
    state = state.copyWith(loading: true, clearError: true);
    try {
      final persisted = await _tokenStore.loadSession();
      if (persisted != null) {
        final refreshedUser = await _api.me(userId: persisted.user.id);
        state = state.copyWith(user: refreshedUser, token: persisted.token);
        await refreshSessions();
      }
      state = state.copyWith(initialized: true, loading: false, clearError: true);
    } catch (_) {
      await _tokenStore.clearSession();
      state = state.copyWith(
        initialized: true,
        loading: false,
        clearUser: true,
        clearToken: true,
        sessions: <RideSessionModel>[],
        error: "Session restore failed. Please log in again.",
      );
    }
  }

  Future<void> registerAndLogin({required String email, required String password, required String displayName}) async {
    state = state.copyWith(loading: true, clearError: true);
    try {
      final registered = await _api.register(email: email, password: password, displayName: displayName);
      final auth = await _api.login(email: email, password: password);
      await _tokenStore.saveSession(user: registered, token: auth.accessToken);
      state = state.copyWith(user: registered, token: auth.accessToken, loading: false, clearError: true);
      await refreshSessions();
    } catch (error) {
      state = state.copyWith(loading: false, error: error.toString());
    }
  }

  Future<void> refreshSessions() async {
    try {
      final sessions = await _api.listRideSessions();
      state = state.copyWith(sessions: sessions, clearError: true);
    } catch (error) {
      state = state.copyWith(error: error.toString());
    }
  }

  Future<void> createSession(String title) async {
    final currentUser = state.user;
    if (currentUser == null) {
      state = state.copyWith(error: "No user logged in");
      return;
    }

    state = state.copyWith(loading: true, clearError: true);
    try {
      final created = await _api.createRideSession(ownerUserId: currentUser.id, title: title);
      final updatedSessions = <RideSessionModel>[...state.sessions, created];
      state = state.copyWith(sessions: updatedSessions, loading: false, clearError: true);
    } catch (error) {
      state = state.copyWith(loading: false, error: error.toString());
    }
  }

  Future<void> joinSessionAndConnect(String roomId) async {
    final currentUser = state.user;
    final currentToken = state.token;
    if (currentUser == null || currentToken == null) {
      state = state.copyWith(error: "User must be logged in before joining sessions");
      return;
    }

    state = state.copyWith(loading: true, clearError: true);
    try {
      await _api.joinRideSession(rideSessionId: roomId, userId: currentUser.id);
      _signalSubscription?.cancel();
      _signaling.connect(roomId: roomId, token: currentToken);

      _signaling.send(
        SignalingEnvelope(
          roomId: roomId,
          userId: currentUser.id,
          type: "join",
          payload: <String, dynamic>{},
        ),
      );

      _signalSubscription = _signaling.messages().listen((dynamic message) {
        state = state.copyWith(lastSignalMessage: message.toString());
      });

      state = state.copyWith(activeRoomId: roomId, loading: false, clearError: true);
    } catch (error) {
      state = state.copyWith(loading: false, error: error.toString());
    }
  }

  Future<void> logout() async {
    await _signalSubscription?.cancel();
    _signaling.close();
    await _tokenStore.clearSession();
    state = state.copyWith(
      clearUser: true,
      clearToken: true,
      sessions: <RideSessionModel>[],
      clearActiveRoomId: true,
      clearLastSignalMessage: true,
      clearError: true,
    );
  }

  @override
  void dispose() {
    _signalSubscription?.cancel();
    _signaling.close();
    super.dispose();
  }
}
