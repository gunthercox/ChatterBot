# 7zip Windows Package via Node.js

<a href="https://www.npmjs.com/package/7zip"><img width="134" height="20" src="https://img.shields.io/npm/dm/7zip.svg"></a>&nbsp;&nbsp;<a href="https://github.com/fritx/win-7zip"><img width="84" height="20" src="https://img.shields.io/badge/license-LGPL-yellow.svg"></a>

This npm package contains a lite-version of [7zip](http://7-zip.org), ≈2.4MB.

And the goal is to bring users a different and easy way to access 7zip.

Being used at library [cross-unzip](https://github.com/fritx/cross-unzip).

```plain
$ npm install -g 7zip   # global
```

```plain
$ 7z --help   # and you get 7z
```

```js
// $ npm install 7zip   # local
// even in node.js
var _7z = require('7zip')['7z']
var task = spawn(_7z, ['x', 'somefile.7z', '-y'])
```

## License of 7zip

```plain
7-Zip Copyright (C) 1999-2015 Igor Pavlov.

Licenses for files are:

  1) 7z.dll: GNU LGPL + unRAR restriction
  2) All other files:  GNU LGPL
```
