Electron DevTools Installer
---------------------------

[![Build Status](https://travis-ci.org/MarshallOfSound/electron-devtools-installer.svg?branch=master)](https://travis-ci.org/MarshallOfSound/electron-devtools-installer)
[![Build Status](https://ci.appveyor.com/api/projects/status/um3h4xqen7vql7o2/branch/master?svg=true)](https://ci.appveyor.com/project/MarshallOfSound/electron-devtools-installer/branch/master)
[![npm version](https://badge.fury.io/js/electron-devtools-installer.svg)](https://www.npmjs.com/package/electron-devtools-installer)
[![npm](https://img.shields.io/npm/dt/electron-devtools-installer.svg?maxAge=2592000)](https://www.npmjs.com/package/electron-devtools-installer)
[![license](https://img.shields.io/github/license/GPMDP/electron-devtools-installer.svg?maxAge=2592000)](https://github.com/GPMDP/electron-devtools-installer/blob/master/LICENSE)
![status](https://img.shields.io/badge/Status-%20Ready%20for%20Awesome-red.svg)

This is an easy way to install DevTool extensions into Electron.  You shouldn't
have to mess around with downloading the extension, finding the right folder and
then configuring the path for everyone's machines.

## Install

```
npm install electron-devtools-installer --save-dev
```
or
```
yarn add electron-devtools-installer -D
```

## Usage
All you have to do now is

```js
import installExtension, { REACT_DEVELOPER_TOOLS } from 'electron-devtools-installer';

installExtension(REACT_DEVELOPER_TOOLS)
    .then((name) => console.log(`Added Extension:  ${name}`))
    .catch((err) => console.log('An error occurred: ', err));
```

Alternatively, using `require()` and destructuring (node v6 or higher) you can

```js
const { default: installExtension, REACT_DEVELOPER_TOOLS } = require('electron-devtools-installer');

installExtension(REACT_DEVELOPER_TOOLS)
    .then((name) => console.log(`Added Extension:  ${name}`))
    .catch((err) => console.log('An error occurred: ', err));
```

## What extensions can I use?

Technically you can use whatever extension you want.  Simply find the ChromeStore ID
of the extension you want to install, and call `installExtension('YOUR_ID_HERE')`.  We
offer a few extension ID's inside the package so you can easily import them to install without
having to find them yourselves.

```js
import installExtension, {
  EMBER_INSPECTOR, REACT_DEVELOPER_TOOLS,
  BACKBONE_DEBUGGER, JQUERY_DEBUGGER,
  ANGULARJS_BATARANG, VUEJS_DEVTOOLS,
  REDUX_DEVTOOLS, REACT_PERF,
  CYCLEJS_DEVTOOL, MOBX_DEVTOOLS,
  APOLLO_DEVELOPER_TOOLS,
} from 'electron-devtools-installer';
```

## How does it work?

Well, you know those steps over in the [Electron Docs](https://github.com/electron/electron/blob/master/docs/tutorial/devtools-extension.md)
that involve downloading, copying, checking paths, Etc.

This does all of that for you, it downloads the chrome extension directly from
the Chrome WebStore.  Then it extracts it to your applications `userData` directory
before loading it into Electron.


License
-------

The MIT License (MIT)

Copyright (c) 2016 Samuel Attard

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
the Software, and to permit persons to whom the Software is furnished to do so,
subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
