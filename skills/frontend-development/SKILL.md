---
name: frontend-development
description: Build modern web applications with React, Vue, Angular, and TypeScript. Learn component design, state management, performance optimization, and responsive design patterns. Use when working with frontend frameworks or web development tasks.
---

# Frontend Development

Master modern frontend technologies and create exceptional user experiences.

## Quick Start

### React with TypeScript
```typescript
import React, { useState } from 'react';

interface Counter {
  value: number;
}

export const CounterComponent: React.FC = () => {
  const [count, setCount] = useState<number>(0);

  return (
    <div className="counter">
      <p>Count: {count}</p>
      <button onClick={() => setCount(c => c + 1)}>
        Increment
      </button>
    </div>
  );
};
```

### Vue with Composition API
```vue
<script setup lang="ts">
import { ref } from 'vue'

interface Counter {
  value: number
}

const count = ref<number>(0)
</script>

<template>
  <div class="counter">
    <p>Count: {{ count }}</p>
    <button @click="count++">Increment</button>
  </div>
</template>
```

### Custom React Hook
```typescript
// useAsync.ts
import { useState, useEffect } from 'react';

interface UseAsyncState<T> {
  data: T | null;
  loading: boolean;
  error: Error | null;
}

export function useAsync<T>(
  fn: () => Promise<T>,
  dependencies: any[] = []
): UseAsyncState<T> {
  const [state, setState] = useState<UseAsyncState<T>>({
    data: null,
    loading: true,
    error: null,
  });

  useEffect(() => {
    let isMounted = true;

    fn()
      .then(data => {
        if (isMounted) setState({ data, loading: false, error: null });
      })
      .catch(error => {
        if (isMounted) setState({ data: null, loading: false, error });
      });

    return () => {
      isMounted = false;
    };
  }, dependencies);

  return state;
}
```

## Key Concepts

### State Management Patterns
- React Context for simple state
- Redux/Zustand for complex state
- Atomic state with Recoil/Jotai
- Server state with React Query/SWR

### Component Architecture
- Presentational vs. Container components
- Composition over inheritance
- Compound components
- Render props and hooks

### Performance Optimization
- Code splitting with React.lazy
- Memoization (React.memo, useMemo, useCallback)
- Virtual scrolling for large lists
- Image optimization and lazy loading

### TypeScript with React
- Component props typing
- Generic components
- React.FC vs. arrow functions
- Typing refs and effects

## Common Patterns

### Error Boundary Pattern
```typescript
interface ErrorBoundaryProps {
  children: React.ReactNode;
  fallback?: React.ComponentType<{ error: Error }>;
}

interface ErrorBoundaryState {
  hasError: boolean;
  error: Error | null;
}

export class ErrorBoundary extends React.Component<
  ErrorBoundaryProps,
  ErrorBoundaryState
> {
  // Implementation here
}
```

### Higher-Order Component (HOC)
```typescript
function withRouter<P extends any>(
  Component: React.ComponentType<P & RouteProps>
): React.ComponentType<P> {
  return (props: P) => {
    const navigate = useNavigate();
    const location = useLocation();

    return <Component {...props} navigate={navigate} location={location} />;
  };
}
```

### Custom Hook for Data Fetching
```typescript
export function useFetch<T>(url: string) {
  const [data, setData] = useState<T | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);

  useEffect(() => {
    fetch(url)
      .then(res => res.json())
      .then(data => {
        setData(data);
        setLoading(false);
      })
      .catch(err => {
        setError(err);
        setLoading(false);
      });
  }, [url]);

  return { data, loading, error };
}
```

## Best Practices

1. **Use TypeScript** - Type safety catches errors early
2. **Composition over inheritance** - More flexible patterns
3. **Keep components small** - Single responsibility principle
4. **Memoize expensive computations** - Performance optimization
5. **Handle errors gracefully** - Error boundaries, error states
6. **Test your components** - Unit and integration tests
7. **Accessibility first** - WCAG compliance from start
8. **Responsive design** - Mobile-first approach

## Resources

- [React Documentation](https://react.dev)
- [Vue Documentation](https://vuejs.org)
- [TypeScript for React](https://www.typescriptlang.org/docs/handbook/react.html)
- [Testing Library](https://testing-library.com)
- [Modern CSS](https://moderncssguru.com)
