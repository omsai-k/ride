import "package:flutter/material.dart";
import "package:flutter_riverpod/flutter_riverpod.dart";

import "screens/home_screen.dart";
import "screens/login_screen.dart";
import "state/app_providers.dart";

void main() {
  runApp(const ProviderScope(child: RideApp()));
}

class RideApp extends ConsumerWidget {
  const RideApp({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final appState = ref.watch(appNotifierProvider);
    return MaterialApp(
      title: "RiderComm",
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: const Color(0xFF15616D)),
        useMaterial3: true,
      ),
      home: !appState.initialized
          ? const Scaffold(body: Center(child: CircularProgressIndicator()))
          : appState.authenticated
              ? const HomeScreen()
              : const LoginScreen(),
    );
  }
}
