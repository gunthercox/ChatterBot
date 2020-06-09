# is-npm [![Build Status](https://travis-ci.org/sindresorhus/is-npm.svg?branch=master)](https://travis-ci.org/sindresorhus/is-npm)

> Check if your code is running as an [npm](https://docs.npmjs.com/misc/scripts) or [yarn](https://yarnpkg.com/lang/en/docs/cli/run/) script


## Install

```
$ npm install is-npm
```


## Usage

```js
const {isNpm} = require('is-npm');

console.log(isNpm);
```

```sh
$ node foo.js
#=> false
$ npm run foo
#=> true
$ yarn run foo
#=> true
```


## License

MIT © [Sindre Sorhus](https://sindresorhus.com)
