---
name: typescript-frontend
description: Advanced TypeScript for frontend development. Master generics, utility types, React type patterns, and building type-safe applications.
sasmp_version: "1.3.0"
bonded_agent: 01-frontend-web-development
bond_type: PRIMARY_BOND
---

# TypeScript for Frontend

Type-safe frontend development.

## Generics with React

```typescript
// Generic component
interface Props<T> {
  items: T[]
  renderItem: (item: T) => React.ReactNode
}

export function List<T extends { id: string | number }>({ items, renderItem }: Props<T>) {
  return <ul>{items.map(item => <li key={item.id}>{renderItem(item)}</li>)}</ul>
}

// Usage
<List<User> items={users} renderItem={user => user.name} />
```

## Utility Types

```typescript
// Partial - all properties optional
type PartialUser = Partial<User>

// Pick - select specific properties
type UserPreview = Pick<User, 'id' | 'name'>

// Omit - exclude properties
type UserWithoutPassword = Omit<User, 'password'>

// Record - object with specific keys
type Status = Record<'pending' | 'loading' | 'success' | 'error', string>

// Readonly - make all properties readonly
type ReadonlyUser = Readonly<User>

// ReturnType - extract function return type
type UserServiceReturn = ReturnType<typeof UserService.getUser>
```

## React Type Patterns

```typescript
// Component props
interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary'
  isLoading?: boolean
}

// Component children
interface LayoutProps {
  children: React.ReactNode
}

// Event handlers
const handleClick: React.MouseEventHandler<HTMLButtonElement> = (e) => {
  console.log(e.currentTarget.value)
}

// Ref types
const ref = useRef<HTMLInputElement>(null)

// State with complex types
const [user, setUser] = useState<User | null>(null)
```

## Advanced Patterns

```typescript
// Discriminated unions
type Status =
  | { status: 'idle' }
  | { status: 'loading' }
  | { status: 'success'; data: User[] }
  | { status: 'error'; error: Error }

function handleStatus(status: Status) {
  switch (status.status) {
    case 'success':
      console.log(status.data) // TypeScript knows data exists
      break
  }
}

// Type guards
function isUser(value: unknown): value is User {
  return typeof value === 'object' && value !== null && 'id' in value && 'name' in value
}

// Conditional types
type IsString<T> = T extends string ? true : false
```

## Best Practices

1. Enable strict mode in tsconfig
2. Avoid `any` - use `unknown` instead
3. Use utility types for DRY code
4. Leverage discriminated unions
5. Create type guards for runtime checks
6. Use interfaces for public APIs
7. Extract types into separate files
8. Document complex types with JSDoc

## Resources

- TypeScript Handbook: https://www.typescriptlang.org/docs
- React TypeScript: https://react-typescript-cheatsheet.netlify.app
