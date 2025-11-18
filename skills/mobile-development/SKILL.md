---
name: mobile-development
description: Build iOS and Android apps with Swift, Kotlin, React Native, and Flutter. Learn native development, cross-platform frameworks, UI/UX design, and app store deployment. Use when working on mobile development.
---

# Mobile Development

Create native and cross-platform mobile applications.

## Quick Start

### Swift with SwiftUI
```swift
import SwiftUI

struct ContentView: View {
    @State private var count = 0

    var body: some View {
        VStack(spacing: 20) {
            Text("Count: \(count)")
                .font(.largeTitle)

            Button(action: { count += 1 }) {
                Text("Increment")
                    .font(.headline)
                    .foregroundColor(.white)
                    .padding()
                    .background(Color.blue)
                    .cornerRadius(8)
            }
        }
        .padding()
    }
}

#Preview {
    ContentView()
}
```

### Kotlin with Jetpack Compose
```kotlin
import androidx.compose.foundation.layout.*
import androidx.compose.material3.*
import androidx.compose.runtime.*

@Composable
fun CounterScreen() {
    var count by remember { mutableStateOf(0) }

    Column(
        modifier = Modifier
            .fillMaxSize()
            .padding(16.dp),
        horizontalAlignment = Alignment.CenterHorizontally,
        verticalArrangement = Arrangement.Center
    ) {
        Text(
            text = "Count: $count",
            style = MaterialTheme.typography.headlineLarge
        )

        Button(onClick = { count++ }) {
            Text("Increment")
        }
    }
}
```

### React Native
```typescript
import React, { useState } from 'react';
import {
  View,
  Text,
  TouchableOpacity,
  StyleSheet,
} from 'react-native';

export const CounterScreen = () => {
  const [count, setCount] = useState(0);

  return (
    <View style={styles.container}>
      <Text style={styles.text}>Count: {count}</Text>
      <TouchableOpacity
        style={styles.button}
        onPress={() => setCount(count + 1)}
      >
        <Text style={styles.buttonText}>Increment</Text>
      </TouchableOpacity>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  text: {
    fontSize: 24,
    marginBottom: 16,
  },
  button: {
    backgroundColor: '#007AFF',
    paddingVertical: 12,
    paddingHorizontal: 24,
    borderRadius: 8,
  },
  buttonText: {
    color: '#fff',
    fontSize: 16,
  },
});
```

### Flutter with Dart
```dart
import 'package:flutter/material.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Counter',
      home: const CounterScreen(),
    );
  }
}

class CounterScreen extends StatefulWidget {
  const CounterScreen({Key? key}) : super(key: key);

  @override
  State<CounterScreen> createState() => _CounterScreenState();
}

class _CounterScreenState extends State<CounterScreen> {
  int count = 0;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Counter')),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Text('Count: $count', style: const TextStyle(fontSize: 24)),
            ElevatedButton(
              onPressed: () => setState(() => count++),
              child: const Text('Increment'),
            ),
          ],
        ),
      ),
    );
  }
}
```

## Key Concepts

### iOS Development
- **SwiftUI**: Declarative UI framework
- **MVVM Architecture**: Model-View-ViewModel pattern
- **State Management**: @State, @ObservedObject, @EnvironmentObject
- **Concurrency**: async/await in Swift

### Android Development
- **Jetpack Compose**: Modern declarative UI
- **MVVM + LiveData**: Reactive architecture
- **Coroutines**: Async operations
- **Dependency Injection**: Hilt framework

### Cross-Platform
- **Code sharing**: Business logic across platforms
- **Navigation**: Managing screens and flow
- **Native modules**: Accessing platform-specific features
- **Performance**: Balancing abstraction and speed

### Mobile UI/UX
- **Responsive design**: Different screen sizes
- **Accessibility**: WCAG compliance
- **Animations**: Smooth transitions
- **Touch gestures**: Intuitive interactions

## Common Patterns

### MVVM with iOS
```swift
class UserViewModel: ObservableObject {
    @Published var users: [User] = []
    @Published var isLoading = false
    @Published var error: Error?

    func loadUsers() {
        isLoading = true
        Task {
            do {
                users = try await userService.fetchUsers()
            } catch {
                self.error = error
            }
            isLoading = false
        }
    }
}

struct UserListView: View {
    @StateObject private var viewModel = UserViewModel()

    var body: some View {
        if viewModel.isLoading {
            ProgressView()
        } else if let error = viewModel.error {
            Text("Error: \(error.localizedDescription)")
        } else {
            List(viewModel.users) { user in
                Text(user.name)
            }
        }
        .onAppear { viewModel.loadUsers() }
    }
}
```

### State Management with Redux (React Native)
```typescript
// Actions
const INCREMENT = 'INCREMENT';

// Reducer
const counterReducer = (state = 0, action: Action) => {
  switch (action.type) {
    case INCREMENT:
      return state + 1;
    default:
      return state;
  }
};

// Store
const store = createStore(counterReducer);

// Component
const Counter = () => {
  const dispatch = useDispatch();
  const count = useSelector((state: RootState) => state);

  return (
    <View>
      <Text>{count}</Text>
      <Button onPress={() => dispatch({ type: INCREMENT })} />
    </View>
  );
};
```

## Best Practices

1. **Native first** - Use native features when needed
2. **Test thoroughly** - UI and unit tests essential
3. **Performance** - Monitor frame rates and memory
4. **Accessibility** - Design for all users
5. **Code sharing** - Maximize shared logic
6. **User feedback** - Responsive UI, loading states
7. **Battery aware** - Efficient algorithms and network
8. **Security** - Secure data storage, HTTPS

## Tools & Libraries

**iOS**: Xcode, SwiftUI, Combine, Core Data
**Android**: Android Studio, Jetpack, Coroutines, Room
**React Native**: React Navigation, Redux, Firebase
**Flutter**: Flutter SDK, Provider, GetX, Firebase
**Testing**: XCTest, Espresso, Detox, flutter_test
