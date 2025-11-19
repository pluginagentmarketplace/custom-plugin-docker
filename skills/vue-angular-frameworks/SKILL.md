---
name: vue-angular-frameworks
description: Master Vue.js and Angular frameworks. Learn Composition API, reactive system, dependency injection, RxJS, and building large-scale applications with these powerful frameworks.
---

# Vue.js & Angular Frameworks

Production-ready Vue and Angular development.

## Vue.js Composition API

```vue
<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'

const items = ref<string[]>([])
const newItem = ref('')

const itemCount = computed(() => items.value.length)

const addItem = () => {
  if (newItem.value) {
    items.value.push(newItem.value)
    newItem.value = ''
  }
}

onMounted(() => {
  console.log('Component mounted')
})
</script>

<template>
  <div>
    <p>Items: {{ itemCount }}</p>
    <input v-model="newItem" @keyup.enter="addItem" />
    <ul>
      <li v-for="item in items" :key="item">{{ item }}</li>
    </ul>
  </div>
</template>
```

## Angular Dependency Injection

```typescript
import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class UserService {
  constructor(private http: HttpClient) {}

  getUsers() {
    return this.http.get<User[]>('/api/users');
  }
}

@Component({
  selector: 'app-user-list',
  template: `
    <ul>
      <li *ngFor="let user of users">{{ user.name }}</li>
    </ul>
  `
})
export class UserListComponent implements OnInit {
  users: User[] = [];

  constructor(private userService: UserService) {}

  ngOnInit() {
    this.userService.getUsers().subscribe(
      users => this.users = users
    );
  }
}
```

## Angular RxJS Observables

```typescript
import { of, Subject } from 'rxjs';
import { map, filter, switchMap } from 'rxjs/operators';

const source$ = of(1, 2, 3, 4, 5);

source$
  .pipe(
    filter(x => x > 2),
    map(x => x * 2),
  )
  .subscribe(console.log); // 6, 8, 10

// Subject for manual control
const subject$ = new Subject<string>();

subject$.subscribe(value => console.log('Observer 1:', value));
subject$.subscribe(value => console.log('Observer 2:', value));

subject$.next('Hello'); // Both observers get the message
```

## Vue Reactive System

```typescript
import { reactive, computed, watch } from 'vue'

const state = reactive({
  count: 0,
  todos: [
    { id: 1, text: 'Learn Vue', done: false },
  ]
})

const completedCount = computed(() =>
  state.todos.filter(t => t.done).length
)

watch(() => state.count, (newVal, oldVal) => {
  console.log(`Count changed from ${oldVal} to ${newVal}`)
})
```

## Angular Routing

```typescript
const routes: Routes = [
  { path: '', redirectTo: '/home', pathMatch: 'full' },
  { path: 'home', component: HomeComponent },
  { path: 'users', component: UsersComponent },
  { path: 'users/:id', component: UserDetailComponent },
  { path: '**', component: NotFoundComponent }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
```

## Key Concepts

### Vue
- Reactivity system and refs
- Composition API for logic reuse
- Teleport for portal patterns
- Transitions and animations

### Angular
- Dependency injection container
- TypeScript-first framework
- RxJS for reactive programming
- Zone.js for change detection

## Best Practices

1. **Vue**: Use Composition API for complex logic
2. **Angular**: Leverage type safety and DI
3. Keep components focused and testable
4. Use service classes for business logic
5. Implement proper error handling
6. Optimize change detection
7. Use lazy loading for routes
8. Write comprehensive unit tests

## Resources

- Vue.js: https://vuejs.org
- Angular: https://angular.io
- RxJS: https://rxjs.dev
- Angular Material: https://material.angular.io
