---
name: ios-android-native
description: Master native iOS development with Swift and native Android development with Kotlin.
---

# Native iOS & Android

Platform-specific mobile development.

## Swift (iOS)

```swift
import SwiftUI

struct ContentView: View {
    @State var count = 0

    var body: some View {
        VStack {
            Text("Count: \(count)")
            Button("Increment") { count += 1 }
        }
    }
}
```

## Kotlin (Android)

```kotlin
@Composable
fun Counter() {
    var count by remember { mutableStateOf(0) }

    Column {
        Text("Count: $count")
        Button(onClick = { count++ }) { Text("Increment") }
    }
}
```

## Key Skills

- SwiftUI/Jetpack Compose
- App lifecycle
- Data persistence
- Network requests
- Testing
