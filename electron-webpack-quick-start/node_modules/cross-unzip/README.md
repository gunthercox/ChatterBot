# cross-unzip

<a href="https://github.com/fritx/cross-unzip"><img width="90" height="20" src="https://img.shields.io/badge/PRs-welcome-brightgreen.svg" /></a>&nbsp;&nbsp;<a href="https://github.com/fritx/cross-unzip"><img width="84" height="20" src="https://img.shields.io/badge/license-LGPL-yellow.svg"></a>

See also: [feross/cross-zip](https://github.com/feross/cross-zip)

- [x] Tested on OSX
- [x] Tested on Windows
- [ ] Progress feedback

```plain
$ npm install cross-unzip
$ npm install 7zip  # windows only
```

```js
const unzip = require('cross-unzip')

unzip('some/archive.zip', 'some/dir', (err) => {
  // done
})
```
