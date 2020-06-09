# electron-webpack [![npm version](https://img.shields.io/npm/v/electron-webpack.svg)](https://npmjs.org/package/electron-webpack)

> Because setting up `webpack` in the `electron` environment shouldn't be difficult.

## Overview
Modern web development practices today require a lot of setup with things like `webpack` to bundle your code, `babel` for transpiling, `eslint` for linting, and so much more that the list just goes on. Unfortunately when creating `electron` applications, all of that setup just became much more difficult. The primary aim of `electron-webpack` is to eliminate all preliminary setup with one simple install so you can get back to developing your application.

> Why create a module and not a full boilerplate?

If you've been in the JavaScript world for even a short period of time, you are very aware that things are always changing, and development setup is no exclusion. Putting all development scripts into a single **updatable** module just makes sense. Sure a full featured boilerplate works too, but doing also involves needing to manually update those pesky `webpack` configuration files that some may call *magic* when something new comes out.

Here are some of the awesome features you'll find using `electron-webpack`...

* Detailed [documentation](https://webpack.electron.build)
* Use of [`webpack`](https://webpack.js.org/) for source code bundling
* Use of [`webpack-dev-server`](https://github.com/webpack/webpack-dev-server) for development
* HMR for both `renderer` and `main` processes
* Use of [`@babel/preset-env`](https://github.com/babel/babel/tree/master/packages/babel-preset-env) that is automatically configured based on your `electron` version
* Ability to add custom `webpack` loaders, plugins, etc.
* [Add-ons](https://webpack.electron.build/add-ons) to support items like [TypeScript](http://www.typescriptlang.org/), [Less](http://lesscss.org/), [EJS](http://www.embeddedjs.com/), etc.

## Quick Start
Get started fast with [electron-webpack-quick-start](https://github.com/electron-userland/electron-webpack-quick-start).
```bash
# create a directory of your choice, and copy template using curl
mkdir my-project && cd my-project
curl -fsSL https://github.com/electron-userland/electron-webpack-quick-start/archive/master.tar.gz | tar -xz --strip-components 1

# or copy template using git clone
git clone https://github.com/electron-userland/electron-webpack-quick-start.git
cd electron-webpack-quick-start
rm -rf .git

# install dependencies
yarn
```

If you already have an existing project, or are looking for a custom approach outside of the quick start template, make sure to read over the [Core Concepts](https://webpack.electron.build/core-concepts), [Project Structure](https://webpack.electron.build/project-structure), and [Development](https://webpack.electron.build/development) sections of `electron-webpack`'s documentation.

### Next Steps
Make sure to take advantage of the detailed [documentation](https://webpack.electron.build) that `electron-webpack` provides. It covers everything from how things work internally, adding custom configurations, and building your application.
