import "package:flutter/material.dart";
import "package:flutter_riverpod/flutter_riverpod.dart";

import "../state/app_providers.dart";

class LoginScreen extends ConsumerStatefulWidget {
  const LoginScreen({super.key});

  @override
  ConsumerState<LoginScreen> createState() => _LoginScreenState();
}

class _LoginScreenState extends ConsumerState<LoginScreen> {
  final TextEditingController _email = TextEditingController(text: "rider@example.com");
  final TextEditingController _password = TextEditingController(text: "secret123");
  final TextEditingController _name = TextEditingController(text: "Rider");

  @override
  void dispose() {
    _email.dispose();
    _password.dispose();
    _name.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final appState = ref.watch(appNotifierProvider);
    final notifier = ref.read(appNotifierProvider.notifier);
    return Scaffold(
      appBar: AppBar(title: const Text("RiderComm Login")),
      body: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          children: <Widget>[
            TextField(controller: _email, decoration: const InputDecoration(labelText: "Email")),
            TextField(controller: _password, decoration: const InputDecoration(labelText: "Password"), obscureText: true),
            TextField(controller: _name, decoration: const InputDecoration(labelText: "Display name")),
            const SizedBox(height: 16),
            if (appState.error != null) Text(appState.error!, style: const TextStyle(color: Colors.red)),
            ElevatedButton(
              onPressed: appState.loading
                  ? null
                  : () async {
                      await notifier.registerAndLogin(
                        email: _email.text,
                        password: _password.text,
                        displayName: _name.text,
                      );
                    },
              child: const Text("Register + Login"),
            ),
          ],
        ),
      ),
    );
  }
}
