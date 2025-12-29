---
name: react-development
description: Master React development including Hooks, Server Components, state management, testing, and performance optimization. Use for building modern React applications with best practices.
sasmp_version: "1.3.0"
bonded_agent: 01-frontend-web-development
bond_type: PRIMARY_BOND
---

# React Development

Expert React patterns and production-ready applications.

## Quick Start

### Functional Component with Hooks
```typescript
import React, { useState, useCallback } from 'react';

export const Counter: React.FC<{ initial?: number }> = ({ initial = 0 }) => {
  const [count, setCount] = useState(initial);
  const increment = useCallback(() => setCount(c => c + 1), []);

  return (
    <div>
      <p>Count: {count}</p>
      <button onClick={increment}>+</button>
    </div>
  );
};
```

### Custom Hook for Data Fetching
```typescript
function useFetch<T>(url: string): { data: T | null; loading: boolean; error: Error | null } {
  const [state, setState] = useState({ data: null, loading: true, error: null });

  useEffect(() => {
    fetch(url)
      .then(r => r.json())
      .then(data => setState({ data, loading: false, error: null }))
      .catch(error => setState({ data: null, loading: false, error }));
  }, [url]);

  return state;
}
```

### Server Components (Next.js 13+)
```typescript
export default async function PostList() {
  const posts = await fetchPosts(); // Server-side only

  return (
    <ul>
      {posts.map(post => (
        <li key={post.id}>{post.title}</li>
      ))}
    </ul>
  );
}
```

## Key Patterns

### Context API for Global State
```typescript
const ThemeContext = createContext<'light' | 'dark'>('light');

function ThemeProvider({ children }) {
  const [theme, setTheme] = useState<'light' | 'dark'>('light');
  return (
    <ThemeContext.Provider value={theme}>
      {children}
    </ThemeContext.Provider>
  );
}
```

### Error Boundaries
```typescript
class ErrorBoundary extends React.Component {
  state = { hasError: false };

  static getDerivedStateFromError(error) {
    return { hasError: true };
  }

  render() {
    return this.state.hasError ? <h1>Error occurred</h1> : this.props.children;
  }
}
```

### Performance Optimization
```typescript
// Memoization
const MemoizedComponent = React.memo(({ data }) => {
  return <div>{data.title}</div>;
});

// useCallback for callbacks
const handleClick = useCallback(() => {
  doSomething();
}, []);

// useMemo for expensive calculations
const value = useMemo(() => expensiveComputation(data), [data]);
```

## Testing

```typescript
import { render, screen } from '@testing-library/react';

test('increments counter', () => {
  render(<Counter initial={0} />);
  const button = screen.getByRole('button');
  fireEvent.click(button);
  expect(screen.getByText('Count: 1')).toBeInTheDocument();
});
```

## Best Practices

1. Prefer hooks over class components
2. Use memoization for expensive operations
3. Separate concerns with custom hooks
4. Test user interactions, not implementation
5. Use TypeScript for type safety
6. Lazy load components with React.lazy
7. Implement error boundaries
8. Monitor performance with React Profiler

## Resources

- React Docs: https://react.dev
- Next.js: https://nextjs.org
- Testing Library: https://testing-library.com
- React Query: https://tanstack.com/query
