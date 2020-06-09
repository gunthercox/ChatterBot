# defer-to-connect

> The safe way to handle the `connect` socket event

Once you receive the socket, it may be already connected.<br>
To avoid checking that, use `defer-to-connect`. It'll do that for you.

## Usage

```js
const deferToConnect = require('defer-to-connect');

deferToConnect(socket, () => {
    console.log('Connected!');
});
```

## API

### deferToConnect(socket, fn)

Calls `fn()` when connected.

## License

MIT
