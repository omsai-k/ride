import "package:flutter/material.dart";
import "package:flutter_riverpod/flutter_riverpod.dart";

import "../state/app_providers.dart";

class HomeScreen extends ConsumerStatefulWidget {
  const HomeScreen({super.key});

  @override
  ConsumerState<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends ConsumerState<HomeScreen> {
  final TextEditingController _titleController = TextEditingController(text: "Morning Ride");

  @override
  void initState() {
    super.initState();
    Future<void>.microtask(() {
      ref.read(appNotifierProvider.notifier).refreshSessions();
    });
  }

  @override
  void dispose() {
    _titleController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final appState = ref.watch(appNotifierProvider);
    final notifier = ref.read(appNotifierProvider.notifier);
    final sessions = appState.sessions;
    final env = ref.watch(appEnvironmentProvider);

    return Scaffold(
      appBar: AppBar(
        title: const Text("RiderComm Sessions"),
        actions: <Widget>[
          IconButton(
            onPressed: () async {
              await notifier.logout();
            },
            icon: const Icon(Icons.logout),
            tooltip: "Logout",
          ),
        ],
      ),
      body: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: <Widget>[
            Text("Logged in as: ${appState.user?.email ?? "unknown"}"),
            Text("API: ${env.apiBaseUrl}"),
            const SizedBox(height: 12),
            Row(
              children: <Widget>[
                Expanded(
                  child: TextField(
                    controller: _titleController,
                    decoration: const InputDecoration(labelText: "New ride title"),
                  ),
                ),
                const SizedBox(width: 12),
                ElevatedButton(
                  onPressed: appState.loading
                      ? null
                      : () async {
                          await notifier.createSession(_titleController.text);
                        },
                  child: const Text("Create"),
                ),
              ],
            ),
            const SizedBox(height: 12),
            if (appState.error != null) Text(appState.error!, style: const TextStyle(color: Colors.red)),
            const Text("Available sessions:"),
            const SizedBox(height: 8),
            Expanded(
              child: ListView.builder(
                itemCount: sessions.length,
                itemBuilder: (BuildContext context, int index) {
                  final session = sessions[index];
                  return ListTile(
                    title: Text(session.title),
                    subtitle: Text("${session.id} • ${session.status}"),
                    trailing: ElevatedButton(
                      onPressed: () async {
                        await notifier.joinSessionAndConnect(session.id);
                      },
                      child: const Text("Join"),
                    ),
                  );
                },
              ),
            ),
            if (appState.activeRoomId != null) Text("Connected room: ${appState.activeRoomId}"),
            if (appState.lastSignalMessage != null) Text("Last signal: ${appState.lastSignalMessage}"),
          ],
        ),
      ),
    );
  }
}
