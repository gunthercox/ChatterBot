## lazy-val 

Lazy value.

```typescript
class Lazy<T> {
    constructor(creator: () => Promise<T>)
    readonly hasValue: boolean
    value: Promise<T>
}
```