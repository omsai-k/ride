import "package:flutter_riverpod/flutter_riverpod.dart";

import "../config/app_environment.dart";
import "../services/api_client.dart";
import "../services/signaling_client.dart";
import "../services/token_store.dart";
import "app_notifier.dart";
import "app_state.dart";

final appEnvironmentProvider = Provider<AppEnvironment>((ProviderRef<AppEnvironment> ref) {
  return AppEnvironment.fromCompileTime();
});

final apiClientProvider = Provider<ApiClient>((ProviderRef<ApiClient> ref) {
  final environment = ref.read(appEnvironmentProvider);
  return ApiClient(baseUrl: environment.apiBaseUrl);
});

final signalingClientProvider = Provider<SignalingClient>((ProviderRef<SignalingClient> ref) {
  final environment = ref.read(appEnvironmentProvider);
  return SignalingClient(wsBaseUrl: environment.wsBaseUrl);
});

final tokenStoreProvider = Provider<TokenStore>((ProviderRef<TokenStore> ref) {
  return TokenStore();
});

final appNotifierProvider = StateNotifierProvider<AppNotifier, AppState>((StateNotifierProviderRef<AppNotifier, AppState> ref) {
  final notifier = AppNotifier(
    api: ref.read(apiClientProvider),
    signaling: ref.read(signalingClientProvider),
    tokenStore: ref.read(tokenStoreProvider),
  );
  notifier.initialize();
  return notifier;
});
