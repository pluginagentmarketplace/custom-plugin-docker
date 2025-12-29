---
name: react-native-flutter
description: Master cross-platform mobile development with React Native and Flutter.
sasmp_version: "1.3.0"
bonded_agent: 01-frontend-web-development
bond_type: PRIMARY_BOND
---

# React Native & Flutter

Cross-platform mobile development.

## React Native

```javascript
import React, { useState } from 'react'
import { View, Text, Button } from 'react-native'

export default function Counter() {
  const [count, setCount] = useState(0)
  return (
    <View>
      <Text>Count: {count}</Text>
      <Button onPress={() => setCount(count + 1)} title="+" />
    </View>
  )
}
```

## Flutter

```dart
class Counter extends StatefulWidget {
  @override
  State<Counter> createState() => _CounterState()
}

class _CounterState extends State<Counter> {
  int count = 0

  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        Text('Count: $count'),
        ElevatedButton(
          onPressed: () => setState(() => count++),
          child: Text('+'),
        ),
      ],
    )
  }
}
```

## Key Skills

- Code sharing
- Navigation
- State management
- Firebase integration
- App distribution
