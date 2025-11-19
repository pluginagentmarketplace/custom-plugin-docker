---
name: python-java-go-rust
description: Master Python, Java, Go, and Rust backend development. Learn framework patterns, concurrency models, and performance optimization for each language.
---

# Python, Java, Go, Rust Backends

Multi-language backend expertise.

## Python FastAPI

```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class User(BaseModel):
    name: str
    email: str

@app.post("/users")
async def create_user(user: User):
    return {"id": 1, **user.dict()}
```

## Java Spring Boot

```java
@SpringBootApplication
public class Application {
    public static void main(String[] args) {
        SpringApplication.run(Application.class, args);
    }
}

@RestController
@RequestMapping("/api/users")
public class UserController {
    @PostMapping
    public User create(@RequestBody User user) {
        return user;
    }
}
```

## Go Goroutines

```go
func main() {
    go fetchData()      // Non-blocking
    time.Sleep(1 * time.Second)
}

func fetchData() {
    for i := 0; i < 5; i++ {
        println("Goroutine:", i)
    }
}
```

## Rust Type Safety

```rust
fn main() {
    let user = User { id: 1, name: "Alice".to_string() };
    println!("{}", user.name);
}

struct User {
    id: i32,
    name: String,
}
```

## Key Patterns

**Python**: Async/await, ASGI, type hints
**Java**: Spring DI, annotations, streams
**Go**: Goroutines, channels, interfaces
**Rust**: Ownership, lifetimes, traits

## Resources

- FastAPI: https://fastapi.tiangolo.com
- Spring Boot: https://spring.io
- Go: https://golang.org
- Rust: https://www.rust-lang.org
